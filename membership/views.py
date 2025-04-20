from django.shortcuts import render,redirect,get_object_or_404
from django.conf import settings
from .models import Membership_plan, User_membership
from .form import MembershipplanForm, UserMembershipForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from django.http import Http404, JsonResponse
from django.utils.timezone import now
from django.urls import reverse
from datetime import timedelta
from account.models import CustomUser
from django.core.paginator import Paginator
from Ecommerce.models import *
import razorpay
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from datetime import date


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
    paginator = Paginator(plans, 10)  # Show 10 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin_dashboard/membership_plan_list.html', {'page_obj': page_obj})





@login_required
@user_passes_test(is_admin_user) 
def membership_plan_add(request):
    
    context = {
        'model_name' : "Membership Plan",
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
        'model_name': 'Membership Plan'
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
    paginator = Paginator(memberships, 10)  # Show 10 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin_dashboard/user_membership.html', {'page_obj': page_obj})





@login_required
@user_passes_test(is_admin_user)  
def add_user_membership(request):
    context = {
        'model_name': "User Member",
        'list':'membership:user_membership', 
    }
    
    if request.method == "POST" and 'plan' in request.POST:
        form = UserMembershipForm(request.POST)
        if form.is_valid():
            plan_id = form.cleaned_data.get('plan')  
            existing_membership = User_membership.objects.filter(user=request.user, plan=plan_id).exists()
            
            if existing_membership:
                messages.error(request, "You already have an active membership for this plan.")
                return render(request, 'admin_dashboard/add_form.html', {'form': form})
            
            membership = form.save(commit=False)
            membership.user = request.user  
            membership.plan = plan_id  
            membership.membership_end_date = membership.membership_start_date + timedelta(days=365)
            membership.save()
            
            messages.success(request, "User membership added successfully!")
            return redirect(reverse('membership:user_membership'))  # ✅ Fixed
        else:
            messages.error(request, "Error adding user membership. Please check the form.")
    else:
        form = UserMembershipForm()

    context['form'] = form
    return render(request, 'admin_dashboard/add_form.html', context)



    
@login_required
def user_membership_details(request, pk):
    
    context = {
        'model_name': 'User Membership'
    }
    
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

    context['form'] = form
    context['membership'] = membership
    return render(request, 'admin_dashboard/view_details.html', context)

@login_required
def show_membership_gold(request):
    membership_plan=Membership_plan.objects.all()
    user_membership = User_membership.objects.filter(
        user=request.user,
        membership_end_date__gte=date.today(),  # Check if membership is still valid
        status=True  # Ensure membership is active
    ).first()  # Get the first active membership if exists
    
    return render(request, "Ecommerce/membership/membership.html",{'membership_plan': membership_plan,'user_membership': user_membership})




razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))



@login_required
def create_razorpay_order(request,plan_id):
    plan = Membership_plan.objects.get(plan_id=plan_id)
    user = request.user
    
    existing_membership = User_membership.objects.filter(
        user=user, 
        plan=plan,
        membership_end_date__gte=now(),  # Check if membership is still active
        status=True  # Ensure it's an active membership
    ).first()

    if existing_membership:
        return JsonResponse({
            "error": "You already have an active membership for this plan."
        }, status=400)

    # Create Razorpay order
    order_amount = int(plan.annual_fees * 100)  # Convert to paisa
    order_currency = "INR"
    razorpay_order = razorpay_client.order.create({
        "amount": order_amount,
        "currency": order_currency,
        "payment_capture": "1"  # Auto capture payment
    })
    
    # Store order details in Payment model
    membership = User_membership.objects.create(
        user=user,
        plan=plan,
        membership_start_date=datetime.today(),
        membership_end_date=datetime.today() + timedelta(days=365),  # 1 year membership
        status=False
    )
    
    payment = Payment.objects.create(
        membership=membership,
        total_price=plan.annual_fees,
        payment_mode="online",
        payment_status="pending",
        razorpay_order_id=razorpay_order["id"]
    )

    return JsonResponse({
        "razorpay_order_id": razorpay_order["id"],
        "razorpay_key": settings.RAZORPAY_KEY_ID,
        "amount": order_amount,
        "plan_name": plan.plan_name,
        "plan_id": plan_id,
    })
    # return JsonResponse({"error": "Invalid request method"}, status=400)
    
    
    
@csrf_exempt
def razorpay_payment_success(request):
    if request.method == "POST":
        data = request.POST
        razorpay_payment_id = data.get("razorpay_payment_id")
        razorpay_order_id = data.get("razorpay_order_id")
        razorpay_signature = data.get("razorpay_signature")
        
        payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)
        
        # Verify Razorpay signature
        try:
            razorpay_client.utility.verify_payment_signature({
                "razorpay_order_id": razorpay_order_id,
                "razorpay_payment_id": razorpay_payment_id,
                "razorpay_signature": razorpay_signature
            })
            payment.payment_status = "completed"
            payment.razorpay_payment_id = razorpay_payment_id
            payment.razorpay_signature = razorpay_signature
            payment.save()
            
            # Activate membership
            user_membership = payment.membership
            user_membership.status = True
            user_membership.save()
            
            return JsonResponse({"status": "success", "message": "Payment successful!"})
        except razorpay.errors.SignatureVerificationError:
            payment.payment_status = "failed"
            payment.save()
            return JsonResponse({"status": "failed", "message": "Payment verification failed!"}, status=400)