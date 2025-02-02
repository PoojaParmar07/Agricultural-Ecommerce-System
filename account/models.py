from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
# Create your models here.



class CustomUser(AbstractUser):
    username=models.CharField(max_length=100,unique=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    mobile_number = models.CharField(max_length=10)
    email=models.EmailField(unique=True,max_length=100)
    address=models.TextField(max_length=255)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    image=models.ImageField(upload_to='account/',default='account/profile.jpg')
    

    class Meta:
         db_table = 'user' 
         
    def __str__(self):
        return str(self.username) if self.username else "Unnamed User"   