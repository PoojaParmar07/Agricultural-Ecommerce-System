from django.db import models
from django.conf import settings

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
        return self.user_name
    