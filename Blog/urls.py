from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Blogs.views.home', name='home'),
    #url(r'^blog/', include('Blogs.urls')),
    url(r'^$', include('Blogs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
