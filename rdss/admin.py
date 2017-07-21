from django.contrib import admin
from rdss import models
import company.models
from django.conf.urls import url,include
import rdss.export

admin.AdminSite.site_header="OpenHouse 管理後台"
admin.AdminSite.site_title="OpenHouse"
#admin.AdminSite.index_template="admin/admin_index.html"


class SponsorshipInline(admin.TabularInline):
    model = models.Sponsorship
    extra = 0


class StuAttendanceInline(admin.TabularInline):
    model = models.StuAttendance
    extra = 0


@admin.register(models.Student)
class StudentAdmin(admin.ModelAdmin):
    inlines = (StuAttendanceInline,)
    list_display = ('idcard_no', 'student_id', 'name', 'phone')

@admin.register(models.RedeemPrize)
class RedeemAdmin(admin.ModelAdmin):
    list_display=('student','prize','points','updated')

@admin.register(models.SeminarSlot)
class SeminarSlotAdmin(admin.ModelAdmin):
    list_display = ('date', 'session', 'company', 'place')


@admin.register(models.SponsorItems)
class SponsorItemsAdmin(admin.ModelAdmin):
    inlines = (SponsorshipInline,)
    list_display = ('name', 'description', 'price', 'limit', 'current_amount')

    def current_amount(self, obj):
        return rdss.models.Sponsorship.objects.filter(item=obj).count()
    current_amount.short_description = '目前贊助數'


@admin.register(models.Signup)
class SignupAdmin(admin.ModelAdmin):
    list_display = ('cid','company_name','seminar','jobfair','career_tutor','visit','lecture','payment')
    inlines = (SponsorshipInline,)

    def company_name(self,obj):
        # com = company.models.Company.objects.filter(cid=obj.cid).first()
        return obj.get_company_name()

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
        print("Hi")
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

@admin.register(models.SeminarOrder)
class SeminarOrderAdmin(admin.ModelAdmin):
    list_display = ("company","time","updated")

@admin.register(models.JobfairOrder)
class JobfairOrderAdmin(admin.ModelAdmin):
    list_display = ("company","time","updated")

@admin.register(models.RdssConfigs)
class RdssConfigsAdmin(admin.ModelAdmin):
    list_display = ("configs",)

    def configs(self,obj):
        return "活動設定"

@admin.register(models.CompanySurvey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ("company",)

    #define export URLs eg:...admin/rdss/signup/export
    def get_urls(self):
        urls = super(SurveyAdmin, self).get_urls()
        my_urls = [
                url(r'^export/$', rdss.export.ExportSurvey),
                ]
        return my_urls + urls

@admin.register(models.Files)
class RDSSFilesAdmin(admin.ModelAdmin):
    list_display=('title','category','upload_file','updated')

@admin.register(models.SlotColor)
class SlotColorAdmin(admin.ModelAdmin):
    list_display=('place','css_color', 'place_info')

@admin.register(models.SeminarInfo)
class SeminarInfoAdmin(admin.ModelAdmin):
    list_display=('company','topic', 'speaker', 'speaker_title','contact',
                  'contact_email','contact_mobile', 'updated' )

@admin.register(models.JobfairInfo)
class JobfairInfoAdmin(admin.ModelAdmin):
    list_display=('company', 'signname','meat_lunchbox','vege_lunchbox',
                  'parking_tickets', 'contact_email','contact_mobile', 'updated' )
@admin.register(models.RdssInfo)
class RdssInfoAdmin(admin.ModelAdmin):
	list_display=('title',)
	def has_add_permission(self, request):
		count = rdss.models.RdssInfo.objects.all().count()
		if count ==0:
			return True
		return False
@admin.register(models.RdssCompanyInfo)
class RdssInfoAdmin(admin.ModelAdmin):
	list_display=('title',)
	def has_add_permission(self, request):
		count = rdss.models.RdssCompanyInfo.objects.all().count()
		if count ==0:
			return True
		return False


# Register your models here.
admin.site.register(models.Sponsorship)
admin.site.register(models.JobfairSlot)
