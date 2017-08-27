from django.conf.urls import url
import rdss.views as views
import rdss.export as export

urlpatterns = [
    # Examples:
    # url(r'^$', 'oh2016_dj.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^sponsorship/$', views.SponsorAdmin),
    url(r'^collect_points/$', views.CollectPoints, name="rdss_collect_points"),
    url(r'^reg_card/$', views.RegisterCard, name="rdss_reg_card"),
    url(r'redeem/$', views.RedeemPrize, name='rdss_redeem'),
    url(r'^export_activity_info/$', export.ExportActivityInfo, name="rdss_export_activity_info"),
    url(r'^export_all/$', export.ExportAll, name="rdss_export_all"),
    url(r'^export_ad/$', export.ExportAdFormat,name="rdss_export_ad"),
    url(r'^export_jobfair/$', export.ExportJobfair,name="rdss_export_jobfair"),
    url(r'^export_seminar/$', export.ExportSeminar,name="rdss_export_seminar"),

	#export urls are defined in admin.py
]
