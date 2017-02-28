from django.conf.urls import  url
from . import views
urlpatterns = [
    url(r'^$', views.company_visit_index, name="company_visit_index"),
    url(r'^info/(?P<id>[0-9]+)/$', views.company_visit_info, name="company_visit_info"),
    url(r'^apply/(?P<id>[0-9]+)/$',views.company_visit_apply, name="company_visit_apply")
]
