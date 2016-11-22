from django.shortcuts import render
from django.db.models import Count, Sum
from . import forms
from . import models

def get_event_status(events):
    for event in events:
        event.full = False
        if event.signup_num < event.limit:
            event.status = "Available：{}人".format(event.limit - event.signup_num)
        elif event.signup_num >= 2*event.limit:
            event.status = "已額滿(Full)"
            event.full = True
        elif event.signup_num > event.limit:
            event.status = "尚可候補：{}人".format(event.limit*2 - event.signup_num)

# Create your views here.
def CareerMentorIndex(request):
    mentor_events = models.Mentor.objects.filter(category="職場導師").order_by('-date')\
        .annotate(signup_num = Count('signup'))
    career_events = models.Mentor.objects.filter(category="職涯教練").order_by('-date')\
        .annotate(signup_num = Count('signup'))

    get_event_status(mentor_events)
    get_event_status(career_events)


    return render(request,'mentor/mentor_index.html',locals())

def CareerMentorSignup(request, event_id):
    try:
        event = models.Mentor.objects.filter(id=event_id).annotate(signup_num = Count('signup')).first()
        if event.signup_num >= 2*event.limit:
            return render(request,'mentor/error.html')
    except:
        return render(request,'mentor/error.html')



    init_data={'mentor': event_id}
    form = forms.SignupForm(initial=init_data)
    if request.method =="POST":
        data = request.POST.copy()
        form = forms.SignupForm(data,request.FILES)
        if form.is_valid():
            form.save()
            return render(request,'mentor/mentor_signup_success.html',locals())

        else:
            print(form.errors)

    return render(request,'mentor/mentor_signup.html',locals())
