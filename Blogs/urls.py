from django.conf.urls import patterns, url
from Blogs import views

urlpatterns = patterns('',
    url(r'(?P<post_id>[0-9]+)/$', views.post, name='single_post'),
)