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
	# control semantic ui class
	step_ui = ["","",""] # for step ui in template
	nav_rdss="active"
	# get the dates from the configs
	configs=rdss.models.RdssConfigs.objects.all()[0]
	my_rdss_signup = rdss.models.Signup.objects.filter(cid=request.user.cid)
	rdss_signup_data = my_rdss_signup[0]
	# control semanti ui class
	if not my_rdss_signup:
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

	try:
		my_signup = rdss.models.Signup.objects.get(cid=request.user.cid)
		if not (my_signup.seminar_noon or my_signup.seminar_night):
			error_msg="貴公司已報名本次研替活動，但並末勾選參加說明會選項。"
			return render(request,'error.html',locals())
	except Exception as e:
		error_msg="貴公司尚未報名本次「研發替代役」活動，請於左方點選「填寫報名資料」"
		return render(request,'error.html',locals())


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
		print(post_data)
		action = post_data.get("action")
		if action == "query":
			slots = rdss.models.Seminar_Slot.objects.all()
			return_data={}
			for s in slots:
				return_data["{}_{}".format(s.session,s.date.strftime("%Y%m%d"))]={"cid":str(s.cid)}
			return JsonResponse({"success":True,"data":return_data})
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
				else:
					return JsonResponse({"success":False})

			except:
				return JsonResponse({"success":False})
		else:
			pass
	raise Http404("What are u looking for?")
