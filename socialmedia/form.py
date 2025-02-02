from django import forms
from .models import *

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'caption', 'likes']

        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'caption': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write a caption...'}),
            'likes': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }
        

# class PostCommentForm(forms.ModelForm):
#     class Meta:
#         model = PostComment
#         fields = ['comment_text', 'parent_comment']

#         widgets = {
#             'comment_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Write a comment...'}),
#             'parent_comment': forms.HiddenInput(),  # Hidden field for nested comments
#         }

class PostCommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = ['comment_text']  # Do NOT include 'post' as input field

    def __init__(self, *args, **kwargs):
        super(PostCommentForm, self).__init__(*args, **kwargs)
        self.fields['comment_text'].widget.attrs.update({'class': 'form-control'})


