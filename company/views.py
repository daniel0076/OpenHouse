from django.shortcuts import render,redirect
from django.http import  HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from company.forms import CompanyCreationForm,CompanyEditForm,CompanyPasswordResetForm
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from .models import Company
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import SetPasswordForm
from company.forms import CompanyCreationForm,CompanyEditForm
import rdss.models
import company.models
# Create your views here.

def CompanyIndex(request):

	#semantic ui control
	nav_company_index = "active"

	# rdss files
	rdss_file_list = rdss.models.Files.objects.all()
	return render(request,'company_index.html',locals())

def CompanyInfo(request):
	company_info = company.model.Company.objects.get(cid=request.user.cid)
	return render(request,'company_info.html',locals())

def CompanyCreation(request):
	submit_btn_name = "創建帳號"
	if request.POST:
		form = CompanyCreationForm(request.POST,request.FILES)
		if form.is_valid():
			user=form.save()
	#        messages.success(request, _("User '{0}' created.").format(user))
			return redirect('/')
		else:
			print(form.errors)
			#messages.error(request, ("The user could not be created due to errors.") )
			return render(request,'company_create_form.html',locals())
	form = CompanyCreationForm();
	return render(request,'company_create_form.html',locals())

def CompanyEdit(request):
	submit_btn_name = "確認修改"
	if request.user and request.user.is_authenticated():
		user=request.user
	else: user=None
	if request.POST:
		form = CompanyEditForm(request.POST,request.FILES,instance=user)
		if form.is_valid():
			user = form.save()
	#        messages.success(request, _("User '{0}' created.").format(user))
			return redirect('/company/')
		else:
			print(form.errors)
			#messages.error(request, ("The user could not be created due to errors.") )
			return render(request,'company_regform.html',locals())
	form = CompanyEditForm(instance=user);
	company_info = company.model.Company.objects.get(cid=request.user.cid)
	return render(request,'company_regform.html',locals())

def CompanyLogin(request):

	if request.POST:
		username=request.POST.get('username')
		password=request.POST.get('password')
		try:
			company_obj = company.models.Company.objects.get(cid=username)
		except:
			error_display = True
			error_msg = "系統查無貴公司統編，請重新註冊"
			return render(request,'login.html',locals())

		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request,user)
			if user.is_staff:
				return redirect('/admin/')
			else:
				return redirect('/company/')
		else:
			error_display = True
			error_msg = "帳號或密碼錯誤"

	return render(request,'login.html',locals())

def CompanyLogout(request):
	logout(request)
	return redirect('/company/login/')


def forget_password(request):
    send = None
    if request.method == 'POST':
        form = CompanyPasswordResetForm(request.POST)
        if form.is_valid():
            form.save(request=request)
    else:
        form = CompanyPasswordResetForm()
    return render(request,'forget_password.html',{'form':form,'send':send})

def password_reset_confirm(request,uidb64,token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Company.objects.get(pk=uid)
    except(TypeError):
        user = None
    if user is not None and default_token_generator.check_token(user,token):
        validlink = True
        if request.method == 'POST':
            form = SetPasswordForm(user,request.POST)
            if form.is_valid():
                form.save()
                return redirect('/company/login/')
        else:
            form = SetPasswordForm(user)
            return render(request,'password_reset_confirm.html',{'form': form})
    else:
        validlink = False
    return redirect('/')
