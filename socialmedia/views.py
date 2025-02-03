from django.shortcuts import render, HttpResponse, redirect,get_object_or_404
from django.conf import settings
from .models import *
from .form import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from django.http import Http404


def is_admin_user(user):
    return user.is_staff

# Create your views here.
@login_required
@user_passes_test(is_admin_user) 
def list_post(request):
    posts = Post.objects.all()
    return render(request,'admin_dashboard/post.html',{'posts':posts})

@login_required
@user_passes_test(is_admin_user)
def add_post(request):
    context={
        'model_name':'Post',
        'list':'socialmedia:post',
    }
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            # Use commit=False to modify the object before saving
            post = form.save(commit=False)
            post.user = request.user  # Assign the logged-in user to the user field
            post.save()  # Save the post
            messages.success(request, "Post added successfully!")
            return redirect('socialmedia:post')  # Redirect to the desired page

    else:
        form = PostForm()
        
    context['form']=form
    return render(request, 'admin_dashboard/add_form.html', context)




@login_required
@user_passes_test(is_admin_user)
def post_view_details(request, pk):
    
    context = {
        'model_name':'Post',
    }
    
    try:
        # Fetch the category or raise Http404 if not found
        post = get_object_or_404(Post, pk=pk)
    except Http404:
        # Render the custom 404 page
        return render(request, '404.html', status=404)

    form = PostForm(instance=post)

    if request.method == 'POST':
        if 'update' in request.POST:  # Update action
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                form.save()
                messages.success(request, "post updated successfully!")
                return redirect('socialmedia:post')
            else:
                messages.error(request, "post update failed. Please correct the errors.")
        if 'delete' in request.POST:  # Delete action
            post.delete()
            messages.success(request, "post deleted successfully!")
            return redirect('socialmedia:post')

        elif 'cancel' in request.POST:  # Cancel action
            return redirect('socialmedia:post')

    context['form'] = form
    context['post'] = post
    return render(request, 'admin_dashboard/view_details.html', context)



def post_comment_list(request):
    post_comment=PostComment.objects.all()
    return render(request,'admin_dashboard/post_comment_list.html',{'post_comment':post_comment})

def post_comment_add(request):
    
    context = {
        'model_name':'Review',
        'list':'socialmedia:post_comment_list',
    }
    
    if request.method == "POST":
        form = PostCommentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Post comment added successfully")
            return redirect('socialmedia:post_comment_list')

    else:
        form = PostCommentForm()
    
    context['form'] = form
    return render(request,'admin_dashboard/add_form.html',context)

def post_comment_view_details(request):
    pass
