from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


class Comment(models.Model):
    content = models.TextField(null=False)
    date = models.DateTimeField()
    author = models.ForeignKey(User, default=0)
    approved = models.BooleanField(default=False)
    activation_key = models.TextField(max_length=150)
    email = models.EmailField(null=False)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        return self.content


class Post(models.Model):
    title = models.TextField()
    content = models.TextField(null=True)
    date = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    picture = models.ImageField(upload_to='static/img/post_image/',
                                default="static/img/post_image/",
                                null=True)
    status = models.TextField(max_length=20, default="published")
    comment_status = models.BooleanField(default=True)
    author = models.ForeignKey(User)
    comment = generic.GenericRelation(Comment)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ["-id"]