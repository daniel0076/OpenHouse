from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^index$',views.index,name="vote_index"),
    url(r'^$',views.vote,name="vote"),
]
