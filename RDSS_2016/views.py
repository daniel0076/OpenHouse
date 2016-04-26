from django.shortcuts import render
from django.http import  HttpResponseRedirect
from django.contrib import messages
from RDSS_2016.forms import CompanyCreationForm
# Create your views here.

def create_company(request):
    if request.POST:
        form = CompanyCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
    #        messages.success(request, _("User '{0}' created.").format(user))
            return redirect('/')
    #    else:
    #        messages.error(request, _("The user could not be created due to errors.") )
    form = CompanyCreationForm();
    return render(request,'create.html',{'form':form})
