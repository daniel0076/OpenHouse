from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^signup/$', views.recruit_signup, name='signup'),
    url(r'^jobfair/info/$', views.jobfair_info, name='jobfair_info'),
    url(r'^sponsor/$', views.recruit_sponsor, name='sponsor'),
]