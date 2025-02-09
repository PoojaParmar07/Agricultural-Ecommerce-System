from django.shortcuts import render,redirect,get_object_or_404
from django.http import Http404, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from Ecommerce.models import *
from .forms import *
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Avg
import json



def is_admin_user(user):
    return user.is_staff  # or use is_superuser if you're referring to admin access


# Home

def home(request):
    return render(request,'Ecommerce/base.html')

def homebody(request):
    categories = Category.objects.all()  # Get all categories from DB
    print(categories)
    category_data = []

    for category in categories:
        print(category.category_image)
        
        category_data.append({
            'category_id': category.category_id,
            'category_name': category.category_name.capitalize(),  # capitalize()
            'category_image': category.category_image.url if category.category_image else None,  # Handle missing images
        })
        
    products = Product.objects.all()
    
    product_data = []
    
    for product in products:
        variant = ProductVariant.objects.filter(product=product).first()  # Get first variant
        if variant:
            inventory = Inventory.objects.filter(batch__variant=variant).first()  # Get price from inventory
            sales_price = inventory.sales_price if inventory else None
        else:
            sales_price = None
        rating=Review.objects.filter(product=product).aggregate(avg_rating=Avg('rating'))['avg_rating']

        product_data.append({
            'product_name': product.product_name,
            'product_image': product.product_image.url if product.product_image else '/static/images/default-product.jpg',
            'sales_price': sales_price if sales_price is not None else "N/A",
            'rating': rating if rating is not None else 0
        })

    return render(request, "Ecommerce/homebody.html", {'categories': category_data,'product_data':product_data})  

    # return render(request,'Ecommerce/homebody.html')

@login_required

def product_list(request, category_id):
    category = get_object_or_404(Category, category_id=category_id)  # Fetch category
    products = Product.objects.filter(category=category)    
    product_data = []
    
    for product in products:
        variant = ProductVariant.objects.filter(product=product).first()  # Get first variant
        if variant:
            inventory = Inventory.objects.filter(batch__variant=variant).first()  # Get price from inventory
            sales_price = inventory.sales_price if inventory else None
        else:
            sales_price = None

        rating = Review.objects.filter(product=product).aggregate(avg_rating=Avg('rating'))['avg_rating']

        product_data.append({
            'product_name': product.product_name,
            'product_image': product.product_image.url if product.product_image else None,  # Check if image exists
            'sales_price': sales_price,
            'rating': rating if rating else 0,  # Default to 0 if no rating
        })

    context = {
        'category_name': category.category_name,  # Pass category name
        'products': product_data,  # Pass product data
    }
    return render(request, 'Ecommerce/product_list_page.html', context)


# View Cart
@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    return render(request, 'Ecommerce/cart.html', {'cart_items': cart_items})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)

    # Get first available variant and batch
    variant = ProductVariant.objects.filter(product=product).first()
    batch = ProductBatch.objects.filter(product=product, variant=variant).first()

    if not variant or not batch:
        return JsonResponse({"success": False, "message": "Product variant or batch not found"})

    # Get or create the user's cart
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Check if the item already exists in the cart
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product_batch=batch,
        product_variant=variant,
        defaults={'quantity': 1}  # Default quantity when adding for the first time
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("Ecommerce:cart_view")
    # return JsonResponse({"success": True, "message": "Product added to cart successfully!"})




# Remove from Cart
@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, cart__user=request.user, cart_item_id=cart_item_id)
    cart_item.delete()

    return redirect('Ecommerce:cart_view')
