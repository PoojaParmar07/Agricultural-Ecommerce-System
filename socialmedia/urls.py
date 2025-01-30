from django.urls import path
from .views import list_post, add_post, post_view_details
from django.conf import settings
from django.conf.urls.static import static
app_name = "socialmedia"

urlpatterns = [
    path('post/', list_post, name='post'),
    path('add_post/', add_post, name='add_post'),
    path('post_view_details/<int:pk>/', post_view_details, name='post_view_details'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
