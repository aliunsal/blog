from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField(upload_to="static/img/user_avatar/",
                               default="static/img/user_avatar/user.png",
                               null=True)
    activation_key = models.TextField(max_length=150, null=True)
    key_expiration_date = models.DateTimeField(auto_now_add=True, null=True)