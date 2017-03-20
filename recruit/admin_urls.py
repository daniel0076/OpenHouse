from django.conf.urls import url
import recruit.views as views
import recruit.export as export

urlpatterns = [
    # Examples:
    # url(r'^$', 'oh2016_dj.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^sponsorship/$', views.SponsorAdmin),
    url(r'^export_activity_info/$', export.ExportActivityInfo, name="recruit_export_activity_info"),
    url(r'^export_all/$', export.ExportAll, name="recruit_export_all"),
    url(r'^export_ad/$', export.ExportAdFormat,name="recruit_export_ad"),
    url(r'^export_seminar_info/$',export.export_seminar_info,name="recruit_export_seminar_info"),
    url(r'^export_jobfair_info/$',export.export_jobfair_info,name="recruit_export_jobfair_info"),
    url(r'^reg_card/$',views.reg_card,name='reg_card'),
    url(r'^collect_points/$',views.collect_points,name='collect_points'),
    url(r'^exchange_prize/$',views.exchange_prize,name='exchange_prize'),
    #export urls are defined in admin.py
]
