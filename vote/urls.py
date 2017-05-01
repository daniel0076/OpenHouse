from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$',views.index,name="vote_index"),
    url(r'^vote$',views.vote,name="vote"),
]
