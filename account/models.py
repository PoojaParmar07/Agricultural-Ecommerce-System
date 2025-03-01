from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from django.conf import settings

# Create your models here.



class CustomUser(AbstractUser):
    username=models.CharField(max_length=100,unique=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100,default='Gujarat')
    pincode = models.CharField(max_length=10)
    mobile_number = models.CharField(max_length=10)
    email=models.EmailField(unique=True,max_length=100)
    address=models.TextField(max_length=255)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    image=models.ImageField(upload_to='account/',default='media/account/profile.jpg', blank=True, null=True)
    
    class Meta:
         db_table = 'user' 
         
    def __str__(self):
        return str(self.username) if self.username else "Unnamed User"   
    
    
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics/', default='default.jpg')
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        # Update CustomUser profile image when profile is updated
        self.user.image = self.image
        self.user.save()
        super().save(*args, **kwargs)