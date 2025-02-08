from django.shortcuts import render,redirect,get_object_or_404
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from Ecommerce.models import *
from .forms import *
from django.db.models import Avg



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
def product_list(request,category_id):
    category = get_object_or_404(Category, category_id=category_id)
    # products = Product.objects.all()
    products = Product.objects.filter(category = category)
    
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
            'product_image': product.product_image.url if product.product_image else None,  # Optional image check
            'sales_price': sales_price,
            'rating': rating
        })
    context = {
        'products': product_data,
    }
    return render(request, 'Ecommerce/product_list_page.html', context)





    