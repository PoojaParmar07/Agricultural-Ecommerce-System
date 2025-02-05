from django.urls import path,include
from django.conf.urls.static import static

from .views import *

app_name = 'Ecommerce'

urlpatterns = [
    path('',home,name='home'),
    path('homepage/',homepage,name='homepage'),
   
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

