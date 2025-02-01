from django import forms

from .models import Category,Brand,ProductVariant,Product, ProductBatch,Inventory




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
        fields = ['product', 'variant', 'manufacture_date', 'expiry_date', 'batch_code']
        
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control', 'onchange': 'this.form.submit()'}),  # Auto-submit on change
            'variant': forms.Select(attrs={'class': 'form-control'}),
            'manufacture_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'batch_code': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(ProductBatchForm, self).__init__(*args, **kwargs)

        if 'product' in self.data:
            try:
                product_id = int(self.data.get('product'))  # Get selected product ID from form data
                self.fields['variant'].queryset = ProductVariant.objects.filter(product_id=product_id)  # Filter variants
            except (ValueError, TypeError):
                self.fields['variant'].queryset = ProductVariant.objects.none()  # No product selected
        else:
            self.fields['variant'].queryset = ProductVariant.objects.none()  # Default empty queryset

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