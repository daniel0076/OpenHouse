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
import recruit.models
import company.models


@staff_member_required
def ExportAll(request):
    # Create the HttpResponse object with the appropriate Excel header.
    filename = "recruit_export_{}.xlsx".format(timezone.localtime(timezone.now()).strftime("%m%d-%H%M"))
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=' + filename
    workbook = xlsxwriter.Workbook(response)

    # Company Basic Info
    signup_cid_list = [s.cid for s in recruit.models.RecruitSignup.objects.all()]
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
    signups = recruit.models.RecruitSignup.objects.all()
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
            {'fieldname': 'company_visit', 'title': '提供企業參訪'},
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
    sponsor_items = recruit.models.SponsorItem.objects.all().annotate(num_sponsor=Count('sponsorship'))
    sponsorships_list = list()
    for c in signups:
        shortname = company.models.Company.objects.filter(cid=c.cid).first().shortname
        sponsorships = recruit.models.SponsorShip.objects.filter(company=c)
        counts = [recruit.models.SponsorShip.objects.filter(company=c, sponsor_item=item).count() for item in sponsor_items]
        amount = 0
        for s in sponsorships:
            amount += s.sponsor_item.price
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
        spon_worksheet.write(1, index+1, "{}/{}".format(item.num_sponsor, item.number_limit))

    row_offset = 2
    for row_count, com in enumerate(sponsorships_list):
        spon_worksheet.write(row_count+row_offset, 0, com['shortname'])
        for col_count, count in enumerate(com['counts']):
            spon_worksheet.write(row_count+row_offset, col_count+1, count)
        spon_worksheet.write(row_count+row_offset, len(com['counts'])+1, com['amount'])

    workbook.close()
    return response

@staff_member_required
def export_seminar_info(request):
    filename =  "recruit_seminar_info.xlsx"
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=' + filename
    workbook = xlsxwriter.Workbook(response)     
    worksheet = workbook.add_worksheet("說明會資訊")
    fields = recruit.models.SeminarInfo._meta.get_fields()[1:-1]
    for index, field in enumerate(fields):
        worksheet.write(0,index,field.verbose_name)
    company_list = recruit.models.SeminarInfo.objects.all()
    for i,info in enumerate(company_list):
        for j,field in enumerate(fields):
            if(field.name != 'company' and  field.name != 'updated'):
                worksheet.write(i+1,j,getattr(info,field.name))
            elif(field.name == 'company'):
                cid = getattr(getattr(info,field.name),'cid')
                company_name = company.models.Company.objects.get(cid=cid).name 
                worksheet.write(i+1,j,company_name)
    workbook.close()
    return response

@staff_member_required
def export_jobfair_info(request):
    filename =  "recruit_jobfair_info.xlsx"
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=' + filename
    workbook = xlsxwriter.Workbook(response)     
    worksheet = workbook.add_worksheet("就博會資訊")
    fields = recruit.models.JobfairInfo._meta.get_fields()[1:]
    for index, field in enumerate(fields):
        worksheet.write(0,index,field.verbose_name)
    company_list = recruit.models.JobfairInfo.objects.all()
    for i,info in enumerate(company_list):
        for j,field in enumerate(fields):
            if(field.name != 'company' and  field.name != 'updated'):
                worksheet.write(i+1,j,getattr(info,field.name))
            elif(field.name == 'company'):
                cid = getattr(getattr(info,field.name),'cid')
                company_name = company.models.Company.objects.get(cid=cid).name 
                worksheet.write(i+1,j,company_name)
    workbook.close()
    return response
@staff_member_required
def ExportSurvey(request):
    # Create the HttpResponse object with the appropriate Excel header.
    filename = "recruit_survey_{}.xlsx".format(timezone.localtime(timezone.now()).strftime("%m%d-%H%M"))
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=' + filename
    workbook = xlsxwriter.Workbook(response)

    survey_worksheet = workbook.add_worksheet("廠商滿意度問卷")
    survey_worksheet.write(0, 0, "廠商")
    # start from index 1 because I don't want id field
    fields = recruit.models.CompanySurvey._meta.get_fields()[1:]
    for index, field in enumerate(fields):
        survey_worksheet.write(0, index+1, field.verbose_name)

    survey_list = recruit.models.CompanySurvey.objects.all()
    for row_count, survey in enumerate(survey_list):
        survey_worksheet.write(row_count+1, 0, survey.company)
        # export timestamp cause problem, TODO:FIX the fields[:-1] to fields
        for col_count, field in enumerate(fields[:-1]):
            survey_worksheet.write(row_count+1, col_count+1, getattr(survey, field.name))

    workbook.close()
    return response

@staff_member_required
def ExportActivityInfo(request):
    # Create the HttpResponse object with the appropriate Excel header.
    filename = "recruit_activity_info_{}.xlsx".format(timezone.localtime(timezone.now()).strftime("%m%d-%H%M"))
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=' + filename
    workbook = xlsxwriter.Workbook(response)
    worksheet = workbook.add_worksheet("說明會資訊")
    worksheet.write(0, 0, "廠商")
    # ignore id and cid which is index 0 and 1
    fields = recruit.models.SeminarInfo._meta.get_fields()[2:]
    for index, field in enumerate(fields):
        worksheet.write(0, index+1, field.verbose_name)

    seminar_into_list = recruit.models.SeminarInfo.objects.all()
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
    fields = recruit.models.JobfairInfo._meta.get_fields()[2:]
    for index, field in enumerate(fields):
        worksheet.write(0, index+1, field.verbose_name)

    jobfair_into_list = recruit.models.JobfairInfo.objects.all()
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
    recruit_company = recruit.models.RecruitSignup.objects.all()
    company_list = [
        all_company.get(cid=c.cid) for c in recruit_company
    ]
    company_list.sort(key=lambda item:getattr(item,'category'))

    return render(request,'admin/export_ad.html',locals())
