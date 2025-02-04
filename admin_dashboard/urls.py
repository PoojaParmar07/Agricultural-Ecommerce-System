# custom_admin/urls.py
from django.urls import path,include
from .views import *
from django.conf.urls.static import static


app_name = 'admin_dashboard'
urlpatterns = [
    path('',admin_dashboard, name='admin_dashboard'),
    
    
    
    
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
    
    # Cart
    path('cart_list/',cart_list,name='cart_list'),
    path('add_cart/',add_cart,name='add_cart'),
    path('cart_view_details/<int:pk>/',cart_view_details,name='cart_view_details'),
    
    # cart Item
    path('cartitem_list/',cartitem_list,name='cartitem_list'),
    path('cartitem_add/',cartitem_add,name='cartitem_add'),
    path('cartitem_view_details/<int:pk>/',cartitem_view_details,name='cartitem_view_details'),
    
    
    # Wishlist
    path('wishlist_list/',wishlist_list,name='wishlist_list'),
    path('wishlist_add/',wishlist_add,name='wishlist_add'),
    path('wishlist_view_details/<int:pk>',wishlist_view_details,name='wishlist_view_details'),
    
    # WishlistItem 
    path('wishlist_item_list/',wishlist_item_list,name='wishlist_item_list'),
    path('wishlist_item_add/',wishlist_item_add,name='wishlist_item_add'),
    path('wishlist_item_view_details/<int:pk>',wishlist_item_view_details,name='wishlist_item_view_details'),
    
    #City
    path('city_list/',city_list,name='city_list'),
    path('add_city/',add_city,name='add_city'),
    path('city_view_details/<int:pk>/',city_view_details,name='city_view_details'),
    
    # Pincode
    path('pincode_list/',pincode_list,name='pincode_list'),
    path('pincode_add/',pincode_add,name='pincode_add'),
    path('pincode_view_details/<int:pk>/',pincode_view_details,name='pincode_view_details'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
