from django.core import urlresolvers
from django.shortcuts import render,redirect
from .forms import RecruitSignupForm, JobfairInfoForm
from .models import RecruitConfigs, SponsorItem, Files
from .models import RecruitSignup, SponsorShip, CompanySurvey
from .models import SlotColor, SeminarOrder
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from . import forms
from django.db.models import Count
import datetime

@login_required(login_url='/company/login/')
def recruit_company_index(request):
    sidebar_ui = {'index': 'active'}
    configs=RecruitConfigs.objects.all()[0]
    plan_file = Files.objects.filter(category = "企畫書").first()
    return render(request,'recruit/company/index.html',locals())

@login_required(login_url='/company/login/')
def recruit_signup(request):
        configs = RecruitConfigs.objects.all()[0]
        if timezone.now() < configs.recruit_signup_start or timezone.now() > configs.recruit_signup_end:
            error_msg = "非報名時間。期間為 {} 至 {}".format(
            timezone.localtime(configs.recruit_signup_start).strftime("%Y/%m/%d %H:%M:%S"),
            timezone.localtime(configs.recruit_signup_end).strftime("%Y/%m/%d %H:%M:%S"))
            return render(request, 'recruit/error.html', locals())
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
                return render(request, 'recruit/company/signup_success.html', locals())

        else:
            form = RecruitSignupForm(instance=signup_info)
        return render(request, 'recruit/company/signup.html', locals())

@login_required(login_url='/company/login/')
def seminar_select_form_gen(request):
    #semanti ui control
    sidebar_ui = {'seminar_select':"active"}

    mycid = request.user.cid
    # check the company have signup rdss
    try:
        my_signup = RecruitSignup.objects.get(cid=request.user.cid)
        # check the company have signup seminar
        if my_signup.seminar == "":
            error_msg="貴公司已報名本次研替活動，但並末勾選參加說明會選項。"
            return render(request,'error.html',locals())
    except Exception as e:
        error_msg="貴公司尚未報名本次「研發替代役」活動，請於左方點選「填寫報名資料」"
        return render(request,'error.html',locals())

    #check the company have been assigned a slot select order and time
    try:
        seminar_select_time = SeminarOrder.objects.filter(company=mycid).first().time
    except Exception as e:
        seminar_select_time = "選位時間及順序尚未排定，您可以先參考下方說明會時間表"

    seminar_session = my_signup.get_seminar_display()

    configs=RecruitConfigs.objects.all()[0]
    seminar_start_date = configs.seminar_start_date
    seminar_end_date = configs.seminar_end_date
    seminar_days = (seminar_end_date - seminar_start_date).days
    table_start_date = seminar_start_date
    # find the nearest Monday
    while(table_start_date.weekday() != 0 ):
        table_start_date -= datetime.timedelta(days=1)
    # make the length to 5 multiples
    table_days = seminar_days + (seminar_days % 7) + 7
    dates_in_week = list()
    for week in range(0, int(table_days/7)):
        # separate into 5 in each list (there are 5 days in a week)
        dates_in_week.append( [(table_start_date + datetime.timedelta(days=day+week*7))\
                for day in range(0,5)])

    slot_colors = SlotColor.objects.all()
    session_list = [
        {"name":"noon", "start_time":configs.session_1_start, "end_time":configs.session_1_end},
        {"name":"night1", "start_time":configs.session_2_start, "end_time":configs.session_2_end},
        {"name":"night2", "start_time":configs.session_3_start, "end_time":configs.session_3_end},
        {"name":"night3", "start_time":configs.session_4_start, "end_time":configs.session_4_end},
    ]
    return render(request,'recruit/company/seminar_select.html',locals())

@login_required(login_url='/company/login/')
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

def Add_SponsorShip(sponsor_items,post_data,sponsor):
    #clear sponsor ships objects
    old_sponsorships = SponsorShip.objects.filter(company=sponsor)
    for i in old_sponsorships:
        i.delete()
    for item in sponsor_items:
        if item.name in post_data and\
            SponsorShip.objects.filter(sponsor_item=item).count() < item.number_limit:
                SponsorShip.objects.create(company=sponsor,sponsor_item=item)


@login_required(login_url='/company/login/')
def Sponsor(request):
    #semantic ui
    sidebar_ui = {'sponsor':"active"}

    # get form post
    try:
        sponsor = RecruitSignup.objects.get(cid=request.user.cid)
    except Exception as e:
        error_msg="貴公司尚未報名本次「研發替代役」活動，請於左方點選「填寫報名資料」"
        return render(request,'error.html',locals())

    if request.POST:
        sponsor_items = SponsorItem.objects.all()
        Add_SponsorShip(sponsor_items,request.POST,sponsor)
        msg = {"display":True,"content":"儲存成功!"}


    #活動專刊的部份是變動不大，且版面特殊，採客製寫法
    monograph_main = SponsorItem.objects.filter(name="活動專刊").first()
    monograph_items =SponsorItem.objects.filter(name__contains="活動專刊(" )\
            .annotate(num_sponsor = Count('sponsors'))
    other_items = SponsorItem.objects.all().exclude(name__contains="活動專刊")\
            .annotate(num_sponsor = Count('sponsors'))
    sponsorship = SponsorShip.objects.filter(company=sponsor)
    my_sponsor_items = [s.sponsor_item for s in sponsorship ]
    return render(request,'recruit/company/sponsor.html',locals())

@staff_member_required
def SponsorAdmin(request):
    site_header="OpenHouse 管理後台"
    site_title="OpenHouse"
    sponsor_items = SponsorItem.objects.all()\
                .annotate(num_sponsor = Count('sponsorship'))
    companies = RecruitSignup.objects.all()
    sponsorships_list = list()
    for c in companies:
        shortname = c.get_company_name()
        sponsorships = SponsorShip.objects.filter(company=c)
        counts = [SponsorShip.objects.filter(company= c,sponsor_item=item).count() for item in sponsor_items]
        amount = 0
        for s in sponsorships:
            amount += s.sponsor_item.price
        sponsorships_list.append({
            "cid":c.cid,
            "counts":counts,
            "amount":amount,
            "shortname":shortname,
            "id":c.id,
            "change_url": urlresolvers.reverse('admin:recruit_recruitsignup_change',
                                                args=(c.id,))
                        })

    return render(request,'recruit/admin/sponsor_admin.html',locals())


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
            (msg_display,msg_type,msg_content) = (True, "green", "問卷填寫完成，感謝您")
        else:
            (msg_display,msg_type,msg_content) = (True, "error", "儲存失敗，有未完成欄位")
            print(form.errors)
    else:
        form = forms.SurveyForm(instance=my_survey)

    return render(request, 'recruit/company/survey_form.html', locals())


@staff_member_required
def sponsorship_admin(request):
    items = SponsorItem.objects.all()
    sponsorships = SponsorShip.objects.all()
    companys = SponsorShip.objects.all()
    return render(request, 'recruit/admin/sponsorship.html', locals())
