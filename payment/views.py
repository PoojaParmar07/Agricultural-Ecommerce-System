from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from Ecommerce.models import *
from account.models import Profile
from membership.models import *
from decimal import Decimal
from datetime import date
from django.db import transaction

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