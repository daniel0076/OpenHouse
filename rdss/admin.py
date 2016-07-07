from django.contrib import admin
from rdss import models
import company.models
from django.conf.urls import url,include

admin.AdminSite.site_header="OpenHouse 管理後台"
admin.AdminSite.site_title="OpenHouse"
admin.AdminSite.index_template="admin/admin_index.html"


@admin.register(models.Seminar_Slot)
class Seminar_SlotAdmin(admin.ModelAdmin):
	list_display = ('date', 'session', 'company_name')
	def company_name(self,obj):
		com = company.models.Company.objects.filter(cid=obj.cid).first()
		return None if com == None else com.shortname

@admin.register(models.Sponsor_Items)
class Sponsor_ItemsAdmin(admin.ModelAdmin):
	list_display = ('name', 'description', 'price','limit','current_amount')
	def current_amount(self,obj):
		return models.Sponsorship.objects.filter(item=obj).count()
	current_amount.short_description = '目前贊助數'

@admin.register(models.Signup)
class SignupAdmin(admin.ModelAdmin):
	list_display = ('cid','company_name','seminar','jobfair','career_tutor','visit','lecture','payment')
	def company_name(self,obj):
		com = company.models.Company.objects.filter(cid=obj.cid).first()
		return com.shortname


@admin.register(models.SignupCompany)
class SignupCompanyAdmin(admin.ModelAdmin):
	list_display = ('cid','company_name','category','hr_name','hr_phone','hr_mobile','hr_email')

	def company_name(self,obj):
		com = company.models.Company.objects.filter(cid=obj.cid).first()
		return com.shortname

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
	company_name.short_description = '公司簡稱'
	category.short_description = '類型'
	hr_name.short_description = '人資姓名'
	hr_phone.short_description = '人資電話'
	hr_mobile.short_description = '人資手機'
	hr_email.short_description = '人資Email'

@admin.register(models.Seminar_Order)
class Seminar_OrderAdmin(admin.ModelAdmin):
	list_display = ("cid","company_name","time","updated")

	def company_name(self,obj):
		com = company.models.Company.objects.filter(cid=obj.cid).first()
		return com.shortname
	company_name.short_description = '公司簡稱'

@admin.register(models.Jobfair_Order)
class Jobfair_OrderAdmin(admin.ModelAdmin):
	list_display = ("cid","company_name","time","updated")

	def company_name(self,obj):
		com = company.models.Company.objects.filter(cid=obj.cid).first()
		return com.shortname
	company_name.short_description = '公司簡稱'


# Register your models here.
admin.site.register(models.RdssConfigs)
admin.site.register(models.Sponsorship)
admin.site.register(models.Seminar_Info)
admin.site.register(models.Jobfair_Slot)
admin.site.register(models.Jobfair_Info)
