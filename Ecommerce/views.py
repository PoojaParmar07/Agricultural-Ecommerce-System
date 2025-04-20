
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, JsonResponse, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from Ecommerce.models import *
from membership.models import *
from socialmedia.models import *
from .forms import *
from socialmedia.forms import *
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.db.models import Avg, F
from django.db import transaction
from datetime import date
from decimal import Decimal
from xhtml2pdf import pisa
import io
from PIL import Image   
from xhtml2pdf import pisa
# from weasyprint import HTML
# import tempfile
import os
import base64
from django.template.loader import get_template,render_to_string
# from django.http import HttpResponse
import json
from account.models import *
from account.form import *
from django.core.paginator import Paginator
from django.views.generic import ListView
import razorpay
import io

RAZORPAY_SECRET = "settings.RAZORPAY_SECRET_KEY"


def is_admin_user(user):
    return user.is_authenticated and user.is_staff  # Example function


def home(request):
    categories = Category.objects.all()  # Get all categories
    category_data = [
        {
            'category_id': category.category_id,
            'category_name': category.category_name.capitalize(),
            'category_image': category.category_image.url if category.category_image else None,
        }
        for category in categories
    ]

   
    products = Product.objects.all()


    product_data = []
    
    
    # Default empty cart_product_ids (for non-logged-in users)
    cart_product_ids = []

    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        # cart_items = CartItem.objects.filter(cart=cart)
        cart_items = CartItem.objects.filter(cart=cart).select_related(  # Filter by user's cart
        "product_variant", "product_variant_variant_id", "product_batch"
    ).prefetch_related("product_batch__inventory_set")

        cart_product_ids = list(cart_items.values_list(
            "product_variant__product__product_id", flat=True))

        cart_count = cart_items.values(
            "product_variant").distinct().count()
        print(cart_count)
        
    for product in products:
        variant = ProductVariant.objects.filter(product=product).first()
        inventory = Inventory.objects.filter(
            batch__variant=variant).first() if variant else None
        sales_price = inventory.sales_price if inventory else None
        rating = Review.objects.filter(product=product).aggregate(
            avg_rating=Avg('rating'))['avg_rating']

        product_data.append({
            'product_id': product.product_id,
            'product_name': product.product_name,
            'product_image': product.product_image.url if product.product_image else '/static/images/default-product.jpg',
            'sales_price': sales_price if sales_price is not None else "N/A",
            'rating': rating if rating is not None else 0
        })

    return render(request, "Ecommerce/base.html", {
        'categories': category_data,
        'product_data': product_data,
        'cart_product_ids': cart_product_ids,
        'cart_count': cart_count,
    })
    # return render(request, 'Ecommerce/base.html')


# def checkout(request):
#     return render(request, 'Ecommerce/checkout_page.html')
def homepage(request):
    categories = Category.objects.all()  # Get all categories
    category_data = [
        {
            'category_id': category.category_id,
            'category_name': category.category_name.capitalize(),
            'category_image': category.category_image.url if category.category_image else None,
        }
        for category in categories
    ]

    products = Product.objects.all()
    product_data = []

    # Default empty cart_product_ids (for non-logged-in users)
    cart_product_variant_ids = []

    # product_name = request.GET.get('product_name', '').strip()

    # if product_name != '' and product_name is not None:
    #     products = products.filter(product_name__icontains = product_name)

    # paginator = Paginator(products,5)
    # page = request.GET.get('page')
    # products = paginator.get_page(page)

    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        cart_product_variant_ids = list(cart_items.values_list(
    "product_variant__variant_id", flat=True))  # New (Tracks Variants)


    for product in products:
        variants = ProductVariant.objects.filter(product=product)
        # inventory = Inventory.objects.filter(
        #     batch__variant=variant).first() if variant else None
        # sales_price = inventory.sales_price if inventory else None
        # inventory_quantity = inventory.quantity if inventory else 0
        # rating = Review.objects.filter(product=product).aggregate(
        #     avg_rating=Avg('rating'))['avg_rating'] or 0

        # print(f"Product: {product.product_name} | Variant: {variant} | Sales Price: {sales_price} | Inventory Quantity: {inventory_quantity}")
        for variant in variants:  # Loop through all variants
                inventory = Inventory.objects.filter(batch__variant=variant).first()
                sales_price = inventory.sales_price if inventory else "N/A"
                inventory_quantity = inventory.quantity if inventory else 0

                rating = Review.objects.filter(product=product).aggregate(
                    avg_rating=Avg("rating")
                )["avg_rating"] or 0
                product_data.append({
                    'product_id': product.product_id,
                    'variant': variant,
                    'units': variant.units,
                    'product_name': product.product_name,
                    'product_image': product.product_image.url if product.product_image else '/static/images/default-product.jpg',
                    'sales_price': sales_price if sales_price else "N/A",
                    'rating': rating,
                    'inventory_quantity': inventory_quantity if inventory_quantity else 0,
                    # 'products' :products,
                })

    return render(request, "Ecommerce/homepage.html", {
        'categories': category_data,
        'product_data': product_data,
        'cart_product_variant_ids': cart_product_variant_ids,  # Pass this to the template
    })


def product_list(request, category_id):
    category = get_object_or_404(Category, category_id=category_id)
    products = Product.objects.filter(category=category)

    product_data = []
    cart_product_variant_ids = []  # Default empty cart for unauthenticated users

    # Check if the user is logged in, then get cart details
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        cart_product_variant_ids = list(cart_items.values_list(
    "product_variant__variant_id", flat=True))
        
    for product in products:
        variants = ProductVariant.objects.filter(product=product)
        
        for variant in variants:  # Loop through all variants
                inventory = Inventory.objects.filter(batch__variant=variant).first()
                sales_price = inventory.sales_price if inventory else "N/A"
                inventory_quantity = inventory.quantity if inventory else 0

                rating = Review.objects.filter(product=product).aggregate(
                    avg_rating=Avg("rating")
                )["avg_rating"] or 0
        product_data.append({ 
            'product_id': product.product_id,
            'variant': variant,
            'units': variant.units,
            'product_name': product.product_name,
            'product_image': product.product_image.url if product.product_image else '/static/images/default-product.jpg',
            'sales_price': sales_price if sales_price else "N/A",
            'rating': rating,
            'inventory_quantity': inventory_quantity if inventory_quantity else 0,
            # 'products' :products,
        })
    
    context = {
        'category_name': category.category_name,
        'product_data': product_data,
        'cart_product_variant_ids': cart_product_variant_ids,  # Pass this to the template
    }

    return render(request, 'Ecommerce/product_list_page.html', context)

def product_view(request, variant_id):
    variant = get_object_or_404(ProductVariant, variant_id=variant_id)

    # Get the product related to this variant
    product = variant.product

    # Fetch inventory details for the variant
    inventories = Inventory.objects.filter(batch__variant=variant).select_related('batch__variant')

    # Calculate total inventory stock
    inventory_quantity = sum(inventory.quantity for inventory in inventories) if inventories else 0

    # Prepare variant price mapping
    variant_prices = {
        str(inventory.batch.variant.variant_id): float(inventory.sales_price)
        for inventory in inventories
    }

    # Get the first available price for this variant
    first_price = variant_prices.get(str(variant.variant_id), "N/A")

    # Calculate product rating
    rating_data = Review.objects.filter(product=product).aggregate(avg_rating=Avg('rating'))
    rating = round(rating_data['avg_rating'], 1) if rating_data['avg_rating'] is not None else 0

    # Fetch reviews (newest first)
    reviews = Review.objects.filter(product=product).order_by('-created_at')

    # Get cart product IDs
    cart_product_variant_ids = []
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        cart_product_variant_ids = list(cart_items.values_list(
    "product_variant__variant_id", flat=True))
        

        # Check if the user has placed an order for this variant
        has_ordered = Order_Item.objects.filter(order__user=request.user, variant=variant).exists()
    else:
        has_ordered = False

    # Handle "Add to Cart" action
    if request.method == "POST" and "add_to_cart" in request.POST:
        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user)

            # Check if the product variant already exists in the cart
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product_variant=variant)

            if not created:
                cart_item.quantity += 1  # Increase quantity if already in cart
                cart_item.save()

            messages.success(request, f"{product.product_name} (Variant: {variant.variant_name}) added to cart!")
            return redirect('Ecommerce:product_view', variant_id=variant.variant_id)
        else:
            messages.error(request, "You need to log in to add items to the cart.")
            return redirect('account:login')

    # Handle review submission if user has placed an order
    if request.method == "POST" and "submit-review" in request.POST and has_ordered:
        rating_value = request.POST.get('rating')
        review_text = request.POST.get('comment')

        if rating_value and review_text:
            Review.objects.create(
                user=request.user,
                product=product,
                rating=int(rating_value),
                review=review_text.strip()
            )
            return redirect('Ecommerce:product_view', variant_id=variant.variant_id)
        else:
            messages.error(request, "Both rating and comment are required to submit a review.")
    else:
        messages.error(request, " You can only review this product if you have placed an order.")

    # Prepare variant data for context
    variant_data = {
        'variant_id': variant.variant_id,
        'variant_name': variant.units,
        'product_name': product.product_name,
        'product_image': product.product_image.url if product.product_image else None,
        'description': product.description or product.description,
        'rating': rating,
        'first_price': first_price,
    }

    context = {
        'product': variant_data,
        'inventory_quantity': inventory_quantity,
        'stars_range': range(1, 6),
        'reviews': reviews,
        'variants': [variant],  # Only show the selected variant here
        'cart_product_variant_ids': cart_product_variant_ids,
        'has_ordered': has_ordered,
        'variant_prices': json.dumps(variant_prices),
    }

    return render(request, 'Ecommerce/product_view.html', context)

# View Cart

@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(
        user=request.user)  # Get the user's cart
    cart_items = CartItem.objects.filter(cart=cart).select_related(  # Filter by user's cart
        "product_variant", "product_variant__product", "product_batch"
    ).prefetch_related("product_batch__inventory_set")

    categories = Category.objects.all()  # Fetch all categories

    # Store variant prices
    variant_prices = {}

    cart_product_ids = list(cart_items.values_list(
        "product_variant__product__product_id", flat=True))

    # Calculate grand total
    grand_total = sum(item.total_price for item in cart_items)

    #  Count unique products in cart
    # cart_count = cart_items.values(
    #     "product_variant__variant_id").distinct().count()

    for item in cart_items:
        
        if not item.product_variant or not item.product_variant.product:
            print(f"❌ Missing product for item {item.id}")  # Debugging line

        
        inventory = Inventory.objects.filter(batch=item.product_batch).first()
        item.product_variants = ProductVariant.objects.filter(
            product=item.product_variant.product)
        # Convert Decimal to float
        item.sales_price = float(inventory.sales_price) if inventory else 0
        # Handle missing inventory
        item.variant_price = inventory.sales_price if inventory else 0

        # Get all variants of the same product
        # item.product_variants = ProductVariant.objects.filter(
        #     product=item.product_variant.product)
        
        # Get the selected variant's units
        item.variant_units = item.product_variant.units

        item.product_variants = ProductVariant.objects.filter(
            product=item.product_variant.product)
        
        # Store prices for each variant
        for variant in item.product_variants:
            inventory_variant = Inventory.objects.filter(
                batch__variant=variant).first()
            variant_prices[str(variant.variant_id)] = float(
                inventory_variant.sales_price) if inventory_variant else 0

    context = {
        "cart_items": cart_items,
        "cart_product_ids": cart_product_ids,
        "variant_prices": variant_prices,
        "grand_total": grand_total,
        # "cart_count": cart_count,
        'categories': categories,
    }

    return render(request, "Ecommerce/cart.html", context)


def get_cart_count(request):
    """Returns the cart product count as a JSON response."""
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        unique_product_count = CartItem.objects.filter(cart=cart).values(
            "product_variant__product").distinct().count() if cart else 0
    else:
        unique_product_count = 0

    return JsonResponse({"cart_count": unique_product_count})


@login_required
def add_to_cart(request, variant_id):
    # product = get_object_or_404(Product, product_id=product_id)

    # Get first available variant and batch
    variant = get_object_or_404(ProductVariant, variant_id=variant_id)
    batch = ProductBatch.objects.filter(variant=variant).first()

    if not variant or not batch:
        return JsonResponse({"success": False, "message": "Product variant or batch not found"})

    # Get or create the user's cart
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Check if the item already exists in the cart
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product_batch=batch,
        product_variant=variant,
        # Default quantity when adding for the first time
        defaults={'quantity': 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("Ecommerce:homepage")


# Remove from Cart
@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(
        CartItem, cart__user=request.user, cart_item_id=item_id)
    cart_item.delete()

    return redirect('Ecommerce:cart_view')


@login_required
def increase_quantity(request):
    """Increases the quantity of a cart item, updates the price, and stores in DB."""

    if request.method == "POST":
        item_id = request.POST.get('item_id')

        if not item_id:
            return redirect("Ecommerce:cart_view")

        cart_item = get_object_or_404(
            CartItem, cart_item_id=item_id, cart__user=request.user)

        product = cart_item.product_variant.product

        if cart_item.quantity < product.max_qty:
            cart_item.quantity += 1
            cart_item.save()

    return redirect('Ecommerce:cart_view')


@login_required
def decrease_quantity(request):
    """Decreases the quantity of a cart item, updates the price, and stores in DB."""

    if request.method == "POST":
        item_id = request.POST.get('item_id')

        if not item_id:
            return redirect("Ecommerce:cart_view")

        cart_item = get_object_or_404(
            CartItem, cart_item_id=item_id, cart__user=request.user)

        product = cart_item.product_variant.product

        if cart_item.quantity > product.min_qty:
            cart_item.quantity -= 1
            cart_item.save()

    return redirect('Ecommerce:cart_view')


def update_variant(request, cart_item_id):
    """Handles variant selection and updates the cart item."""

    if request.method == "POST":
        variant_id = request.POST.get("variant_id")

        if not variant_id:
            # Redirect if no variant selected
            return redirect("Ecommerce:homepage")

        # Get the cart item
        cart_item = get_object_or_404(
            CartItem, cart_item_id=cart_item_id, cart__user=request.user)

        # Get the selected variant
        new_variant = get_object_or_404(ProductVariant, variant_id=variant_id)

        # Get the corresponding batch
        new_batch = get_object_or_404(ProductBatch, variant=new_variant)

        # Fetch the inventory record for the selected variant
        inventory = Inventory.objects.filter(
            batch__variant=new_variant).first()

        if inventory:
            # Update the cart item with the new variant and price
            cart_item.product_variant = new_variant
            cart_item.product_batch = new_batch
            cart_item.save()
        else:
            print("No inventory found for this variant")  # Debugging

    # Reload the cart page to reflect changes
    return redirect("Ecommerce:homepage")
# Initialize Razorpay client
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))


@login_required
def checkout(request):
    """ Renders the checkout page and fetches delivery charge dynamically """
   
    cart = Cart.objects.get(user=request.user)
    cart_items = cart.cartitem_set.all()
    cities = City.objects.all()

    selected_city_id = request.GET.get("city")
    selected_pincode_id = request.GET.get("pincode")

    # Fetch available pincodes for the selected city
    pincodes = Pincode.objects.filter(city_id=selected_city_id) if selected_city_id else []

    # Check if user has an active membership
    user_membership = User_membership.objects.filter(
        user=request.user,
        status=True,
        membership_end_date__gte=date.today()
    ).select_related('plan').first()

    is_member = bool(user_membership)
    membership_discount = Decimal(user_membership.plan.discount_rate) if is_member else Decimal(0)

    # Calculate total price before discount
    grand_total = sum(Decimal(item.total_price) for item in cart_items)
    discount_amount = (grand_total * membership_discount / Decimal(100)) if is_member else Decimal(0)
    total_after_discount = grand_total - discount_amount

    # Default delivery charge
    delivery_charge = Decimal(0)

    if is_member:
        delivery_charge = Decimal(0)  # Free delivery for members
    elif selected_pincode_id:
        delivery_charge = Pincode.objects.filter(area_pincode=selected_pincode_id).values_list('delivery_charges', flat=True).first() or Decimal(0)

    # Final total including delivery charge
    final_total = total_after_discount + delivery_charge
    amount = int(final_total * 100)  # Convert to paise for Razorpay
    

    context = {
        "cart_items": cart_items,
        "grand_total": float(grand_total),
        "discount_amount": float(discount_amount),
        "total_after_discount": float(total_after_discount),
        "final_total": float(final_total),
        "is_member": is_member,
        "cities": cities,
        "pincodes": pincodes,
        "selected_city_id": selected_city_id,
        "selected_pincode_id": selected_pincode_id,
        "delivery_charge": float(delivery_charge),
        "razorpay_key": settings.RAZORPAY_KEY_ID,
        "amount": amount,  # Amount for Razorpay
    }

    return render(request, "Ecommerce/checkout_page.html", context)

@login_required
def get_delivery_charge_ajax(request, pincode_id):
    """ 
    Fetch delivery charge based on pincode selection 
    and create a new Razorpay order with updated amount.
    """

    # Check if user is a member
    is_member = User_membership.objects.filter(
        user=request.user,
        status=True,
        membership_end_date__gte=date.today()
    ).exists()

    # Free delivery for members
    

    try:
        # Fetch delivery charge
        pincode_instance = Pincode.objects.get(area_pincode=str(pincode_id))
        delivery_charge = float(pincode_instance.delivery_charges)
        # print(delivery_charge)
        # Get user's cart details
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.cartitem_set.all()
        grand_total = sum(float(item.total_price) for item in cart_items)

        # Fetch membership discount
        user_membership = User_membership.objects.filter(
            user=request.user,
            status=True,
            membership_end_date__gte=date.today()
        ).select_related('plan').first()

        discount_rate = float(user_membership.plan.discount_rate) if user_membership else 0.0
        discount_amount = (grand_total * discount_rate / 100) if user_membership else 0.0

        # Calculate final total
        total_after_discount = grand_total - discount_amount
        final_total = total_after_discount + delivery_charge
        amount = int(final_total * 100)  # Convert to paise

        # 🔥 Create a new Razorpay order with the updated amount
        order_currency = "INR"
        new_payment_order = client.order.create(dict(amount=amount, currency=order_currency, payment_capture=1))
        new_order_id = new_payment_order['id']
        if is_member:
            return JsonResponse({
                "delivery_charge": 0.0,
                "new_total": total_after_discount,
                "new_order_id": new_order_id,
                "discount_amount": discount_amount,
        })
        
        return JsonResponse({
            "delivery_charge": delivery_charge,
            "new_total": final_total,
            "new_order_id": new_order_id,
            "discount_amount": discount_amount ,
        })

    except Exception as e:
        import traceback
        traceback.print_exc()  # logs full error to console
        return JsonResponse({"error": str(e)}, status=500)

    
    
    

@csrf_protect
@login_required
def payment_success(request):
    
    print("!!!!!")
    """Handles order creation after successful payment"""
    if request.method == "POST":
        try:
            # ✅ Extract Payment Data
            razorpay_payment_id = request.POST.get("razorpay_payment_id")
            razorpay_order_id = request.POST.get("razorpay_order_id")

            # ✅ Extract User Entered Details
            user = request.user
            # first_name = request.POST.get("first_name")
            address = request.POST.get("address")
            city_id = request.POST.get("city")  # Assuming ID is stored
            pincode = request.POST.get("pincode")
            pincode_instance= Pincode.objects.get(area_pincode=pincode)
            delivery_charge = Decimal(request.POST.get('delivery_charge') or 0)
            cart = Cart.objects.get(user=user)
            cart_items = cart.cartitem_set.all()

            if not cart_items:
                return JsonResponse({"success": False, "message": "Cart is empty. Cannot place order."})

            # ✅ Check Membership Discount
            user_membership = User_membership.objects.filter(
                user=user, status=True, membership_end_date__gte=date.today()
            ).select_related('plan').first()

            is_member = bool(user_membership)
            membership_discount = Decimal(user_membership.plan.discount_rate) if is_member else Decimal(0)

            # ✅ Calculate total price before discount
            grand_total = sum(Decimal(item.total_price) for item in cart_items)
            discount_amount = (grand_total * membership_discount / Decimal(100)) if is_member else Decimal(0)
            total_after_discount = grand_total - discount_amount
            
            if is_member:
                 delivery_charge = Decimal(0)
 # Default delivery charge
            print(f"grand_total-{grand_total}")

            final_total = total_after_discount + delivery_charge

            # ✅ Store Order & Payment Data
            with transaction.atomic():
                # Create Order
                order = Order.objects.create(
                    user=user,
                    order_user_type="member" if is_member else "non-member",
                    total_price=grand_total,
                    discounted_price=discount_amount,
                    order_status="pending",
                    state=user.state,
                    city_id=city_id,  # Store city entered by user
                    address=address,  # Store updated address
                    pincode=pincode_instance,  # Store pincode entered by user
                    delivery_charges=delivery_charge,
                )

                # Move Cart Items to Order Items
                for item in cart_items:
                    Order_Item.objects.create(
                        order=order,
                        batch=item.product_batch,  # Ensure field names match
                        variant=item.product_variant,  # Ensure field names match
                        quantity=item.quantity,
                        price=item.total_price,  # Store total price of the item
                    )

                # Create Payment Record
                Payment.objects.create(
                    order=order,
                    total_price=final_total,
                    payment_mode="online",
                    payment_status="completed",
                    razorpay_order_id=razorpay_order_id,
                    razorpay_payment_id=razorpay_payment_id,
                )

                # ✅ Clear Cart after transferring items to order
                cart.cartitem_set.all().delete()

            return JsonResponse({"success": True, "message": "Order placed successfully!"})

        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})
    else:
        print("Not create order in backend")
    
            
@login_required
def confirm_Order(request):
    # Get the latest order for the logged-in user
    order = Order.objects.filter(user=request.user).last()

    if not order:  # Handle case when no order exists
        return render(request, 'Ecommerce/confirm.html', {'error': "No order found"})

    return render(request, 'Ecommerce/confirm.html', {'order': order})


@login_required
def get_pincode(request, city_id):
    """Fetches all pincodes for a given city ID."""
    city = get_object_or_404(City, pk=city_id)  # Ensures the city exists
    # Using related_name for clarity
    pincodes = city.pincodes.values("pincode_id", "area_pincode")
    print("🚀 Pincode API Response:", list(pincodes))
    print(f"Fetching pincodes for city ID: {city}")
    return JsonResponse({"pincodes": list(pincodes)})



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


# def render_pdf_view(request):
#     users = CustomUser.objects.all()
#     template_path = 'admin_dashboard/userlist.html'
#     context = {'users': users}

#     template = get_template(template_path)
#     html = template.render(context)

#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="user_report.pdf"'

#     pisa_status = pisa.CreatePDF(html, dest=response)

#     if pisa_status.err:
#         return HttpResponse('We had some errors <pre>' + html + '</pre>')

#     return response


@login_required
def wishlist_view(request):
    wishlist, _ = Wishlist.objects.get_or_create(
        user=request.user)  # Get the user's cart
    wishlist_items = WishlistItem.objects.filter(wishlist=wishlist).select_related(  # Filter by user's cart
        "product_variant", "product_variant__product", "product_batch"
    ).prefetch_related("product_batch__inventory_set")

    categories = Category.objects.all()  # Fetch all categories

    # Store variant prices
    variant_prices = {}

    wishlist_product_ids = list(wishlist_items.values_list(
        "product_variant__product__product_id", flat=True))

    # Calculate grand total
    # grand_total = sum(item.total_price for item in wishlist_items)

    for item in wishlist_items:
        if not item.product_variant or not item.product_variant.product:
            print(f"❌ Missing product for item {item.id}")  # Debugging line

        inventory = Inventory.objects.filter(batch=item.product_batch).first()
        item.product_variants = ProductVariant.objects.filter(
            product=item.product_variant.product)
        # Convert Decimal to float
        item.sales_price = float(inventory.sales_price) if inventory else 0
        # Handle missing inventory
        item.variant_price = inventory.sales_price if inventory else 0

        item.variant_units = item.product_variant.units
        # Get all variants of the same product
        item.product_variants = ProductVariant.objects.filter(
            product=item.product_variant.product)

        # Store prices for each variant
        for variant in item.product_variants:
            inventory_variant = Inventory.objects.filter(
                batch__variant=variant).first()
            variant_prices[str(variant.variant_id)] = float(
                inventory_variant.sales_price) if inventory_variant else 0

    context = {
        "wishlist_items": wishlist_items,
        "wishlist_product_ids": wishlist_product_ids,
        "variant_prices": variant_prices,
        'categories': categories,
    }

    return render(request, "Ecommerce/wishlist_view.html", context)


@login_required
def add_to_wishlist(request, variant_id):
    # Get the product variant
    variant = get_object_or_404(ProductVariant, variant_id=variant_id)

    # Get the first available batch of this variant
    batch = ProductBatch.objects.filter(variant=variant).first()

    if not batch:
        return JsonResponse({"success": False, "message": "No available batch for this variant."})

    # Get or create the wishlist for the user
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)

    # Check if the item already exists in the wishlist
    wishlist_item, created = WishlistItem.objects.get_or_create(
        wishlist=wishlist,
        product_batch=batch,
        product_variant=variant
    )

    if created:
        message = "Item added to wishlist."
    else:
        message = "Item already in wishlist."

    return redirect('Ecommerce:homepage')


@login_required
def remove_from_wishlist(request, item_id):
    print(f"Trying to remove wishlist item: {item_id}")  # Debugging line

    wishlist_item = get_object_or_404(
        # Use wishlist__user instead of cart__user
        WishlistItem, wishlist__user=request.user, id=item_id)

    wishlist_item.delete()
    print(f"Removed wishlist item: {item_id}")  # Debugging line

    return redirect('Ecommerce:wishlist')


class ProductSearchView(ListView):
    model = Product
    template_name = "Ecommerce/search.html"
    context_object_name = "products"

    def get_queryset(self):
        query = self.request.GET.get("product_name", "").strip()
        if query:
            return Product.objects.filter(product_name__icontains=query)
        return Product.objects.none()

    # def get(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     if not queryset.exists():
    #         return redirect(reverse("Ecommerce:homepage"))
    #     return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get("product_name", "")
        context["search_query"] = search_query

        if self.request.user.is_authenticated:
            cart_items = CartItem.objects.filter(cart__user=self.request.user).values_list(
                "product_batch__product_id", flat=True
            )
            wishlist_items = WishlistItem.objects.filter(
                wishlist__user=self.request.user
            ).values_list("product_batch__product_id", flat=True)
        else:
            cart_items = []
            wishlist_items = []

        product_data = []
        products = self.get_queryset()
        
        if not search_query:
            context["message"] = "Please enter a product name to search."
        elif not products.exists():
            context["message"] = "No products found for your search."


        for product in products:
            variants = ProductVariant.objects.filter(product=product)  # Fetch all variants

            for variant in variants:  # Loop through all variants
                inventory = Inventory.objects.filter(batch__variant=variant).first()
                sales_price = inventory.sales_price if inventory else "N/A"
                inventory_quantity = inventory.quantity if inventory else 0

                rating = Review.objects.filter(product=product).aggregate(
                    avg_rating=Avg("rating")
                )["avg_rating"] or 0

                product_data.append({
                    "product_id": product.product_id,  # Product ID remains the same
                    "product_name": product.product_name,
                    "product_image": product.product_image.url if product.product_image else "/static/images/default-product.jpg",
                    "variant_id": variant.variant_id,  # Unique Variant ID
                    "units": variant.units,
                    "sales_price": sales_price,
                    "inventory_quantity": inventory_quantity,
                    "rating": rating,
                })

        context["cart_product_ids"] = list(cart_items)
        context["wishlist_product_ids"] = list(wishlist_items)
        context["product_data"] = product_data  # Now includes all variants

        return context

    


def aboutus(request):
    return render(request, 'Ecommerce/aboutus.html')


def enquiry(request):
    return render(request, 'Ecommerce/enquiry.html')


def crop_info(request):
    return render(request, 'Ecommerce/crop_info.html')


def okra(request):
    return render(request, 'Ecommerce/crop_detail/okra.html')

def spinach(request):
    return render(request, 'Ecommerce/crop_detail/spinach.html')

def tomato(request):
    return render(request, 'Ecommerce/crop_detail/tomato.html')

def corainder(request):
    return render(request, 'Ecommerce/crop_detail/corainder.html')

def potato(request):
    return render(request, 'Ecommerce/crop_detail/potato.html')

def peas(request):
    return render(request, 'Ecommerce/crop_detail/peas.html')


def kishan_charcha(request):

    posts = Post.objects.all().order_by('-created_at')
    comment_form = PostCommentForm()
    show_comments = request.GET.get("show_comments", None)
    return render(request, "Ecommerce/kishan_charcha.html", {"posts": posts, "comment_form": comment_form, "show_comments": show_comments})


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, post_id=post_id)
    if request.method == "POST":
        comment_text = request.POST.get("comment_text")
        # Get parent comment ID (if replying)
        parent_comment_id = request.POST.get("parent_comment_id")

        if comment_text:
            parent_comment = None
            if parent_comment_id:
                parent_comment = get_object_or_404(
                    PostComment, comment_id=parent_comment_id)

            PostComment.objects.create(
                user=request.user,
                post=post,
                comment_text=comment_text,
                parent_comment=parent_comment
            )

        # Redirect back to post page
        return redirect("Ecommerce:kishan_charcha")

    return redirect("Ecommerce:homepage")


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-create_at')
    return render(request, 'Ecommerce/order_history.html', {'orders': orders})

@csrf_exempt
@login_required
def order_invoice(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    order_items = order.order_item_set.all()

    subtotal = sum(Decimal(item.price) * item.quantity for item in order_items)
    discount = Decimal(order.discounted_price) if order.discounted_price else Decimal(0)
    shipping = Decimal(order.delivery_charges) if order.delivery_charges else Decimal(0)
    grand_total = subtotal - discount + shipping

    # Convert the logo image to Base64
    logo_path = os.path.join(settings.BASE_DIR, "media/logo.jpg")  # Adjust path
    with open(logo_path, "rb") as image_file:
        logo_base64 = base64.b64encode(image_file.read()).decode("utf-8")

    html_string = render_to_string('Ecommerce/order_invoice.html', {
        'order': order,
        'order_items': order_items,
        'total_products': sum(item.quantity for item in order_items),
        "subtotal": float(subtotal),
        "discount": float(discount),
        "shipping": float(shipping),
        "grand_total": float(grand_total),
        'logo_base64': f"data:image/jpeg;base64,{logo_base64}",
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order.order_id}.pdf"'

    pdf = io.BytesIO()
    pdf_status = pisa.CreatePDF(html_string, dest=pdf)

    if pdf_status.err:
        return HttpResponse("Error generating PDF", status=500)

    response.write(pdf.getvalue())
    return response
    

@login_required
def order_details(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)

    if order.user != request.user:
        return HttpResponse("You do not have permission to view this order", status=403)

    order_items = order.order_item_set.all()
    
    # Extract values
    subtotal = sum(Decimal(item.price) * item.quantity for item in order_items)
    discount = Decimal(order.discounted_price) if order.discounted_price else Decimal(0)
    shipping = Decimal(order.delivery_charges) if order.delivery_charges else Decimal(0)
    grand_total = subtotal - discount + shipping
    for item in order_items:
        item.total_price = item.price * item.quantity

    # Calculate total order price
    total_price = sum(item.total_price for item in order_items)

    return render(request, "Ecommerce/order_detail.html", {
        "order": order,
        "order_items": order_items,
        "total_products": sum(item.quantity for item in order_items),
        "subtotal": float(subtotal),
        "discount": float(discount),
        "shipping": float(shipping),
        "grand_total": float(grand_total),
        'total_price': total_price  
       
    })



@login_required
def enquiry_view(request):
    if request.method == 'POST':
        form = EnquiryForm(request.POST)
        if form.is_valid():
            enquiry = form.save(commit=False)
            enquiry.user = request.user
            enquiry.save()
            return redirect('Ecommerce:homepage')
    else:
        form = EnquiryForm()

    return render(request, 'Ecommerce/enquiry.html', {'form': form})

def membership_plan(request):
    membership_plans = Membership_plan.objects.all()
    for plan in membership_plans:
        print(plan.plan_name) 
    return render(request, 'membership/membership.html', {'membership_plans': membership_plans})\
        
        
        

@csrf_exempt
@login_required
def payment_success(request):
    
   
    """Handles order creation after successful payment"""
    if request.method == "POST":
        try:
            # ✅ Extract Payment Data
            razorpay_payment_id = request.POST.get("razorpay_payment_id")
            razorpay_order_id = request.POST.get("razorpay_order_id")
            razorpay_signature=request.POST.get('razorpay_signature')

            # ✅ Extract User Entered Details
            user = request.user
            # first_name = request.POST.get("first_name")
            address = request.POST.get("address")
            city_id = request.POST.get("city")  # Assuming ID is stored
            pincode = request.POST.get("pincode")
            pincode_instance= Pincode.objects.get(area_pincode=pincode)
           
            cart = Cart.objects.get(user=user)
            cart_items = cart.cartitem_set.all()

            if not cart_items:
                return JsonResponse({"success": False, "message": "Cart is empty. Cannot place order."})

            # ✅ Check Membership Discount
            user_membership = User_membership.objects.filter(
                user=user, status=True, membership_end_date__gte=date.today()
            ).select_related('plan').first()

            is_member = bool(user_membership)
            membership_discount = Decimal(user_membership.plan.discount_rate) if is_member else Decimal(0)

            # ✅ Calculate total price before discount
            grand_total = sum(Decimal(item.total_price) for item in cart_items)
            discount_amount = (grand_total * membership_discount / Decimal(100)) if is_member else Decimal(0)
            total_after_discount = grand_total - discount_amount
            delivery_charge = Decimal(0) if is_member else Decimal(50)  # Default delivery charge

            final_total = total_after_discount + delivery_charge

            # ✅ Store Order & Payment Data
            with transaction.atomic():
                # Create Order
                order = Order.objects.create(
                    user=user,
                    order_user_type="member" if is_member else "non-member",
                    total_price=grand_total,
                    discounted_price=discount_amount,
                    order_status="pending",
                    state=user.state,
                    city_id=city_id,  # Store city entered by user
                    address=address,  # Store updated address
                    pincode=pincode_instance,  # Store pincode entered by user
                    delivery_charges=delivery_charge,
                )

                # Move Cart Items to Order Items
                for item in cart_items:
                    Order_Item.objects.create(
                        order=order,
                        batch=item.product_batch,  # Ensure field names match
                        variant=item.product_variant,  # Ensure field names match
                        quantity=item.quantity,
                        price=item.total_price,  # Store total price of the item
                    )
                    
                inventory = Inventory.objects.filter(batch=item.product_batch).first()
                if inventory and inventory.quantity >= item.quantity:
                    inventory.quantity -= item.quantity
                    inventory.save()
                else:
                    messages.error(request, f"Not enough stock for {item.product_variant}.")
                    return redirect("Ecommerce:cart_view")

                # Create Payment Record
                Payment.objects.create(
                    order=order,
                    total_price=final_total,
                    payment_mode="online",
                    payment_status="completed",
                    razorpay_order_id=razorpay_order_id,
                    razorpay_payment_id=razorpay_payment_id,
                    razorpay_signature=razorpay_signature,
                )

                # ✅ Clear Cart after transferring items to order
                cart.cartitem_set.all().delete()

            return JsonResponse({"success": True, "message": "Order placed successfully!"})

        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})
    else:
        print("Not create order in backend")
        
        
def product_listing(request):
    
    categories = Category.objects.all()
    category_data = []
    category_data = [
        {
            'category_id': category.category_id,
            'category_name': category.category_name.capitalize(),
            'category_image': category.category_image.url if category.category_image else None,
        }
        for category in categories
    ]

    
    products = Product.objects.all()
    product_data = []
    cart_product_variant_ids = []
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        cart_product_variant_ids = list(cart_items.values_list(
    "product_variant__variant_id", flat=True))  # New (Tracks Variants)


    for product in products:
        variants = ProductVariant.objects.filter(product=product)
        # inventory = Inventory.objects.filter(
        #     batch__variant=variant).first() if variant else None
        # sales_price = inventory.sales_price if inventory else None
        # inventory_quantity = inventory.quantity if inventory else 0
        # rating = Review.objects.filter(product=product).aggregate(
        #     avg_rating=Avg('rating'))['avg_rating'] or 0

        # print(f"Product: {product.product_name} | Variant: {variant} | Sales Price: {sales_price} | Inventory Quantity: {inventory_quantity}")
        for variant in variants:  # Loop through all variants
                inventory = Inventory.objects.filter(batch__variant=variant).first()
                sales_price = inventory.sales_price if inventory else "N/A"
                inventory_quantity = inventory.quantity if inventory else 0

                rating = Review.objects.filter(product=product).aggregate(
                    avg_rating=Avg("rating")
                )["avg_rating"] or 0
                product_data.append({
                    'product_id': product.product_id,
                    'variant': variant,
                    'units': variant.units,
                    'product_name': product.product_name,
                    'product_image': product.product_image.url if product.product_image else '/static/images/default-product.jpg',
                    'sales_price': sales_price if sales_price else "N/A",
                    'rating': rating,
                    'inventory_quantity': inventory_quantity if inventory_quantity else 0,
                    # 'products' :products,
                })

    return render(request, "Ecommerce/product_listing.html", {
        'categories': category_data,
        'product_data': product_data,
        'cart_product_variant_ids': cart_product_variant_ids,  # Pass this to the template
    })