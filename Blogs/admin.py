from django.contrib import admin
from Blogs.models import(Post, Comment)

admin.site.register(Post)
admin.site.register(Comment)