from django.urls import path,include


from .views import *

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
    path('product_variant_view_details/<int:pk>/',product_variant_view_details,name='product_variant_view_details'),

    # Product List
    path('product_list/',product_list,name='product_list'),
    path('add_product/',add_product,name='add_product'),
    path('product_view_details/<int:pk>/',product_view_details,name='product_view_details'),

    # Product Batch
    path('productbatch_list/',productbatch_list,name='productbatch_list'),
    path('productbatch_add/',productbatch_add,name='productbatch_add'),
    path('productbatch_view_details/<int:pk>/',productbatch_view_details,name='productbatch_view_details'),

    # Inventory
    path('inventory_list/',inventory_list,name='inventory_list'),
    path('inventory_add/',inventory_add,name='inventory_add'),
    path('inventory_view_details/<int:pk>/',inventory_view_details,name='inventory_view_details'),


    # Delivery Zone
    path('deliveryzone_list/',deliveryzone_list,name='deliveryzone_list'),
    path('deliveryzone_add',deliveryzone_add,name='deliveryzone_add'),
    path('deliveryzone_view_details/<int:pk>',deliveryzone_view_details,name='deliveryzone_view_details'),

    # Order
    path('order_list/',order_list,name='order_list'),
    path('order_add/',order_add,name='order_add'),
    path('order_view_details/<int:pk>/',order_view_details,name='order_view_details'),

    # Order Item
    path('orderitem_list/',orderitem_list,name='orderitem_list'),
    path('orderitem_add/',orderitem_add,name='orderitem_add'),
    path('orderitem_view_details/<int:pk>/',orderitem_view_details,name='orderitem_view_details'),
    
    # Payment 
    path('payment_list/',payment_list,name='payment_list'),
    path('payment_add/',payment_add,name='payment_add'),
    path('payment_view_details/<int:pk>/',payment_view_details,name='payment_view_details'),
    
    # Feedback
    path('feedback_list/',feedback_list,name='feedback_list'),
    path('feedback_add/',feedback_add,name='feedback_add'),
    path('feedback_view_details/<int:pk>/',feedback_view_details,name='feedback_view_details'),
    
    # Review
    path('review_list/',review_list,name='review_list'),
    path('review_add/',review_add,name='review_add'),
    path('review_view_details/<int:pk>/',review_view_details,name='review_view_details'),
    
]





