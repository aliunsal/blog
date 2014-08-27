import hashlib
import random
from time import timezone
import uuid
from django.core.exceptions import ValidationError
from django.forms.widgets import PasswordInput
import task
from django.template.loader import render_to_string
from django import forms
from django.contrib.auth.models import User
from Users.models import UserProfile as usp


class UserRegister(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    password1 = forms.CharField(widget=PasswordInput)
    password2 = forms.CharField(widget=PasswordInput)

    def clean_email(self):
        email = self.cleaned_data["email"]
        if email and User.objects.filter(email=email).count():
            self.fields['email'].error_messages["u_error"] = "Email addresses must be unique."
            raise forms.ValidationError(self.fields['email'].error_messages["u_error"])
        return email

    def clean_password(self):
        p1 = self.cleaned_data["password1"]
        p2 = self.cleaned_data["password2"]
        if p1 != p2:
            self.fields['password1'].error_messages["p_error"] = "Passwords do not match."
            raise forms.ValidationError(self.fields['password1'].error_messages["p_error"])
        return p1

    def save(self, commit=True):
        user = User.objects.create_user(username=uuid.uuid4(),
                                        email=self.clean_email(),
                                        password=self.clean_password(),
                                        )
        user.is_active = False
        user.save()

        user_profile = usp()
        user_profile.user = user
        user_profile.activation_key = hashlib.sha256(user.email + str(random.random())).hexdigest()

        user_profile.save()


        content = render_to_string("Email/user_activation.html", {"activation_key": user_profile.activation_key})
        task.mail_send.delay("Email Activation", content, None, [user.email])


class UserProfile(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    avatar = forms.ImageField(required=False)
    email = forms.EmailField()




class UserPost(forms.Form):
    title = forms.CharField(max_length=250)
    content = forms.CharField(widget=forms.Textarea)
    picture = forms.ImageField(required=False)

