from django.shortcuts import render
from .forms import RecruitSignupForm, JobfairInfoForm
from .models import RecruitConfigs, SponsorItem
from .models import RecruitSignup
from django.core.exceptions import ObjectDoesNotExist
def recruit_signup(request):
        signup_info_exist_exist = False
        recruit_configs = RecruitConfigs.objects.all()[0]
        try:
            signup_info = RecruitSignup.objects.get(cid=request.user.cid)
            signup_info_exist = True
        except ObjectDoesNotExist:
            signup_info = None

        if request.method == 'POST':
            form = RecruitSignupForm(data=request.POST, instance=signup_info)
            if form.is_valid():
                new_form = form.save(commit=False)
                new_form.cid = request.user.cid
                new_form.save()
                signup_info_exist = True

        else:
            form = RecruitSignupForm(instance=signup_info)
        return render(request, 'signup.html', locals())

def jobfair_info(request):

    if request.POST:
        form = JobfairInfoForm(data=request.POST)
        if form.is_valid():
            new_info = form.save(commit=False)
            company = RecruitSignup.objects.get(cid=request.user.cid)
            new_info.company = company
            new_info.save()
    form = JobfairInfoForm()
    return render(request, 'jobfair_info.html', locals())

def recruit_sponsor(request):
    if request.POST:
        
        if form.is_valid():
            pass
    sponsor_items = SponsorItem.objects.all()

    return render(request, 'recruit_sponsor.html', locals())

