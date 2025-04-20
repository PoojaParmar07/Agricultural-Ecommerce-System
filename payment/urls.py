from django.urls import path
from payment.views import *

app_name = "payment"

urlpatterns = [
   
    path('cod_checkout/',cod_checkout,name='cod_checkout'),
    
    
]

