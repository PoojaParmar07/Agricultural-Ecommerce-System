from django.shortcuts import render,redirect,get_object_or_404
from django.http import Http404
from django.contrib import messages
from .models import *
from .forms import *

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
    return render(request,'admin_dashboard/product_list.html', {'products':products})



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


def product_view_details(request,pk):
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



def product_variant_list(request):
    product_variant=ProductVariant.objects.all()
    return render(request,'admin_dashboard/product_variant_list.html',{'product_variant':product_variant})



def product_variant_add(request):
    context={
        'model_name':'Product Variant',
        'list':'Ecommerce:product_variant_list',
    }
    if request.method == 'POST':
        form = ProductVariantForm(request.POST)
        if form.is_valid():
                form.save()
                messages.success(request, "Variant added successfully.")
                return redirect('Ecommerce:product_variant_list')
    else:
        form = ProductVariantForm()
        
    context['form']=form
    return render(request,'admin_dashboard/add_form.html',context)




def product_variant_view_details(request,pk):
    context = {
        'model_name': 'Product Variant',
    }
    try:
        product_variant = get_object_or_404(ProductVariant, pk=pk)
    except Http404:
         return render(request, '404.html', status=404)
        
    form = ProductVariantForm(instance=product_variant)
    if request.method=='POST':
        if 'update' in request.POST:
            form=ProductVariantForm(request.POST,instance=product_variant)
            if form.is_valid():
                form.save()
                messages.success(request,"Product variant updated successfully")
                return redirect('Ecommerce:product_variant_list')
            else:
                messages.error(request,"Product update failed. Please correct the errors.")
        elif 'delete' in request.POST:
            product_variant.delete()
            messages.success(request,"Product deleted successfully")
            return redirect('Ecommerce:product_variant_list')
        elif 'cancel' in request.POST:
            return redirect('Ecommerce:product_variant_list')
    context['form']=form
    context['product_variant']=product_variant
    return render(request, 'admin_dashboard/view_details.html', context)



def productbatch_list(request):
    productbatchies = ProductBatch.objects.all()
    return render(request, 'admin_dashboard/productbatch_list.html',{'productbatchies':productbatchies})


    
def inventory_list(request):
    inventory=Inventory.objects.all()
    return render(request,'admin_dashboard/inventory_list.html',{'inventory':inventory})

def inventory_add(request):
   context = {
        'model_name' : 'Inventory',
        'list' : 'Ecommerce:inventory_list',
    }
    
   if request.method == "POST" and 'batch' in request.POST:
        form = InventoryForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request,"Inventory added successfully")
            return redirect('Ecommerce:inventory_list')
        else:
            messages.error(request,"Inventory add failed. Please correct the errors.")
    
   else:
        form = InventoryForm()
        
   context['form'] = form
    
   return render(request,'admin_dashboard/add_form.html',context)


def inventory_view_details(request,pk):
    context={
        'modeal_name':"Inventory",
    }
    try:
        inventory=get_object_or_404(Inventory,pk=pk)
    except Http404:
        return render(request,'404.html',status=404)
    
    form=InventoryForm(instance=inventory)
    if request.method=='POST':
        if 'update' in request.POST:
            form=InventoryForm(request.POST,instance=inventory)
            if form.is_valid():
                form.save()
                messages.success(request,"Inventory updated successfully")
                return redirect('Ecommerce:inventory_list')
            else:
                messages.error(request,"Inventory update failed. Please correct the errors.")
        elif 'delete' in request.POST:
            inventory.delete()
            messages.success(request,"Inventory deleted successfully")
            return redirect('Ecommerce:inventory_list')
        elif 'cancel' in request.POST:
            return redirect('Ecommerce:inventory_list')
    context['form']=form
    context['inventory']=inventory
    return render(request, 'admin_dashboard/view_details.html', context)

        


def productbatch_add(request):
    context = {
        'model_name' : 'Product Batch',
        'list' : 'Ecommerce:productbatch_list',
    }
    
    if request.method == "POST" and 'batch_code' in request.POST:
        form = ProductBatchForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Product batch added successfully")
            return redirect('Ecommerce:productbatch_list')
        else:
            messages.error(request,"Product batch add failed. Please correct the errors.")
    
    else:
        form = ProductBatchForm()
        
    context['form'] = form
    
    return render(request,'admin_dashboard/add_form.html',context)


def productbatch_view_details(request, pk):
    context = {
        'model_name':'Product Update'
    }
    
    try:
        productbatch = get_object_or_404(ProductBatch, pk=pk)
    except Http404:
         return render(request, '404.html', status=404)
     
    form = ProductBatchForm(instance=productbatch)
    
    if request.method == "POST":
        
        if 'update' in request.POST:
            
            form=ProductBatchForm(request.POST,instance=productbatch)
            if form.is_valid():
                form.save()
                messages.success(request,"Product Batch updated successfully")
                return redirect('Ecommerce:productbatch_list')
            else:
                messages.error(request,"Product Batch update failed. Please correct the errors.")
                
        elif 'delete' in request.POST:
            productbatch.delete()
            messages.success(request,"Product Batch deleted successfully")
            return redirect('Ecommerce:productbatch_list')
        
        elif 'cancel' in request.POST:
            return redirect('Ecommerce:productbatch_list')
        
    context['form']=form
    context['productbatch']=productbatch
    return render(request, 'admin_dashboard/view_details.html', context)


def deliveryzone_list(request):
    delivery_zone=DeliveryZone.objects.all()
    return render(request,'admin_dashboard/delivery_list.html',{'delivery_zone':delivery_zone})

def deliveryzone_add(request):
    pass

def deliveryzone_view_details(request):
    pass

def order_list(request):
    orders=Order.objects.all()
    return render(request,'admin_dashboard/order_list.html',{'orders':orders})


def order_add(request):
    context = {
        'model_name':"Order",
        'list':'Ecommerce:order_list'
    }
    
    if request.method == "POST" and 'state' in request.POST:
        form = OrderForm(request.POST)
        
        if form.is_valid():
            
            form.save()
            messages.success(request,"Order added successfully")
            return redirect('Ecommerce:order_list')
        else:
            messages.error(request,"Order add failed. Please correct the errors.")
    
    else:
        form = OrderForm()
        
    context['form'] = form
    return render(request,'admin_dashboard/add_form.html',context)
        
        
        