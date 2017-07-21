from django.shortcuts import render,redirect
from django.http import  HttpResponseRedirect, JsonResponse,Http404,HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core import serializers
from django.utils import timezone
import rdss.forms
import company.models
import rdss.models
import datetime,json,csv
from company.models import Company
from .forms import EmailPostForm
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Sum
from django.core import urlresolvers
from django.db.models import Q
# for logging
import logging
# Create your views here.

logger = logging.getLogger('rdss')
collect_pts_logger = logging.getLogger('stu_attend')

@login_required(login_url='/company/login/')
def RDSSCompanyIndex(request):
	sidebar_ui = {'index': 'active'}
	configs=rdss.models.RdssConfigs.objects.all()[0]
	rdss_company_info = rdss.models.RdssCompanyInfo.objects.all()
	plan_file = rdss.models.Files.objects.filter(category = "企畫書").first()
	return render(request,'company/rdss_company_entrance.html',locals())

@login_required(login_url='/company/login/')
def Status(request):
    if request.user.is_staff:
        return redirect("/admin")
    mycid = request.user.cid
    # get the dates from the configs
    configs=rdss.models.RdssConfigs.objects.all()[0]
    signup_data = rdss.models.Signup.objects.filter(cid=mycid).first()

    slot_info = {
            "seminar_select_time":"選位時間正在排定中",
            "jobfair_select_time":"選位時間正在排定中",
            "seminar_slot":"-",
            "jobfair_slot":"-",
            }
    seminar_session_display = {
            "noon":"{}~{}".format(configs.session1_start,configs.session1_end),
            "night1":"{}~{}".format(configs.session2_start,configs.session2_end),
            "night2":"{}~{}".format(configs.session3_start,configs.session3_end),
            "extra":"補場",
            "jobfair":"就博會",
            }
    # 問卷狀況
    try:
        rdss.models.CompanySurvey.objects.get(cid = request.user.cid)
        fill_survey = True
    except:
        fill_survey = False

    # 選位時間和數量狀態
    seminar_select_time = rdss.models.SeminarOrder.objects.filter(company=mycid).first()
    jobfair_select_time = rdss.models.JobfairOrder.objects.filter(company=mycid).first()
    seminar_slot = rdss.models.SeminarSlot.objects.filter(company=mycid).first()
    jobfair_slot = rdss.models.JobfairSlot.objects.filter(company=mycid)
    if seminar_select_time and not seminar_slot:
        slot_info['seminar_select_time'] = seminar_select_time.time
        slot_info['seminar_slot'] = "請依時段於左方選單選位"
    if jobfair_select_time and not jobfair_slot:
        slot_info['jobfair_select_time'] = jobfair_select_time.time
        slot_info['jobfair_slot'] = "請依時段於左方選單選位"

    if seminar_slot:
        slot_info['seminar_slot'] = "{} {}".format(seminar_slot.date,
                seminar_session_display[seminar_slot.session])
    if jobfair_slot:
        slot_info['jobfair_slot'] = [int(s.serial_no) for s in jobfair_slot]

    # Fee display
    fee = 0
    try:
        if signup_data.seminar == "noon":
            fee += configs.session1_fee
        elif signup_data.seminar == "night":
            fee += configs.session2_fee
        fee += signup_data.jobfair*configs.jobfair_booth_fee
    except AttributeError:
        pass

    # Sponsor fee display
    sponsor_amount = 0
    sponsorships = rdss.models.Sponsorship.objects.filter(company__cid = request.user.cid)
    for s in sponsorships:
        sponsor_amount += s.item.price

    # Seminar and Jobfair info status
    try:
        seminar_info = rdss.models.SeminarInfo.objects.get(company = request.user.cid)
    except ObjectDoesNotExist:
        seminar_info = None
    try:
        jobfair_info = rdss.models.JobfairInfo.objects.get(company = request.user.cid)
    except ObjectDoesNotExist:
        jobfair_info = None

    # control semantic ui class
    step_ui = ["","",""] # for step ui in template
    nav_rdss="active"
    sidebar_ui = {'status':"active"}

    step_ui[0] = "completed" if signup_data else "active"
    step_ui[1] = "completed" if jobfair_slot or seminar_slot else "active"
    step_ui[2] = "completed" if jobfair_info or seminar_info else "active"


    return render(request,'company/status.html',locals())

@login_required(login_url='/company/login/')
def SignupRdss(request):
    if request.user.is_staff:
        return redirect("/admin")
    #semanti ui control
    sidebar_ui = {'signup':"active"}
    configs=rdss.models.RdssConfigs.objects.all()[0]
    # use timezone now to get current time with GMT+8
    if timezone.now() > configs.rdss_signup_end or timezone.now() < configs.rdss_signup_start:
        if request.user.username!="77777777":
            error_msg="現在並非報名時間。報名期間為 {} 至 {}".format(
                    timezone.localtime(configs.rdss_signup_start).strftime("%Y/%m/%d %H:%M:%S"),
                    timezone.localtime(configs.rdss_signup_end).strftime("%Y/%m/%d %H:%M:%S"))
            return render(request,'error.html',locals())

    edit_instance_list = rdss.models.Signup.objects.filter(cid=request.user.cid)
    if request.POST:
        # copy the data from post
        data = request.POST.copy()
        # decide cid in the form
        data['cid']=request.user.cid
        if edit_instance_list:
            form = rdss.forms.SignupCreationForm(data,instance=edit_instance_list[0])
        else:
            form = rdss.forms.SignupCreationForm(data)
        if form.is_valid():
            form.save()
        else:
            # for debug usage
            print(form.errors.items())
        return redirect(SignupRdss)
    # edit
    if edit_instance_list:
        form = rdss.forms.SignupCreationForm(instance=edit_instance_list[0])
        signup_edit_ui = True # for semantic ui control
    else:
        form = rdss.forms.SignupCreationForm

    plan_file = rdss.models.Files.objects.filter(category = "企畫書").first()
    return render(request,'company/signup_form.html',locals())

@login_required(login_url='/company/login/')
def SeminarInfo(request):
    try:
        company = rdss.models.Signup.objects.get(cid=request.user.cid)
    except Exception as e:
        error_msg="貴公司尚未報名本次「研發替代役」活動，請於左方點選「填寫報名資料」"
        return render(request,'error.html',locals())

    try:
        seminar_info = rdss.models.SeminarInfo.objects.get(company=company)
    except ObjectDoesNotExist:
        seminar_info = None
    if request.POST:
        data = request.POST.copy()
        data['company'] = company.cid
        form = rdss.forms.SeminarInfoCreationForm(data=data ,instance=seminar_info)
        if form.is_valid():
            form.save()
            return redirect(SeminarInfo)
        else:
            print(form.errors)
    else:
        form = rdss.forms.SeminarInfoCreationForm(instance=seminar_info)

    #semantic ui
    sidebar_ui = {'seminar_info':"active"}
    return render(request,'company/seminar_info_form.html',locals())

@login_required(login_url='/company/login/')
def JobfairInfo(request):

    try:
        company = rdss.models.Signup.objects.get(cid=request.user.cid)
    except Exception as e:
        error_msg="貴公司尚未報名本次「研發替代役」活動，請於左方點選「填寫報名資料」"
        return render(request,'error.html',locals())
    # check whether the company job fair info is in the DB
    try:
        jobfair_info = rdss.models.JobfairInfo.objects.get(company=company)
    except ObjectDoesNotExist:
        jobfair_info = None
    if request.POST:
        data = request.POST.copy()
        data['company'] = company.cid
        form = rdss.forms.JobfairInfoCreationForm(data=data,instance=jobfair_info)
        if form.is_valid():
            form.save()
            return redirect('rdss_jobfair_info')
    else:
        form = rdss.forms.JobfairInfoCreationForm(instance=jobfair_info)

    #semantic ui
    sidebar_ui = {'jobfair_info':"active"}
    return render(request,'company/jobfair_info_form.html',locals())

@login_required(login_url='/company/login/')
def SeminarSelectFormGen(request):
    #semanti ui control
    sidebar_ui = {'seminar_select':"active"}

    mycid = request.user.cid
    # check the company have signup rdss
    try:
        my_signup = rdss.models.Signup.objects.get(cid=request.user.cid)
        # check the company have signup seminar
        if my_signup.seminar == "":
            error_msg="貴公司已報名本次研替活動，但並末勾選參加說明會選項。"
            return render(request,'error.html',locals())
    except Exception as e:
        error_msg="貴公司尚未報名本次「研發替代役」活動，請於左方點選「填寫報名資料」"
        return render(request,'error.html',locals())

    #check the company have been assigned a slot select order and time
    try:
        seminar_select_time = rdss.models.SeminarOrder.objects.filter(company=mycid).first().time
    except Exception as e:
        seminar_select_time = "選位時間及順序尚未排定，您可以先參考下方說明會時間表"

    seminar_session = my_signup.get_seminar_display()

    configs=rdss.models.RdssConfigs.objects.all()[0]
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

    slot_colors = rdss.models.SlotColor.objects.all()
    return render(request,'company/seminar_select.html',locals())

@login_required(login_url='/company/login/')
def SeminarSelectControl(request):
    if request.method =="POST":
        post_data=json.loads(request.body.decode())
        action = post_data.get("action")
    else:
        raise Http404("What are u looking for?")

    #action query
    if action == "query":
        slots = rdss.models.SeminarSlot.objects.all()
        return_data={}
        for s in slots:
            #night1_20160707
            index= "{}_{}".format(s.session,s.date.strftime("%Y%m%d"))
            return_data[index] = {}

            return_data[index]['place_color'] = None if not s.place else\
                s.place.css_color
            return_data[index]["cid"] = "None" if not s.company else\
                s.company.get_company_name()

            my_seminar_session = rdss.models.Signup.objects.filter(cid=request.user.cid).first().seminar
            #session wrong (signup noon but choose night)
            #and noon is not full yet
            if (my_seminar_session not in s.session) and\
                (rdss.models.SeminarSlot.objects.filter(session__contains=my_seminar_session, company=None).exists()):
            # 選別人的時段，而且自己的時段還沒滿
                return_data[index]['valid'] = False
            else:
                return_data[index]['valid'] = True

        my_slot = rdss.models.SeminarSlot.objects.filter(company__cid=request.user.cid).first()
        if my_slot:
            return_data['my_slot'] = True
        else:
            return_data['my_slot'] = False

        try:
            my_select_time = rdss.models.SeminarOrder.objects.filter(company=request.user.cid).first().time
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
        my_select_time = rdss.models.SeminarOrder.objects.filter(company=mycid).first().time
        if not my_select_time or timezone.now() <my_select_time:
            return JsonResponse({"success":False,'msg':'選位失敗，目前非貴公司選位時間'})

        slot_session , slot_date_str = post_data.get("slot").split('_')
        slot_date = datetime.datetime.strptime(slot_date_str,"%Y%m%d")
        try:
            slot = rdss.models.SeminarSlot.objects.get(date=slot_date,session=slot_session)
            my_signup = rdss.models.Signup.objects.get(cid=request.user.cid)
        except:
            return JsonResponse({"success":False,'msg':'選位失敗，時段錯誤或貴公司未勾選參加說明會'})

        if slot.company != None:
            return JsonResponse({"success":False,'msg':'選位失敗，該時段已被選定'})

        if slot and my_signup:
            #不在公司時段，且該時段未滿
            if my_signup.seminar not in slot.session and\
            rdss.models.SeminarSlot.objects.filter(session=my_signup.seminar, company=None):
                return JsonResponse({"success":False,"msg":"選位失敗，時段錯誤"})

            slot.company = my_signup
            slot.save()
            logger.info('{} select seminar slot {} {}'.format(my_signup.get_company_name(),slot.date,slot.session))
            return JsonResponse({"success":True})
        else:
            return JsonResponse({"success":False,'msg':'選位失敗，時段錯誤或貴公司未勾選參加說明會'})

    # end of action select
    elif action == "cancel":

        my_slot = rdss.models.SeminarSlot.objects.filter(company__cid=request.user.cid).first()
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
def JobfairSelectFormGen(request):
    #semanti ui control
    sidebar_ui = {'jobfair_select':"active"}

    mycid = request.user.cid
    # check the company have signup rdss
    try:
        my_signup = rdss.models.Signup.objects.get(cid=request.user.cid)
        # check the company have signup seminar
        if my_signup.jobfair== 0:
            error_msg="貴公司已報名本次研替活動，但並末填寫就博會攤位。"
            return render(request,'error.html',locals())
    except Exception as e:
        error_msg="貴公司尚未報名本次「研發替代役」活動，請於左方點選「填寫報名資料」"
        return render(request,'error.html',locals())
    #check the company have been assigned a slot select order and time
    try:
        jobfair_select_time = rdss.models.JobfairOrder.objects.filter(company=mycid).first().time
    except Exception as e:
        jobfair_select_time = "選位時間及順序尚未排定，您可以先參考攤位圖"

    slots = rdss.models.JobfairSlot.objects.all()
    place_map = rdss.models.Files.objects.filter(category='就博會攤位圖').first()

    return render(request,'company/jobfair_select.html',locals())

@login_required(login_url='/company/login/')
def JobfairSelectControl(request):
    if request.method =="POST":
        mycid = request.user.cid
        post_data=json.loads(request.body.decode())
        action = post_data.get("action")
    else:
        raise Http404("What are u looking for?")

    if action == "query":
        slot_list = rdss.models.JobfairSlot.objects.all()
        slot_list_return = list()
        for slot in slot_list:
            return_data = dict()
            return_data["serial_no"] = slot.serial_no
            return_data["company"] = None if not slot.company else\
                slot.company.get_company_name()
            slot_list_return.append(return_data)
        my_slot_list = [slot.serial_no for slot in rdss.models.JobfairSlot.objects.filter(company__cid=request.user.cid)]

        try:
            my_select_time = rdss.models.JobfairOrder.objects.filter(company=request.user.cid).first().time
        except AttributeError:
            my_select_time = None
        if not my_select_time or timezone.now() < my_select_time:
            select_ctrl = dict()
            select_ctrl['display'] = True
            select_ctrl['msg'] = '目前非貴公司選位時間，可先參考攤位圖，並待選位時間內選位'
            select_ctrl['select_btn'] = False
        else:
            select_ctrl = dict()
            select_ctrl['display'] = False
            select_ctrl['select_btn'] = True

        return JsonResponse({"success":True,"data":slot_list_return,"my_slot_list":my_slot_list,"select_ctrl":select_ctrl})

    elif action == "select":
        try:
            slot = rdss.models.JobfairSlot.objects.get(serial_no = post_data.get('slot'))
            my_signup = rdss.models.Signup.objects.get(cid=request.user.cid)
        except:
            ret = dict()
            ret['success'] = False
            ret['msg'] = "選位失敗，攤位錯誤或貴公司未勾選參加就博會"
            return JsonResponse(ret)
        if slot.company!= None:
            return JsonResponse({"success":False,'msg':'選位失敗，該攤位已被選定'})

        my_select_time = rdss.models.JobfairOrder.objects.filter(company=request.user.cid).first().time
        if timezone.now() < my_select_time:
            return JsonResponse({"success":False,'msg':'選位失敗，目前非貴公司選位時間'})

        my_slot_list = rdss.models.JobfairSlot.objects.filter(company__cid = request.user.cid)
        if my_slot_list.count() >= my_signup.jobfair:
            return JsonResponse({"success":False,'msg':'選位失敗，貴公司攤位數已達上限'})

        slot.company = my_signup
        slot.save()
        logger.info('{} select jobfair slot {}'.format(my_signup.get_company_name(),slot.serial_no))
        return JsonResponse({"success":True})

    elif action == "cancel":
        cancel_slot_no = post_data.get('slot')
        cancel_slot = rdss.models.JobfairSlot.objects.filter(
            company__cid=request.user.cid,
            serial_no=cancel_slot_no).first()
        if cancel_slot:
            logger.info('{} cancel jobfair slot {}'.format(cancel_slot.company.get_company_name(),cancel_slot.serial_no))
            cancel_slot.company = None
            cancel_slot.save()
            return JsonResponse({"success":True})
        else:
            return JsonResponse({"success":False,"msg":"刪除就博會攤位失敗"})
    else:
        raise Http404("Invalid")

def Add_SponsorShip(sponsor_items,post_data,sponsor):
    #clear sponsor ships objects
    old_sponsorships = rdss.models.Sponsorship.objects.filter(company=sponsor)
    for i in old_sponsorships:
        i.delete()
    for item in sponsor_items:
        if item.name in post_data and\
            rdss.models.Sponsorship.objects.filter(item=item).count() < item.limit:
                rdss.models.Sponsorship.objects.create(company=sponsor,item=item)


@login_required(login_url='/company/login/')
def Sponsor(request):
    #semantic ui
    sidebar_ui = {'sponsor':"active"}

    # get form post
    try:
        sponsor = rdss.models.Signup.objects.get(cid=request.user.cid)
    except Exception as e:
        error_msg="貴公司尚未報名本次「研發替代役」活動，請於左方點選「填寫報名資料」"
        return render(request,'error.html',locals())

    if request.POST:
        sponsor_items = rdss.models.SponsorItems.objects.all()
        Add_SponsorShip(sponsor_items,request.POST,sponsor)
        msg = {"display":True,"content":"儲存成功!"}


    #活動專刊的部份是變動不大，且版面特殊，採客製寫法
    monograph_main = rdss.models.SponsorItems.objects.filter(name="活動專刊").first()
    monograph_items = rdss.models.SponsorItems.objects.filter(name__contains="活動專刊(" )\
            .annotate(num_sponsor = Count('sponsorship'))
    other_items = rdss.models.SponsorItems.objects.all().exclude(name__contains="活動專刊")\
            .annotate(num_sponsor = Count('sponsorship'))
    sponsorship = rdss.models.Sponsorship.objects.filter(company=sponsor)
    my_sponsor_items = [s.item for s in sponsorship ]
    return render(request,'company/sponsor.html',locals())

@staff_member_required
def SponsorAdmin(request):
    site_header="OpenHouse 管理後台"
    site_title="OpenHouse"
    sponsor_items = rdss.models.SponsorItems.objects.all()\
                .annotate(num_sponsor = Count('sponsorship'))
    companies = rdss.models.Signup.objects.all()
    sponsorships_list = list()
    for c in companies:
        shortname = company.models.Company.objects.filter(cid=c.cid).first().shortname
        sponsorships = rdss.models.Sponsorship.objects.filter(company=c)
        counts = [rdss.models.Sponsorship.objects.filter(company= c,item=item).count() for item in sponsor_items]
        amount = 0
        for s in sponsorships:
            amount += s.item.price
        sponsorships_list.append({
            "cid":c.cid,
            "counts":counts,
            "amount":amount,
            "shortname":shortname,
            "id":c.id,
            "change_url": urlresolvers.reverse('admin:rdss_signup_change',
                                                args=(c.id,))
                        })

    return render(request,'admin/sponsor_admin.html',locals())

@login_required(login_url='/company/login/')
def CompanySurvey(request):
    configs=rdss.models.RdssConfigs.objects.all()[0]

    #semantic ui
    sidebar_ui = {'survey':"active"}

    if timezone.now() > configs.survey_end or timezone.now() < configs.survey_start :
        error_msg="問卷填答已結束。期間為 {} 至 {}".format(
                timezone.localtime(configs.survey_start).strftime("%Y/%m/%d %H:%M:%S"),
                timezone.localtime(configs.survey_end).strftime("%Y/%m/%d %H:%M:%S"))
        return render(request,'error.html',locals())

    try:
        my_survey = rdss.models.CompanySurvey.objects.get(cid=request.user.cid)
    except ObjectDoesNotExist:
        my_survey = None
    if request.POST:
        data = request.POST.copy()
        # decide cid in the form
        data['cid']=request.user.cid
        form = rdss.forms.SurveyForm(data=data, instance = my_survey)
        if form.is_valid():
            form.save()
            (msg_display,msg_type,msg_content) = (True,"green","問卷填寫完成，感謝您")
        else:
            (msg_display,msg_type,msg_content) = (True,"error","儲存失敗，有未完成欄位")
            print(form.errors)
    else:
        form = rdss.forms.SurveyForm(instance=my_survey)

    return render(request,'company/survey_form.html',locals())


@staff_member_required
def CollectPoints(request):
    site_header = "OpenHouse 管理後台"
    site_title = "OpenHouse"
    configs=rdss.models.RdssConfigs.objects.all()[0]
    today = datetime.datetime.now().date()
    now = datetime.datetime.now().time()
    if now < configs.session1_start:
        current_session = "noon"
    elif now > configs.session1_start and now <configs.session2_start:
        current_session = "noon"
    elif now > configs.session2_start and now <configs.session3_start:
        current_session = "night1"
    elif now > configs.session3_start:
        current_session = "night2"

    seminar_list = rdss.models.SeminarSlot.objects.filter(date=today)
    current_seminar = seminar_list.filter(session = current_session).first()

    if request.method =="POST":
        idcard_no = request.POST['idcard_no']
        seminar_id = request.POST['seminar_id']
        seminar_obj = rdss.models.SeminarSlot.objects.get(id=seminar_id)
        student_obj, created = rdss.models.Student.objects.get_or_create(
            idcard_no=idcard_no
        )
        attendance_obj , created = rdss.models.StuAttendance.objects.get_or_create(
            student=student_obj,
            seminar=seminar_obj
        )
        student_obj = rdss.models.Student.objects.filter(idcard_no=idcard_no).annotate(
            points=Sum('attendance__points')).first()
        collect_pts_logger.info('{} attend {} {}'.format(idcard_no, seminar_obj.date, seminar_obj.session))

        #maintain current seminar from post
        current_seminar = seminar_obj

    if seminar_list and current_seminar in seminar_list:
        # put current seminar to the default
        seminar_list = list(seminar_list)
        seminar_list.remove(current_seminar)
        seminar_list.insert(0,current_seminar)

    return render(request, 'admin/collect_points.html', locals())

@staff_member_required
def RedeemPrize(request):
    site_header = "OpenHouse 管理後台"
    site_title = "OpenHouse"
    if request.method == "GET":
        idcard_no = request.GET.get('idcard_no','')
        if idcard_no:
            student_obj = rdss.models.Student.objects.filter(idcard_no=idcard_no).annotate(
                points=Sum('attendance__points')).first()

            if student_obj:
                student_form = rdss.forms.StudentForm(instance=student_obj)
                redeem_form = rdss.forms.RedeemForm()

    if request.method == "POST":
        data = request.POST.copy()
        student_obj = rdss.models.Student.objects.filter(idcard_no = data['idcard_no']).first()
        redeem_obj = rdss.models.RedeemPrize.objects.create(
            student=student_obj
        )

        form = rdss.forms.StudentForm(data, instance = student_obj)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
            ui_message = {"type":"error", "msg":"註冊失敗"}
        redeem_form = rdss.forms.RedeemForm(data, instance = redeem_obj)
        if redeem_form.is_valid():
            redeem_form.save()
            ui_message = {"type":"green", "msg":"儲存成功，已兌換{}，花費{}點".format(
            data['prize'],data['points'])}
            redeem_form = rdss.forms.RedeemForm()
        else:
            print(redeem_form.errors)
            ui_message = {"type":"error", "msg":"註冊失敗"}

        student_form = rdss.forms.StudentForm(instance=student_obj)


    return render(request, 'admin/redeem_prize.html', locals())

@staff_member_required
def RegisterCard(request):
    if request.method =="POST":
        data = request.POST.copy()
        instance = rdss.models.Student.objects.filter(idcard_no = data['idcard_no']).first()
        form = rdss.forms.StudentForm(data, instance = instance)
        if form.is_valid():
            form.save()
            ui_message = {"type":"green", "msg":"註冊成功"}
            collect_pts_logger.info('{} registered {} {}'.format(data['idcard_no'], data['student_id'],
                data['phone']))
        else:
            print(form.errors)
            ui_message = {"type":"error", "msg":"註冊失敗"}

    form = rdss.forms.StudentForm()
    return render(request, 'admin/reg_card.html', locals())

# ========================RDSS public view=================
def RDSSPublicIndex(request):
	all_company = company.models.Company.objects.all()
	rdss_company = rdss.models.Signup.objects.all()
	rdss_info = rdss.models.RdssInfo.objects.all()
	#rdss_history = rdss.models.RdssInfo.objects.using("oh_2016").all()
	#print(rdss_history)
	company_list = [
		all_company.get(cid=c.cid) for c in rdss_company
	]
	company_list.sort(key=lambda item:getattr(item,'category'))
	return render(request,'public/rdss_index.html',locals())

def SeminarPublic(request):
    #semanti ui control
    configs=rdss.models.RdssConfigs.objects.all()[0]
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
        week_slot_info = []
        for day in range(5):
            today = table_start_date + datetime.timedelta(days=day+week*7)
            noon_slot = rdss.models.SeminarSlot.objects.filter(date=today, session='noon').first()
            night1_slot= rdss.models.SeminarSlot.objects.filter(date=today, session='night1').first()
            night2_slot= rdss.models.SeminarSlot.objects.filter(date=today, session='night2').first()
            week_slot_info.append(
                {
                    'date': today,
                    'noon': '' if not noon_slot or not noon_slot.company else
                    {
                        'company': noon_slot.company.get_company_name(),
                        'place_color':noon_slot.place.css_color
                    },
                    'night1': '' if not night1_slot or not night1_slot.company else
                    {
                        'company': night1_slot.company.get_company_name(),
                        'place_color': night1_slot.place.css_color
                    },
                    'night2': '' if not night2_slot or not night2_slot.company else
                    {
                        'company': night2_slot.company.get_company_name(),
                        'place_color': night2_slot.place.css_color
                    },
                }
            )
        dates_in_week.append(week_slot_info)

    slot_colors = rdss.models.SlotColor.objects.all()
    return render(request,'public/rdss_seminar.html',locals())

def JobfairPublic(request):
    place_map = rdss.models.Files.objects.filter(category='就博會攤位圖').first()
    slots = rdss.models.JobfairSlot.objects.all()
    return render(request,'public/rdss_jobfair.html',locals())

def QueryPoints(request):
    if request.method == 'POST':
        data = request.POST.copy()
        student_id = data.get('student_id')
        cellphone = data.get('cellphone')
        student_obj = rdss.models.Student.objects.filter(student_id=student_id,phone=cellphone).first()
        records = rdss.models.StuAttendance.objects.filter(student=student_obj)
        redeems = rdss.models.RedeemPrize.objects.filter(student=student_obj)

    return render(request,'public/rdss_querypts.html',locals())


def ListJobs(request):

    all_company = company.models.Company.objects.all()
    rdss_company = rdss.models.Signup.objects.all()
    company_list = [
        all_company.get(cid=c.cid) for c in rdss_company
    ]
    company_list.sort(key=lambda item:getattr(item,'category'))

    return render(request,'public/rdss_jobs.html',locals())

