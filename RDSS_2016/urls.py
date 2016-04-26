from django.conf.urls import url
import RDSS_2016.views as views

urlpatterns = [
    # Examples:
    # url(r'^$', 'oh2016_dj.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^create/',views.CompanyCreation,name="create"),
]
