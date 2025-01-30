from django import forms
from .models import CustomUser
from django.core.exceptions import ValidationError

class AdminLoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)



from django import forms
from .models import CustomUser

class AddUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    is_staff = forms.BooleanField(required=False, label="Staff Status")
    is_superuser = forms.BooleanField(required=False, label="Superuser Status")
    is_active = forms.BooleanField(required=False, label="Active Status", initial=True)

    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'password', 'confirm_password', 
            'city', 'state', 'pincode', 'mobile_number', 'address',
            'is_staff', 'is_superuser', 'is_active'
        ]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data


class DeleteUserForm(forms.ModelForm):
    is_staff = forms.BooleanField(required=False, label="Staff Status", disabled=True)
    is_superuser = forms.BooleanField(required=False, label="Superuser Status", disabled=True)
    is_active = forms.BooleanField(required=False, label="Active Status", disabled=True)

    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 
            'city', 'state', 'pincode', 
            'mobile_number', 'address', 
            'is_staff', 'is_superuser', 'is_active'
        ]