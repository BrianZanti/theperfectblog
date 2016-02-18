from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
import blog.views as views

urlpatterns = [
    # Examples:
    # url(r'^$', 'ThePerfectBlog.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.home),
    url(r'^accounts/login/$', auth_views.login),
    url(r'^accounts/create/$', views.createuser),
    url(r'^(\d+)$', views.viewpost),
    url(r'^new$', views.new),
    url(r'^account$', views.account),
    url(r'^accounts/delete', views.delete),
]
