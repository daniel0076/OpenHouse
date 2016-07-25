from django.conf.urls import url
import company.views as views

urlpatterns = [
    # Examples:
    # url(r'^$', 'oh2016_dj.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$',views.CompanyIndex,name="company_index"),
    url(r'^create/$',views.CompanyCreation,name="company_create"),
    url(r'^edit/$',views.CompanyEdit,name="company_edit"),
    url(r'^login/$',views.CompanyLogin,name="login"),
    url(r'^logout/$',views.CompanyLogout,name="logout"),
    url(r'^info/$',views.CompanyInfo,name="info"),
]
