from django.urls import path,include
from .views import home

app_name = 'Ecommerce'
urlpatterns = [
    path('',home,name='home')
]


