
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

