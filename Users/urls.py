from django.conf.urls import url, patterns
from Users import views

urlpatterns = patterns('Users',
    url(r'^$', views.index, name="user_index"),
    url(r'^login/', views.UserLogin, name='user_login'),
    url(r'^logout/', views.UserLogout, name='user_logout'),
)