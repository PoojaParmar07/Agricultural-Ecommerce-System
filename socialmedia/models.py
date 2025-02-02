from django.db import models
from django.conf import settings
from account.models import *
from Ecommerce.models  import *
# from .models import PostComment

# Create your models here.

class Post(models.Model):
    
    post_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/',default="media/defaultUser.jpg")
    caption = models.TextField()
    likes = models.IntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'post'
        
    def __str__(self):
        return self.user
    
    
class PostComment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'PostComment'        

    def __str__(self):
        return f"Comment {self.comment_id} by {self.user.username}"