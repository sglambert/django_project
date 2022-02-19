from django import forms
from .models import Post, Comment


class CommentForm(forms.ModelForm):
    """
    As we do not want to create additional fields we will directly go to "class:Meta"
    """

    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'md-textarea form-control',
        'placeholder': 'comment here',
        'rows': '4',
    }))

    class Meta:
        model = Comment
        fields = ('content', )


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'tags')
