from django.urls import path,include
from django.conf.urls.static import static

from .views import *

app_name = 'Ecommerce'

urlpatterns = [
    path('home/',home,name='home'),

    path('',homebody,name='homebody'),
    path('product_list/<int:category_id>/', product_list, name='product_list')

   
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

