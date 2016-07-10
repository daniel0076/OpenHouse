from django.shortcuts import render,redirect
import staff.forms

# Create your views here.

def StaffCreation(request):
	if request.POST:
		form = staff.forms.StaffCreationForm(request.POST,request.FILES)
		if form.is_valid():
			user=form.save()
			return redirect('/admin/')
		else:
			print(form.errors)
			#messages.error(request, ("The user could not be created due to errors.") )
			return render(request,'staff_form.html',{'form':form})

	form = staff.forms.StaffCreationForm
	return render(request,'staff_form.html',{'form':form})
