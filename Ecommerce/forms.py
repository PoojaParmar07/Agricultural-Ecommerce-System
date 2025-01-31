from django import forms
from .models import Category


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