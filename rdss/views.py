from django.shortcuts import render,redirect
from django.http import  HttpResponseRedirect, JsonResponse,Http404
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
import rdss.forms
import rdss.models
import datetime,json

# Create your views here.

@login_required(login_url='/company/login/')
def ControlPanel(request):
	mycid = request.user.cid
	# control semantic ui class
	step_ui = ["","",""] # for step ui in template
	nav_rdss="active"
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

	# control semanti ui class
	if not signup_data:
		step_ui[0] = "active"
	else:
		step_ui[0] = "completed"
		step_ui[1] = "active"

	return render(request,'rdss.html',locals())

@login_required(login_url='/company/login/')
def SignupRdss(request):
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
		dates_in_week.append( [(table_start_date + datetime.timedelta(days=day+week*7))\
				for day in range(0,5)])
	form = rdss.forms.SeminarInfoCreationForm
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
				return_data["{}_{}".format(s.session,s.date.strftime("%Y%m%d"))]={"cid":str(s.cid)}
			return JsonResponse({"success":True,"data":return_data})

		#action select
		elif action == "select":
			slot = post_data.get("slot");
			slot_session , slot_date_str = slot.split('_')
			slot_date = datetime.datetime.strptime(slot_date_str,"%Y%m%d")
			try:
				slot = rdss.models.Seminar_Slot.objects.get(date=slot_date,session=slot_session)
				my_signup = rdss.models.Signup.objects.get(cid=request.user.cid)

				if slot and my_signup:
					slot.cid = my_signup
					slot.save()
					return JsonResponse({"success":True})
				else:
					return JsonResponse({"success":False})

			except:
				return JsonResponse({"success":False})
		else:
			pass
	raise Http404("What are u looking for?")
