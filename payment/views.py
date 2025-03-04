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
import razorpay
import hmac
import hashlib
import base64


logger = logging.getLogger(__name__)

RAZORPAY_SECRET = "settings.RAZORPAY_SECRET"








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






@login_required
def razorpay_checkout(request):
    user = request.user
    cart = get_object_or_404(Cart, user=user)

    if not cart.cartitem_set.exists():
        messages.error(request, "Your cart is empty!")
        return redirect("Ecommerce:cart_view")

    total_price = sum(item.total_price for item in cart.cartitem_set.all())
    user_membership = User_membership.objects.filter(
        user=user, status=True, membership_end_date__gte=now().date()
    ).first()

    discount_amount = (Decimal(user_membership.plan.discount_rate) / 100) * total_price \
        if user_membership and user_membership.plan else Decimal(0)
    total_price -= discount_amount

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
            messages.error(request, "Invalid pincode. Please enter a valid one.")
            return redirect("Ecommerce:checkout")

        try:
            city_obj = City.objects.get(city_id=city_id)
        except City.DoesNotExist:
            messages.error(request, "Invalid city selection.")
            return redirect("Ecommerce:checkout")

        final_total = total_price + delivery_charges

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))
        razorpay_order = client.order.create({
            "amount": int(final_total * 100),  # Convert to paise
            "currency": "INR",
            "payment_capture": 1,  # Auto capture payment
        })

        with transaction.atomic():
            order = Order.objects.create(
                user=user,
                order_user_type="member" if user_membership else "non-member",
                total_price=total_price,
                discounted_price=discount_amount,
                order_status="pending",
                state=user.state,
                city=city_obj,
                address=address,
                pincode=pincode_obj,
                delivery_charges=delivery_charges,
            )

            payment = Payment.objects.create(
                order=order,
                total_price=final_total,
                payment_mode="Online",
                payment_status="pending",
                razorpay_order_id=razorpay_order["id"],
            )

        context = {
            "cart": cart,
            "total_price": total_price,
            "discount_amount": discount_amount,
            "final_total": int(final_total * 100),
            "razorpay_order_id": razorpay_order["id"],
            "razorpay_key": settings.RAZORPAY_KEY_ID,
        }

        return render(request, "payment/razorpay_checkout.html", context)

    return redirect("Ecommerce:checkout")




@csrf_exempt
def razorpay_webhook(request):
    if request.method == "POST":
        try:
            print("\n🔹 Webhook Received")

            # Read raw request body
            raw_body = request.body.decode("utf-8").strip()
            received_data = json.loads(raw_body)
            provided_signature = request.headers.get("X-Razorpay-Signature")

            if not provided_signature:
                return JsonResponse({"error": "Missing signature"}, status=400)

            webhook_secret = settings.RAZORPAY_WEBHOOK_SECRET.encode()
            expected_signature = hmac.new(webhook_secret, raw_body.encode("utf-8"), hashlib.sha256).hexdigest()

            if not hmac.compare_digest(provided_signature, expected_signature):
                return JsonResponse({"error": "Invalid webhook signature"}, status=400)

            event = received_data.get("event", "")

            if event == "order.paid":
                payment_entity = received_data["payload"]["payment"]["entity"]
                razorpay_payment_id = payment_entity["id"]
                razorpay_order_id = payment_entity["order_id"]
                amount_paid = Decimal(payment_entity["amount"]) / 100  # Convert to INR

                try:
                    with transaction.atomic():
                        # ✅ Fetch payment and order
                        payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)
                        order = payment.order

                        # ✅ Update payment details
                        payment.payment_status = "completed"
                        payment.razorpay_payment_id = razorpay_payment_id
                        payment.total_price = amount_paid
                        payment.save()

                        # ✅ Update order status
                        order.order_status = "confirmed"
                        order.save()

                        # ✅ Transfer cart items to order items
                        cart = Cart.objects.get(user=order.user)
                        cart_items = cart.cartitem_set.select_related("product_variant", "product_batch").all()

                        for item in cart_items:
                            Order_Item.objects.create(
                                order=order,
                                batch=item.product_batch,
                                variant=item.product_variant,
                                quantity=item.quantity,
                                price=item.total_price,
                            )

                            # ✅ Reduce stock
                            inventory = Inventory.objects.filter(batch=item.product_batch).first()
                            if inventory and inventory.quantity >= item.quantity:
                                inventory.quantity -= item.quantity
                                inventory.save()
                            else:
                                print(f"⚠️ Not enough stock for {item.product_variant}")

                        # ✅ Clear the cart
                        cart_items.delete()

                        print("✅ Order confirmed, items transferred, stock updated, and cart cleared.")
                        return JsonResponse({"message": "Payment & order updated successfully"}, status=200)

                except Payment.DoesNotExist:
                    return JsonResponse({"error": "Payment not found"}, status=404)

            return JsonResponse({"message": "Unhandled event"}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)



