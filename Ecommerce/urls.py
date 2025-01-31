from django.urls import path,include
<<<<<<< Updated upstream
<<<<<<< Updated upstream
from .views import home, category_list, category_add, category_view_details,list_brand,add_brand,brand_view_details,product_variant_list,product_variant_add
=======
from .views import home, category_list, category_add, category_view_details,list_brand,add_brand,brand_view_details, product_list, add_product, product_view_details
>>>>>>> Stashed changes
=======
from .views import home, category_list, category_add, category_view_details,list_brand,add_brand,brand_view_details, product_list, add_product, product_view_details
>>>>>>> Stashed changes

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
    

    
    # Product Variant
    path('product_variant_list/',product_variant_list,name='product_variant_list'),
    path('product_variant_add/',product_variant_add,name='product_variant_add'),

    # Product List
    path('product_list/',product_list,name='product_list'),
    path('add_product/',add_product,name='add_product'),
    path('product_view_details/',product_view_details,name='product_view_details'),
    

]





