
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
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Avg,F
from django.db import transaction
from datetime import date
from decimal import Decimal

from xhtml2pdf import pisa
from django.template.loader import get_template
# from django.http import HttpResponse
import json
from account.models import *
from account.form import *
from django.core.paginator import Paginator
from django.views.generic import ListView
import razorpay

RAZORPAY_SECRET = "settings.RAZORPAY_SECRET"

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
    
    cart_count = cart_items.values(
        "product_variant__product").distinct().count()

    product_data = []

    # Default empty cart_product_ids (for non-logged-in users)
    cart_product_ids = []

    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        cart_product_ids = list(cart_items.values_list(
            "product_variant__product__product_id", flat=True))

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
    cart_product_ids = []


    # product_name = request.GET.get('product_name', '').strip()
    
    # if product_name != '' and product_name is not None:
    #     products = products.filter(product_name__icontains = product_name)

    # paginator = Paginator(products,5)
    # page = request.GET.get('page')
    # products = paginator.get_page(page)

    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        cart_product_ids = list(cart_items.values_list(
            "product_variant__product__product_id", flat=True))

    for product in products:
        variant = ProductVariant.objects.filter(product=product).first() if ProductVariant.objects.filter(product=product).exists() else None
        inventory = Inventory.objects.filter(batch__variant=variant).first() if variant else None
        sales_price = inventory.sales_price if inventory else None
        inventory_quantity = inventory.quantity if inventory else 0
        rating = Review.objects.filter(product=product).aggregate(
            avg_rating=Avg('rating'))['avg_rating'] or 0

        # print(f"Product: {product.product_name} | Variant: {variant} | Sales Price: {sales_price} | Inventory Quantity: {inventory_quantity}")

        product_data.append({
            'product_id': product.product_id,
            'variant': variant,
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
        'cart_product_ids': cart_product_ids,  #  Pass this to the template
    })


def product_list(request, category_id):
    category = get_object_or_404(Category, category_id=category_id)
    products = Product.objects.filter(category=category)

    product_data = []
    cart_product_ids = []  # Default empty cart for unauthenticated users
    
    

    # Check if the user is logged in, then get cart details
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        cart_product_ids = list(cart_items.values_list(
            "product_variant__product__product_id", flat=True))

    for product in products:
        variant = ProductVariant.objects.filter(product=product).first()
        inventory = Inventory.objects.filter(
            batch__variant=variant).first() if variant else None
        sales_price = inventory.sales_price if inventory else None
        inventory_quantity = inventory.quantity if inventory else 0  #  Get stock quantity

        # Get average rating
        rating = Review.objects.filter(product=product).aggregate(
            avg_rating=Avg('rating'))['avg_rating'] or 0

        product_data.append({
            'product_id': product.product_id,
            'product_name': product.product_name,
            'product_image': product.product_image.url if product.product_image else None,
            'sales_price': sales_price,
            'rating': rating,
            'inventory_quantity': inventory_quantity,  #  Include quantity for stock check
        })

    context = {
        'category_name': category.category_name,
        'products': product_data,
        #  Add this for the cart check in the template
        'cart_product_ids': cart_product_ids,
    }

    return render(request, 'Ecommerce/product_list_page.html', context)


def product_view(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    print(f"Product ID: {product.product_id}")  # Debugging

    # Fetch variants and related brands
    variants = list(ProductVariant.objects.filter(product=product).select_related('brand'))

    # Fetch inventory related to those variants
    inventories = Inventory.objects.filter(batch__variant__in=variants).select_related('batch__variant')
    inventory_quantity = sum(inventory.quantity for inventory in inventories) if inventories else 0

    # Build variant prices dictionary
    variant_prices = {
        str(inventory.batch.variant.variant_id): float(inventory.sales_price)
        for inventory in inventories
    }

    # Get the first available price, else "N/A"
    first_price = next((price for price in variant_prices.values() if price is not None), "N/A")

    # Calculate average rating
    rating_data = Review.objects.filter(product=product).aggregate(avg_rating=Avg('rating'))
    rating = round(rating_data['avg_rating'], 1) if rating_data['avg_rating'] is not None else 0

    # Fetch reviews in descending order
    reviews = Review.objects.filter(product=product).order_by('-created_at')

    #  Get cart product IDs
    cart_product_ids = []
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        cart_product_ids = list(cart_items.values_list("product_variant__product__product_id", flat=True))

        #  Check if the user has placed an order for this product
        has_ordered = Order_Item.objects.filter(order__user=request.user, variant__product=product).exists()

    else:
        has_ordered = False

    #  Handle review submission only if user has placed an order
    if request.method == "POST" and has_ordered:
        rating_value = request.POST.get('rating')
        review_text = request.POST.get('comment')

        if rating_value and review_text:  # Ensure both fields are filled
            Review.objects.create(
                user=request.user,
                product=product,
                rating=int(rating_value),  # Convert to integer
                review=review_text.strip()  # Trim spaces
            )
            return redirect('Ecommerce:product_view', product_id=product.product_id)
    else:
        messages.error(request," You can only review this product if you have placed an order.")

    # Prepare product data
    product_data = {
        'product_id': product.product_id,
        'product_name': product.product_name,
        'product_image': product.product_image.url if product.product_image else "/static/images/no_image.jpg",
        'description': product.description,
        'rating': rating,
        'first_price': first_price,
    }

    print(" Variant Prices JSON:", json.dumps(variant_prices, ensure_ascii=False))
    print(f"Inventory: {inventory_quantity}")

    context = {
        'product': product_data,
        'inventory_quantity': inventory_quantity,
        'stars_range': range(1, 6),
        'reviews': reviews,
        'variants': variants,
        'cart_product_ids': cart_product_ids,  #  Add cart products for button logic
        'has_ordered': has_ordered,  #  Pass order status to template
    }

    return render(request, 'Ecommerce/product_view.html', {**context, 'variant_prices': json.dumps(variant_prices)})



# View Cart

@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(
        user=request.user)  # Get the user's cart
    cart_items = CartItem.objects.filter(cart=cart).select_related(  #  Filter by user's cart
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
    cart_count = cart_items.values(
        "product_variant__product").distinct().count()

    for item in cart_items:
        inventory = Inventory.objects.filter(batch=item.product_batch).first()
        item.product_variants = ProductVariant.objects.filter(
            product=item.product_variant.product)
        # Convert Decimal to float
        item.sales_price = float(inventory.sales_price) if inventory else 0
        # Handle missing inventory
        item.variant_price = inventory.sales_price if inventory else 0

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
        "cart_items": cart_items,
        "cart_product_ids": cart_product_ids,
        "variant_prices": variant_prices,
        "grand_total": grand_total,
        "cart_count": cart_count,
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
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)

    # Get first available variant and batch
    variant = ProductVariant.objects.filter(product=product).first()
    batch = ProductBatch.objects.filter(
        product=product, variant=variant).first()

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



@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = cart.cartitem_set.all()

    # Fetch cities
    cities = City.objects.all()

    # Get selected city and pincode from GET request
    selected_city_id = request.GET.get("city")
    selected_pincode_id = request.GET.get("pincode")

    # Filter pincodes based on selected city
    pincodes = Pincode.objects.filter(city_id=selected_city_id) if selected_city_id else []

    # Check for active membership
    user_membership = User_membership.objects.filter(
        user=request.user,
        status=True,
        membership_end_date__gte=date.today()
    ).select_related('plan').first()

    is_member = bool(user_membership)
    membership_discount = Decimal(user_membership.plan.discount_rate) if is_member else Decimal(0)

    # Calculate grand total
    grand_total = sum(Decimal(item.total_price) for item in cart_items)
    discount_amount = (grand_total * membership_discount / Decimal(100)) if is_member else Decimal(0)
    total_after_discount = grand_total - discount_amount

    # Fetch delivery charge (default to 0)
    delivery_charge = Decimal(0)

    if is_member:
        delivery_charge = Decimal(0)
    elif selected_pincode_id:
        try:
                pincode_instance = Pincode.objects.get(area_pincode=selected_pincode_id)
                delivery_charge = Decimal(pincode_instance.delivery_charges)
        except Pincode.DoesNotExist:
                delivery_charge = Decimal(0)  # Default to free shipping if not found


    # Final total calculation
    final_total = total_after_discount + delivery_charge
   
    context = {
    "cart_items": cart_items,
    "grand_total": float(grand_total),  # Convert Decimal to float
    "discount_amount": float(discount_amount),
    "total_after_discount": float(total_after_discount),
    "final_total": float(final_total),
    "is_member": is_member,
    "cities": cities,
    "pincodes": pincodes,
    "selected_city_id": selected_city_id,
    "selected_pincode_id": selected_pincode_id,
    "delivery_charge": float(delivery_charge),  # Convert Decimal to float
    # "razorpay_key": settings.RAZORPAY_KEY_ID,
}

    

    return render(request, "Ecommerce/checkout_page.html", context)





@login_required
def get_delivery_charge_ajax(request, pincode_id):
    """AJAX view to fetch delivery charge based on pincode selection."""
    
    # Check if user is a member
    is_member = User_membership.objects.filter(
        user=request.user,
        status=True,
        membership_end_date__gte=date.today()
    ).exists()

    # If user is a member, delivery is free
    if is_member:
        print(f"User {request.user} is a member. Delivery charge set to 0.")
        return JsonResponse({"delivery_charge": 0.0})  # Convert Decimal to float

    try:
        pincode_instance = Pincode.objects.get(area_pincode=str(pincode_id))
        delivery_charge = float(pincode_instance.delivery_charges)  # Convert Decimal to float
        print(f"Pincode: {pincode_id}, Delivery Charge: {delivery_charge}")
    except Pincode.DoesNotExist:
        delivery_charge = 0.0  # Default to 0 if pincode not found
        print(f"Pincode: {pincode_id} not found!")  # Debugging

    return JsonResponse({"delivery_charge": delivery_charge})







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
    pincodes = city.pincode_set.values("pincode_id", "area_pincode")

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
    wishlist_items = WishlistItem.objects.filter(wishlist=wishlist).select_related(  #  Filter by user's cart
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
        WishlistItem, wishlist__user=request.user, id=item_id)  #  Use wishlist__user instead of cart__user

    wishlist_item.delete()
    print(f"Removed wishlist item: {item_id}")  # Debugging line

    return redirect('Ecommerce:wishlist')



# class ProductSearchView(ListView):
#     model = Product
#     template_name = "Ecommerce/search.html"
#     context_object_name = "products"
    
#     home = "Ecommerce:homepage"

    
#     def get_queryset(self):
#         query = self.request.GET.get("product_name", "")
#         if query:
#             products = Product.objects.filter(product_name__icontains=query)
#             if not products.exists():  # Redirect if no products found
#                 return redirect("Ecommerce:homepage")
#             return products
#         return Product.objects.none()
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["search_query"] = self.request.GET.get("product_name", "")
#         return context


class ProductSearchView(ListView):
    model = Product
    template_name = "Ecommerce/search.html"
    context_object_name = "products"

    def get_queryset(self):
        query = self.request.GET.get("product_name", "").strip()
        if query:
            products = Product.objects.filter(product_name__icontains=query).annotate(
                sales_price=F("productbatch__inventory__sales_price")
            )
            return products
        return Product.objects.none()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return redirect(reverse("Ecommerce:homepage"))  #  Redirects if no products found
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get("product_name", "")
        context["search_query"] = search_query

        if self.request.user.is_authenticated:
            cart_items = CartItem.objects.filter(cart__user=self.request.user).values_list("product_batch__product_id", flat=True)
            wishlist_items = WishlistItem.objects.filter(wishlist__user=self.request.user).values_list("product_batch__product_id", flat=True)
        else:
            cart_items = []
            wishlist_items = []

        context["cart_product_ids"] = list(cart_items)
        context["wishlist_product_ids"] = list(wishlist_items)

        return context

def aboutus(request):
    return render(request, 'Ecommerce/aboutus.html') 

def enquiry(request):
    return render(request, 'Ecommerce/enquiry.html')   

def crop_info(request):
    return render(request, 'Ecommerce/crop_info.html')   

def okra(request):
    return render(request, 'Ecommerce/crop_detail/okra.html')


def kishan_charcha(request):
    
    posts = Post.objects.all().order_by('-created_at')
    comment_form = PostCommentForm()
    show_comments = request.GET.get("show_comments", None)
    return render(request, "Ecommerce/kishan_charcha.html", {"posts": posts,"comment_form": comment_form, "show_comments": show_comments})

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, post_id=post_id)
    if request.method == "POST":
        comment_text = request.POST.get("comment_text")
        parent_comment_id = request.POST.get("parent_comment_id")  # Get parent comment ID (if replying)

        if comment_text:
            parent_comment = None
            if parent_comment_id:
                parent_comment = get_object_or_404(PostComment, comment_id=parent_comment_id)

            PostComment.objects.create(
                user=request.user,
                post=post,
                comment_text=comment_text,
                parent_comment=parent_comment
            )

        return redirect("Ecommerce:kishan_charcha")  # Redirect back to post page

    return redirect("Ecommerce:homepage")

@login_required
def order_history(request):
    orders=Order.objects.filter(user=request.user).order_by('-create_at')
    return render(request,'Ecommerce/order_history.html',{'orders':orders})


@login_required
def order_details(request, order_id):
    order = Order.objects.filter(order_id=order_id).first()

    if not order:
        return HttpResponse("Order not found in the database", status=404)

    if order.user != request.user:
        return HttpResponse("You do not have permission to view this order", status=403)

    order_items = order.order_item_set.all()
    total_products = sum(item.quantity for item in order_items)

    return render(request, "Ecommerce/order_detail.html", {
        "order": order,
        "order_items": order_items,
        "total_products": total_products,
    })
    
    
@login_required
def download_invoice_pdf(request, order_id):
    # Fetch the order details
    order = get_object_or_404(Order, pk=order_id)
    order_items = Order_Item.objects.filter(order=order)
    payment = Payment.objects.filter(order=order).first()

    # Ensure we handle cases where payment may not exist
    payment_total = payment.total_price if payment else 0.00
    payment_status = payment.payment_status if payment else "Pending"

    # Prepare the template context
    context = {
        "order": order,
        "order_items": order_items,
        "payment_total": payment_total,
        "payment_status": payment_status,
    }

    # Load template and render to HTML
    template_path = "Ecommerce/download_invoice.html"
    template = get_template(template_path)
    html = template.render(context)

    # Create a PDF response
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f"attachment; filename=invoice_{order_id}.pdf"


@login_required
def generate_invoice(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    order_items = Order_Item.objects.filter(order=order)
    payment = Payment.objects.filter(order=order).first()

    template_path = "Ecommerce/invoice_template.html"
    context = {
        "order": order,
        "order_items": order_items,
        "payment": payment
    }

    template = get_template(template_path)
    html = template.render(context)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="invoice_{order_id}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("Error generating PDF", content_type="text/plain")

    return response



