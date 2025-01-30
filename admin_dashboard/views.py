# custom_admin/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

# Check if the user is staff
def is_admin_user(user):
    return user.is_staff

@login_required
@user_passes_test(is_admin_user)  # Ensure only admin users can access
def admin_dashboard(request):
    return render(request, 'admin_dashboard/index.html')  # Your custom template

# @login_required
