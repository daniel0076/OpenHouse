from django.conf.urls import url
import rdss.views as views

urlpatterns = [
    # Examples:
    # url(r'^$', 'oh2016_dj.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^',views.ControlPanel,name="index"),
]
