from django.db import models
from django.conf import settings
# Create your models here.
class Membership_plan(models.Model):
    plan_id=models.AutoField(primary_key=True,null=None)
    
    plan_name=models.CharField(max_length=100)
    annual_fees = models.DecimalField(max_digits=10, decimal_places=2)
    discount_rate = models.FloatField()  # Discount rate in percentage
    description = models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.plan_name 
    
    class Meta:
        db_table = 'Membership_plan' 
        
        
class User_membership(models.Model):
    
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=False)
    plan = models.ForeignKey('membership.Membership_plan',on_delete=models.CASCADE)
    membership_start_date = models.DateField()
    membership_end_date = models.DateField()
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_membership'
        
    
    def __str__(self):
        return f"{self.user} - {self.plan} ({self.status})"