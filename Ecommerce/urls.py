from django.urls import path,include
<<<<<<< HEAD
from .views import home, category_list, category_add, category_view_detail
=======
from .views import home,add_brand,list_brand,brand_view_details
>>>>>>> 3c03436d3d7f31d135e8f7db906f2acdd35483a8

app_name = 'Ecommerce'
urlpatterns = [
    path('',home,name='home'),
<<<<<<< HEAD
    path('category_list/',category_list,name='category_list'),
    path('category_add/',category_add,name='category_add'),
    path('category_view_detail/<int:pk>/',category_view_detail,name='category_view_detail'),
=======
    
    # Brand list
    path('list_brand/',list_brand,name='list_brand'),
    # Brand add
    path('add_brand/',add_brand,name='add_brand'),
    # Brand Update
    path('brand_view_details/<int:pk>/',brand_view_details,name='brand_view_details'),
    
>>>>>>> 3c03436d3d7f31d135e8f7db906f2acdd35483a8
]


