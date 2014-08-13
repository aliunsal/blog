from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'Blogs.views.index', name='index'),
    url(r'^blog/', include('Blogs.urls')),
    url(r'^user/', include('Users.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
