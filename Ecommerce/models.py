from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings

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
    min_qty = models.IntegerField(default=1)
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
        
    def __str__(self):
        return f"{self.product.product_name} - {self.brand.brand_name} - {self.units}"
        
        

class ProductBatch(models.Model):
    batch_id = models.AutoField(primary_key=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    variant = models.ForeignKey('ProductVariant',on_delete=models.CASCADE)
    manufacture_date = models.DateField()
    expiry_date = models.DateField()
    batch_code = models.CharField(max_length=100,unique=True)
    create_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        db_table = 'ProductBatch'
        
        
    def __str__(self):
        return self.batch_code
        
class Inventory(models.Model):
    inventory_id = models.AutoField(primary_key=True)
    batch = models.ForeignKey("ProductBatch", on_delete=models.CASCADE)
    quatity = models.IntegerField(default=0)
    purchase_price = models.DecimalField(max_digits=5, decimal_places=2)
    sales_price = models.DecimalField(max_digits=5, decimal_places=2)
    create_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'Inventory'
        
    def __str__(self):
        return f"{self.quantity}"

        

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
        
    def __str__(self):
        return f"{self.order_id}"


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
    
    def __str__(self):
        return f"{self.order_item_id}"
    



class Payment(models.Model):
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    PAYMENT_MODE=[
        ('cash','Cash'),
        ('online','Online'),
    ]
    
    payment_id = models.AutoField(primary_key=True)
    order = models.ForeignKey("Order", on_delete=models.CASCADE, blank=True, null=True)
    membership = models.ForeignKey('membership.User_membership', on_delete=models.CASCADE, blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_mode = models.CharField(max_length=50,choices=PAYMENT_MODE, default='cash')
    payment_status = models.CharField(max_length=100, choices=PAYMENT_STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    payment_date = models.DateTimeField(auto_now=True)
    create_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Payment'
    
    def clean(self):
        """
        Ensures that at a time either order or membership is filled, not both.
        """
        if self.order and self.membership:
            raise ValidationError("Either 'order' or 'membership' should be filled, but not both.")
        if not self.order and not self.membership:
            raise ValidationError("Either 'order' or 'membership' must be provided.")

    def save(self, *args, **kwargs):
        self.clean()  # Validate before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Payment {self.payment_id}"

        
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
        
    def __str__(self):
        return f"{self.zone_name}"
    
        
        
        
class Feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    user = models.ForeignKey("account.CustomUser", on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    description = models.TextField(max_length=255)
    create_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "Feedback"
    
    def __str__(self):
        return f"{self.feedback_id}"
    
class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    user = models.ForeignKey("account.CustomUser", on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    rating = models.IntegerField()
    review = models.CharField(max_length=255)
    create_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "Review"
        
    def __str__(self):
        return f"{self.review_id}"
    
    
    
class Cart(models.Model):
    cart_id=models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'Cart'
        
    def __str__(self):
        return f"Cart of {self.user}"    
        

class CartItem(models.Model):
    cart_item_id=models.AutoField(primary_key=True)
    cart = models.ForeignKey('Cart',on_delete=models.CASCADE)
    product_batch = models.ForeignKey('ProductBatch',on_delete=models.CASCADE)
    product_variant = models.ForeignKey('ProductVariant',on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'CartItem'
        unique_together = (('cart', 'product_batch', 'product_variant'),)
        
    def __str__(self):
        return f"CartItem: {self.product_variant} (Qty: {self.quantity})"


class Wishlist(models.Model):
    wishlist_id=models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'Wishlist'
        
    def __str__(self):
        return f"Wishlist of {self.user}"

class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist,on_delete=models.CASCADE)
    product_batch = models.ForeignKey('ProductBatch',on_delete=models.CASCADE)
    product_variant = models.ForeignKey('ProductVariant',on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'WishlistItem'
        unique_together = (('wishlist', 'product_batch', 'product_variant'),)
        
    def __str__(self):
        return f"WishlistItem: {str(self.product_variant)}"
    
    
    
    
    
    

