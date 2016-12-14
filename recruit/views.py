from django.core import urlresolvers
from django.shortcuts import render,redirect
from .forms import RecruitSignupForm, JobfairInfoForm, SeminarInfoCreationForm
from .models import RecruitConfigs, SponsorItem, Files
from .models import RecruitSignup, SponsorShip, CompanySurvey
from .models import SeminarSlot, SlotColor, SeminarOrder, SeminarInfo
from .models import JobfairSlot, JobfairOrder, JobfairInfo
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from django.http import  HttpResponseRedirect, JsonResponse,Http404,HttpResponse
from . import forms
from django.db.models import Count
import datetime
import json
import logging

logger = logging.getLogger('recruit')

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
    try:
        my_signup = RecruitSignup.objects.get(cid=request.user.cid)
        # check the company have signup seminar
        if my_signup.seminar == "":
            error_msg="貴公司已報名本次活動，但並末勾選參加說明會選項。"
            return render(request,'recruit/error.html',locals())
    except Exception as e:
        error_msg="貴公司尚未報名本次活動，請於左方點選「填寫報名資料」"
        return render(request,'recruit/error.html',locals())

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
def seminar_select_control(request):
    if request.method =="POST":
        post_data=json.loads(request.body.decode())
        action = post_data.get("action")
    else:
        raise Http404("What are u looking for?")

    #action query
    if action == "query":
        slots = SeminarSlot.objects.all()
        return_data={}
        for s in slots:
            # make index first night1_20160707
            index= "{}_{}".format(s.session,s.date.strftime("%Y%m%d"))
            # dict for return data
            return_data[index] = {}

            return_data[index]['place_color'] = None if not s.place else\
                s.place.css_color
            return_data[index]["cid"] = "None" if not s.company else\
                s.company.get_company_name()

            my_seminar_session = RecruitSignup.objects.filter(cid=request.user.cid).first().seminar
            #session wrong (signup noon but choose night)
            #and noon is not full yet
            if (my_seminar_session not in s.session) and\
                (SeminarSlot.objects.filter(session__contains=my_seminar_session, company=None).exists()):
            # 選別人的時段，而且自己的時段還沒滿
                return_data[index]['valid'] = False
            else:
                return_data[index]['valid'] = True

        my_slot = SeminarSlot.objects.filter(company__cid=request.user.cid).first()
        if my_slot:
            return_data['my_slot'] = True
        else:
            return_data['my_slot'] = False

        try:
            my_select_time = SeminarOrder.objects.filter(company=request.user.cid).first().time
        except AttributeError:
            my_select_time = None

        if not my_select_time or timezone.now() < my_select_time:
            select_ctrl = dict()
            select_ctrl['display'] = True
            select_ctrl['msg'] = '目前非貴公司選位時間，可先參考說明會時間表，並待選位時間內選位'
            select_ctrl['select_btn'] = False
        else:
            select_ctrl = dict()
            select_ctrl['display'] = False
            select_ctrl['select_btn'] = True

        return JsonResponse({"success":True,"data":return_data,"select_ctrl":select_ctrl})

    #action select
    elif action == "select":
        mycid = request.user.cid
        my_select_time = SeminarOrder.objects.filter(company=mycid).first().time
        if not my_select_time or timezone.now() <my_select_time:
            return JsonResponse({"success":False,'msg':'選位失敗，目前非貴公司選位時間'})

        slot_session , slot_date_str = post_data.get("slot").split('_')
        slot_date = datetime.datetime.strptime(slot_date_str,"%Y%m%d")
        try:
            slot = SeminarSlot.objects.get(date=slot_date,session=slot_session)
            my_signup = RecruitSignup.objects.get(cid=request.user.cid)
        except:
            return JsonResponse({"success":False,'msg':'選位失敗，時段錯誤或貴公司未勾選參加說明會'})

        if slot.company != None:
            return JsonResponse({"success":False,'msg':'選位失敗，該時段已被選定'})

        if slot and my_signup:
            #不在公司時段，且該時段未滿
            if my_signup.seminar not in slot.session and\
            SeminarSlot.objects.filter(session=my_signup.seminar, company=None):
                return JsonResponse({"success":False,"msg":"選位失敗，時段錯誤"})

            slot.company = my_signup
            slot.save()
            logger.info('{} select seminar slot {} {}'.format(my_signup.get_company_name(),slot.date,slot.session))
            return JsonResponse({"success":True})
        else:
            return JsonResponse({"success":False,'msg':'選位失敗，時段錯誤或貴公司未勾選參加說明會'})

    # end of action select
    elif action == "cancel":

        my_slot = SeminarSlot.objects.filter(company__cid=request.user.cid).first()
        if my_slot:
            logger.info('{} cancel seminar slot {} {}'.format(
                my_slot.company.get_company_name(),my_slot.date,my_slot.session))
            my_slot.company = None
            my_slot.save()
            return JsonResponse({"success":True})
        else:
            return JsonResponse({"success":False,"msg":"刪除說明會選位失敗"})

    else:
        pass
    raise Http404("What are u looking for?")


@login_required(login_url='/company/login/')
def seminar_info(request):
    try:
        company = RecruitSignup.objects.get(cid=request.user.cid)
    except Exception as e:
        error_msg="貴公司尚未報名本次活動，請於左方點選「填寫報名資料」"
        return render(request,'recruit/error.html',locals())

    try:
        seminar_info = SeminarInfo.objects.get(company=company)
    except ObjectDoesNotExist:
        seminar_info = None
    if request.POST:
        data = request.POST.copy()
        data['company'] = company.cid
        form = SeminarInfoCreationForm(data=data ,instance=seminar_info)
        if form.is_valid():
            form.save()
            return render(request, 'recruit/company/success.html', locals())
        else:
            print(form.errors)
    else:
        form = SeminarInfoCreationForm(instance=seminar_info)

    #semantic ui
    sidebar_ui = {'seminar_info':"active"}
    return render(request,'recruit/company/seminar_info_form.html',locals())

@login_required(login_url='/company/login/')
def jobfair_select_form_gen(request):
    #semanti ui control
    sidebar_ui = {'jobfair_select':"active"}

    mycid = request.user.cid
    # check the company have signup recruit
    try:
        my_signup = RecruitSignup.objects.get(cid=request.user.cid)
        # check the company have signup seminar
        if my_signup.jobfair== 0:
            error_msg="貴公司已報名本次研替活動，但並末填寫就博會攤位。"
            return render(request,'recruit/error.html',locals())
    except Exception as e:
        error_msg="貴公司尚未報名本次活動，請於左方點選「填寫報名資料」"
        return render(request,'recruit/error.html',locals())
    #check the company have been assigned a slot select order and time
    try:
        jobfair_select_time = JobfairOrder.objects.filter(company=mycid).first().time
    except Exception as e:
        jobfair_select_time = "選位時間及順序尚未排定，您可以先參考攤位圖"

    place_maps = Files.objects.filter(category='就博會攤位圖')

    return render(request,'recruit/company/jobfair_select.html',locals())

@login_required(login_url='/company/login/')
def jobfair_select_control(request):
    if request.method =="POST":
        mycid = request.user.cid
        post_data=json.loads(request.body.decode())
        action = post_data.get("action")
    else:
        raise Http404("What are u looking for?")

    slot_group = [
        {"slot_type":"半導體", "display":"半導體","category":["半導體"], "slot_list":list(),
         "is_mygroup":False, "color":"pink"},

        {"slot_type":"資訊軟體", "display":"資訊軟體","category":["資訊軟體"], "slot_list":list(),
         "is_mygroup":False, "color":"blue"},

        {"slot_type":"消費電子", "display":"消費電子","category":["消費電子"], "slot_list":list(),
         "is_mygroup":False, "color":"yellow"},

        {"slot_type":"網路通訊", "display":"網路通訊","category":["網路通訊"], "slot_list":list(),
         "is_mygroup":False, "color":"teal"},

        {"slot_type":"光電光學", "display":"光電光學","category":["光電光學"], "slot_list":list(),
         "is_mygroup":False, "color":"grey"},

        {"slot_type":"綜合", "display":"綜合(綜合、集團、機構、人力銀行)"
         ,"category":["綜合","集團","機構","人力銀行"],
         "slot_list":list(), "is_mygroup":False, "color":"purple"},
    ]
    try:
        my_signup = RecruitSignup.objects.get(cid=request.user.cid)
    except:
        ret = dict()
        ret['success'] = False
        ret['msg'] = "選位失敗，攤位錯誤或貴公司未勾選參加就博會"
        return JsonResponse(ret)
    # 把自己的group enable並放到最前面顯示
    my_slot_group = next(group for group in slot_group\
                         if my_signup.get_company().category in group['category'] )
    slot_group.remove(my_slot_group)
    my_slot_group['is_mygroup'] = True
    slot_group.insert(0,my_slot_group)

    if action == "query":
        for group in slot_group:
            slot_list = JobfairSlot.objects.filter(category=group['slot_type'])
            for slot in slot_list:
                slot_info = dict()
                slot_info["serial_no"] = slot.serial_no
                slot_info["company"] = None if not slot.company else\
                    slot.company.get_company_name()
                group['slot_list'].append(slot_info)

        my_slot_list = [slot.serial_no for slot in JobfairSlot.objects.filter(company__cid=request.user.cid)]

        try:
            my_select_time = JobfairOrder.objects.filter(company=request.user.cid).first().time
        except AttributeError:
            my_select_time = None
        if not my_select_time or timezone.now() < my_select_time:
            select_ctrl = dict()
            select_ctrl['display'] = True
            select_ctrl['msg'] = '目前非貴公司選位時間，可先參考攤位圖，並待選位時間內選位'
            select_ctrl['select_enable'] = False
        else:
            select_ctrl = dict()
            select_ctrl['display'] = False
            select_ctrl['select_enable'] = True

        return JsonResponse({"success":True,
                             "slot_group":slot_group,
                             "my_slot_list":my_slot_list,
                             "select_ctrl":select_ctrl})

    elif action == "select":
        try:
            slot = JobfairSlot.objects.get(serial_no = post_data.get('slot'))
        except:
            ret = dict()
            ret['success'] = False
            ret['msg'] = "選位失敗，攤位錯誤"
            return JsonResponse(ret)
        if slot.company!= None:
            return JsonResponse({"success":False,'msg':'選位失敗，該攤位已被選定'})

        my_select_time = JobfairOrder.objects.filter(company=request.user.cid).first().time
        if timezone.now() < my_select_time:
            return JsonResponse({"success":False,'msg':'選位失敗，目前非貴公司選位時間'})

        my_slot_list = JobfairSlot.objects.filter(company__cid = request.user.cid)
        if my_slot_list.count() >= my_signup.jobfair:
            return JsonResponse({"success":False,'msg':'選位失敗，貴公司攤位數已達上限'})

        my_slot_group = next(group for group in slot_group\
                            if my_signup.get_company().category in group['category'] )
        if my_slot_group['slot_type'] != slot.category:
            return JsonResponse({"success":False,'msg':'選位失敗，該攤位非貴公司類別'})


        slot.company = my_signup
        slot.save()
        logger.info('{} select jobfair slot {}'.format(my_signup.get_company_name(),slot.serial_no))
        return JsonResponse({"success":True})

    elif action == "cancel":
        cancel_slot_no = post_data.get('slot')
        cancel_slot = JobfairSlot.objects.filter(
            company__cid=request.user.cid,
            serial_no=cancel_slot_no
        ).first()
        if cancel_slot:
            logger.info('{} cancel jobfair slot {}'.format(cancel_slot.company.get_company_name(),cancel_slot.serial_no))
            cancel_slot.company = None
            cancel_slot.save()
            return JsonResponse({"success":True})
        else:
            return JsonResponse({"success":False,"msg":"刪除就博會攤位失敗"})
    else:
        raise Http404("Invalid")

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
        error_msg="貴公司尚未報名本次「校園徵才」活動，請於左方點選「填寫報名資料」"
        return render(request,'recruit/error.html',locals())

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
