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
    return render(request,'Ecommerce/homebody.html')





