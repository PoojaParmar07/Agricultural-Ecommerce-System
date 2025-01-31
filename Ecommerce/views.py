from django.shortcuts import render
from .models import Brand

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
        'list':'Ecommerce:brand_list',
    }
    return render(request,'admin_dashboard/add_form.html',context)