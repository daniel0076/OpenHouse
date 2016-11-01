from django.shortcuts import render
from .forms import RecruitSignupForm, JobfairInfoForm
from .models import RecruitConfigs, SponsorItem, Files
from .models import RecruitSignup, SponsorShip, CompanySurvey
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from . import forms

@login_required(login_url='/company/login/')
def recruit_company_index(request):
    sidebar_ui = {'index': 'active'}
    configs=RecruitConfigs.objects.all()[0]
    plan_file = Files.objects.filter(category = "企畫書").first()
    return render(request,'recruit/company/index.html',locals())

@login_required(login_url='/company/login/')
def recruit_signup(request):
        signup_info_exist_exist = False
        recruit_configs = RecruitConfigs.objects.all()[0]
        try:
            signup_info = RecruitSignup.objects.get(cid=request.user.cid)
            signup_info_exist = True
        except ObjectDoesNotExist:
            signup_info = None

        if request.method == 'POST':
            for i in request.POST:
                print(i)
            form = RecruitSignupForm(data=request.POST, instance=signup_info)
            if form.is_valid():
                new_form = form.save(commit=False)
                new_form.cid = request.user.cid
                new_form.save()
                signup_info_exist = True

        else:
            form = RecruitSignupForm(instance=signup_info)
        return render(request, 'recruit/company/signup.html', locals())

def jobfair_info(request):

    if request.POST:
        form = JobfairInfoForm(data=request.POST)
        if form.is_valid():
            new_info = form.save(commit=False)
            company = RecruitSignup.objects.get(cid=request.user.cid)
            new_info.company = company
            new_info.save()
    form = JobfairInfoForm()
    return render(request, 'recruit/company/jobfair_info.html', locals())

def recruit_sponsor(request):
    if request.POST:
        cid = RecruitSignup.objects.get(cid=request.user.cid)
        add_sponsorship(request.POST, cid)
    sponsor_items = SponsorItem.objects.all()

    return render(request, 'recruit/company/sponsor.html', locals())


def add_sponsorship(items, cid):
    for item in items:
        try:
            sponsor_item = SponsorItem.objects.get(name=item)
            #print(sponsor_item.name)
            sponsor_ship = SponsorShip(sponsor_item=sponsor_item, company=cid)
            sponsor_ship.save()
        except ObjectDoesNotExist:
            continue

@login_required(login_url='/company/login/')
def company_servey(request):
    #semantic ui
    sidebar_ui = {'survey':"active"}
    configs = RecruitConfigs.objects.all()[0]

    if timezone.now() > configs.survey_end or timezone.now() < configs.survey_start :
        error_msg="問卷填答已結束。期間為 {} 至 {}".format(
                timezone.localtime(configs.survey_start).strftime("%Y/%m/%d %H:%M:%S"),
                timezone.localtime(configs.survey_end).strftime("%Y/%m/%d %H:%M:%S"))
        return render(request,'recruit/error.html',locals())

    try:
        my_survey = CompanySurvey.objects.get(cid=request.user.cid)
    except ObjectDoesNotExist:
        my_survey = None
    if request.POST:
        data = request.POST.copy()
        # decide cid in the form
        data['cid']=request.user.cid
        form = forms.SurveyForm(data=data, instance = my_survey)
        if form.is_valid():
            form.save()
            (msg_display,msg_type,msg_content) = (True,"green","問卷填寫完成，感謝您")
        else:
            (msg_display,msg_type,msg_content) = (True,"error","儲存失敗，有未完成欄位")
            print(form.errors)
    else:
        form = forms.SurveyForm(instance=my_survey)

    return render(request,'recruit/company/survey_form.html',locals())


