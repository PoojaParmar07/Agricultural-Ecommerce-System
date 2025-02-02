from django.shortcuts import render,redirect,get_object_or_404
from django.http import Http404
from django.contrib import messages
from .models import *
from .forms import *

def is_admin_user(user):
    return user.is_staff  # or use is_superuser if you're referring to admin access


# Home

def home(request):
    return render(request,'Ecommerce/base.html')

# Category View

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'admin_dashboard/category_list.html', {'categories': categories})


def category_add(request):
    context = {
        'model_name': 'Add Category',
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
        'model_name': 'Update Category',
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





# Brand View

def list_brand(request):
    brand=Brand.objects.all()
    return render(request, 'admin_dashboard/brand_list.html', {'brand':brand})


def add_brand(request):
    context={
        'model_name':'Add Brand',
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
        'model_name':'Update Brand',
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


# Product View

def product_list(request):
    products = Product.objects.all()
    return render(request,'admin_dashboard/product_list.html', {'products':products})



def add_product(request):
    context = {
        'model_name': 'Add Product',
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
        'model_name': 'Update Product',
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

# Product Variant View

def product_variant_list(request):
    product_variant=ProductVariant.objects.all()
    return render(request,'admin_dashboard/product_variant_list.html',{'product_variant':product_variant})



def product_variant_add(request):
    context={
        'model_name':'Add Product Variant',
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
        'model_name': 'Update Product Variant',
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
                messages.error(request,"Product variant update failed. Please correct the errors.")
        elif 'delete' in request.POST:
            product_variant.delete()
            messages.success(request,"Product variant deleted successfully")
            return redirect('Ecommerce:product_variant_list')
        elif 'cancel' in request.POST:
            return redirect('Ecommerce:product_variant_list')
    context['form']=form
    context['product_variant']=product_variant
    return render(request, 'admin_dashboard/view_details.html', context)

# Product Batch View

def productbatch_list(request):
    productbatchies = ProductBatch.objects.all()
    return render(request, 'admin_dashboard/productbatch_list.html',{'productbatchies':productbatchies})


def productbatch_add(request):
    context = {
        'model_name' : 'Add Product Batch',
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
        'model_name':'Update Product Batch'
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

   
# Inventory View
 
def inventory_list(request):
    inventory=Inventory.objects.all()
    return render(request,'admin_dashboard/inventory_list.html',{'inventory':inventory})

def inventory_add(request):
   context = {
        'model_name' : 'Add Inventory',
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
        'modeal_name':"Update Inventory",
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

        


# Delivery View

def deliveryzone_list(request):
    delivery_zone=DeliveryZone.objects.all()
    return render(request,'admin_dashboard/delivery_list.html',{'delivery_zone':delivery_zone})

def deliveryzone_add(request):
     
    context = {
        'model_name': 'Add Delivery Zone',
        'list': 'Ecommerce:deliveryzone_list'
    }

    if request.method == 'POST' and 'zone_name' in request.POST:
        form = DeliveryZoneForm(request.POST)

        if form.is_valid():
            zone_name = form.cleaned_data['zone_name']
            
            # Check if the delivery zone already exists
            if DeliveryZone.objects.filter(zone_name=zone_name).exists():
                messages.error(request, "Delivery Zone already exists")
            else:
                form.save()
                messages.success(request, "Delivery Zone added successfully")
                return redirect('Ecommerce:deliveryzone_list')  # Redirect to correct list

        else:
            messages.error(request, "Not valid")
            print(form.errors)  # Debugging purpose
    
    else:
        form = DeliveryZoneForm()

    context['form'] = form
    return render(request, 'admin_dashboard/add_form.html', context)


def deliveryzone_view_details(request,pk):
    context = {
        'model_name':'Update Delivery Zone'
    }
    
    try:
        delivery_zone = get_object_or_404(DeliveryZone, pk=pk)
    except Http404:
         return render(request, '404.html', status=404)
     
    form = DeliveryZoneForm(instance=delivery_zone)
    
    if request.method == "POST":
        
        if 'update' in request.POST:
            
            form=DeliveryZoneForm(request.POST,instance=delivery_zone)
            if form.is_valid():
                form.save()
                messages.success(request,"Delivery Zone updated successfully")
                return redirect('Ecommerce:deliveryzone_list')
            else:
                messages.error(request,"Delivery Zone update failed. Please correct the errors.")
                
        elif 'delete' in request.POST:
            delivery_zone.delete()
            messages.success(request,"Product Batch deleted successfully")
            return redirect('Ecommerce:deliveryzone_list')
        
        elif 'cancel' in request.POST:
            return redirect('Ecommerce:deliveryzone_list')
        
    context['form']=form
    context['delivery_zone']=delivery_zone
    return render(request, 'admin_dashboard/view_details.html', context)

# Order View

def order_list(request):
    orders=Order.objects.all()
    return render(request,'admin_dashboard/order_list.html',{'orders':orders})


def order_add(request):
    context = {
        'model_name':"Add Order",
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
        
def order_view_details(request, pk):
    context = {
        'model_name':"Update Order",
        'list':'Ecommerce:order_list',
    }
    
    try:
        order = get_object_or_404(Order, pk = pk)
    except Http404:
        return render(request, '404.html', status=404)
    
    form = OrderForm(instance = order)
    
    if request.method == "POST":
        if 'update' in request.POST:
            form=ProductVariantForm(request.POST,instance=order)
            if form.is_valid():
                form.save()
                messages.success(request,"Order updated successfully")
                return redirect('Ecommerce:order_list')
            else:
                messages.error(request,"Order update failed. Please correct the errors.")
        elif 'delete' in request.POST:
            order.delete()
            messages.success(request,"Order deleted successfully")
            return redirect('Ecommerce:order_list')
        elif 'cancel' in request.POST:
            return redirect('Ecommerce:order_list')
    context['form']=form
    context['order']=order
    return render(request, 'admin_dashboard/view_details.html', context)
  
    
    
# Order Item View

def orderitem_list(request):
    orderitems = Order_Item.objects.all()
    return render(request,'admin_dashboard/orderitem_list.html',{'orderitems':orderitems})

def orderitem_add(request):
    context ={
        'model_name':"Order Item",
        'list':'Ecommerce:orderitem_list',
    }
    
    if request.method == 'POST':
        form = OrderItemForm(request.POST)
        if form.is_valid():
                form.save()
                messages.success(request, "Order Item added successfully.")
                return redirect('Ecommerce:orderitem_list')
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
                return redirect('Ecommerce:orderitem_list')
            else:
                messages.error(request,"Order Item update failed. Please correct the errors.")
        elif 'delete' in request.POST:
            orderitem.delete()
            messages.success(request,"Order Item deleted successfully")
            return redirect('Ecommerce:orderitem_list')
        elif 'cancel' in request.POST:
            return redirect('Ecommerce:orderitem_list')
    context['form']=form
    context['orderitem']=orderitem
    return render(request, 'admin_dashboard/view_details.html', context)


# Payment View

def payment_list(request):
    payments=Payment.objects.all()
    return render(request,'admin_dashboard/payment_list.html',{'payments':payments})
   

def payment_add(request):
    context ={
        'model_name':"Payment",
        'list':'Ecommerce:payment_list',
    }
    
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
                form.save()
                messages.success(request, "Payment added successfully.")
                return redirect('Ecommerce:payment_list')
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
            form=OrderItemForm(request.POST,instance=payment)
            if form.is_valid():
                form.save()
                messages.success(request,"Payment updated successfully")
                return redirect('Ecommerce:payment_list')
            else:
                messages.error(request,"Payment update failed. Please correct the errors.")
        elif 'delete' in request.POST:
            payment.delete()
            messages.success(request,"Payment deleted successfully")
            return redirect('Ecommerce:payment_list')
        elif 'cancel' in request.POST:
            return redirect('Ecommerce:payment_list')
    context['form']=form
    context['payment']=payment
    return render(request, 'admin_dashboard/view_details.html', context)







# feedback view

def feedback_list(request):
    feedbacks = Feedback.objects.all()
    return render(request,'admin_dashboard/feedback_list.html',{'feedbacks':feedbacks})

def feedback_add(request):
    context={
        'model_name':'Add Feedback',
        'list':'Ecommerce:feedback_list',
    }
     
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
                form.save()
                messages.success(request, "Feedback added successfully.")
                return redirect('Ecommerce:feedback_list')
    else:
        form = FeedbackForm()
        
    context['form']=form
    return render(request,'admin_dashboard/add_form.html',context)


def feedback_view_details(request, pk):
    context = {
        'model_name': 'Update Feedback',
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
                return redirect('Ecommerce:feedback_list')
            else:
                messages.error(request,"feedback update failed. Please correct the errors.")
        elif 'delete' in request.POST:
            feedback.delete()
            messages.success(request,"Feedback deleted successfully")
            return redirect('Ecommerce:feedback_list')
        elif 'cancel' in request.POST:
            return redirect('Ecommerce:feedback_list')
    context['form']=form
    context['feedback']=feedback
    return render(request, 'admin_dashboard/view_details.html', context)


# Review View

def review_list(request):
    reviews = Review.objects.all()
    return render(request,'admin_dashboard/review_list.html',{'reviews':reviews})

def review_add(request):
    
    context = {
        'model_name':'Add Review',
        'list':'Ecommerce:review_list',
    }
    
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Review added successfully")
            return redirect('Ecommerce:review_list')

    else:
        form = ReviewForm()
    
    context['form'] = form
    return render(request,'admin_dashboard/add_form.html',context)


            
def review_view_details(request, pk):
    context = {
        'model_name':'Update Review',
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
                return redirect('Ecommerce:review_list')
            else:
                messages.error(request,"Review update failed. Please correct the errors.")
        elif 'delete' in request.POST:
            review.delete()
            messages.success(request,"Review deleted successfully")
            return redirect('Ecommerce:review_list')
        elif 'cancel' in request.POST:
            return redirect('Ecommerce:review_list')
    context['form']=form
    context['review']=review
    return render(request, 'admin_dashboard/view_details.html', context)