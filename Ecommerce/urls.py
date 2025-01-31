from django.urls import path,include
from .views import home,add_brand,list_brand,brand_view_details

app_name = 'Ecommerce'
urlpatterns = [
    path('',home,name='home'),
    
    # Brand list
    path('list_brand/',list_brand,name='list_brand'),
    # Brand add
    path('add_brand/',add_brand,name='add_brand'),
    # Brand Update
    path('brand_view_details/<int:pk>/',brand_view_details,name='brand_view_details'),
    
]


