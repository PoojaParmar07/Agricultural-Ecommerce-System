from django.shortcuts import render,redirect,get_object_or_404
from django.conf import settings
from .models import Membership_plan, User_membership
from .form import MembershipplanForm, UserMembershipForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from django.http import Http404
from django.utils.timezone import now
from datetime import timedelta
from account.models import CustomUser


def is_admin_user(user):
    return user.is_staff



def home(request):
    print(settings.TEMPLATES[0]['DIRS'])
    return render(request, 'Ecommerce/base.html')




# Create your views here.
@login_required
@user_passes_test(is_admin_user) 
def membership_plan_list(request):
    plans = Membership_plan.objects.all()
    return render(request,'admin_dashboard/membership_plan_list.html', {'plans': plans})




@login_required
@user_passes_test(is_admin_user) 
def membership_plan_add(request):
    
    context = {
        'model_name' : "Add Membership Plan",
        'list':'membership:membership_plan_list',
    }
    
    if request.method == 'POST':
        form = MembershipplanForm(request.POST)
        if form.is_valid():
            plan_name = form.cleaned_data['plan_name']
            if Membership_plan.objects.filter(plan_name = plan_name).exists():
                messages.error(request, "Membership Plan already exists.")
            else:
                form.save()
                messages.success(request, "Membership Plan added successfully.")
                return redirect('membership:membership_plan_list')
    else:
        form = MembershipplanForm()
       
    context['form'] = form 
    return render(request,'admin_dashboard/add_form.html',context)






@login_required
@user_passes_test(is_admin_user) 
def membership_view_details(request, pk):
    
    context = {
        'model_name': 'Update Membership Plan'
    }
    
    try:
        plan = get_object_or_404(Membership_plan, pk = pk)
    except Http404:
        return render(request, '404.html', status=404)
    
    form = MembershipplanForm(instance=plan)
    
    if request.method == 'POST':
        if 'update' in request.POST:
            form = MembershipplanForm(request.POST, instance=plan)
            
            if form.is_valid():
                form.save()
                messages.success(request, "Membership plan updated successfully!")
                return redirect('membership:membership_plan_list')
            else:
                messages.error(request, "Membership plan update failed. Please correct the errors.")

        elif 'delete' in request.POST:  # Delete action
            plan.delete()
            messages.success(request, "Membership plan deleted successfully!")
            return redirect('membership:membership_plan_list')
        
        elif 'cancel' in request.POST:
            return redirect('membership:membership_plan_list')
        
    context['form'] = form
    context['plan'] = plan
    return render(request, 'admin_dashboard/view_details.html',context)





@login_required
@user_passes_test(is_admin_user) 
def user_membership(request):
    memberships = User_membership.objects.all()
    return render(request, 'admin_dashboard/user_membership.html', {'memberships':memberships})




@login_required
@user_passes_test(is_admin_user)  # Ensure only admin users can access
def add_user_membership(request):
    
    context = {
        'model_name' : "Add User Member",
        'list':'membership:membership_plan_list',
    }
    
    if request.method == "POST" and 'plan' in request.POST:
        form = UserMembershipForm(request.POST)
        if form.is_valid():
            plan_id = form.cleaned_data.get('plan')  # Fetch the selected plan from the form
            # Check if the user already has an active membership for the selected plan
            existing_membership = User_membership.objects.filter(user=request.user, plan=plan_id).exists()
            
            if existing_membership:
                messages.error(request, "You already have an active membership for this plan.")
                return render(request, 'admin_dashboard/add_user_membership.html', {'form': form})
            
            # Proceed to create the membership if no active membership exists
            membership = form.save(commit=False)
            membership.user = request.user  # Assign the logged-in user
            membership.plan = plan_id  # Assign the selected plan

            # Calculate membership_end_date
            start_date = membership.membership_start_date
            membership.membership_end_date = start_date + timedelta(days=365)

            # Save the membership
            membership.save()
            messages.success(request, "User membership added successfully!")
            return redirect('membership:user_membership')
        else:
            messages.error(request, "Error adding user membership. Please check the form.")
    else:
        form = UserMembershipForm()

    return render(request, 'admin_dashboard/add_user_membership.html', {'form': form})



    
    
def user_membership_details(request, pk):
    try:
        # Fetch the category or raise Http404 if not found
        membership = get_object_or_404(User_membership, pk=pk)
    except Http404:
        # Render the custom 404 page
        return render(request, '404.html', status=404)
    
    form = UserMembershipForm(instance=membership)
    
    if request.method == 'POST':
        if 'update' in request.POST:  # Update action
            form = UserMembershipForm(request.POST, instance=membership)
            if form.is_valid():
                form.save()
                messages.success(request, "Membership updated successfully!")
                return redirect('membership:user_membership')
            else:
                messages.error(request, "Membership update failed. Please correct the errors.")
        if 'delete' in request.POST:  # Delete action
            membership.delete()
            messages.success(request, "Membership deleted successfully!")
            return redirect('membership:user_membership')

        elif 'cancel' in request.POST:  # Cancel action
            return redirect('membership:user_membership')

    return render(request, 'admin_dashboard/user_membership_details.html', {'form': form, 'membership': membership})


        