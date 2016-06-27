from django.conf.urls import url
import rdss.views as views

urlpatterns = [
    # Examples:
    # url(r'^$', 'oh2016_dj.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$',views.ControlPanel,name="rdss_index"),
    url(r'^signup/$',views.SignupActivity,name="rdss_signup"),
    url(r'^seminar/info$',views.SeminarInfo,name="rdss_seminar_info"),
    url(r'^seminar/select$',views.SeminarSelect,name="rdss_seminar_select"),
    url(r'^jobfair/info$',views.JobfairInfo,name="rdss_jobfair_info"),
]
