from django.contrib import admin
from django.conf.urls import url
from .models import RecruitConfigs, RecruitSignup,JobfairSlot,JobfairInfo,SponsorItem,SponsorShip,\
    Files,RecruitConfigs,CompanySurvey, Company, SeminarSlot, SlotColor, SeminarOrder, SeminarInfo,Student,StuAttendance
from .models import JobfairOrder
from company.models import Company
from recruit import export

class SponsorshipInline(admin.TabularInline):
    model = SponsorShip
    extra = 0

class RecruitConfigAdmin(admin.ModelAdmin):
    list_display=['title']
    def title(self,obj):
        return '活動設定'
admin.site.register(RecruitConfigs, RecruitConfigAdmin)

class StuAttendanceInline(admin.TabularInline):
    model = StuAttendance
    extra = 0

class StuAttendanceAdmin(admin.ModelAdmin):
    pass
admin.site.register(StuAttendance,StuAttendanceAdmin)
    
    

class StudentAdmin(admin.ModelAdmin):
    inlines = (StuAttendanceInline,)
    list_display = ('card_num', 'student_id', 'name', 'phone')

admin.site.register(Student,StudentAdmin)
        
class RecruitSignupAdmin(admin.ModelAdmin):
    search_fields = ('cid','seminar',)
    list_display = ('cid','company_name','seminar','jobfair','career_tutor','company_visit','lecture','payment')
    list_filter = ('seminar','career_tutor','company_visit','lecture','payment',)
    inlines = (SponsorshipInline,)

    # custom search the company name field in other db
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super(RecruitSignupAdmin, self).get_search_results(request, queryset, search_term)

        company_list = Company.objects.filter(name__icontains=search_term)
        company_list |= Company.objects.filter(shortname__icontains=search_term)
        for company in company_list:
            queryset |= self.model.objects.filter(cid = company.cid)
        return queryset, use_distinct

    def company_name(self,obj):
        return obj.get_company_name()
admin.site.register(RecruitSignup, RecruitSignupAdmin)

@admin.register(SeminarSlot)
class SeminarSlotAdmin(admin.ModelAdmin):
    list_display = ('date', 'session', 'company', 'place')
    raw_id_fields = ("company",)

@admin.register(SeminarOrder)
class SeminarOrderAdmin(admin.ModelAdmin):
    list_display = ("company","time","updated")
    raw_id_fields = ("company",)

@admin.register(SeminarInfo)
class SeminarInfoAdmin(admin.ModelAdmin):
    list_display=('company','topic', 'speaker', 'speaker_title','contact',
                  'contact_email','contact_mobile', 'updated' )


@admin.register(SlotColor)
class SlotColorAdmin(admin.ModelAdmin):
    list_display=('place','css_color', 'place_info')

@admin.register(JobfairOrder)
class JobfairOrderAdmin(admin.ModelAdmin):
    list_display=('company', 'time')

class JobfairSlotAdmin(admin.ModelAdmin):
    list_display = ('serial_no','category','company','updated')

admin.site.register(JobfairSlot, JobfairSlotAdmin)

class JobfairInfoAdmin(admin.ModelAdmin):
    list_display = ('company',)
admin.site.register(JobfairInfo, JobfairInfoAdmin)

class SponsorItemAdmin(admin.ModelAdmin):
    inlines = (SponsorshipInline,)
    list_display = ('name', 'description', 'price', 'number_limit', 'current_amount')

    def current_amount(self, obj):
        return SponsorShip.objects.filter(sponsor_item=obj).count()
    current_amount.short_description = '目前贊助數'

admin.site.register(SponsorItem, SponsorItemAdmin)

class SponsorShipAdmin(admin.ModelAdmin):
    pass
admin.site.register(SponsorShip, SponsorShipAdmin)

@admin.register(CompanySurvey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ("company",)

    #define export URLs eg:...admin/recruit/signup/export
    def get_urls(self):
        urls = super(SurveyAdmin, self).get_urls()
        my_urls = [
                url(r'^export/$', export.ExportSurvey, name="recruit_survey_export"),
                ]
        return my_urls + urls

@admin.register(Files)
class RecruitFilesAdmin(admin.ModelAdmin):
    list_display=('title','category','upload_file','updated')
