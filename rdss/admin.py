from django.contrib import admin
from rdss import models
import company.models
from django.conf.urls import url,include
import rdss.export

admin.AdminSite.site_header="OpenHouse 管理後台"
admin.AdminSite.site_title="OpenHouse"
admin.AdminSite.index_template="admin/admin_index.html"


class SponsorshipInline(admin.TabularInline):
    model = models.Sponsorship
    extra = 0

@admin.register(models.Seminar_Slot)
class Seminar_SlotAdmin(admin.ModelAdmin):
    list_display = ('date', 'session', 'cid')

@admin.register(models.Sponsor_Items)
class Sponsor_ItemsAdmin(admin.ModelAdmin):
    inlines = (SponsorshipInline,)
    list_display = ('name', 'description', 'price','limit','current_amount')
    def current_amount(self,obj):
        return models.Sponsorship.objects.filter(item=obj).count()
    current_amount.short_description = '目前贊助數'


@admin.register(models.Signup)
class SignupAdmin(admin.ModelAdmin):
    list_display = ('cid','company_name','seminar','jobfair','career_tutor','visit','lecture','payment')
    inlines = (SponsorshipInline,)

    def company_name(self,obj):
        com = company.models.Company.objects.filter(cid=obj.cid).first()
        return com.shortname

    #define export URLs eg:...admin/rdss/signup/export
    def get_urls(self):
        urls = super(SignupAdmin, self).get_urls()
        my_urls = [
                url(r'^export/$', rdss.export.Export_Signup),
                ]
        return my_urls + urls



@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('cid','category','hr_name','hr_phone','hr_mobile','hr_email')

    def get_urls(self):
        urls = super(CompanyAdmin, self).get_urls()
        my_urls = [
                url(r'^export/$', rdss.export.Export_Company),
                ]
        return my_urls + urls

    def category(self,obj):
        com = company.models.Company.objects.filter(cid=obj.cid).first()
        return com.category

    def hr_name(self,obj):
        com = company.models.Company.objects.filter(cid=obj.cid).first()
        return com.hr_name

    def hr_phone(self,obj):
        com = company.models.Company.objects.filter(cid=obj.cid).first()
        return com.hr_phone

    def hr_mobile(self,obj):
        com = company.models.Company.objects.filter(cid=obj.cid).first()
        return com.hr_mobile

    def hr_email(self,obj):
        com = company.models.Company.objects.filter(cid=obj.cid).first()
        return com.hr_email

    category.short_description = '類型'
    hr_name.short_description = '人資姓名'
    hr_phone.short_description = '人資電話'
    hr_mobile.short_description = '人資手機'
    hr_email.short_description = '人資Email'

@admin.register(models.Seminar_Order)
class Seminar_OrderAdmin(admin.ModelAdmin):
    list_display = ("cid","time","updated")

@admin.register(models.Jobfair_Order)
class Jobfair_OrderAdmin(admin.ModelAdmin):
    list_display = ("cid","time","updated")

@admin.register(models.RdssConfigs)
class RdssConfigsAdmin(admin.ModelAdmin):
    list_display = ("configs",)

    def configs(self,obj):
        return "活動設定"

@admin.register(models.CompanySurvey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ("company",)

@admin.register(models.Files)
class RDSSFilesAdmin(admin.ModelAdmin):
	list_display=('title','category','upload_file','updated_time')

# Register your models here.
admin.site.register(models.Sponsorship)
admin.site.register(models.Seminar_Info)
admin.site.register(models.Jobfair_Slot)
admin.site.register(models.Jobfair_Info)
