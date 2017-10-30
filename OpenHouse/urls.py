"""OpenHouse URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
import rdss.views
import general.views

urlpatterns = [
	#custom sponsorship admin url and view
    url(r'', include('general.urls')),  # add '' on the include path!!!
    url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
    url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URL
    url(r'^admin/rdss/', include('rdss.admin_urls')),
    url(r'^admin/recruit/', include('recruit.admin_urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^company/', include('company.urls')),  # add '' on the include path!!!
    url(r'^company/rdss/', include('rdss.internal_urls')),  # add '' on the include path!!!
    url(r'^company/recruit/', include('recruit.internal_urls')),  # add '' on the include path!!!
    url(r'^staff/', include('staff.urls')),  # add '' on the include path!!!
    url(r'^admin/staff/', include('staff.admin_urls')),

    url(r'^rdss/', include('rdss.public_urls')),  # add '' on the include path!!!
	url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^mentor/', include('careermentor.urls')),
    url(r'^recruit/',include('recruit.public_urls')),
    url(r'^visit/',include('company_visit.urls')),
    url(r'^vote/',include('vote.urls')),
]
