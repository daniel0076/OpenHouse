from django.conf.urls import url
import staff.views as views
import staff.export as export

urlpatterns = [
    # Examples:
    # url(r'^$', 'oh2016_dj.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^create/$',views.StaffCreation,name="staff_create"),
]
