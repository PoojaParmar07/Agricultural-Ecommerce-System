from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
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
from django.contrib.auth.decorators import login_required
import logging


logger = logging.getLogger(__name__)
stripe.api_key = settings.STRIPE_SECRET_KEY
# @login_required
# def cod_checkout(request):
#     user = request.user
#     cart = Cart.objects.filter(user=user).first()

#     if not cart or not cart.cartitem_set.exists():
#         messages.error(request, "Your cart is empty!")
#         return redirect("Ecommerce:cart_view")

#     total_price = sum(item.total_price for item in cart.cartitem_set.all())

#     # Check user membership
#     user_membership = User_membership.objects.filter(
#         user=user, status=True, membership_end_date__gte=date.today()
#     ).first()

#     discount_amount = Decimal(0)
#     if user_membership:
#         discount_rate = Decimal(
#             user_membership.plan.discount_rate)  # Convert to Decimal
#         discount_amount = (discount_rate / Decimal(100)) * total_price
#         total_price -= discount_amount
#         delivery_charges = Decimal(0)  # Free delivery for members
#     else:
#         delivery_charges = Decimal(0)  # Default, updated below

#     if request.method == "POST":
#         address = request.POST.get("address", "").strip()
#         city_id = request.POST.get("city", "").strip()
#         pincode = request.POST.get("pincode", "").strip()
#         print(f"Received pincode from user: '{pincode}'")

#         if not address or not city_id or not pincode:
#             messages.error(
#                 request, "All fields (Address, City, and Pincode) are required!")
#             return redirect("Ecommerce:checkout")

#         try:
#             pincode_obj = Pincode.objects.get(area_pincode__iexact=pincode)
#             delivery_charges = Decimal(0) if user_membership else Decimal(
#                 pincode_obj.delivery_charges)
#         except Pincode.DoesNotExist:
#             messages.error(request, "Invalid pincode.")
#             return redirect("Ecommerce:checkout")

#         # Create order in an atomic transaction
#         with transaction.atomic():
#             order = Order.objects.create(
#                 user=user,
#                 order_user_type="member" if user_membership else "non-member",
#                 total_price=total_price + delivery_charges,
#                 discounted_price=discount_amount,
#                 order_status="pending",
#                 state=user.state,
#                 city_id=city_id,
#                 address=address,
#                 pincode=pincode_obj,
#                 delivery_charges=delivery_charges,
#             )

#             # Move cart items to order items
#             for item in cart.cartitem_set.all():
#                 Order_Item.objects.create(
#                     order=order,
#                     batch=item.product_batch,
#                     variant=item.product_variant,
#                     quantity=item.quantity,
#                     price=item.total_price,
#                 )

#                 # Decrease stock
#                 inventory = Inventory.objects.filter(
#                     batch=item.product_batch).first()
#                 if inventory and inventory.quantity >= item.quantity:
#                     inventory.quantity -= item.quantity
#                     inventory.save()
#                 else:
#                     messages.error(
#                         request, f"Not enough stock for {item.product_variant}.")
#                     return redirect("Ecommerce:cart_view")

#             # Create payment record for COD
#             Payment.objects.create(
#                 order=order,
#                 total_price=total_price + delivery_charges,
#                 payment_mode="cash",
#                 payment_status="pending",
#             )

#             # Clear the cart
#             cart.cartitem_set.all().delete()

#         messages.success(
#             request, "Order placed successfully! Pay on delivery.")
#         return redirect("Ecommerce:confirm_Order")

#     return render(request, "checkout.html", {"cart": cart, "total_price": total_price, "discount_amount": discount_amount})





# def stripe_checkout(request):
#     if request.method == "POST":
#         user = request.user
#         cart = Cart.objects.filter(user=user).first()

#         if not cart or not cart.cartitem_set.exists():
#             messages.error(request, "Your cart is empty!")
#             return redirect("Ecommerce:cart_view")

#         # Initialize price calculations
#         total_price = Decimal(0)
#         discount_rate = Decimal(0)
#         delivery_charges = Decimal(0)
#         line_items = []

#         # Fetch user membership details
#         user_membership = User_membership.objects.filter(
#             user=user, status=True, membership_end_date__gte=date.today()
#         ).first()
        
#         if user_membership:
#             discount_rate = Decimal(user_membership.plan.discount_rate)

#         # Calculate total price from cart items (applying discount per item)
#         for cart_item in cart.cartitem_set.all():
#             variant = cart_item.product_variant

#             # Fetch latest inventory price
#             inventory = Inventory.objects.filter(batch__variant=variant).order_by('-create_at').first()
#             if not inventory or inventory.sales_price is None:
#                 return JsonResponse({"error": f"Price not available for variant {variant}"}, status=400)

#             original_price = Decimal(inventory.sales_price)
#             discounted_price = original_price * (1 - discount_rate / 100)  # Apply discount
#             item_total_price = discounted_price * cart_item.quantity
#             total_price += item_total_price  # Accumulate total price

#             # Get product image
#             product_image_url = (
#                 request.build_absolute_uri(variant.product.product_image.url)
#                 if variant.product.product_image else "https://via.placeholder.com/150"
#             )

#             # ✅ Add product details to Stripe line items (with discounted price)
#             line_items.append({
#                 'price_data': {
#                     "currency": "inr",
#                     'product_data': {
#                         'name': str(variant),
#                         'images': [product_image_url],
#                     },
#                     "unit_amount": max(1, int(discounted_price * 100)),  # Convert to paise
#                 },
#                 'quantity': cart_item.quantity,
#             })

#         # Fetch pincode and calculate delivery charges
#         address = request.POST.get("address", "").strip()
#         city_id = request.POST.get("city", "").strip()
#         pincode = request.POST.get("pincode", "").strip()

#         if not address or not city_id or not pincode:
#             messages.error(request, "All fields (Address, City, and Pincode) are required!")
#             return JsonResponse({"error": "Missing address, city, or pincode!"}, status=400)

#         try:
#             pincode_obj = Pincode.objects.get(area_pincode__iexact=pincode)
#             if user_membership:
#                 delivery_charges = Decimal(0)  # Free delivery for members
#             else:
#                 delivery_charges = Decimal(pincode_obj.delivery_charges)  # Delivery charge for non-members
#         except Pincode.DoesNotExist:
#             messages.error(request, "Invalid pincode.")
#             return JsonResponse({"error": "Invalid pincode!"}, status=400)

#         # ✅ Calculate final price with delivery
#         final_price = total_price + delivery_charges
#         final_amount = max(1, int(final_price * 100))  # Convert to paise, ensure min 1 paise

#         # ✅ Add Delivery Charge Separately (If Applicable)
#         if delivery_charges > 0:
#             line_items.append({
#                 'price_data': {
#                     "currency": "inr",
#                     'product_data': {'name': "Delivery Charges"},
#                     "unit_amount": int(delivery_charges * 100),  # Convert to paise
#                 },
#                 'quantity': 1,
#             })

#         # ✅ Debugging Prints
#         print(f"✅ Corrected Final Amount Sent to Stripe: {final_amount}")
#         print(f"✅ Updated Line Items Sent to Stripe: {line_items}")

#         # ✅ Create Stripe Checkout Session
#         try:
#             session = stripe.checkout.Session.create(
#                 payment_method_types=['card'],
#                 line_items=line_items,
#                 mode='payment',
#                 success_url='http://127.0.0.1:8000/payment/success/',
#                 cancel_url='http://127.0.0.1:8000/payment/cancel/',
#                 metadata={
#                     "final_total": str(final_price)  # Helps verify the final amount in Stripe Dashboard
#                 }
#             )

#             return redirect(session.url)

#         except stripe.error.StripeError as e:
#             print(f"Stripe API error: {e}")  # Debugging
#             return JsonResponse({"error": f"Stripe error: {str(e)}"}, status=500)

#         except Exception as e:
#             print(f"General error: {e}")  # Debugging
#             return JsonResponse({"error": "Stripe session creation failed"}, status=500)





def stripe_success(request):
    return render(request, "payment/success.html")

def stripe_cancel(request):
   return render(request, "payment/cancel.html")




# @csrf_exempt
# def stripe_webhook(request):
#     """Handles Stripe webhook events with Indian export compliance."""
#     payload = request.body
#     sig_header = request.headers.get("Stripe-Signature")
#     endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

#     try:
#         event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
#     except ValueError:
#         return JsonResponse({"error": "Invalid payload"}, status=400)
#     except stripe.error.SignatureVerificationError:
#         return JsonResponse({"error": "Invalid signature"}, status=400)

#     # ✅ Handle successful checkout session completion
#     if event["type"] == "checkout.session.completed":
#         session = event["data"]["object"]

#         # Extract essential data
#         customer_email = session.get("customer_email")
#         stripe_payment_id = session["payment_intent"]
#         final_price = Decimal(session["amount_total"]) / 100  # Convert from paise

#         # ✅ Extract customer details for exports
#         customer_details = session.get("customer_details", {})
#         customer_name = customer_details.get("name", "Unknown")
#         customer_address = customer_details.get("address", {})

#         if not customer_name or not customer_address:
#             return JsonResponse({"error": "Customer name and address are required for exports"}, status=400)

#         state = customer_address.get("state", "Unknown")
#         city = customer_address.get("city", "Unknown")
#         address = customer_address.get("line1", "") + " " + customer_address.get("line2", "")
#         pincode = customer_address.get("postal_code", "")

#         # ✅ Fetch the user using email
#         user = get_object_or_404(CustomUser, email=customer_email)

#         # ✅ Fetch the user's cart
#         cart = Cart.objects.filter(user=user).first()
#         if not cart or not cart.cartitem_set.exists():
#             return JsonResponse({"error": "Cart not found or empty"}, status=400)

#         # ✅ Check for active membership (for discounts)
#         user_membership = getattr(user, "user_membership", None)
#         is_member = user_membership and user_membership.status and user_membership.membership_end_date

#         discount_amount = Decimal(0)
#         delivery_charges = Decimal(50)  # Default delivery charge

#         if is_member:
#             discount_rate = Decimal(user_membership.plan.discount_rate)
#             discount_amount = (discount_rate / Decimal(100)) * final_price
#             final_price -= discount_amount
#             delivery_charges = Decimal(0)  # Free delivery for members

#         # ✅ Create the order inside an atomic transaction
#         with transaction.atomic():
#             order = Order.objects.create(
#                 user=user,
#                 customer_name=customer_name,  # Required for exports
#                 customer_email=customer_email,
#                 order_user_type="member" if is_member else "non-member",
#                 total_price=final_price,
#                 discounted_price=discount_amount,
#                 order_status="paid",
#                 state=state,
#                 city=city,
#                 address=address,
#                 pincode=pincode,
#                 delivery_charges=delivery_charges,
#             )

#             # ✅ Move cart items to order items
#             for item in cart.cartitem_set.all():
#                 Order_Item.objects.create(
#                     order=order,
#                     batch=item.product_batch,
#                     variant=item.product_variant,
#                     quantity=item.quantity,
#                     price=item.total_price,
#                 )

#                 # ✅ Decrease stock in inventory
#                 inventory = Inventory.objects.filter(batch=item.product_batch).first()
#                 if inventory and inventory.quantity >= item.quantity:
#                     inventory.quantity -= item.quantity
#                     inventory.save()

#             # ✅ Create payment record
#             Payment.objects.create(
#                 order=order,
#                 total_price=final_price,
#                 payment_mode="online",
#                 payment_status="completed",
#                 transaction_id=stripe_payment_id,
#             )

#             # ✅ Clear the cart
#             cart.cartitem_set.all().delete()

#         return JsonResponse({"status": "success", "message": "Payment processed successfully with export compliance!"}, status=200)

#     return JsonResponse({"status": "ignored", "message": "Event not processed"}, status=200)

@login_required

def cod_checkout(request):
    user = request.user
    try:
        cart = Cart.objects.get(user=user)
    except Cart.DoesNotExist:
        messages.error(request, "Your cart is empty!")
        return redirect("Ecommerce:cart_view")

    if not cart.cartitem_set.exists():
        messages.error(request, "Your cart is empty!")
        return redirect("Ecommerce:cart_view")

    total_price = sum(item.total_price for item in cart.cartitem_set.all())

    # Check user membership
    user_membership = User_membership.objects.filter(
        user=user, status=True, membership_end_date__gte=date.today()
    ).first()

    discount_amount = (Decimal(user_membership.plan.discount_rate) / 100) * total_price if user_membership else Decimal(0)
    total_price -= discount_amount
    delivery_charges = Decimal(0) if user_membership else Decimal(0)

    if request.method == "POST":
        address = request.POST.get("address", "").strip()
        city_id = request.POST.get("city", "").strip()
        pincode = request.POST.get("pincode", "").strip()

        if not all([address, city_id, pincode]):
            messages.error(request, "All fields (Address, City, and Pincode) are required!")
            return redirect("Ecommerce:checkout")

        try:
            pincode_obj = Pincode.objects.get(area_pincode__iexact=pincode)
            delivery_charges = Decimal(0) if user_membership else Decimal(pincode_obj.delivery_charges)
        except Pincode.DoesNotExist:
            messages.error(request, "Invalid pincode.")
            return redirect("Ecommerce:checkout")

        # Create order
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
            for item in cart.cartitem_set.select_related("product_variant", "product_batch").all():
                Order_Item.objects.create(
                    order=order,
                    batch=item.product_batch,
                    variant=item.product_variant,
                    quantity=item.quantity,
                    price=item.total_price,
                )

                # Reduce stock
                inventory = Inventory.objects.filter(batch=item.product_batch).first()
                if inventory and inventory.quantity >= item.quantity:
                    inventory.quantity -= item.quantity
                    inventory.save()
                else:
                    messages.error(request, f"Not enough stock for {item.product_variant}.")
                    return redirect("Ecommerce:cart_view")

            # Create payment record
            Payment.objects.create(
                order=order,
                total_price=total_price + delivery_charges,
                payment_mode="cash",
                payment_status="pending",
            )

            # Clear the cart
            cart.cartitem_set.all().delete()

        messages.success(request, "Order placed successfully! Pay on delivery.")
        return redirect("Ecommerce:confirm_Order")

    return render(request, "checkout.html", {"cart": cart, "total_price": total_price, "discount_amount": discount_amount})



def stripe_checkout(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    user = request.user
    cart = Cart.objects.filter(user=user).first()
    if not cart or cart.cartitem_set.count() == 0:
        messages.error(request, "Your cart is empty!")
        return redirect("Ecommerce:cart_view")

    total_price = Decimal(0)
    discount_rate = Decimal(0)
    line_items = []

    user_membership = User_membership.objects.filter(user=user, status=True, membership_end_date__gte=date.today()).first()
    if user_membership:
        discount_rate = Decimal(user_membership.plan.discount_rate)

    for cart_item in cart.cartitem_set.select_related("product_variant", "product_batch").all():
        inventory = Inventory.objects.filter(batch__variant=cart_item.product_variant).order_by('-create_at').first()
        if not inventory or inventory.sales_price is None:
            return JsonResponse({"error": f"Price not available for {cart_item.product_variant}"}, status=400)

        original_price = Decimal(inventory.sales_price)
        discounted_price = original_price * (1 - discount_rate / 100)
        total_price += discounted_price * cart_item.quantity

        product_image_url = (
            request.build_absolute_uri(cart_item.product_variant.product.product_image.url)
            if cart_item.product_variant.product.product_image else "https://via.placeholder.com/150"
        )

        line_items.append({
            'price_data': {
                "currency": "inr",
                'product_data': {'name': str(cart_item.product_variant), 'images': [product_image_url]},
                "unit_amount": max(1, int(discounted_price * 100)),
            },
            'quantity': cart_item.quantity,
        })

    address = request.POST.get("address", "").strip()
    city_id = request.POST.get("city", "").strip()
    pincode = request.POST.get("pincode", "").strip()

    if not all([address, city_id, pincode]):
        return JsonResponse({"error": "Missing address, city, or pincode!"}, status=400)

    pincode_obj, _ = Pincode.objects.get_or_create(area_pincode__iexact=pincode, defaults={'delivery_charges': 50})
    delivery_charges = Decimal(0) if user_membership else Decimal(pincode_obj.delivery_charges or 50)

    final_price = total_price + delivery_charges
    final_amount = max(1, int(final_price * 100))

    if delivery_charges > 0:
        line_items.append({
            'price_data': {
                "currency": "inr",
                'product_data': {'name': "Delivery Charges"},
                "unit_amount": int(delivery_charges * 100),
            },
            'quantity': 1,
        })

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url='http://127.0.0.1:8000/payment/success/',
            cancel_url='http://127.0.0.1:8000/payment/cancel/',
            metadata={"final_total": str(final_price)},
             billing_address_collection="required",
        shipping_address_collection={"allowed_countries": ["IN"]},
            
        )
        return redirect(session.url)
    except stripe.error.StripeError as e:
        return JsonResponse({"error": f"Stripe error: {str(e)}"}, status=500)


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.headers.get("Stripe-Signature")
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except (ValueError, stripe.error.SignatureVerificationError) as e:
        logger.error(f"Webhook error: {e}")
        return JsonResponse({"error": "Webhook validation failed"}, status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        customer_email = session.get("customer_email")
        stripe_payment_id = session.get("payment_intent")
        amount_total = session.get("amount_total")

        if not all([customer_email, stripe_payment_id, amount_total]):
            logger.error("Missing essential payment details")
            return JsonResponse({"error": "Missing essential payment details"}, status=400)

        final_price = Decimal(amount_total) / 100
        user = get_object_or_404(CustomUser, email=customer_email)

        cart = Cart.objects.filter(user=user).first()
        if not cart or not cart.cartitem_set.exists():
            logger.error("Cart is empty or does not exist")
            return JsonResponse({"error": "Cart not found or empty"}, status=400)

        user_membership = User_membership.objects.filter(user=user, status=True, membership_end_date__gte=date.today()).first()
        discount_rate = Decimal(user_membership.plan.discount_rate) if user_membership else Decimal(0)
        discount_amount = final_price * (discount_rate / 100)
        final_price -= discount_amount
        delivery_charges = Decimal(0) if user_membership else Decimal(50)

        try:
            with transaction.atomic():
                order = Order.objects.create(
                    user=user,
                    customer_email=customer_email,
                    total_price=final_price,
                    discounted_price=discount_amount,
                    order_status="Pending",
                    state=user.state,
                    city_id=user.city,
                    address=user.address,
                    pincode=user.pincode,
                    delivery_charges=delivery_charges,
                )

                for cart_item in cart.cartitem_set.all():
                    inventory = Inventory.objects.filter(batch=cart_item.product_batch).first()
                    if not inventory or inventory.quantity < cart_item.quantity:
                        logger.error(f"Insufficient stock for {cart_item.product_variant}")
                        return JsonResponse({"error": f"Insufficient stock for {cart_item.product_variant}"}, status=400)

                    Order_Item.objects.create(
                        order=order,
                        batch=cart_item.product_batch,
                        variant=cart_item.product_variant,
                        quantity=cart_item.quantity,
                        price=inventory.sales_price,
                    )

                    # Decrease inventory stock
                    inventory.quantity -= cart_item.quantity
                    inventory.save()

                Payment.objects.create(
                    order=order,
                    total_price=final_price,
                    payment_mode="online",
                    payment_status="completed",
                    transaction_id=str(stripe_payment_id),
                )

                # Clear the cart after successful order
                cart.cartitem_set.all().delete()

            return JsonResponse({"status": "success", "message": "Payment processed successfully!"}, status=200)

        except Exception as e:
            logger.error(f"Order processing error: {e}")
            return JsonResponse({"error": "Error processing order"}, status=500)

    return JsonResponse({"status": "ignored", "message": "Event not processed"}, status=200)

