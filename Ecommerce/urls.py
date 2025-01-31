from django.urls import path,include
from .views import home,add_brand

app_name = 'Ecommerce'
urlpatterns = [
    path('',home,name='home'),
    
    # Brand add
    path('add_brand',add_brand,name='add_brand'),
    
]


