# custom_admin/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.http import Http404
from django.template.loader import get_template
from datetime import datetime
from xhtml2pdf import pisa
from django.contrib import messages
from admin_dashboard.models import *
from .forms import *
from django.core.paginator import Paginator
from membership .models import *
from account.models import *
from Ecommerce.models import *
from Ecommerce.forms import *
# Check if the user is staff
def is_admin_user(user):
    return user.is_staff

@login_required
@user_passes_test(is_admin_user)  # Ensure only admin users can access
def admin_dashboard(request):
    return render(request, 'admin_dashboard/main.html')  # Your custom template


def demo(request):
    return render(request,'admin_dashboard/main.html')






""" Admin Side CRUD Operation"""
# Category View

def category_list(request):
    categories = Category.objects.all()
    paginator = Paginator(categories, 5)  # Show 10 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin_dashboard/category_list.html', {'page_obj': page_obj})



def category_add(request):
    context = {
        'model_name': 'Category',
        'list':'admin_dashboard:category_list'
    }
    
    if request.method == 'POST':
        form = CategoryForm(request.POST,request.FILES)  
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            if Category.objects.filter(category_name=category_name).exists():
                messages.error(request, "Category already exists.")
            else:
                form.save()
                messages.success(request, "Category added successfully!")
                return redirect('admin_dashboard:category_list')
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
            form = CategoryForm(request.POST,request.FILES,instance=category)
            if form.is_valid():
                form.save()
                messages.success(request, "Category updated successfully!")
                return redirect('admin_dashboard:category_list')
            else:
                messages.error(request, "Category update failed. Please correct the errors.")

        elif 'delete' in request.POST:  # Delete action
            category.delete()
            messages.success(request, "Category deleted successfully!")
            return redirect('admin_dashboard:category_list')

        elif 'cancel' in request.POST:  # Cancel action
            return redirect('admin_dashboard:category_list')
    context['form'] = form
    context['category']=category
    return render(request, 'admin_dashboard/view_details.html', context)



# Brand View

def list_brand(request):
    brand=Brand.objects.all()
     # Pagination
    paginator = Paginator(brand, 5)  # Show 10 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin_dashboard/brand_list.html', {'page_obj': page_obj})

def add_brand(request):
    context={
        'model_name':'Brand',
        'list':'admin_dashboard:list_brand',
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
                return redirect('admin_dashboard:list_brand')
    else:
        form = BrandForm()
        
    context['form']=form
    return render(request,'admin_dashboard/add_form.html',context)


def brand_view_details(request,pk):
    context={
        'model_name':' Brand',
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
                return redirect('admin_dashboard:list_brand')
            else:
                messages.error(request, "Brand update failed. Please correct the errors.")

        elif 'delete' in request.POST:  # Delete action
            brand.delete()
            messages.success(request, "Brand deleted successfully!")
            return redirect('admin_dashboard:list_brand')
        
        elif 'cancel' in request.POST:
            return redirect('admin_dashboard:list_brand')
    context['form']=form
    context['brand']=brand
    return render(request, 'admin_dashboard/view_details.html',context)


# Product View

def product_list(request):
    products = Product.objects.all()
     # Pagination
    paginator = Paginator(products, 5)  # Show 10 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin_dashboard/product_list.html', {'page_obj': page_obj})


def add_product(request):
    context = {
        'model_name': 'Product',
        'list':'admin_dashboard:product_list'
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
                return redirect('admin_dashboard:product_list')
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
            form=ProductForm(request.POST,request.FILES,instance=product)
            if form.is_valid():
                form.save()
                messages.success(request,"Product updated successfully")
                return redirect('admin_dashboard:product_list')
            else:
                messages.error(request,"Product update failed. Please correct the errors.")
        elif 'delete' in request.POST:
            product.delete()
            messages.success(request,"Product deleted successfully")
            return redirect('admin_dashboard:product_list')
        elif 'cancel' in request.POST:
            return redirect('admin_dashboard:product_list')
    context['form']=form
    context['product']=product
    return render(request, 'admin_dashboard/view_details.html', context)

# Product Variant View

def product_variant_list(request):
    product_variant=ProductVariant.objects.all()
    paginator = Paginator(product_variant, 5)  # Show 10 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin_dashboard/product_variant_list.html', {'page_obj': page_obj})




def product_variant_add(request):
    context={
        'model_name':'Product Variant',
        'list':'admin_dashboard:product_variant_list',
    }
    if request.method == 'POST':
        form = ProductVariantForm(request.POST)
        if form.is_valid():
                form.save()
                messages.success(request, "Variant added successfully.")
                return redirect('admin_dashboard:product_variant_list')
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
                return redirect('admin_dashboard:product_variant_list')
            else:
                messages.error(request,"Product variant update failed. Please correct the errors.")
        elif 'delete' in request.POST:
            product_variant.delete()
            messages.success(request,"Product variant deleted successfully")
            return redirect('admin_dashboard:product_variant_list')
        elif 'cancel' in request.POST:
            return redirect('admin_dashboard:product_variant_list')
    context['form']=form
    context['product_variant']=product_variant
    return render(request, 'admin_dashboard/view_details.html', context)

# Product Batch View

def productbatch_list(request):
    productbatchies = ProductBatch.objects.all()
    paginator = Paginator(productbatchies, 10)  # Show 10 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin_dashboard/productbatch_list.html', {'page_obj': page_obj})



def productbatch_add(request):
    context = {
        'model_name' : 'Product Batch',
        'list' : 'admin_dashboard:productbatch_list',
    }
    
    if request.method == "POST" and 'batch_code' in request.POST:
        form = ProductBatchForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"Product batch added successfully")
            return redirect('admin_dashboard:productbatch_list')
        else:
            messages.error(request,"Product batch add failed. Please correct the errors.")
    
    else:
        form = ProductBatchForm()
        
    context['form'] = form
    
    return render(request,'admin_dashboard/add_form.html',context)


def productbatch_view_details(request, pk):
    context = {
        'model_name':'Product Batch'
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
                return redirect('admin_dashboard:productbatch_list')
            else:
                messages.error(request,"Product Batch update failed. Please correct the errors.")
                
        elif 'delete' in request.POST:
            productbatch.delete()
            messages.success(request,"Product Batch deleted successfully")
            return redirect('admin_dashboard:productbatch_list')
        
        elif 'cancel' in request.POST:
            return redirect('admin_dashboard:productbatch_list')
        
    context['form']=form
    context['productbatch']=productbatch
    return render(request, 'admin_dashboard/view_details.html', context)

   
# Inventory View
 
def inventory_list(request):
    inventory=Inventory.objects.all()
    paginator = Paginator(inventory, 10)  # Show 10 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin_dashboard/inventory_list.html', {'page_obj': page_obj})


def inventory_add(request):
   context = {
        'model_name' : 'Inventory',
        'list' : 'admin_dashboard:inventory_list',
    }
    
   if request.method == "POST" and 'batch' in request.POST:
        form = InventoryForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request,"Inventory added successfully")
            return redirect('admin_dashboard:inventory_list')
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
                return redirect('admin_dashboard:inventory_list')
            else:
                messages.error(request,"Inventory update failed. Please correct the errors.")
        elif 'delete' in request.POST:
            inventory.delete()
            messages.success(request,"Inventory deleted successfully")
            return redirect('admin_dashboard:inventory_list')
        elif 'cancel' in request.POST:
            return redirect('admin_dashboard:inventory_list')
    context['form']=form
    context['inventory']=inventory
    return render(request, 'admin_dashboard/view_details.html', context)

        
# Order View

def order_list(request):
    orders = Order.objects.all()  # Fetch orders and sort by latest ID

    # Pagination (10 orders per page)
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin_dashboard/order_list.html', {'page_obj': page_obj})

def order_add(request):
    context = {
        'model_name':"Order",
        'list':'admin_dashboard:order_list'
    }
    
    if request.method == "POST" and 'state' in request.POST:
        form = OrderForm(request.POST)
        
        if form.is_valid():
            
            form.save()
            messages.success(request,"Order added successfully")
            return redirect('admin_dashboard:order_list')
        else:
            messages.error(request,"Order add failed. Please correct the errors.")
    
    else:
        form = OrderForm()
        
    context['form'] = form
    return render(request,'admin_dashboard/add_form.html',context)
        
def order_view_details(request, pk):
    context = {
        'model_name':"Order",
        'list':'admin_dashboard:order_list',
    }
    
    try:
        order = get_object_or_404(Order, pk = pk)
    except Http404:
        return render(request, '404.html', status=404)
    
    form = OrderForm(instance = order)
    
    if request.method == "POST":
        if 'update' in request.POST:
            form=OrderForm(request.POST,instance=order)
            if form.is_valid():
                form.save()
                messages.success(request,"Order updated successfully")
                return redirect('admin_dashboard:order_list')
            else:
                messages.error(request,"Order update failed. Please correct the errors.")
                return redirect('admin_dashboard:order_list')
        elif 'delete' in request.POST:
            order.delete()
            messages.success(request,"Order deleted successfully")
            return redirect('admin_dashboard:order_list')
        elif 'cancel' in request.POST:
            return redirect('admin_dashboard:order_list')
    context['form']=form
    context['order']=order
    return render(request, 'admin_dashboard/view_details.html', context)
  
    
    
# Order Item View

def orderitem_list(request):
    orderitems = Order_Item.objects.all()
    paginator = Paginator(orderitems, 10)  # Show 10 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin_dashboard/orderitem_list.html', {'page_obj': page_obj})


def orderitem_add(request):
    context ={
        'model_name':"Order Item",
        'list':'admin_dashboard:orderitem_list',
    }
    
    if request.method == 'POST':
        form = OrderItemForm(request.POST)
        if form.is_valid():
                form.save()
                messages.success(request, "Order Item added successfully.")
                return redirect('admin_dashboard:orderitem_list')
    else:
        form = OrderItemForm()
        
    context['form']=form
    return render(request,'admin_dashboard/add_form.html',context)


def orderitem_view_details(request, pk):
    context = {
        'model_name': 'OrderItem',
    }
    try:
        orderitem = get_object_or_404(Order_Item, pk=pk)
    except Http404:
         return render(request, '404.html', status=404)
        
    form = OrderItemForm(instance=orderitem)
    if request.method=='POST':
        if 'update' in request.POST:
            form=OrderItemForm(request.POST,instance=orderitem)
            if form.is_valid():
                form.save()
                messages.success(request,"Ordet Item updated successfully")
                return redirect('admin_dashboard:orderitem_list')
            else:
                messages.error(request,"Order Item update failed. Please correct the errors.")
        elif 'delete' in request.POST:
            orderitem.delete()
            messages.success(request,"Order Item deleted successfully")
            return redirect('admin_dashboard:orderitem_list')
        elif 'cancel' in request.POST:
            return redirect('admin_dashboard:orderitem_list')
    context['form']=form
    context['orderitem']=orderitem
    return render(request, 'admin_dashboard/view_details.html', context)


# Payment View

def payment_list(request):
    payments=Payment.objects.all()
    paginator = Paginator(payments, 10)  # Show 10 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin_dashboard/payment_list.html', {'page_obj': page_obj})

   

def payment_add(request):
    context ={
        'model_name':"Payment",
        'list':'admin_dashboard:payment_list',
    }
    
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
                form.save()
                messages.success(request, "Payment added successfully.")
                return redirect('admin_dashboard:payment_list')
    else:
        form = PaymentForm()
        
    context['form']=form
    return render(request,'admin_dashboard/add_form.html',context)

def payment_view_details(request,pk):
    context = {
        'model_name': 'Payment',
    }
    try:
        payment = get_object_or_404(Payment, pk=pk)
    except Http404:
         return render(request, '404.html', status=404)
        
    form = PaymentForm(instance=payment)
    if request.method=='POST':
        if 'update' in request.POST:
            form=PaymentForm(request.POST,instance=payment)
            if form.is_valid():
                form.save()
                messages.success(request,"Payment updated successfully")
                return redirect('admin_dashboard:payment_list')
            else:
                messages.error(request,"Payment update failed. Please correct the errors.")
        elif 'delete' in request.POST:
            payment.delete()
            messages.success(request,"Payment deleted successfully")
            return redirect('admin_dashboard:payment_list')
        elif 'cancel' in request.POST:
            return redirect('admin_dashboard:payment_list')
    context['form']=form
    context['payment']=payment
    return render(request, 'admin_dashboard/view_details.html', context)







# feedback view

def feedback_list(request):
    feedbacks = Feedback.objects.all()
    paginator = Paginator(feedbacks, 10)  # Show 10 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin_dashboard/feedback_list.html', {'page_obj': page_obj})


def feedback_add(request):
    context={
        'model_name':'Feedback',
        'list':'admin_dashboard:feedback_list',
    }
     
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
                form.save()
                messages.success(request, "Feedback added successfully.")
                return redirect('admin_dashboard:feedback_list')
    else:
        form = FeedbackForm()
        
    context['form']=form
    return render(request,'admin_dashboard/add_form.html',context)


def feedback_view_details(request, pk):
    context = {
        'model_name': 'Feedback',
    }
    try:
        feedback = get_object_or_404(Feedback, pk=pk)
    except Http404:
         return render(request, '404.html', status=404)
        
    form = FeedbackForm(instance=feedback)
    if request.method=='POST':
        if 'update' in request.POST:
            form=FeedbackForm(request.POST,instance=feedback)
            if form.is_valid():
                form.save()
                messages.success(request,"Feedback updated successfully")
                return redirect('admin_dashboard:feedback_list')
            else:
                messages.error(request,"feedback update failed. Please correct the errors.")
        elif 'delete' in request.POST:
            feedback.delete()
            messages.success(request,"Feedback deleted successfully")
            return redirect('admin_dashboard:feedback_list')
        elif 'cancel' in request.POST:
            return redirect('admin_dashboard:feedback_list')
    context['form']=form
    context['feedback']=feedback
    return render(request, 'admin_dashboard/view_details.html', context)


# Review View

def review_list(request):
    reviews = Review.objects.all()
    paginator = Paginator(reviews, 10)  # Show 10 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin_dashboard/review_list.html', {'page_obj': page_obj})


def review_add(request):
    
    context = {
        'model_name':'Review',
        'list':'admin_dashboard:review_list',
    }
    
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Review added successfully")
            return redirect('admin_dashboard:review_list')

    else:
        form = ReviewForm()
    
    context['form'] = form
    return render(request,'admin_dashboard/add_form.html',context)


            
def review_view_details(request, pk):
    context = {
        'model_name':' Review',
    }
    
    try:
        review = get_object_or_404(Review,pk = pk)
    except Http404:
        return render(request,'404.html',status=404)
    
    form = ReviewForm(instance=review)
    
    if request.method == "POST":
        
        if 'update' in request.POST:
            form=ReviewForm(request.POST,instance=review)
            if form.is_valid():
                form.save()
                messages.success(request,"Review updated successfully")
                return redirect('admin_dashboard:review_list')
            else:
                messages.error(request,"Review update failed. Please correct the errors.")
        elif 'delete' in request.POST:
            review.delete()
            messages.success(request,"Review deleted successfully")
            return redirect('admin_dashboard:review_list')
        elif 'cancel' in request.POST:
            return redirect('admin_dashboard:review_list')
    context['form']=form
    context['review']=review
    return render(request, 'admin_dashboard/view_details.html', context)



# Wishlist View

def wishlist_list(request):
    wishlist=Wishlist.objects.all()
    paginator = Paginator(wishlist, 10)  # Show 10 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin_dashboard/wishlist_list.html', {'page_obj': page_obj})


def wishlist_add(request):
    context = {
        'model_name':'Wishlist',
        'list':'admin_dashboard:wishlist_list',
    }
    
    if request.method == "POST":
        form = WishlistForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Wishlist added successfully")
            return redirect('admin_dashboard:wishlist_list')

    else:
        form = WishlistForm()
    
    context['form'] = form
    return render(request,'admin_dashboard/add_form.html',context)

def wishlist_view_details(request,pk):
    context = {
        'model_name':' Wishlist',
    }
    
    try:
        wishlist = get_object_or_404(Wishlist,pk=pk)
    except Http404:
        return render(request,'404.html',status=404)
    
    form = WishlistForm(instance=wishlist)
    
    if request.method == "POST":
        
        if 'update' in request.POST:
            form=WishlistForm(request.POST,instance=wishlist)
            if form.is_valid():
                form.save()
                messages.success(request,"Wishlist updated successfully")
                return redirect('admin_dashboard:wishlist_list')
            else:
                messages.error(request,"Wishlist update failed. Please correct the errors.")
        elif 'delete' in request.POST:
            wishlist.delete()
            messages.success(request,"Wishlist deleted successfully")
            return redirect('admin_dashboard:wishlist_list')
        elif 'cancel' in request.POST:
            return redirect('admin_dashboard:wishlist_list')
    context['form']=form
    context['wishlist']=wishlist
    return render(request, 'admin_dashboard/view_details.html', context)



def wishlist_item_list(request):
    wishlist_item=WishlistItem.objects.all()
    paginator = Paginator(wishlist_item, 10)  # Show 10 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin_dashboard/wishlist_item_list.html', {'page_obj': page_obj})


def wishlist_item_add(request):
    context = {
        'model_name':'Wishlist Item',
        'list':'admin_dashboard:wishlist_item_list',
    }
    
    if request.method == "POST":
        form = WishlistItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Wishlist Item added successfully")
            return redirect('admin_dashboard:wishlist_item_list')

    else:
        form = WishlistItemForm()
    
    context['form'] = form
    return render(request,'admin_dashboard/add_form.html',context)

def wishlist_item_view_details(request,pk):
    context = {
        'model_name':' Wishlist Item',
    }
    
    try:
        wishlist_item = get_object_or_404(WishlistItem,pk=pk)
    except Http404:
        return render(request,'404.html',status=404)
    
    form = WishlistItemForm(instance=wishlist_item)
    
    if request.method == "POST":
        
        if 'update' in request.POST:
            form=WishlistItemForm(request.POST,instance=wishlist_item)
            if form.is_valid():
                form.save()
                messages.success(request,"Wishlist Item updated successfully")
                return redirect('admin_dashboard:wishlist_item_list')
            else:
                messages.error(request,"Wishlist Item update failed. Please correct the errors.")
        elif 'delete' in request.POST:
            wishlist_item.delete()
            messages.success(request,"Wishlist Item deleted successfully")
            return redirect('admin_dashboard:wishlist_item_list')
        elif 'cancel' in request.POST:
            return redirect('admin_dashboard:wishlist_item_list')
    context['form']=form
    context['wishlist_item']=wishlist_item
    return render(request, 'admin_dashboard/view_details.html', context)


# Cart view

def cart_list(request):
    carts = Cart.objects.all()
    paginator = Paginator(carts, 10)  # Show 10 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin_dashboard/cart_list.html', {'page_obj': page_obj})


def add_cart(request):

    context = {
        'model_name':'Cart',
        'list':'admin_dashboard:cart_list',
    }
    
    if request.method == "POST":
        form = CartForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Product added to cart added successfully")
            return redirect('admin_dashboard:cart_list')

    else:
        form = CartForm()
    
    context['form'] = form
    return render(request,'admin_dashboard/add_form.html',context)


def cart_view_details(request, pk):
    context = {
        'model_name':'Cart',
    }
    
    try:
        cart = get_object_or_404(Cart,pk = pk)
    except Http404:
        return render(request,'404.html',status=404)
    
    form = CartForm(instance=cart)
    
    if request.method == "POST":
        
        if 'update' in request.POST:
            form=CartForm(request.POST,instance=cart)
            if form.is_valid():
                form.save()
                messages.success(request,"Cart updated successfully")
                return redirect('admin_dashboard:cart_list')
            else:
                messages.error(request,"cart update failed. Please correct the errors.")
        elif 'delete' in request.POST:
            cart.delete()
            messages.success(request,"cart deleted successfully")
            return redirect('admin_dashboard:cart_list')
        elif 'cancel' in request.POST:
            return redirect('admin_dashboard:cart_list')
    context['form']=form
    context['cart']=cart
    return render(request, 'admin_dashboard/view_details.html', context)


# Cart Item

def cartitem_list(request):
    cartitems = CartItem.objects.all()
    paginator = Paginator(cartitems, 10)  # Show 10 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin_dashboard/cartitem_list.html', {'page_obj': page_obj})


def cartitem_add(request):
    context = {
        'model_name':'Cart Item',
        'list':'admin_dashboard:cartitem_list',
    }
    
    if request.method == "POST":
        form = CartItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Cart Item added successfully")
            return redirect('admin_dashboard:cartitem_list')

    else:
        form = CartForm()
    
    context['form'] = form
    return render(request,'admin_dashboard/add_form.html',context)

def cartitem_view_details(request, pk):
    context = {
        'model_name':'Cart Item',
    }
    
    try:
        cartitem = get_object_or_404(CartItem,pk = pk)
    except Http404:
        return render(request,'404.html',status=404)
    
    form = CartItemForm(instance=cartitem)
    
    if request.method == "POST":
        
        if 'update' in request.POST:
            form=CartItemForm(request.POST,instance=cartitem)
            if form.is_valid():
                form.save()
                messages.success(request,"Cart Item updated successfully")
                return redirect('admin_dashboard:cartitem_list')
            else:
                messages.error(request,"cart Item update failed. Please correct the errors.")
        elif 'delete' in request.POST:
            cartitem.delete()
            messages.success(request,"cart Item deleted successfully")
            return redirect('admin_dashboard:cartitem_list')
        elif 'cancel' in request.POST:
            return redirect('admin_dashboard:cartitem_list')
    context['form']=form
    context['cartitem']=cartitem
    return render(request, 'admin_dashboard/view_details.html', context)


# City

def city_list(request):
    cities = City.objects.all()
    paginator = Paginator(cities, 10)  # Show 10 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin_dashboard/city_list.html', {'page_obj': page_obj})



def add_city(request):
    context = {
        'model_name':'City',
        'list':'admin_dashboard:city_list',
    }
    
    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"City added successfully")
            return redirect('admin_dashboard:city_list')

    else:
        form = CityForm()
    
    context['form'] = form
    return render(request,'admin_dashboard/add_form.html',context)

def city_view_details(request, pk):
    context = {
        'model_name':' City',
    }
    
    try:
        city = get_object_or_404(City,pk = pk)
    except Http404:
        return render(request,'404.html',status=404)
    
    form = CityForm(instance=city)
    
    if request.method == "POST":
        
        if 'update' in request.POST:
            form=CityForm(request.POST,instance=city)
            if form.is_valid():
                form.save()
                messages.success(request,"City updated successfully")
                return redirect('admin_dashboard:city_list')
            else:
                messages.error(request,"City update failed. Please correct the errors.")
        elif 'delete' in request.POST:
            city.delete()
            messages.success(request,"City deleted successfully")
            return redirect('admin_dashboard:city_list')
        elif 'cancel' in request.POST:
            return redirect('admin_dashboard:city_list')
    context['form']=form
    context['city']=city
    return render(request, 'admin_dashboard/view_details.html', context)


def pincode_list(request):
    pincodes = Pincode.objects.all()
    # paginator = Paginator(pincodes,5)  # Show 10 products per page
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)

    # return render(request, 'admin_dashboard/pincode_list.html', {'page_obj': page_obj})
    return render(request, 'admin_dashboard/pincode_list.html', {'pincodes': pincodes})


def pincode_add(request):
    context = {
        'model_name':'Pincode',
        'list':'admin_dashboard:pincode_list',
    }
    
    if request.method == "POST":
        form = PincodeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Pincode added successfully")
            return redirect('admin_dashboard:pincode_list')

    else:
        form = PincodeForm()
    
    context['form'] = form
    return render(request,'admin_dashboard/add_form.html',context)


def pincode_view_details(request, pk):
    context = {
        'model_name':' Pincode',
    }
    
    try:
        pincode = get_object_or_404(Pincode,pk=pk)
    except Http404:
        return render(request,'404.html',status=404)
    
    form = PincodeForm(instance=pincode)
    
    if request.method == "POST":
        
        if 'update' in request.POST:
            form=PincodeForm(request.POST,instance=pincode)
            if form.is_valid():
                form.save()
                messages.success(request,"Pincode updated successfully")
                return redirect('admin_dashboard:pincode_list')
            else:
                messages.error(request,"Pincode update failed. Please correct the errors.")
        elif 'delete' in request.POST:
            pincode.delete()
            messages.success(request,"Pincode deleted successfully")
            return redirect('admin_dashboard:pincode_list')
        elif 'cancel' in request.POST:
            return redirect('admin_dashboard:pincode_list')
    context['form']=form
    context['pincode']=pincode
    return render(request, 'admin_dashboard/view_details.html', context)





# REPORT LAYOUT CODE


def order_report(request):
    products = ProductVariant.objects.all()
    orders = None

    if request.method == "GET":
        product_id = request.GET.get("product")
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")

        if product_id and start_date and end_date:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")

            orders = Order_Item.objects.filter(
                variant_id=product_id, create_at__date__range=[start_date, end_date]
            )

    return render(request, "admin_dashboard/order_report.html", {"products": products, "orders": orders})


def order_report_pdf(request):
    product_id = request.GET.get("product")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    orders = None
    if product_id and start_date and end_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

        orders = Order_Item.objects.filter(
            variant_id=product_id, create_at__date__range=[start_date, end_date]
        )

    template_path = "admin_dashboard/report_pdf.html"
    context = {"orders": orders}
    template = get_template(template_path)
    html = template.render(context)
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "attachment; filename=report.pdf"

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("Error generating PDF", content_type="text/plain")

    return response



def membership_report(request):
    plans = Membership_plan.objects.all()
    selected_plan = request.GET.get('plan')

    members = []  # Initialize as empty list
    if selected_plan:
        members = User_membership.objects.select_related('user', 'plan').filter(plan_id=selected_plan)

    context = {
        'plans': plans,
        'members': members,
        'selected_plan': selected_plan
    }
    return render(request, 'admin_dashboard/membership_report.html', context)



def download_membership_report_pdf(request):
    selected_plan = request.GET.get('plan')

    members = []  # Default empty
    if selected_plan:
        members = User_membership.objects.select_related('user', 'plan').filter(plan_id=selected_plan)

    template_path = "admin_dashboard/membership_report_pdf.html"
    context = {"members": members}

    template = get_template(template_path)
    html = template.render(context)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "attachment; filename=membership_report.pdf"

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("Error generating PDF", content_type="text/plain")

    return response



def enquiry_list(request):
    enquiries = Enquiry.objects.all()
    return render(request,"admin_dashboard/enquiry_list.html",{'enquiries':enquiries})


def enquiry_view_detail(request, enquiry_id):
    context = {
        'model_name': 'Enquiry',
    }
    
    try:
        enquiry = get_object_or_404(Enquiry, enquiry_id = enquiry_id)
    except Http404:
        return HttpResponse(request,"404.html", enquiry_id = enquiry_id)
    
    form = EnquiryForm(instance = enquiry)
    
    if request.method == 'POST':
        if 'update' in request.POST:  # Update action
            form = EnquiryForm(request.POST,request.FILES,instance=enquiry)
            if form.is_valid():
                form.save()
                messages.success(request, "Enquiry updated successfully!")
                return redirect('admin_dashboard:enquiry_list')
            else:
                messages.error(request, "Enquiry update failed. Please correct the errors.")

        elif 'delete' in request.POST:  # Delete action
            enquiry.delete()
            messages.success(request, "Enquiry deleted successfully!")
            return redirect('admin_dashboard:enquiry_list')

        elif 'cancel' in request.POST:  # Cancel action
            return redirect('admin_dashboard:enquiry_list')
    context['form'] = form
    context['enquiry']=enquiry
    return render(request, 'admin_dashboard/view_details.html', context)

