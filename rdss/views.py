from django.shortcuts import render,redirect
from django.http import  HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
import rdss.forms
import rdss.models

# Create your views here.

@login_required(login_url='/company/login/')
def ControlPanel(request):
	step=["","",""] # for step ui in template
	nav_rdss="active"
	configs=rdss.models.RdssConfigs.objects.all()[0]
	my_rdss_signup = rdss.models.Activity.objects.filter(cid=request.user.cid)
	if not my_rdss_signup:
		step[0]="active"
	return render(request,'rdss.html',locals())

@login_required(login_url='/company/login/')
def SignupActivity(request):
	configs=rdss.models.RdssConfigs.objects.all()[0]
	if request.POST:
		form = rdss.forms.ActivityCreationForm(request.POST)
		form.cid=request.user.cid
		if form.valid():
			form.save()
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
