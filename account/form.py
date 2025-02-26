from django import forms
from .models import *
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
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}),
        label="Password"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'}),
        label="Confirm Password"
    )
    is_staff = forms.BooleanField(
        required=False, label="Staff Status", widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    is_superuser = forms.BooleanField(
        required=False, label="Superuser Status", widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    is_active = forms.BooleanField(
        required=False, label="Active Status", initial=True, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        help_text="Upload a profile picture (JPG, JPEG, PNG)."
    )

    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'password', 'confirm_password', 'image',
            'city', 'state', 'pincode', 'mobile_number', 'address',
            'is_staff', 'is_superuser', 'is_active'
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'pincode': forms.NumberInput(attrs={'class': 'form-control'}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

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
        widgets = {
            'username': forms.TextInput(attrs={'readonly': 'readonly'}),
            'email': forms.EmailInput(attrs={'readonly': 'readonly'}),
            'city': forms.TextInput(attrs={'readonly': 'readonly'}),
            'state': forms.TextInput(attrs={'readonly': 'readonly'}),
            'pincode': forms.NumberInput(attrs={'readonly': 'readonly'}),
            'mobile_number': forms.TextInput(attrs={'readonly': 'readonly'}),
            'address': forms.Textarea(attrs={'rows': 3, 'readonly': 'readonly'}),
        }



class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser  
        fields = ['username', 'email', 'mobile_number', 'address', 'city', 'state', 'pincode', 'image']

    image = forms.ImageField(required=False)

        