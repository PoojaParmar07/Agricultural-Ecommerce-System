from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
# from account.views import handlelog,handleregi,handlelgout,user_list,user_add,user_view_details
from account.views import user_list,user_add,user_view_details,handleregi
from .views import *
from django.contrib.auth.views import LogoutView


app_name = 'account'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),  # Custom login view
    # path('', include('django.contrib.auth.urls')),  # Built-in auth URLs
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', handleregi, name='registration'), 
    path('user_list/',user_list,name='user_list'),
    path('user_add/',user_add,name='user_add'),
    path('user_view_details/<int:pk>',user_view_details,name='user_view_details'),
    path("profile/", update_profile, name="profile"),
    
    
    
     
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)