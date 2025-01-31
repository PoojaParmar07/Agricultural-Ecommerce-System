from django.shortcuts import render,redirect,get_object_or_404
from django.http import Http404
from django.contrib import messages
from .models import Brand
from .forms import BrandForm
# Create your views here.
def is_admin_user(user):
    return user.is_staff  # or use is_superuser if you're referring to admin access




def home(request):
    return render(request,'Ecommerce/base.html')



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