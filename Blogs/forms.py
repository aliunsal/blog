from django import forms
from Blogs.models import Comment


class AnonymousUserCommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['email', 'content']


class UserCommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['content']