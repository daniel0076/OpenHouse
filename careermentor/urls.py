from django.conf.urls import url
from . import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'oh2016_dj.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$',views.CareerMentorIndex,name="mentor_index"),
    url(r'^signup/(?P<event_id>[0-9].*)/$', views.CareerMentorSignup, name="mentor_signup"),
    url(r'^info/(?P<event_id>[0-9].*)/$', views.event_info, name="event_info"),

]
