from django.urls import path,include
from .views import *
from django.conf.urls.static import static
from django.conf import settings



app_name = 'Ecommerce'

urlpatterns = [
    path('home/',home,name='home'),

    path('',homebody,name='homebody'),
    path('product_list/<int:category_id>/', product_list, name='product_list'),
   path('product_view/<int:product_id>/',product_view, name='product_view'),


   
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

