from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey, GenericRelation


class Comment(models.Model):
    content = models.TextField(null=False)
    date = models.DateTimeField()
    author = models.ForeignKey(User, default=0)
    approved = models.BooleanField(default=False)
    activation_key = models.TextField(max_length=150)
    email = models.EmailField(null=False)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    comment = GenericRelation("Comment")

    def __unicode__(self):
        return self.content


class Post(models.Model):
    title = models.CharField(max_length=300)
    content = models.TextField(null=True)
    date = models.DateTimeField(auto_now_add=True)
    picture = models.ImageField(upload_to='static/img/post_image/',
                                null=True)
    author = models.ForeignKey(User)
    comment = GenericRelation(Comment)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ["-id"]