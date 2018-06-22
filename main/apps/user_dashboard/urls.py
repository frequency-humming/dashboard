from django.conf.urls import url
from . import views           

urlpatterns = [
    url(r'^$', views.index),
    url(r'^signin$', views.signin),
    url(r'^register$', views.register), 
    url(r'^dashboard/admin$', views.admin),
    url(r'^login$', views.login),
    url(r'^user/create$', views.newuser),
    url(r'^users/show/(?P<id>\d+)$', views.show),
    url(r'^users/(?P<id>\d+)$', views.post),
    url(r'^users/edit/(?P<id>\d+)$', views.edit),
    url(r'^edit/(?P<id>\d+)$', views.edit_user)    
]
