from django import forms
from .models import Membership_plan, User_membership

class MembershipplanForm(forms.ModelForm):
    class Meta:
        model = Membership_plan
        fields = ['plan_name', 'annual_fees', 'discount_rate', 'description']
        labels = {
            'plan_name': 'Plan Name',
            'annual_fees': 'Annual Fees',
            'discount_rate': 'Discount Rate',
            'description': 'Description',
        }
        widgets = {
            'plan_name': forms.TextInput(attrs={'class': 'form-control'}),
            'annual_fees': forms.NumberInput(attrs={'class': 'form-control'}),
            'discount_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
        
        
class UserMembershipForm(forms.ModelForm):
    class Meta:
        model = User_membership
        fields = ['plan', 'user','membership_start_date', 'membership_end_date', 'status']
        widgets = {
            'plan': forms.Select(attrs={'class': 'form-control'}),  # Dropdown for selecting a plan
            'user': forms.Select(attrs={'class': 'form-control'}),  # Dropdown for selecting a plan
            'membership_start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'membership_end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-control'}),  # Dropdown for selecting status
        }
        
    