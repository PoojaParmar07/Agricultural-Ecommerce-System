from django.urls import path,include
from django.conf.urls.static import static

from .views import *

app_name = 'Ecommerce'

urlpatterns = [
    path('home/',home,name='home'),

    path('',homebody,name='homebody'),
    path('product_list/<int:category_id>/', product_list, name='product_list'),
    path('cart_view/',cart_view, name='cart_view'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', remove_from_cart, name='remove_from_cart'),

   
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

