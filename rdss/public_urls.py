from django.conf.urls import url
import rdss.views as views
import rdss.export as export

urlpatterns = [
    # Examples:
    # url(r'^$', 'oh2016_dj.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$',views.RDSSIndex,name="rdss_index"),

	#export urls are defined in admin.py
]
