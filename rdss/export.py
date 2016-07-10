from django.contrib.auth.decorators import login_required
from django.http import  HttpResponse
from django.core import serializers
from django.forms.models import model_to_dict
from django.utils import timezone
from datetime import datetime
import xlsxwriter,json
import rdss.models,company.models

@login_required(login_url='/company/login/')
def Export_Signup(request):
	# Create the HttpResponse object with the appropriate Excel header.
	filename="rdss_signup_info_{}.xlsx".format(timezone.localtime(timezone.now()).strftime("%m%d-%H%M"))
	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename=' + filename

	workbook = xlsxwriter.Workbook(response)
	worksheet = workbook.add_worksheet()

	signups = rdss.models.Signup.objects.all()
	signups_dict = json.loads(serializers.serialize('json', signups))
	#join company info
	for signup in signups_dict:
		company_obj = company.models.Company.objects.get(cid = signup['fields']['cid'])
		company_dict = model_to_dict(company_obj)
		for key,value in company_dict.items():
			signup['fields'][key]=value

	title_pairs = [
			{'fieldname':'cid','title':'公司統一編號'},
			{'fieldname':'shortname','title':'公司簡稱'},
			{'fieldname':'hr_name','title':'人資姓名'},
			{'fieldname':'hr_phone','title':'人資電話'},
			{'fieldname':'hr_mobile','title':'人資手機'},
			{'fieldname':'hr_email','title':'人資Email'},
			{'fieldname':'seminar','title':'說明會場次'},
			{'fieldname':'jobfair','title':'就博會攤位數'},
			{'fieldname':'visit','title':'提供企業參訪'},
			{'fieldname':'career_tutor','title':'提供職場導師'},
			{'fieldname':'lecture','title':'提供就業力講座'},
			{'fieldname':'payment','title':'是否繳費'},
			{'fieldname':'updated','title':'更新時間'},
			]
	for index,pair in enumerate(title_pairs):
		worksheet.write(0,index,pair['title'])

	for row_count,signup in enumerate(signups_dict):
		for col_count,pairs in enumerate(title_pairs):
			worksheet.write(row_count+1,col_count, signup['fields'][ pairs['fieldname'] ])

	workbook.close()
	return response

@login_required(login_url='/company/login/')
def Export_Company(request):
	# Create the HttpResponse object with the appropriate Excel header.
	filename="rdss_company_{}.xlsx".format(timezone.localtime(timezone.now()).strftime("%m%d-%H%M"))
	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename=' + filename

	signup_cid_list = [s.cid for s in rdss.models.Signup.objects.all()]
	company_list = list()
	for cid in signup_cid_list:
		company_list.append(company.models.Company.objects.filter(cid=cid).first())

	fieldname_list = ['cid','name','shortname','category','phone','postal_code','address','website',
			'hr_name','hr_phone','hr_mobile','hr_name','hr_email','brief','introduction']
	title_pairs = dict()
	for fieldname in fieldname_list:
		title_pairs[fieldname] = company.models.Company._meta.get_field(fieldname).verbose_name

	workbook = xlsxwriter.Workbook(response)
	worksheet = workbook.add_worksheet()

	for index,fieldname in enumerate(fieldname_list):
		worksheet.write(0,index,title_pairs[fieldname])

	for row_count,company_obj in enumerate(company_list):
		for col_count,fieldname in enumerate(fieldname_list):
			worksheet.write(row_count+1,col_count, getattr(company_obj,fieldname))

	workbook.close()
	return response
