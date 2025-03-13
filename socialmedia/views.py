from django.shortcuts import render, HttpResponse, redirect,get_object_or_404
from django.conf import settings
from django.db.models import Count
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from django.http import Http404
from django.core.paginator import Paginator


def is_admin_user(user):
    return user.is_staff

# Create your views here.
@login_required
@user_passes_test(is_admin_user) 
def list_post(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 10)  # Show 10 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin_dashboard/post.html', {'page_obj': page_obj})


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
    paginator = Paginator(post_comment, 10)  # Show 10 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin_dashboard/post_comment_list.html', {'page_obj': page_obj})


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

def post_comment_view_details(request, pk):
    context = {
        'model_name':'PostComment',
    }
    
    try:
        # Fetch the category or raise Http404 if not found
        postcomment = get_object_or_404(Post, pk=pk)
    except Http404:
        # Render the custom 404 page
        return render(request, '404.html', status=404)

    form = PostForm(instance=postcomment)

    if request.method == 'POST':
        if 'update' in request.POST:  # Update action
            form = PostCommentForm(request.POST, instance=postcomment)
            if form.is_valid():
                form.save()
                messages.success(request, "comment updated successfully!")
                return redirect('socialmedia:post_comment_list')
            else:
                messages.error(request, "comment update failed. Please correct the errors.")
        if 'delete' in request.POST:  # Delete action
            postcomment.delete()
            messages.success(request, "Comment deleted successfully!")
            return redirect('socialmedia:post_comment_list')

        elif 'cancel' in request.POST:  # Cancel action
            return redirect('socialmedia:post_comment_list')

    context['form'] = form
    context['postcomment'] = postcomment
    return render(request, 'admin_dashboard/view_details.html', context)



def my_feed(request):
    
    # posts = Post.objects.all().order_by('-created_at')
    comment_form = PostCommentForm()
    posts = Post.objects.annotate(comments_count=Count('comments'))
    show_comments = request.GET.get("show_comments", None)
    
    return render(request, "Ecommerce/my_feed.html", {"posts": posts,"comment_form": comment_form, "show_comments": show_comments})

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, post_id=post_id)
    if request.method == "POST":
        comment_text = request.POST.get("comment_text")
        parent_comment_id = request.POST.get("parent_comment_id")  # Get parent comment ID (if replying)

        if comment_text:
            parent_comment = None
            if parent_comment_id:
                parent_comment = get_object_or_404(PostComment, comment_id=parent_comment_id)

            PostComment.objects.create(
                user=request.user,
                post=post,
                comment_text=comment_text,
                parent_comment=parent_comment
            )

        return redirect("socialmedia:my_feed")  # Redirect back to post page

    return redirect("Ecommerce:homepage")

@login_required
def create_post(request):
    
    form = PostForm()
    
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit = False)
            new_post.user = request.user
            new_post.save()
            return redirect('socialmedia:my_feed')
        else:
            form = PostForm()
            
    return render(request,"Ecommerce/create_post.html",{"form":form})



@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, post_id=post_id)

    # Increase like count
    post.likes += 1
    post.save()

    # Redirect back to the feed (or previous page)
    return redirect(request.META.get('HTTP_REFERER', 'socialmedia:my_feed'))

@login_required
def create_post(request):
    if request.method == "POST":
        image = request.FILES.get("image")
        caption = request.POST.get("caption")

        if image and caption:  # Ensure both fields are filled
            post = Post.objects.create(
                user=request.user,  # Assign the logged-in user
                image=image,
                caption=caption
            )
            return redirect("socialmedia:my_feed")  # Redirect to the feed after posting

    return redirect("socialmedia:my_feed")  # Redirect if the form is invalid

@login_required
def user_feed(request):
    user_posts = Post.objects.filter(user=request.user).order_by("-created_at")  # Get only the logged-in user's posts
    return render(request, "Ecommerce/user_feed.html", {"posts": user_posts})