from django.conf.urls import url
import recruit.views as views

urlpatterns = [
    # Examples:
    # url(r'^$', 'oh2016_dj.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^sponsorship/$', views.SponsorAdmin),

	#export urls are defined in admin.py
]
