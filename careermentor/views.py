from django.shortcuts import render
from . import forms
from . import models

# Create your views here.
def CareerMentorIndex(request):
    mentor_events = models.Mentor.objects.filter(category="職場導師")
    career_events = models.Mentor.objects.filter(category="職涯教練")
    return render(request,'mentor_index.html',locals())

def CareerMentorSignup(request, event_id):
    init_data={'mentor': event_id}
    form = forms.SignupForm(initial=init_data)
    if request.method =="POST":
        data = request.POST.copy()
        form = forms.SignupForm(data=data)
        if form.is_valid():
            form.save()
            ui_message = {"type":"green", "msg":"報名成功"}
            return render(request,'mentor_signup_success.html',locals())

        else:
            print(form.errors)
            ui_message = {"type":"error", "msg":"報名失敗"}

    return render(request,'mentor_signup.html',locals())
