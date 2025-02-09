from django import forms
from .models import CustomUser
from django.core.exceptions import ValidationError

class AdminLoginForm(forms.Form):
    email = forms.EmailField(
        max_length=100,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'})
    )



class AddUserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}),
        label="Password"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}),
        label="Confirm Password"
    )
    is_staff = forms.BooleanField(required=False, label="Staff Status")
    is_superuser = forms.BooleanField(required=False, label="Superuser Status")
    is_active = forms.BooleanField(required=False, label="Active Status", initial=True)
    
    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        help_text="Upload a profile picture (JPG, JPEG, PNG)."
    )

    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'password', 'confirm_password', 'image',
            'city', 'state', 'pincode', 'mobile_number', 'address',
            'is_staff', 'is_superuser', 'is_active'
        ]

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return confirm_password



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