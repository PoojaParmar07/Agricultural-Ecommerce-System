from django.contrib import admin
from .models import Category,Brand,Product,ProductVariant,ProductBatch,Payment,Order,Order_Item
# Register your models here.
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(ProductVariant)
admin.site.register(ProductBatch)
admin.site.register(Payment)
admin.site.register(Order)
admin.site.register(Order_Item)