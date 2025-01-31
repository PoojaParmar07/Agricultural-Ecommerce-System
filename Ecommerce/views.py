from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from .models import Category
from .forms import CategoryForm
from django.contrib import messages

# Create your views here.
def is_admin_user(user):
    return user.is_staff  # or use is_superuser if you're referring to admin access




def home(request):
    return render(request,'Ecommerce/base.html')


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'admin_dashboard/category_list.html',{'categories':categories})

def category_add(request):
    context = {
        'method-name':'Category',
        'list':'Ecommerce:category_list',
    }
    
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            if Category.objects.all().filter(category_name=category_name).exists():
                messages.error(request, "Category is already exist")
            else:
                form.save()
                messages.error(request,"Category Added successfully")
                return redirect('Ecommerce:category_list')
                
    else:
        form = CategoryForm()
    context['form']=form   
    return render(request,'admin_dashboard/add_form.html',context)
    
def category_view_detail(request,pk):
    
    context = {
        'method-name':'Update Category',
        
    }
    
    try:
        category = get_object_or_404(Category, pk = pk)
    except Http404:
        return render(request, '404.html', status=404)
    
    form = CategoryForm(instance=category)
    
    if request.method == 'POST':
        if 'update' in request.POST:
            form = CategoryForm(request.POST,instance=category)
            
            
            if form.is_valid():
                form.save()
                messages.success(request,"Category updeated successfully")
            else:
                messages.error(request,'Category update failed. Please correct the errors.')
        elif 'delete' in request.POST:
            category.delete()
            messages.success(request,"Category Deleted successfully")
            return redirect('Ecommerce:category_list')
        
            
        elif 'cancel' in request.POST:
            return redirect('Ecommerce:category_list')
        
    context['form'] = form
    context['category']=category
    
    return render(request,'admin_dashboard/view_details.html',context)