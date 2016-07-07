from django.shortcuts import render
import staff.forms

# Create your views here.

def StaffCreation(request):
	form = staff.forms.StaffCreationForm
	return render(request,'staff_form.html',{'form':form})
