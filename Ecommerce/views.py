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

@login_required


def product_list(request):
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
            'product_image': product.product_image.url,
            'sales_price': sales_price,
            'rating':rating
        })

    return render(request, 'Ecommerce/product_list_page.html', {'products': product_data})






