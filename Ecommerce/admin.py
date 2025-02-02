from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(ProductVariant)
admin.site.register(ProductBatch)
admin.site.register(Payment)
admin.site.register(Order)
admin.site.register(Order_Item)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Wishlist)
admin.site.register(WishlistItem)
