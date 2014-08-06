from django.conf.urls import patterns, url

from Blogs import views

urlpatterns = patterns('',

    url(r'^$', views.index, name='index'),
    url(r'^(?P<post_id>[0-9])/$', views.post, name='post'),

)