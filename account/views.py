from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib import messages
from .models import CustomUser
from django.contrib.auth import authenticate, login,logout
from .form import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required,user_passes_test
from Ecommerce.views import is_admin_user
from django.http import Http404
from django.urls import reverse_lazy
# Create your views here.





class CustomLoginView(LoginView):
    """Custom Login View to authenticate users with email instead of username."""
    
    template_name = 'registration/login.html'  
    form_class = AdminLoginForm  # Use your custom form

    def dispatch(self, request, *args, **kwargs):
        """Prevent already authenticated users from accessing the login page."""
        if request.user.is_authenticated:
            return redirect(self.get_success_url())  
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        """
        Override get_form_kwargs to remove 'request' from form initialization.
        """
        kwargs = super().get_form_kwargs()
        kwargs.pop('request', None)  # Remove 'request' argument
        return kwargs

    def form_valid(self, form):
        """Authenticate user using email instead of username."""
        email = form.cleaned_data.get("email")  
        password = form.cleaned_data.get("password")

        user = authenticate(self.request, username=email, password=password)  # Authenticate using email

        if user is not None:
            login(self.request, user)
            messages.success(self.request, "Successfully logged in")
            return redirect(self.get_success_url())
        else:
            messages.error(self.request, "Invalid email or password")
            return self.form_invalid(form)

    def form_invalid(self, form):
        """Handles invalid login attempts."""
        messages.error(self.request, "Invalid login details. Please try again.")
        return super().form_invalid(form)

    def get_success_url(self):
        """Redirect users based on their role."""
        if self.request.user.is_staff:
            return reverse_lazy('admin_dashboard:admin_dashboard')  # Redirect admin users
        return reverse_lazy('Ecommerce:homepage')  # Redirect normal users

    




def handleregi(request):
    if request.method == 'POST':
        # Extract POST data
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        mobile_number = request.POST['mobile_number']
        city = request.POST['city']
        state = request.POST['state']
        pincode = request.POST['pincode']
        address=request.POST['address']


        # Validation checks
        
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already taken")
            return redirect('account:registration')

        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
            return redirect('account:registration')

        if len(pass1) < 8:
            messages.warning(request, "Your password is too short. Consider using a longer password for better security.")
            return redirect('account:registration')
        
        if len(address) > 255:
            messages.warning(request,"Address must be less than 255 characaters")
            return redirect('account:registration')

        # Create user
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=pass1,
            mobile_number=mobile_number,
            city=city,
            state=state,
            pincode=pincode,
            address=address,
        )
        user.save()
        messages.success(request, "Your account has been successfully created")
        return redirect('account:login')
    return render(request, 'account/registration.html')



@login_required
# @user_passes_test(is_admin_user) 
def user_list(request):
    users=CustomUser.objects.all()
    return render(request,'admin_dashboard/users_list.html',{'users':users})



#ADD USER VIEW ON ADMIN SIDE


@login_required
@user_passes_test(is_admin_user) 
def user_add(request):
    context = {
        'model_name': 'User',
        'list':'account:user_list',
    }
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])  # Hash the password

            # Set additional fields
            user.is_staff = form.cleaned_data['is_staff']
            user.is_superuser = form.cleaned_data['is_superuser']
            user.is_active = form.cleaned_data['is_active']
            
            user.save()
            return redirect('account:user_list')  # Redirect to admin dashboard
    else:
        form = AddUserForm()

    context['form'] = form
    return render(request, 'admin_dashboard/add_form.html',context)


@login_required
@user_passes_test(is_admin_user) 
def user_view_details(request,pk):
    context = {
        'model_name': 'User',
    }
    try:
        user=get_object_or_404(CustomUser,pk=pk)
    except Http404:
        return render(request,'404.html')
    form=DeleteUserForm(instance=user)
    if request.method == 'POST':
        if 'delete'  in request.POST:
            user.delete()
            messages.success(request, "User deleted successfully!")
            return redirect('account:user_list')
        elif 'cancel'  in request.POST:
            return redirect('account:user_list')
        else:
            return redirect('account:user_list')


    context['form'] = form   
    return render(request,'admin_dashboard/view_details.html',context)

# @login_required
# def profile_view(request):
#     profile, created = Profile.objects.get_or_create(user=request.user)
    
#     if request.method == 'POST':
#         form = ProfileForm(request.POST, request.FILES, instance=profile)
#         if form.is_valid():
#             form.save()
#             return redirect('profile_view')
#     else:
#         form = ProfileForm(instance=profile)

#     return render(request, 'Ecommerce/user_profile.html', {'form': form})




@login_required
def update_profile(request):
    user = request.user 

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            user = form.save(commit=False)

            # Check if a new image is uploaded
            if 'image' in request.FILES:
                user.image = request.FILES['image']

            user.save()
            messages.success(request, "Profile Updated Successfully")
            return redirect('account:profile') 

    else:
        form = ProfileForm(instance=user)

    return render(request, 'Ecommerce/user_profile.html', {'form': form})
    




