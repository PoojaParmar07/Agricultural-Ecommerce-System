from django.urls import path
from payment.views import *

app_name = "payment"

urlpatterns = [
    path('success/', stripe_success, name='stripe_success'),
    path('cancel/', stripe_cancel, name='stripe_cancel'),
    path('cod_checkout/',cod_checkout,name='cod_checkout'),
    path('stripe_checkout/', stripe_checkout, name='stripe_checkout'),
    path("stripe/webhook/", stripe_webhook, name="stripe_webhook"),
]
