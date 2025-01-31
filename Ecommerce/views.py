from django.shortcuts import render

# Create your views here.
def is_admin_user(user):
    return user.is_staff  # or use is_superuser if you're referring to admin access




def home(request):
    return render(request,'Ecommerce/base.html')

def add_brand(request):
    context={
        'model_name':'Brand',
        'list':'Ecommerce:brand_list',
    }
    return render(request,'admin_dashboard/add_form.html',context)