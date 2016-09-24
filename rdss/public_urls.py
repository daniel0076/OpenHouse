from django.conf.urls import url
import rdss.views as views
import rdss.export as export

urlpatterns = [
    # Examples:
    # url(r'^$', 'oh2016_dj.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$',views.RDSSPublicIndex,name="rdss_index"),
    url(r'^seminar$',views.SeminarPublic,name="seminar_public"),
    url(r'^jobfair$',views.JobfairPublic,name="jobfair_public"),
    url(r'^jobs$',views.ListJobs,name="rdss_jobs"),
    url(r'^querypts$',views.QueryPoints,name="rdss_querypts"),

	#export urls are defined in admin.py
]
