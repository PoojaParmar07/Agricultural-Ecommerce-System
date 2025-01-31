from django.urls import path,include
from .views import home, category_list, category_add, category_view_details,list_brand,add_brand,brand_view_details

app_name = 'Ecommerce'
urlpatterns = [
    path('',home,name='home'),
    path('category_list/',category_list,name='category_list'),
    path('category_add/',category_add,name='category_add'),
    path('category_view_details/<int:pk>/',category_view_details,name='category_view_details'),
    
    # Brand List
    path('list_brand/',list_brand,name='list_brand'),
    path('add_brand/',add_brand,name='add_brand'),
    path('brand_view_details/<int:pk>/',brand_view_details,name='brand_view_details'),
]





