from django.urls import path
from payment.views import *

app_name = "payment"

urlpatterns = [
   
    path('cod_checkout/',cod_checkout,name='cod_checkout'),
    # path('stripe_checkout/', stripe_checkout, name='stripe_checkout'),
    # path("stripe/webhook/", stripe_webhook, name="stripe_webhook"),
    path('razorpay_checkout/',razorpay_checkout,name='razorpay_checkout'),
    path("razorpay/webhook/", razorpay_webhook, name="razorpay_webhook"),
]
