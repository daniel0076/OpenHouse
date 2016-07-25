from django.conf.urls import url
import rdss.views as views
import rdss.export as export

urlpatterns = [
    # Examples:
    # url(r'^$', 'oh2016_dj.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$',views.RDSSCompanyIndex,name="rdss_company_index"),
    url(r'^status$',views.ControlPanel,name="rdss_status"),
    url(r'^signup/$',views.SignupRdss,name="rdss_signup"),
    #url(r'^seminar/$',views.SeminarPublic,name="rdss_seminar_public"),
    url(r'^seminar/info$',views.SeminarInfo,name="rdss_seminar_info"),
    url(r'^seminar/select$',views.SeminarSelectFormGen,name="rdss_seminar_select"),
    url(r'^seminar/select_ctrl$',views.SeminarSelectControl,name="rdss_seminar_select_control"),
    url(r'^sponsor$',views.Sponsor,name="rdss_sponsor"),
    #url(r'^jobfair/$',views.JobfairPublic,name="rdss_jobfair_public"),
    url(r'^jobfair/info$',views.JobfairInfo,name="rdss_jobfair_info"),
    url(r'^jobfair/select$',views.JobfairSelectFormGen,name="rdss_jobfair_select"),
    url(r'^jobfair/select_ctrl$',views.JobfairSelectControl,name="rdss_jobfair_select_control"),
	#export urls are defined in admin.py
]
