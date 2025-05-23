"""
URL configuration for jyotiagro project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordChangeView,PasswordChangeDoneView


urlpatterns = [
    path('built-in_admin/', admin.site.urls),
    path('admin/dashboard/',include('admin_dashboard.urls')),
    path('',include('Ecommerce.urls')),
    path('account/',include('account.urls')),
    path('membership/',include('membership.urls')),
    path('socialmedia/',include('socialmedia.urls')),
    path('payment/',include('payment.urls')),
    
    
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password_change/',PasswordChangeView.as_view(template_name='registration/password_change_form.html'),name='password_change'),
    path('password_change_done',PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'),name='password_change_done'),
    
    
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)