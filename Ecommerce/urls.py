from django.urls import path,include
from .views import home,add_brand,list_brand

app_name = 'Ecommerce'
urlpatterns = [
    path('',home,name='home'),
    
    # Brand list
    path('list_brand/',list_brand,name='list_brand'),
    # Brand add
    path('add_brand/',add_brand,name='add_brand'),
    
]


