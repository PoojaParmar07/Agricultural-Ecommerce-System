
from django import forms
from .models import *

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'review']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'class': 'form-control'}),
            'review': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    
class CartItemForm(forms.Form):

    variant_id = forms.ModelChoiceField(queryset=ProductVariant.objects.all(), required=True, empty_label=None)
    quantity = forms.IntegerField(min_value=1, max_value=10)
    sales_price = forms.DecimalField(max_digits=5,decimal_places=2)

    class Meta:
        model = CartItem
        fields = ['variant_id', 'quantity','sales_price']
        
class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = ['email', 'message'] 

        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

