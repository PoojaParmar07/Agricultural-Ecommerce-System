from django import forms

from .models import *




class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name']

        widgets = {
            'category_name': forms.TextInput(attrs={
                'class': 'form-control',  # Add any custom CSS class
                'placeholder': 'Enter Category Name',  # Add a placeholder
                'maxlength': '100',  # Limit input length
        }),
    }
        
class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['brand_name']  # Add other fields if needed
        labels = {'brand_name': 'Brand Name'}  # Customize label
        widgets = {
            'brand_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter brand name'}),
        }
        
class ProductVariantForm(forms.ModelForm):
    class Meta:
        model = ProductVariant
        fields = ['product', 'brand', 'units']  # Add any fields you want to include in the form
        
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'brand': forms.Select(attrs={'class': 'form-control'}),
            'units': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category','product_name',  'description', 'product_image', 'min_qty', 'max_qty']
        
        widgets = {
             'category': forms.Select(attrs={
                'class': 'form-select',
            }),
            'product_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product name',
            }),
           
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter product description',
            }),
            'product_image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
            'min_qty': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,  # Minimum allowed quantity
            }),
            'max_qty': forms.NumberInput(attrs={
                'class': 'form-control',
                'max': 5,  # You can set an appropriate maximum value
            }),

        }
        
        
class ProductBatchForm(forms.ModelForm):
    class Meta:
        model = ProductBatch
        fields = ['variant', 'manufacture_date', 'expiry_date', 'batch_code']

        widgets = {

            'product': forms.Select(attrs={'class': 'form-control', 'onchange': 'this.form.submit()'}),  # Auto-submit on change
            'variant': forms.Select(attrs={'class': 'form-control' , 'onchange': 'this.form.submit()'}),
            'manufacture_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'batch_code': forms.TextInput(attrs={'class': 'form-control'}),

            'variant': forms.Select(attrs={'class': 'form-control'}),
            'manufacture_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'expiry_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'batch_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Batch Code'}),

        }
        
        

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['batch', 'quatity', 'purchase_price', 'sales_price']
        
        widgets = {
            'batch': forms.Select(attrs={'class': 'form-control'}),
            'quatity': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'purchase_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'sales_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
        
        
        


class DeliveryZoneForm(forms.ModelForm):
    class Meta:
        model = DeliveryZone
        fields = ['zone_name', 'pincode_start', 'pincode_end', 'delivery_charge']
        
        widgets = {
            'zone_name': forms.TextInput(attrs={'class': 'form-control'}),
            'pincode_start': forms.NumberInput(attrs={'class': 'form-control'}),
            'pincode_end': forms.NumberInput(attrs={'class': 'form-control'}),
            'delivery_charge': forms.NumberInput(attrs={
                'class': 'form-control','step': '0.01'}),
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'user', 'order_user_type', 'total_price', 'discounted_price', 
            'order_status', 'state', 'city', 'address', 'pincode', 'delivery_charges'
        ]
        
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'order_user_type': forms.Select(attrs={'class': 'form-control'}),
            'total_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'discounted_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'order_status': forms.Select(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'pincode': forms.TextInput(attrs={'class': 'form-control'}),
            'delivery_charges': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
        
        
class OrderItemForm(forms.ModelForm):
    class Meta:
        model = Order_Item
        fields = ['order', 'batch', 'variant', 'quantity', 'price']
        widgets = {
            'order': forms.Select(),
            'batch': forms.Select(),
            'variant': forms.Select(),
            'quantity': forms.NumberInput(attrs={'min': 1}),
            'price': forms.NumberInput(attrs={'step': '0.01'}),
        }
        
        
        
class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'
        widgets = {
            'payment_mode': forms.Select(attrs={'class': 'form-control'}),
            'payment_status': forms.Select(attrs={'class': 'form-select'}),
            'transaction_id': forms.TextInput(attrs={'class': 'form-control'}),
            'total_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'order': forms.Select(attrs={'class': 'form-select'}),
            'membership': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        order = cleaned_data.get('order')
        membership = cleaned_data.get('membership')

        if order and membership:
            raise ValidationError("You can only select either 'Order' or 'Membership', not both.")
        if not order and not membership:
            raise ValidationError("You must select either 'Order' or 'Membership'.")

        return cleaned_data
        
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['user', 'product', 'description']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select User'}),
            'product': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select Product'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Write your feedback here...'}),
        }
        

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['user', 'product', 'rating', 'review']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select User'}),
            'product': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select Product'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5, 'placeholder': 'Rating (1-5)'}),
            'review': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Write your review here...'}),
        }

