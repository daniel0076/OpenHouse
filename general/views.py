from django.shortcuts import render,redirect
from django.http import  HttpResponseRedirect, JsonResponse,Http404,HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.utils import timezone
from django.db.models import Q
import datetime,json
from . import models

def Index(request):
	general_news_list = models.News.objects.filter(category="最新消息").exclude(perm="company_only").order_by("-updated_time")
	recruit_news_list = models.News.objects.filter(category="徵才專區").exclude(perm="company_only")
	return render(request,'general/index.html',locals())

#TODO permission
def ReadNews(request,news_id):
	news = models.News.objects.filter(id = news_id).first()
	if not news:
		raise Http404("Not found")
	return render(request,'general/read_news.html',locals())

@login_required
def GetCompanyNewsList(request):
	news_list = models.News.objects.filter(Q(perm="both") | Q(perm="company_only"))

	ret_news_list = []
	for news in news_list:
		news_dict = {"title":news.title,"updated_time":news.updated_time,"url":"/news/"+news.id}
		ret_news_list.append(news_dict)

	return JsonResponse({'success':True,'data':ret_news_list})


