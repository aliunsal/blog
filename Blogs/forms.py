import random
from django import forms
from django.core.urlresolvers import reverse
from Blogs.models import Comment
from django.utils import timezone
from django.contrib.auth.models import User
import task
import uuid
import hashlib


class AnonymousUserCommentForm(forms.ModelForm):

    name = forms.CharField(max_length=100)

    class Meta:
        model = Comment
        fields = ['name', 'email', 'content']

    def save(self, post):
        user = User.objects.get(email=self.cleaned_data["email"])
        if not user:
            user = User.objects.create_user(username=uuid.uuid4(), email=self.cleaned_data["email"])

        comment = Comment()
        comment.content = self.cleaned_data["content"]
        comment.author = user
        comment.date = timezone.now()
        comment.approved = False
        comment.email = user.email
        comment.content_object = post
        comment.activation_key = hashlib.sha256(user.email + str(random.random())).hexdigest()
        comment.save()

        task.mail_send.delay("Email Activation", reverse("email", args=(comment.activation_key,)), None, [comment.email])


class UserCommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['content']

    def save(self, post, user):
        comment = Comment()
        comment.content = self.cleaned_data["content"]
        comment.author = user
        comment.date = timezone.now()
        comment.approved = True
        comment.email = user.email
        comment.content_object = post
        comment.activation_key = "0"
        comment.save()