from django.shortcuts import render,redirect
from django.http import  HttpResponseRedirect, JsonResponse,Http404,HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.utils import timezone
import datetime,json
from . import models

def Index(request):
	general_news_list = models.News.objects.filter(category="最新消息")
	company_news_list = models.News.objects.filter(category="廠商專區")
	return render(request,'general/index.html',locals())

def ReadNews(request,news_id):
	news = models.News.objects.filter(id = news_id).first()
	if not news:
		raise Http404("Not found")
	return render(request,'general/read_news.html',locals())

