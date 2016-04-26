from django.shortcuts import render,redirect
from django.http import  HttpResponseRedirect
from django.contrib import messages
from RDSS_2016.forms import CompanyCreationForm
# Create your views here.

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
			return render(request,'company/create.html',{'form':form})
	form = CompanyCreationForm();
	return render(request,'company/create.html',{'form':form})
