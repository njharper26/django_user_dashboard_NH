from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.login),
    url(r'^process/login$', views.process_login),
    url(r'^register', views.register),
    url(r'^process/register$', views.process_register),
    url(r'^logout$', views.logout),
    url(r'^dashboard/(?P<user_level>\w+)$', views.dashboard),
    url(r'^users/new$', views.add),
    url(r'^process/new$', views.process_add),
    url(r'^users/edit/info/(?P<id>\d+)$', views.edit_info),
    url(r'^process/edit/info/(?P<id>\d+)$', views.process_edit_info),    
    url(r'^process/remove/(?P<id>\d+)$', views.process_remove),
    url(r'^users/edit/profile/(?P<id>\d+)$', views.edit_profile),    
    url(r'^process/edit/profile/(?P<id>\d+)$', views.process_edit_profile),
    url(r'^users/show/profile/(?P<id>\d+)$', views.show),
    url(r'^process/message/(?P<id>\d+)$', views.process_message),
    url(r'^process/comment/(?P<id>\d+)$', views.process_comment)
]