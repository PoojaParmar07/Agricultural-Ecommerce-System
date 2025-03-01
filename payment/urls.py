from django.urls import path
from payment.views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = "payment"

urlpatterns = [
    path('success/', stripe_success, name='stripe_success'),
    path('cancel/', stripe_cancel, name='stripe_cancel'),
    path('cod_checkout/',cod_checkout,name='cod_checkout'),
    path('stripe_checkout/', stripe_checkout, name='stripe_checkout'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)    
