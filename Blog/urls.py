from django.conf.urls import patterns, include, url
import settings
from django.contrib import admin
from django.conf.urls.static import static
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'Blogs.views.index', name='index'),
    url(r'^(?P<page_index>[0-9]+)/', 'Blogs.views.index', name='index_pager'),
    url(r'^blog/', include('Blogs.urls')),
    url(r'^user/', include('Users.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
