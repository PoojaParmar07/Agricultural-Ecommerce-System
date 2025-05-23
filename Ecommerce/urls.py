from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from .views import *

app_name = 'Ecommerce'

urlpatterns = [
    
    path('home/',home,name='home'),

    path('',homepage,name='homepage'),
    path('product_list/<int:category_id>/', product_list, name='product_list'),
    path('product_view/<int:variant_id>/',product_view,name='product_view'),
    
    
    path('cart_view/',cart_view, name='cart_view'),
    path('add_to_cart/<int:variant_id>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    
    
    path('Ecommerce/increase_quantity/', increase_quantity, name='increase_quantity'),
    path('Ecommerce/decrease_quantity/', decrease_quantity, name='decrease_quantity'),
    path('Ecommerce/update_variant/<int:cart_item_id>/', update_variant, name='update_variant'),
    path("cart/count/", get_cart_count, name="cart_count"), 
    
    
    path('checkout/',checkout,name='checkout'),
    path('get-delivery-charge/<int:pincode_id>/',
         get_delivery_charge_ajax, name='get_delivery_charge'),
    path('checkout/', checkout, name='checkout'),
    path('get_pincode/<int:city_id>/', get_pincode, name='get_pincode'),
    path('payment_success/', payment_success, name='payment_success'),
    
    
    
    # path('cod_checkout/',cod_checkout,name='cod_checkout'),
    path('order_history/',order_history,name='order_history'),
    path('order_invoice/<int:order_id>/',order_invoice,name="order_invoice"),
    path('order_details/<int:order_id>/',order_details,name="order_details"),

    path('confirm_Order/',confirm_Order,name='confirm_Order'),
    # path('render_pdf_view',render_pdf_view,name="render_pdf_view"),
    
    path('wishlist/', wishlist_view, name='wishlist'),
    path('add-to-wishlist/<int:variant_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('remove/<int:item_id>/',remove_from_wishlist, name='remove_from_wishlist'),

    
    path("search-results/", ProductSearchView.as_view(), name="search_results"),

    path('aboutus/',aboutus,name="aboutus"),
    path('enquiry/',enquiry,name="enquiry"),
    path('crop_info/',crop_info,name="crop_info"),
    
    path('okra/',okra,name="okra"),
    path('spinach/',spinach,name="spinach"),
    path('tomato/',tomato,name="tomato"),
    path('corainder/',corainder,name="corainder"),
    path('potato/',potato,name="potato"),
    path('peas/',peas,name="peas"),
    
    path('enquiry_view/',enquiry_view,name='enquiry_view'),
    path('membership_plan/',membership_plan,name='membership_plan'),
    
    path('product_listing/',product_listing,name='product_listing'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

