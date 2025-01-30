from django import forms
from .models import Membership_plan, User_membership

class MembershipplanForm(forms.ModelForm):
    class Meta:
        model = Membership_plan
        fields = ['plan_name','annual_fees','discount_rate','description']
        labels = {
            'plan_name': 'Plan Name',
            'annual_fees': 'Annual Fees',
            'discount_rate': 'Discount Rate',
            'description': 'Description',
        }
        
        
class UserMembershipForm(forms.ModelForm):
    class Meta:
        model = User_membership
        fields = ['plan','membership_start_date','membership_end_date','status']
        widgets = {
            'membership_start_date': forms.DateInput(attrs={'type': 'date'}),
            'membership_end_date': forms.DateInput(attrs={'type': 'date'}),
        }
        
    