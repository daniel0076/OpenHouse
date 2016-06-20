from django.conf.urls import url
import rdss.views as views

urlpatterns = [
    # Examples:
    # url(r'^$', 'oh2016_dj.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$',views.ControlPanel,name="rdss_index"),
    url(r'^signup/$',views.SignupActivity,name="rdss_act_signup"),
    url(r'^seminar/$',views.SeminarInfo,name="rdss_seminar"),
    url(r'^jobfair/$',views.JobfairInfo,name="rdss_jobfair"),
]
