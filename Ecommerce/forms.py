from django import forms
from .models import Brand  # Import your Brand model

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['brand_name']  # Add other fields if needed
        labels = {'brand_name': 'Brand Name'}  # Customize label
        widgets = {
            'brand_name': forms.TextInput(),
        }
