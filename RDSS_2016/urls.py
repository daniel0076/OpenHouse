from django.conf.urls import url
from RDSS_2016.views import create_company

urlpatterns = [
    # Examples:
    # url(r'^$', 'oh2016_dj.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^create/',create_company ,name="create"),
]
