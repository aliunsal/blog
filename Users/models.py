from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField(upload_to="/img/user_avatar/", null=True)
    activation_key = models.TextField(null=True)
    key_expiration_date = models.DateTimeField(null=True)