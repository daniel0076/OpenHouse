from django.shortcuts import render, redirect
from django.http import  HttpResponseRedirect, JsonResponse,Http404, HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.utils import timezone
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import datetime, json
from . import models

def Index(request):
    general_news_list = models.News.objects.filter(category="最新消息").exclude(perm="company_only")\
            .order_by("-updated_time")[:5]
    recruit_news_list = models.News.objects.filter(category="徵才專區").exclude(perm="company_only")\
            .order_by("-updated_time")[:5]

    photo_slide_list = models.PhotoSlide.objects.all().order_by('order')

    return render(request,'general/index.html',locals())


#TODO permission
def ReadNews(request,news_id):
    news = models.News.objects.filter(id = news_id).first()
    if not news:
        raise Http404("Not found")
    return render(request,'general/read_news.html',locals())

def GeneralNewsListing(request):
    general_news_list = models.News.objects.filter(category="最新消息").exclude(perm="company_only")\
            .order_by("-updated_time")
    paginator = Paginator(general_news_list, 10) # Show 10 news per page

    page = request.GET.get('page')
    try:
        general_news_page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        general_news_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        general_news_page = paginator.page(paginator.num_pages)

    return render(request, 'general/general_news_list.html', locals())

def RecruitNewsListing(request):
    recruit_news_list = models.News.objects.filter(category="徵才專區").exclude(perm="company_only")\
            .order_by("-updated_time")
    paginator = Paginator(recruit_news_list, 10) # Show 10 news per page

    page = request.GET.get('page')
    try:
        recruit_news_page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        recruit_news_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        recruit_news_page = paginator.page(paginator.num_pages)

    return render(request, 'general/recruit_news_list.html', locals())

#temporary deprecated
@login_required
def GetCompanyNewsList(request):
    news_list = models.News.objects.filter(Q(perm="both") | Q(perm="company_only"))

    ret_news_list = []
    for news in news_list:
        news_dict = {"title":news.title,"updated_time":news.updated_time,"url":"/news/"+news.id}
        ret_news_list.append(news_dict)

    return JsonResponse({'success':True,'data':ret_news_list})


