from django.shortcuts import render,redirect
from django.http import  HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='/company/login/')
def ControlPanel(request):
	nav_rdss="active"
	return render(request,'rdss.html',locals())
