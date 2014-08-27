from django.conf.urls import url, patterns
from Users import views



urlpatterns = patterns('Users',
    url(r'^$', views.index, name="user_index"),
    url(r'^login/', views.user_login, name='user_login'),
    url(r'^logout/', views.user_logout, name='user_logout'),
    url(r'^posts/remove/(?P<post_id>[0-9]+)', views.user_post_remove, name='user_post_remove'),
    url(r'^posts/(?P<post_id>[0-9]+)', views.user_post_edit, name='user_post_edit'),
    url(r'^posts/add', views.user_post_add, name='user_post_add'),
    url(r'^posts/', views.user_post_list, name='user_post_list'),
    url(r'^profile/', views.user_profile, name='user_profile'),
    url(r'^register/', views.register, name='user_register'),
)