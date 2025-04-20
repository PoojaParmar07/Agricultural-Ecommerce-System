from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
from account.models import CustomUser

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
    category_image = models.ImageField(upload_to='media/products/')
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
        return f"{self.product_name},{self.product_id}"
        

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
    quantity = models.IntegerField(default=0)
    purchase_price = models.DecimalField(max_digits=5, decimal_places=2)
    sales_price = models.DecimalField(max_digits=5, decimal_places=2)
    create_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'Inventory'
        
    def __str__(self):
        return f"{self.quantity}-{self.product_variant.name} - {self.sales_price}"

    def get_price(self):
        """Get the latest sales price from the Inventory table for this variant"""
        inventory = Inventory.objects.filter(batch__variant=self).order_by('-create_at').first()
        return inventory.sales_price if inventory else 0
    
    def decrease_stock(self, quantity):
        """Decreases stock if available; raises error if not enough stock"""
        if self.quantity >= quantity:
            self.quantity -= quantity
            self.save()
        else:
            raise ValueError("Not enough stock available")

    
      
class City(models.Model):
    city_id = models.AutoField(primary_key=True)
    city_name = models.CharField(max_length=100)
    create_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'City'

    def get_delivery_charges(self, pincode):
        try:
            pincode_instance = self.pincode_set.get(pincode=pincode)
            return pincode_instance.delivery_charges
        except Pincode.DoesNotExist:
            return None
        
    def __str__(self):
        return str(self.city_name)

class Pincode(models.Model):
    pincode_id = models.AutoField(primary_key=True)
    area_pincode = models.CharField(max_length=10,unique=True)
    city = models.ForeignKey('City', on_delete=models.CASCADE, related_name="pincodes")
    delivery_charges = models.DecimalField(max_digits=5, decimal_places=2)
    create_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'Pincode'
        
    def __str__(self):
        return f" {self.city} -{self.area_pincode}"


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
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_status = models.CharField(max_length=100,default='pending',choices=STATUS_CHOICES)
    state = models.CharField(max_length=100,default='Gujarat')
    city = models.ForeignKey('City',on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    pincode = models.ForeignKey('Pincode',on_delete=models.CASCADE,null=True, blank=True)
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
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)  # Add this field
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, null=True, blank=True)
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
    review = models.CharField(max_length=255,null=True,blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    
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
        
    def total_cart_items(self):
        """Returns the total quantity of all products in the cart."""
        return sum(item.quantity for item in self.cartitem_set.all())
        
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
        
    @property
    def total_price(self):
        """Calculates total price based on quantity and selected variant's sales price."""
        inventory = Inventory.objects.filter(batch=self.product_batch, batch__variant=self.product_variant).first()
        return self.quantity * inventory.sales_price if inventory else 0
    
   

    def save(self, *args, **kwargs):
        """Override save method to recalculate and ensure price updates."""
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"CartItem: {self.product_variant} (Qty: {self.quantity})"


class Wishlist(models.Model):
    wishlist_id=models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'Wishlist'
        
    def __str__(self):
        return f"self.wishlist_id"

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
    
class Enquiry(models.Model):
    enquiry_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE) 
    email = models.EmailField(max_length=255) 
    message = models.TextField(max_length=255)  
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"Enquiry {self.enquiry_id} by {self.email}"
    
    
      
