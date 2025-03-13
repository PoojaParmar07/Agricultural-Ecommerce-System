from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
app_name = "socialmedia"

urlpatterns = [
    # Post
    path('post/', list_post, name='post'),
    path('add_post/', add_post, name='add_post'),
    path('post_view_details/<int:pk>/', post_view_details, name='post_view_details'),
    
    
    # Post's Comment
    path('post_comment_list/',post_comment_list,name='post_comment_list'),
    path('post_comment_add/',post_comment_add,name='post_comment_add'),
    path('post_comment_view_details/<int:pk>/',post_comment_view_details,name='post_comment_view_details'), 
    
    path("my_feed/",my_feed,name="my_feed"),
    path("add_comment/<int:post_id>/", add_comment, name="add_comment"),
    path("create_post/",create_post,name="create_post"),
    path('like/<int:post_id>/', like_post, name='like_post'),
    path("create_post/",create_post,name="create_post"),
     path("user_feed/", user_feed, name="user_feed"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
