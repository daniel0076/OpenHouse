from django.shortcuts import render,redirect
from django.http import  HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
import rdss.forms

# Create your views here.

@login_required(login_url='/company/login/')
def ControlPanel(request):
	nav_rdss="active"
	return render(request,'rdss.html',locals())

@login_required(login_url='/company/login/')
def SignupActivity(request):
	form = rdss.forms.ActivityCreationForm
	return render(request,'activity_form.html',locals())

@login_required(login_url='/company/login/')
def SeminarInfo(request):
	form = rdss.forms.SeminarInfoCreationForm
	return render(request,'seminar_info_form.html',locals())

@login_required(login_url='/company/login/')
def JobfairInfo(request):
	form = rdss.forms.JobfairInfoCreationForm
	return render(request,'jobfair_info_form.html',locals())
