from django.shortcuts import render,redirect
from django.http import  HttpResponseRedirect, JsonResponse,Http404
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
import rdss.forms
import company.models
import rdss.models
import datetime,json

# Create your views here.
sidebar_ui = dict()

@login_required(login_url='/company/login/')
def ControlPanel(request):
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
			"noon":"{}~{}".format(configs.session_1_start,configs.session_1_end),
			"night1":"{}~{}".format(configs.session_2_start,configs.session_2_end),
			"night2":"{}~{}".format(configs.session_3_start,configs.session_3_end)
			}
	seminar_select_time = rdss.models.Seminar_Order.objects.filter(cid=mycid).first()
	jobfair_select_time = rdss.models.Jobfair_Order.objects.filter(cid=mycid).first()
	seminar_slot = rdss.models.Seminar_Slot.objects.filter(cid=mycid).first()
	jobfair_slot = rdss.models.Jobfair_Slot.objects.filter(cid=mycid).first()
	if seminar_select_time:
		slot_info['seminar_select_time'] = seminar_select_time.time
		slot_info['seminar_slot'] = "請依時段於左方選單選位"
	if jobfair_select_time:
		slot_info['jobfair_select_time'] = jobfair_select_time.time
		slot_info['jobfair_slot'] = "請依時段於左方選單選位"
	if seminar_slot:
		slot_info['seminar_slot'] = "{} {}".format(seminar_slot.date,
				seminar_session_display[seminar_slot.session])
	if jobfair_slot:
		slot_info['jobfair_slot'] = jobfair_slot

	# control semantic ui class
	step_ui = ["","",""] # for step ui in template
	nav_rdss="active"
	sidebar_ui = {'index':"active"}

	if not signup_data:
		step_ui[0] = "active"
	else:
		step_ui[0] = "completed"
		step_ui[1] = "active"

	return render(request,'rdss.html',locals())

@login_required(login_url='/company/login/')
def SignupRdss(request):
	#semanti ui control
	sidebar_ui = {'signup':"active"}
	configs=rdss.models.RdssConfigs.objects.all()[0]
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
	# edit
	if edit_instance_list:
		form = rdss.forms.SignupCreationForm(instance=edit_instance_list[0])
		signup_edit_ui = True # for semantic ui control
	else:
		form = rdss.forms.SignupCreationForm



	return render(request,'signup_form.html',locals())

@login_required(login_url='/company/login/')
def SeminarInfo(request):
	form = rdss.forms.SeminarInfoCreationForm
	return render(request,'seminar_info_form.html',locals())

@login_required(login_url='/company/login/')
def JobfairInfo(request):
	form = rdss.forms.JobfairInfoCreationForm
	return render(request,'jobfair_info_form.html',locals())

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
		my_select_time = rdss.models.Seminar_Order.objects.get(cid=my_signup)
	except Exception as e:
		error_msg="選位時間及順序尚未排定，請靜候選位通知"
		return render(request,'error.html',locals())

	seminar_select_time = rdss.models.Seminar_Order.objects.filter(cid=mycid).first().time
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
	return render(request,'seminar_select.html',locals())

@login_required(login_url='/company/login/')
def SeminarSelectControl(request):
	if request.method =="POST":
		post_data=json.loads(request.body.decode())
		action = post_data.get("action")

		#action query
		if action == "query":
			slots = rdss.models.Seminar_Slot.objects.all()
			return_data={}
			for s in slots:
				#night1_20160707
				index= "{}_{}".format(s.session,s.date.strftime("%Y%m%d"))
				return_data[index] = {}

				return_data[index]["cid"] = "None" if not s.cid else\
				company.models.Company.objects.filter(cid=s.cid).first().shortname

				seminar_session = rdss.models.Signup.objects.filter(cid=request.user.cid).first().seminar
				#session wrong (signup noon but choose night)
				#and noon is not full yet
				if (seminar_session not in s.session) and\
					rdss.models.Seminar_Slot.objects.filter(session=seminar_session):
					return_data[index]['valid'] = False
				else:
					return_data[index]['valid'] = True
			my_slot = rdss.models.Seminar_Slot.objects.filter(cid__cid=request.user.cid).first()
			if my_slot:
				return_data['my_slot'] = True
			else:
				return_data['my_slot'] = False

			return JsonResponse({"success":True,"data":return_data})

		#action select
		elif action == "select":
			slot = post_data.get("slot");
			slot_session , slot_date_str = slot.split('_')
			slot_date = datetime.datetime.strptime(slot_date_str,"%Y%m%d")
			#TODO fix try except coding style
			#TODO fix foreignkey lookup
			try:
				slot = rdss.models.Seminar_Slot.objects.get(date=slot_date,session=slot_session)
				my_signup = rdss.models.Signup.objects.get(cid=request.user.cid)

				if slot and my_signup:

					#不在公司時段，且該時段未滿
					if my_signup.seminar not in slot.session and\
					rdss.models.Seminar_Slot.objects.filter(session=my_signup.seminar):
						return JsonResponse({"success":False,"msg":"選位失敗，時段錯誤"})

					slot.cid = my_signup
					slot.save()
					return JsonResponse({"success":True})
				else:
					return JsonResponse({"success":False})

			except:
				ret['success'] = False
				ret['msg'] = "選位失敗，時段錯誤或貴公司未勾選參加說明會"
				return JsonResponse(ret)
		# end of action select
		elif action == "cancel":

			my_slot = rdss.models.Seminar_Slot.objects.filter(cid__cid=request.user.cid).first()
			if my_slot:
				my_slot.cid = None
				my_slot.save()
				return JsonResponse({"success":True})
			else:
				return JsonResponse({"success":False})

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
		my_select_time = rdss.models.Jobfair_Order.objects.get(cid=my_signup)
	except Exception as e:
		error_msg="選位時間及順序尚未排定，請靜候選位通知"
		return render(request,'error.html',locals())

	jobfair_select_time = rdss.models.Jobfair_Order.objects.filter(cid=mycid).first().time
	slots = rdss.models.Jobfair_Slot.objects.all()


	return render(request,'jobfair_select.html',locals())

def Add_SponsorShip(sponsor_items,post_data,sponsor):
	#clear sponsor ships objects
	old_sponsorships = rdss.models.Sponsorship.objects.filter(cid=sponsor)
	for i in old_sponsorships:
		i.delete()
	for item in sponsor_items:
		if item.name in post_data and\
			rdss.models.Sponsorship.objects.filter(item=item).count() < item.limit:
				rdss.models.Sponsorship.objects.create(cid=sponsor,item=item)


@login_required(login_url='/company/login/')
def Sponsor(request):
	#semantic ui
	sidebar_ui = {'sponsor':"active"}
	# get form post
	sponsor = rdss.models.Signup.objects.get(cid=request.user.cid)
	if request.POST:
		sponsor_items = rdss.models.Sponsor_Items.objects.all()
		Add_SponsorShip(sponsor_items,request.POST,sponsor)
		msg = {"display":True,"content":"儲存成功!"}


	#活動專刊的部份是變動不大，且版面特殊，採客製寫法
	monograph_main = rdss.models.Sponsor_Items.objects.filter(name="活動專刊").first()
	monograph_items = rdss.models.Sponsor_Items.objects.filter(name__contains="活動專刊(" )
	other_items = rdss.models.Sponsor_Items.objects.all().exclude(name__contains="活動專刊")
	sponsorship = rdss.models.Sponsorship.objects.filter(cid=sponsor)
	my_sponsor_items = [s.item for s in sponsorship ]
	return render(request,'sponsor.html',locals())
