from django.shortcuts import render,redirect,get_object_or_404
from django.http import Http404
from django.contrib import messages
from .models import Category, Brand, Product
from .forms import BrandForm, CategoryForm, ProductForm
# Create your views here.
def is_admin_user(user):
    return user.is_staff  # or use is_superuser if you're referring to admin access




def home(request):
    return render(request,'Ecommerce/base.html')

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'admin_dashboard/category_list.html', {'categories': categories})


def category_add(request):
    context = {
        'model_name': 'Category',
        'list':'Ecommerce:category_list'
    }
    if request.method == 'POST':
        form = CategoryForm(request.POST)  
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            if Category.objects.filter(category_name=category_name).exists():
                messages.error(request, "Category already exists.")
            else:
                form.save()
                messages.success(request, "Category added successfully!")
                return redirect('Ecommerce:category_list')
    else:
        form = CategoryForm()

    # Merge form into the context
    context['form'] = form
    return render(request, 'admin_dashboard/add_form.html', context)


def category_view_details(request, pk):
    context = {
        'model_name': 'Category',
    }
    try:
        category = get_object_or_404(Category, pk=pk)
    except Http404:
        # Render the custom 404 page
        return render(request, '404.html', status=404)

    form = CategoryForm(instance=category)

    if request.method == 'POST':
        if 'update' in request.POST:  # Update action
            form = CategoryForm(request.POST, instance=category)
            if form.is_valid():
                form.save()
                messages.success(request, "Category updated successfully!")
                return redirect('Ecommerce:category_list')
            else:
                messages.error(request, "Category update failed. Please correct the errors.")

        elif 'delete' in request.POST:  # Delete action
            category.delete()
            messages.success(request, "Category deleted successfully!")
            return redirect('Ecommerce:category_list')

        elif 'cancel' in request.POST:  # Cancel action
            return redirect('Ecommerce:category_list')
    context['form'] = form
    context['category']=category
    return render(request, 'admin_dashboard/view_details.html', context)







def list_brand(request):
    brand=Brand.objects.all()
    return render(request, 'admin_dashboard/brand_list.html', {'brand':brand})


def add_brand(request):
    context={
        'model_name':'Brand',
        'list':'Ecommerce:list_brand',
    }
    if request.method == 'POST':
        form = BrandForm(request.POST)
        if form.is_valid():
            brand_name = form.cleaned_data['brand_name']
            if Brand.objects.filter(brand_name = brand_name).exists():
                messages.error(request, "Brand already exists.")
            else:
                form.save()
                messages.success(request, "Brand added successfully.")
                return redirect('membership:list_brand')
    else:
        form = BrandForm()
        
    context['form']=form
    return render(request,'admin_dashboard/add_form.html',context)


def brand_view_details(request,pk):
    context={
        'model_name':'Brand',
    }
    try:
        brand = get_object_or_404(Brand, pk = pk)
    except Http404:
        return render(request, '404.html', status=404)
    
    form = BrandForm(instance=brand)
    
    if request.method == 'POST':
        if 'update' in request.POST:
            form = BrandForm(request.POST, instance=brand)
            
            if form.is_valid():
                form.save()
                messages.success(request, "Brand updated successfully!")
                return redirect('Ecommerce:list_brand')
            else:
                messages.error(request, "Brand update failed. Please correct the errors.")

        elif 'delete' in request.POST:  # Delete action
            brand.delete()
            messages.success(request, "Brand deleted successfully!")
            return redirect('Ecommerce:list_brand')
        
        elif 'cancel' in request.POST:
            return redirect('Ecommerce:list_brand')
    context['form']=form
    context['brand']=brand
    return render(request, 'admin_dashboard/view_details.html',context)


def product_list(request):
    products = Product.objects.all()
    return render(request,'admin_dashboard/product_list.html',{'products':products})



def add_product(request):
    context = {
        'model_name': 'Product',
        'list':'Ecommerce:product_list'
    }
    if request.method == 'POST' and 'product_name' in request.POST:

        form=ProductForm(request.POST,request.FILES)
        if form.is_valid():
            product_name=form.cleaned_data['product_name']
            if Product.objects.filter(product_name=product_name).exists():
                messages.error(request,"Product already exists")
            else:
                form.save()
                messages.success(request,"Product added successfully")
                return redirect('Ecommerce:product_list')
        else:
            messages.error(request,"Not valid")
            print(form.errors) 
    else:
        form=ProductForm()
    
    context['form']=form
    return render(request,'admin_dashboard/add_form.html',context)


def product_view_details(request):
    context = {
        'model_name': 'Product',
    }
    try:
        product = get_object_or_404(Product, pk=pk)
    except Http404:
         return render(request, '404.html', status=404)
        
    form = ProductForm(instance=product)
    if request.method=='POST':
        if 'update' in request.POST:
            form=ProductForm(request.POST,instance=product)
            if form.is_valid():
                form.save()
                messages.success(request,"Product updated successfully")
                return redirect('Ecommerce:product_list')
            else:
                messages.error(request,"Product update failed. Please correct the errors.")
        elif 'delete' in request.POST:
            product.delete()
            messages.success(request,"Product deleted successfully")
            return redirect('Ecommerce:product_list')
        elif 'cancel' in request.POST:
            return redirect('Ecommerce:product_list')
    context['form']=form
    context['product']=product
    return render(request, 'admin_dashboard/view_details.html', context)