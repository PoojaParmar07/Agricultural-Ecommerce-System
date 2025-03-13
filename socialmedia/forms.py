from django import forms
from .models import *

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields =['user','image', 'caption']

        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'caption': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write a caption...'}),
            'likes': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }
        

class PostCommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = '__all__'

        widgets = {
            'comment_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Write a comment...'}),
            'parent_comment': forms.Select(),  # Hidden field for nested comments
        }

