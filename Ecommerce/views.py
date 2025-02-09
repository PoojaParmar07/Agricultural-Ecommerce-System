from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from Ecommerce.models import Category, Product, ProductVariant, Inventory, Review
import json


def is_admin_user(user):
    return user.is_authenticated and user.is_staff  # Example function

def home(request):
    return render(request, 'Ecommerce/base.html')


def homebody(request):
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

    for product in products:
        variant = ProductVariant.objects.filter(product=product).first()
        inventory = Inventory.objects.filter(batch__variant=variant).first() if variant else None
        sales_price = inventory.sales_price if inventory else None
        rating = Review.objects.filter(product=product).aggregate(avg_rating=Avg('rating'))['avg_rating']

        product_data.append({
            'product_id': product.product_id,
            'product_name': product.product_name,
            'product_image': product.product_image.url if product.product_image else '/static/images/default-product.jpg',
            'sales_price': sales_price if sales_price is not None else "N/A",
            'rating': rating if rating is not None else 0
        })

    return render(request, "Ecommerce/homebody.html", {'categories': category_data, 'product_data': product_data})


@login_required
def product_list(request, category_id):
    category = get_object_or_404(Category, category_id=category_id)
    products = Product.objects.filter(category=category)

    product_data = []
    for product in products:
        variant = ProductVariant.objects.filter(product=product).first()
        inventory = Inventory.objects.filter(batch__variant=variant).first() if variant else None
        sales_price = inventory.sales_price if inventory else None
        rating = Review.objects.filter(product=product).aggregate(avg_rating=Avg('rating'))['avg_rating']

        product_data.append({
            'product_id': product.product_id,
            'product_name': product.product_name,
            'product_image': product.product_image.url if product.product_image else None,
            'sales_price': sales_price,
            'rating': rating,
        })

    return render(request, 'Ecommerce/product_list_page.html', {'products': product_data})





def product_view(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    variants = list(ProductVariant.objects.filter(product=product).select_related('brand'))
    inventories = Inventory.objects.filter(batch__variant__in=variants).select_related('batch__variant')

    # Build a dictionary with string keys for correct JSON mapping
    variant_prices = {str(variant.variant_id): None for variant in variants}
    for inventory in inventories:
        variant_prices[str(inventory.batch.variant.variant_id)] = float(inventory.sales_price)

    # Get the first available price
    first_price = next((price for price in variant_prices.values() if price is not None), None)

    # Calculate average rating
    rating_data = Review.objects.filter(product=product).aggregate(avg_rating=Avg('rating'))
    rating = rating_data['avg_rating'] if rating_data['avg_rating'] is not None else 0

    # Fetch reviews in descending order of creation time
    reviews = Review.objects.filter(product=product).order_by('-created_at') 

    # Prepare product data
    product_data = {
        'product_id': product.product_id,
        'product_name': product.product_name,
        'product_image': product.product_image.url if product.product_image else "/static/images/no_image.jpg",
        'description': product.description,
        'rating': round(rating, 1),
        "variant_prices": json.dumps(variant_prices),  # ✅ Ensure valid JSON
        'first_price': first_price if first_price is not None else "N/A",
    }

    return render(request, 'Ecommerce/product_view.html', {
        'product': product_data,
        'reviews': reviews,
        'variants': variants,
    })
