from django.shortcuts import render,redirect
from django.http import  HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout

# Create your views here.

def ControlPanel(request):
	nav_rdss="active"
	return render(request,'rdss.html',locals())
