from django import forms

from .models import Category,Brand,ProductVariant

from .models import Category,Brand, Product

from .models import Category,Brand, Product

from .models import Category,Brand, Product




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
        fields = ['product_name', 'category', 'description', 'product_image', 'min_qty', 'max_qty']
        
        widgets = {
            'product_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product name',
            }),
            'category': forms.Select(attrs={
                'class': 'form-select',
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
                'max': 100,  # You can set an appropriate maximum value
            }),

        }