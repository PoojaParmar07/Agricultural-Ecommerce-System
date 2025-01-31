from django.db import models

# Create your models here.

class Brand(models.Model):
    
    brand_id = models.AutoField(primary_key=True)
    brand_name = models.CharField(max_length=100)
    create_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table='Brand'
        
    def __str__(self):
        return self.brand_name
        
        
class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100)
    create_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'Category'
        
    def __str__(self):
        return self.category_name
        
class Product(models.Model):
    
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    description = models.TextField()
    product_image = models.ImageField(upload_to='media/products/')
    min_qty = models.ImageField(default=1)
    max_qty = models.IntegerField(default=5)
    create_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        db_table = 'Product'
        
    def __str__(self):
        return self.product_name
        

class ProductVariant(models.Model):
    
    variant_id = models.AutoField(primary_key=True)
    product = models.ForeignKey('Product',on_delete=models.CASCADE)    
    brand = models.ForeignKey('Brand',on_delete=models.CASCADE)
    units = models.CharField(max_length=50)
    create_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'ProductVariant'
        
        

class ProductBatch(models.Model):
    batch_id = models.AutoField(primary_key=True)
    variant = models.ForeignKey('ProductVariant',on_delete=models.CASCADE)
    manufacture_date = models.DateField()
    expiry_date = models.DateField()
    batch_code = models.CharField(max_length=100,unique=True)
    create_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        db_table = 'ProductBatch'
        
class Inventory(models.Model):
    inventory_id = models.AutoField(primary_key=True)
    batch = models.ForeignKey("ProductBatch", on_delete=models.CASCADE)
    quatity = models.IntegerField(default=0)
    purchase_price = models.DecimalField(max_digits=5, decimal_places=2)
    sales = models.DecimalField(max_digits=5, decimal_places=2)
    create_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'Inventory'
        

class Order(models.Model):
    
    user_type = [
        ('member','Member'),
        ('non-member','Non-member'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    ]
    
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey("account.CustomUser", on_delete=models.CASCADE)
    order_user_type = models.CharField(max_length=50,choices=user_type,default='member')
    total_price = models.DecimalField(max_digits=5, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=5, decimal_places=2)
    order_status = models.CharField(max_length=100,default='pending',choices=STATUS_CHOICES)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    pincode = models.CharField(max_length=100)
    delivery_charges = models.DecimalField(max_digits=5, decimal_places=2)
    create_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        db_table = 'Order'


class Order_Item(models.Model):
    order_item_id = models.AutoField(primary_key=True)
    order = models.ForeignKey("Order", on_delete=models.CASCADE)
    batch = models.ForeignKey("ProductBatch", on_delete=models.CASCADE)
    variant = models.ForeignKey("ProductVariant", on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    create_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'OrderItem'
    
    
class Payment(models.Model):
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    payment_id = models.AutoField(primary_key=True)
    order = models.ForeignKey("Order", on_delete=models.CASCADE)
    membership= models.ForeignKey('membership.User_membership', on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=5, decimal_places=2,default=0.00)
    payment_mode = models.CharField(max_length=50)
    payment_status=models.CharField(max_length=100,choices=PAYMENT_STATUS_CHOICES,default='pending')
    transaction_id=models.CharField(unique=True,max_length=100, null=True)
    payment_date=models.DateTimeField(auto_now=True)
    create_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table='Payment'
        
        
class DeliveryZone(models.Model):
    zone_name = models.CharField(max_length=100)  # Name of the zone (e.g., Ahmedabad, Surat)
    pincode_start = models.IntegerField()         # Start of the pincode range
    pincode_end = models.IntegerField()           # End of the pincode range
    delivery_charge = models.DecimalField(max_digits=6, decimal_places=2)  # Delivery charge for this zone
    create_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.zone_name} ({self.pincode_start} - {self.pincode_end})"

    class Meta:
        db_table = "DeliveryZone"
        
        
        
