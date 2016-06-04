from django.shortcuts import render,redirect
from django.http import  HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from company.forms import CompanyCreationForm,CompanyEditForm
from company import models as company_model
# Create your views here.

def ControlPanel(request):
	nav_index="active"
	return render(request,'index.html',locals())

def CompanyInfo(request):
	company_info = company_model.Company.objects.get(cid=request.user.cid)
	return render(request,'company_info.html',locals())



def CompanyCreation(request):
	if request.POST:
		form = CompanyCreationForm(request.POST,request.FILES)
		if form.is_valid():
			user=form.save()
	#        messages.success(request, _("User '{0}' created.").format(user))
			return redirect('/')
		else:
			print(form.errors)
			#messages.error(request, ("The user could not be created due to errors.") )
			return render(request,'company/form.html',{'form':form})
	form = CompanyCreationForm();
	return render(request,'form.html',{'form':form})

def CompanyEdit(request):
	submit_btn_name = "確認修改"
	if request.user and request.user.is_authenticated():
		user=request.user
	else: user=None
	if request.POST:
		company_form = CompanyEditForm(request.POST,request.FILES,instance=user)
		if company_form.is_valid():
			user = company_form.save()
	#        messages.success(request, _("User '{0}' created.").format(user))
			return redirect('/company/')
		else:
			print(company_form.errors)
			#messages.error(request, ("The user could not be created due to errors.") )
			return render(request,'form.html',locals())
	company_form = CompanyEditForm(instance=user);
	company_info = company_model.Company.objects.get(cid=request.user.cid)
	return render(request,'form.html',locals())

def CompanyLogin(request):

	if request.POST:
		username=request.POST.get('username')
		password=request.POST.get('password')
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request,user)
				return redirect('/company/')

	return render(request,'login.html',locals())

def CompanyLogout(request):
	logout(request)
	return redirect('/company/login/')
