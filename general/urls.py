from django.conf.urls import url
import general.views as views

urlpatterns = [
    # Examples:
    # url(r'^blog/', include('blog.urls')),
     url(r'^$', views.Index, name='index'),
     url(r'^news/(?P<news_id>[0-9].*)/$', views.ReadNews),
     url(r'^general_news/$', views.GeneralNewsListing, name = 'general_news_list'),
     url(r'^recruit_news/$', views.RecruitNewsListing, name = 'recruit_news_list'),

	#export urls are defined in admin.py
]
