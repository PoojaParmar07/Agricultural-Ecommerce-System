from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
import stripe
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from Ecommerce.models import *
from account.models import *
from membership.models import *
from decimal import Decimal
from datetime import date
from django.db import transaction
import json
from django.http import JsonResponse



stripe.api_key = settings.STRIPE_SECRET_KEY
# @login_required
def cod_checkout(request):
    user = request.user
    cart = Cart.objects.filter(user=user).first()

    if not cart or not cart.cartitem_set.exists():
        messages.error(request, "Your cart is empty!")
        return redirect("Ecommerce:cart_view")

    total_price = sum(item.total_price for item in cart.cartitem_set.all())

    # Check user membership
    user_membership = User_membership.objects.filter(
        user=user, status=True, membership_end_date__gte=date.today()
    ).first()

    discount_amount = Decimal(0)
    if user_membership:
        discount_rate = Decimal(
            user_membership.plan.discount_rate)  # Convert to Decimal
        discount_amount = (discount_rate / Decimal(100)) * total_price
        total_price -= discount_amount
        delivery_charges = Decimal(0)  # Free delivery for members
    else:
        delivery_charges = Decimal(0)  # Default, updated below

    if request.method == "POST":
        address = request.POST.get("address", "").strip()
        city_id = request.POST.get("city", "").strip()
        pincode = request.POST.get("pincode", "").strip()
        print(f"Received pincode from user: '{pincode}'")

        if not address or not city_id or not pincode:
            messages.error(
                request, "All fields (Address, City, and Pincode) are required!")
            return redirect("Ecommerce:checkout")

        try:
            pincode_obj = Pincode.objects.get(area_pincode__iexact=pincode)
            delivery_charges = Decimal(0) if user_membership else Decimal(
                pincode_obj.delivery_charges)
        except Pincode.DoesNotExist:
            messages.error(request, "Invalid pincode.")
            return redirect("Ecommerce:checkout")

        # Create order in an atomic transaction
        with transaction.atomic():
            order = Order.objects.create(
                user=user,
                order_user_type="member" if user_membership else "non-member",
                total_price=total_price + delivery_charges,
                discounted_price=discount_amount,
                order_status="pending",
                state=user.state,
                city_id=city_id,
                address=address,
                pincode=pincode_obj,
                delivery_charges=delivery_charges,
            )

            # Move cart items to order items
            for item in cart.cartitem_set.all():
                Order_Item.objects.create(
                    order=order,
                    batch=item.product_batch,
                    variant=item.product_variant,
                    quantity=item.quantity,
                    price=item.total_price,
                )

                # Decrease stock
                inventory = Inventory.objects.filter(
                    batch=item.product_batch).first()
                if inventory and inventory.quantity >= item.quantity:
                    inventory.quantity -= item.quantity
                    inventory.save()
                else:
                    messages.error(
                        request, f"Not enough stock for {item.product_variant}.")
                    return redirect("Ecommerce:cart_view")

            # Create payment record for COD
            Payment.objects.create(
                order=order,
                total_price=total_price + delivery_charges,
                payment_mode="cash",
                payment_status="pending",
            )

            # Clear the cart
            cart.cartitem_set.all().delete()

        messages.success(
            request, "Order placed successfully! Pay on delivery.")
        return redirect("Ecommerce:confirm_Order")

    return render(request, "checkout.html", {"cart": cart, "total_price": total_price, "discount_amount": discount_amount})




# def stripe_checkout(request):
#     user = request.user
#     cart = Cart.objects.filter(user=user).first()

#     if not cart or not cart.cartitem_set.exists():
#         messages.error(request, "Your cart is empty!")
#         return redirect("Ecommerce:cart_view")

#     total_price = sum(item.total_price for item in cart.cartitem_set.all())

#     try:
#         # Create Stripe checkout session
#         session = stripe.checkout.Session.create(
#             payment_method_types=["card"],
#             line_items=[{
#                 "price_data": {
#                     "currency": "inr",
#                     "product_data": {
#                         "name": "Order Payment"
#                     },
#                     "unit_amount": int(total_price * 100),
#                 },
#                 "quantity": 1,
#             }],
#             mode="payment",
#             success_url=request.build_absolute_uri("/payment/success/"),
#             cancel_url=request.build_absolute_uri("/payment/cancel/"),
#         )
#         return redirect(session.url)
#     except stripe.error.StripeError as e:
#         messages.error(request, f"Stripe error: {e.user_message}")
#         return redirect("Ecommerce:checkout")


def stripe_checkout(request):
    user = request.user
    cart = Cart.objects.filter(user=user).first()

    if not cart or not cart.cartitem_set.exists():
        messages.error(request, "Your cart is empty!")
        return redirect("Ecommerce:cart_view")

    total_price = sum(item.total_price for item in cart.cartitem_set.all())

    # Ensure user has a profile
    profile, created = Profile.objects.get_or_create(user=user)

    customer_name = f"{user.first_name} {user.last_name}"
    customer_email = user.email
    billing_address = {
        "line1": profile.address,  # Use profile fields
        "city": profile.city,
        "state": profile.state,
        "postal_code": profile.pincode,
        "country": "IN",
    }

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            customer_email=customer_email,
            line_items=[{
                "price_data": {
                    "currency": "inr",
                    "product_data": {
                        "name": "Order Payment"
                    },
                    "unit_amount": int(total_price * 100),
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url=request.build_absolute_uri("/payment/success/"),
            cancel_url=request.build_absolute_uri("/payment/cancel/"),
            billing_address_collection="required",
            metadata={"customer_name": customer_name},
        )
        return redirect(session.url)

    except stripe.error.StripeError as e:
        messages.error(request, f"Stripe error: {e.user_message}")
        return redirect("Ecommerce:checkout")


def stripe_success(request):
    return render(request, "payment/success.html")

def stripe_cancel(request):
   return render(request, "payment/cancel.html")


@csrf_exempt
def stripe_webhook(request):
    """Handles Stripe webhook events."""
    payload = request.body
    sig_header = request.headers.get("Stripe-Signature")
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET  # Store in .env

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError:
        return JsonResponse({"error": "Invalid payload"}, status=400)
    except stripe.error.SignatureVerificationError:
        return JsonResponse({"error": "Invalid signature"}, status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        customer_email = session.get("customer_email")
        total_price = Decimal(session["amount_total"]) / 100  # Convert from cents
        stripe_payment_id = session["payment_intent"]

        # Get the user from email
        user = get_object_or_404(CustomUser, email=customer_email)

        # Fetch cart
        cart = Cart.objects.filter(user=user).first()
        if not cart:
            return JsonResponse({"error": "Cart not found"}, status=400)

        # Check if the user has an active membership
        user_membership = getattr(user, "user_membership", None)
        is_member = user_membership and user_membership.status and user_membership.membership_end_date

        discount_amount = Decimal(0)
        if is_member:
            discount_rate = Decimal(user_membership.plan.discount_rate)
            discount_amount = (discount_rate / Decimal(100)) * total_price
            total_price -= discount_amount
            delivery_charges = Decimal(0)  # Free delivery for members
        else:
            delivery_charges = Decimal(0)  # Default

        # Create order inside an atomic transaction
        with transaction.atomic():
            order = Order.objects.create(
                user=user,
                order_user_type="member" if is_member else "non-member",
                total_price=total_price,
                discounted_price=discount_amount,
                order_status="paid",
                state=user.profile.state,
                city=user.profile.city,
                address=user.profile.address,
                pincode=user.profile.pincode,
                delivery_charges=delivery_charges,
            )

            # Move cart items to order items
            for item in cart.cartitem_set.all():
                Order_Item.objects.create(
                    order=order,
                    batch=item.product_batch,
                    variant=item.product_variant,
                    quantity=item.quantity,
                    price=item.total_price,
                )

                # Decrease stock
                inventory = Inventory.objects.filter(batch=item.product_batch).first()
                if inventory and inventory.quantity >= item.quantity:
                    inventory.quantity -= item.quantity
                    inventory.save()

            # Create payment record
            Payment.objects.create(
                order=order,
                total_price=total_price,
                payment_mode="online",
                payment_status="completed",
                transaction_id=stripe_payment_id,  # Store Stripe transaction ID
            )

            # Clear the cart
            cart.cartitem_set.all().delete()

        return JsonResponse({"message": "Payment successful and order created"}, status=200)

    return JsonResponse({"message": "Unhandled event type"}, status=400)
