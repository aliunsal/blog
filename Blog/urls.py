from django.conf.urls import patterns, include, url, handler400, handler500
import settings
from django.contrib import admin
from Blogs.views import handler_404, handler_500

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'Blogs.views.index', name='index'),
    url(r'^(?P<page_index>[0-9]+)/', 'Blogs.views.index', name='index_pager'),
    url(r'^blog/', include('Blogs.urls')),
    url(r'^user/', include('Users.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^email_activation/(?P<key>.*)', 'Blogs.views.email_activation', name="email_activation"),
    url(r'^user_activation/(?P<key>.*)', 'Users.views.user_activation', name="user_activation"),
    url(r'subcomment/(?P<comment_id>[0-9]+)/$', 'Blogs.views.sub_comment_add', name='sub_comment_add'),

)

if settings.DEBUG is False:
    urlpatterns += patterns('',
            url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
            )


handler500 = handler_500
handler404 = handler_404