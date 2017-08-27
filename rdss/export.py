from django.shortcuts import render,redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.core import serializers
from django.forms.models import model_to_dict
from django.utils import timezone
from django.db.models import Count
from django.conf import settings
import xlsxwriter
import json
import datetime
import rdss.models
import company.models


@staff_member_required
def Export_Signup(request):
    # Create the HttpResponse object with the appropriate Excel header.
    filename = "rdss_signup_info_{}.xlsx".format(
        timezone.localtime(timezone.now()).strftime("%m%d-%H%M"))
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=' + filename

    workbook = xlsxwriter.Workbook(response)
    worksheet = workbook.add_worksheet()

    signups = rdss.models.Signup.objects.all()
    signups_dict = json.loads(serializers.serialize('json', signups))
    # join company info
    for signup in signups_dict:
        company_obj = company.models.Company.objects.get(
                        cid=signup['fields']['cid'])
        company_dict = model_to_dict(company_obj)
        for key, value in company_dict.items():
            signup['fields'][key] = value

    title_pairs = [
            {'fieldname': 'cid', 'title': '公司統一編號'},
            {'fieldname': 'shortname', 'title': '公司簡稱'},
            {'fieldname': 'hr_name', 'title': '人資姓名'},
            {'fieldname': 'hr_phone', 'title': '人資電話'},
            {'fieldname': 'hr_mobile', 'title': '人資手機'},
            {'fieldname': 'hr_email', 'title': '人資Email'},
            {'fieldname': 'hr2_name', 'title': '人資2姓名'},
            {'fieldname': 'hr2_phone', 'title': '人資2電話'},
            {'fieldname': 'hr2_mobile', 'title': '人資2手機'},
            {'fieldname': 'hr2_email', 'title': '人資2Email'},
            {'fieldname': 'seminar', 'title': '說明會場次'},
            {'fieldname': 'jobfair', 'title': '就博會攤位數'},
            {'fieldname': 'visit', 'title': '提供企業參訪'},
            {'fieldname': 'career_tutor', 'title': '提供職場導師'},
            {'fieldname': 'lecture', 'title': '提供就業力講座'},
            {'fieldname': 'payment', 'title': '是否繳費'},
            {'fieldname': 'updated', 'title': '更新時間'},
            ]

    for index, pair in enumerate(title_pairs):
        worksheet.write(0, index, pair['title'])

    for row_count, signup in enumerate(signups_dict):
        for col_count, pairs in enumerate(title_pairs):
            worksheet.write(row_count+1, col_count,
                            signup['fields'][pairs['fieldname']])

    workbook.close()
    return response


@staff_member_required
def Export_Company(request):
    # Create the HttpResponse object with the appropriate Excel header.
    filename = "rdss_company_{}.xlsx".format(
        timezone.localtime(timezone.now()).strftime("%m%d-%H%M"))
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=' + filename

    signup_cid_list = [s.cid for s in rdss.models.Signup.objects.all()]
    company_list = list()
    for cid in signup_cid_list:
        company_list.append(
            company.models.Company.objects.filter(cid=cid).first())

    fieldname_list = ['cid', 'name', 'shortname', 'category', 'phone',
                      'postal_code', 'address', 'website',
                      'hr_name', 'hr_phone', 'hr_mobile', 'hr_email',
                      'hr2_name', 'hr2_phone', 'hr2_mobile', 'hr2_email', 'hr_ps',
                      'brief', 'recruit_info']
    title_pairs = dict()
    for fieldname in fieldname_list:
        title_pairs[fieldname] = company.models.Company._meta.get_field(fieldname).verbose_name

    workbook = xlsxwriter.Workbook(response)
    worksheet = workbook.add_worksheet()

    for index, fieldname in enumerate(fieldname_list):
        worksheet.write(0, index, title_pairs[fieldname])

    for row_count, company_obj in enumerate(company_list):
        for col_count, fieldname in enumerate(fieldname_list):
            worksheet.write(row_count+1, col_count,  getattr(company_obj, fieldname))

    workbook.close()
    return response


@staff_member_required
def ExportAll(request):
    # Create the HttpResponse object with the appropriate Excel header.
    filename = "rdss_export_{}.xlsx".format(timezone.localtime(timezone.now()).strftime("%m%d-%H%M"))
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=' + filename
    workbook = xlsxwriter.Workbook(response)

    # Company Basic Info
    signup_cid_list = [s.cid for s in rdss.models.Signup.objects.all()]
    company_list = list()
    for cid in signup_cid_list:
        company_list.append(
            company.models.Company.objects.filter(cid=cid).first())

    fieldname_list = ['cid', 'name', 'shortname', 'category', 'phone',
                      'postal_code', 'address', 'website',
                      'hr_name', 'hr_phone', 'hr_mobile', 'hr_email',
                      'hr2_name', 'hr2_phone', 'hr2_mobile', 'hr2_email', 'hr_ps',
                      'brief', 'recruit_info']
    # avoid 'can't subtract offset-naive and offset-aware datetimes'

    title_pairs = dict()
    for fieldname in fieldname_list:
        title_pairs[fieldname] = company.models.Company._meta.get_field(fieldname).verbose_name

    info_worksheet = workbook.add_worksheet("廠商資料")

    for index, fieldname in enumerate(fieldname_list):
        info_worksheet.write(0, index, title_pairs[fieldname])

    for row_count, company_obj in enumerate(company_list):
        for col_count, fieldname in enumerate(fieldname_list):
            info_worksheet.write(row_count+1, col_count,  getattr(company_obj, fieldname))
    # ============= end of company basic info =============

    # Company Signup
    signups = rdss.models.Signup.objects.all()
    signups_dict = json.loads(serializers.serialize('json', signups))
    # join company info
    for signup in signups_dict:
        company_obj = company.models.Company.objects.get(
                        cid=signup['fields']['cid'])
        company_dict = model_to_dict(company_obj)
        for key, value in company_dict.items():
            signup['fields'][key] = value

    title_pairs = [
            {'fieldname': 'cid', 'title': '公司統一編號'},
            {'fieldname': 'shortname', 'title': '公司簡稱'},
            {'fieldname': 'seminar', 'title': '說明會場次'},
            {'fieldname': 'jobfair', 'title': '就博會攤位數'},
            {'fieldname': 'visit', 'title': '提供企業參訪'},
            {'fieldname': 'career_tutor', 'title': '提供職場導師'},
            {'fieldname': 'lecture', 'title': '提供就業力講座'},
            {'fieldname': 'payment', 'title': '是否繳費'},
            {'fieldname': 'updated', 'title': '更新時間'},
            ]

    signup_worksheet = workbook.add_worksheet("廠商報名情況")

    for index, pair in enumerate(title_pairs):
        signup_worksheet.write(0, index, pair['title'])

    for row_count, signup in enumerate(signups_dict):
        for col_count, pairs in enumerate(title_pairs):
            signup_worksheet.write(row_count+1, col_count,
                                   signup['fields'][pairs['fieldname']])

    # Sponsorships
    sponsor_items = rdss.models.SponsorItems.objects.all().annotate(num_sponsor=Count('sponsorship'))
    sponsorships_list = list()
    for c in signups:
        shortname = company.models.Company.objects.filter(cid=c.cid).first().shortname
        sponsorships = rdss.models.Sponsorship.objects.filter(company=c)
        counts = [rdss.models.Sponsorship.objects.filter(company=c, item=item).count() for item in sponsor_items]
        amount = 0
        for s in sponsorships:
            amount += s.item.price
        sponsorships_list.append({
            "cid": c.cid,
            "counts": counts,
            "amount": amount,
            "shortname": shortname,
            "id": c.id,
                        })
    spon_worksheet = workbook.add_worksheet("贊助")
    spon_worksheet.write(0, 0, "廠商/贊助品")
    spon_worksheet.write(1, 0, "目前數量/上限")
    spon_worksheet.write(0, len(sponsor_items)+1, "贊助額")
    for index, item in enumerate(sponsor_items):
        spon_worksheet.write(0, index+1, item.name)
        spon_worksheet.write(1, index+1, "{}/{}".format(item.num_sponsor, item.limit))

    row_offset = 2
    for row_count, com in enumerate(sponsorships_list):
        spon_worksheet.write(row_count+row_offset, 0, com['shortname'])
        for col_count, count in enumerate(com['counts']):
            spon_worksheet.write(row_count+row_offset, col_count+1, count)
        spon_worksheet.write(row_count+row_offset, len(com['counts'])+1, com['amount'])

    workbook.close()
    return response

@staff_member_required
def ExportSeminar(request):
    # Create the HttpResponse object with the appropriate Excel header
    filename = "rdss_seminar_{}.xlsx".format(timezone.localtime(timezone.now()).strftime("%m%d-%H%M"))
    response = HttpResponse(content_type='application/ms-excel') # microsoft excel
    response['Content-Disposition'] = 'attachment; filename=' + filename # set "attachment" filename
    with xlsxwriter.Workbook(response) as workbook:
        seminar_worksheet = workbook.add_worksheet("說明會資訊") # set the excel sheet
        seminar_worksheet.write(0,0,"廠商") # The excel at (0,0) name is "廠商"
        fields = rdss.models.SeminarInfo._meta.get_fields()[2:]
        for index, field in enumerate(fields,1):
            seminar_worksheet.write(0,index,field.verbose_name) # set the title for each colume
        seminar_list = rdss.models.SeminarInfo.objects.all()
        
        for row_count, seminar in enumerate(seminar_list,1):
            seminar_worksheet.write(row_count, 0, str(seminar.company)) # the jobfair.company is type of rdss.models.Signup, so we change to str
            for col_count, field in enumerate(fields,1):
                try:
                    seminar_worksheet.write(row_count, col_count, getattr(seminar, field.name))
                except TypeError as e:
                    # xlsxwriter do not accept django timzeone aware time, so use
                    # except, to write string
                    seminar_worksheet.write(row_count, col_count,timezone.localtime(getattr(seminar,field.name)).strftime("%Y-%m-%d %H:%M:%S"))
    return response
@staff_member_required
def ExportJobfair(request):
    # Create the HttpREsponse object with the appropriate Excel header
    filename = "rdss_jobfair_{}.xlsx".format(timezone.localtime(timezone.now()).strftime("%m%d-%H%M"))
    response = HttpResponse(content_type='application/ms-excel') # microsoft excel
    response['Content-Disposition'] = 'attachment; filename=' + filename # set "attachment" filename
    with xlsxwriter.Workbook(response) as workbook:
        jobfair_worksheet = workbook.add_worksheet("就博會資訊") # set the excel sheet
        jobfair_worksheet.write(0,0,"廠商") # The excel at (0,0) name is "廠商"
        fields = rdss.models.JobfairInfo._meta.get_fields()[2:]
        for index, field in enumerate(fields,1):
            jobfair_worksheet.write(0,index,field.verbose_name) # set the title for each colume
        jobfair_list = rdss.models.JobfairInfo.objects.all()
        # We need to remove company beacuse it's type is rdss.models.Signup, and it just a id
        for row_count, jobfair in enumerate(jobfair_list,1):
            jobfair_worksheet.write(row_count, 0, jobfair.signname)
            for col_count, field in enumerate(fields,1):
                try:
                    jobfair_worksheet.write(row_count, col_count, getattr(jobfair, field.name))
                except TypeError as e:
                    # xlsxwriter do not accept django timzeone aware time, so use
                    # except, to write string
                    jobfair_worksheet.write(row_count, col_count,timezone.localtime(getattr(jobfair,field.name)).strftime("%Y-%m-%d %H:%M:%S"))
    return response

@staff_member_required
def ExportSurvey(request):
    # Create the HttpResponse object with the appropriate Excel header.
    filename = "rdss_survey_{}.xlsx".format(timezone.localtime(timezone.now()).strftime("%m%d-%H%M"))
    response = HttpResponse(content_type='application/ms-excel') # microsoft excel
    response['Content-Disposition'] = 'attachment; filename=' + filename # set "attachment" filename
    with xlsxwriter.Workbook(response) as workbook:
        survey_worksheet = workbook.add_worksheet("廠商滿意度問卷")# set the excel sheet
        survey_worksheet.write(0, 0, "廠商") # The excel at(0,0) name is "廠商"
        fields = rdss.models.CompanySurvey._meta.get_fields()[1:]
        #print(fields)
        for index, field in enumerate(fields,1):
            survey_worksheet.write(0, index,field.verbose_name) # set the title for each colume
        survey_list = rdss.models.CompanySurvey.objects.all()
        #print(survey_list)
        for row_count, survey in enumerate(survey_list,1):
            survey_worksheet.write(row_count, 0, survey.company)
            for col_count, field in enumerate(fields,1):
                try:
                    survey_worksheet.write(row_count, col_count, getattr(survey, field.name))
                except TypeError as e:
                    # xlsxwriter do not accept django timzeone aware time, so use
                    # except, to write string
                    survey_worksheet.write(row_count, col_count,timezone.localtime(getattr(survey,field.name)).strftime("%Y-%m-%d %H:%M:%S"))
    return response

@staff_member_required
def ExportActivityInfo(request):
    # Create the HttpResponse object with the appropriate Excel header.
    filename = "rdss_activity_info_{}.xlsx".format(timezone.localtime(timezone.now()).strftime("%m%d-%H%M"))
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=' + filename
    workbook = xlsxwriter.Workbook(response)
    worksheet = workbook.add_worksheet("說明會資訊")
    worksheet.write(0, 0, "廠商")
    # ignore id and cid which is index 0 and 1
    fields = rdss.models.SeminarInfo._meta.get_fields()[2:]
    for index, field in enumerate(fields):
        worksheet.write(0, index+1, field.verbose_name)

    seminar_into_list = rdss.models.SeminarInfo.objects.all()
    for row_count, info in enumerate(seminar_into_list):
        worksheet.write(row_count+1, 0, info.company.get_company_name())
        for col_count, field in enumerate(fields):
            try:
                worksheet.write(row_count+1, col_count+1, getattr(info, field.name))
            except TypeError as e:
                # xlsxwriter do not accept django timzeone aware time, so use
                # except, to write string
                worksheet.write(row_count+1, col_count+1,info.updated.strftime("%Y-%m-%d %H:%M:%S"))

    worksheet = workbook.add_worksheet("就博會資訊")
    worksheet.write(0, 0, "廠商")
    # ignore id and cid which is index 0 and 1
    fields = rdss.models.JobfairInfo._meta.get_fields()[2:]
    for index, field in enumerate(fields):
        worksheet.write(0, index+1, field.verbose_name)

    jobfair_into_list = rdss.models.JobfairInfo.objects.all()
    for row_count, info in enumerate(jobfair_into_list):
        worksheet.write(row_count+1, 0, info.company.get_company_name())
        for col_count, field in enumerate(fields):
            try:
                worksheet.write(row_count+1, col_count+1, getattr(info, field.name))
            except TypeError as e:
                # same as above
                worksheet.write(row_count+1, col_count+1,info.updated.strftime("%Y-%m-%d %H:%M:%S"))

    workbook.close()
    return response


@staff_member_required
def ExportAdFormat(request):
    all_company = company.models.Company.objects.all()
    rdss_company = rdss.models.Signup.objects.all()
    company_list = [
        all_company.get(cid=c.cid) for c in rdss_company
    ]
    company_list.sort(key=lambda item:getattr(item,'category'))

    return render(request,'admin/export_ad.html',locals())
