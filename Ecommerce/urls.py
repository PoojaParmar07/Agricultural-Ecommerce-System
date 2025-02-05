from django.urls import path,include
from django.conf.urls.static import static

from .views import *

app_name = 'Ecommerce'

urlpatterns = [
    path('',home,name='home'),

    path('homebody/',homebody,name='homebody'),

    path('product_list/',product_list,name='product_list'),

   
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

