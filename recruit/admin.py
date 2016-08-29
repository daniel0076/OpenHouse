from django.contrib import admin
from .models import RecruitConfigs, RecruitSignup,JobfairSlot,JobfairInfo
from company.models import Company


class RecruitConfigAdmin(admin.ModelAdmin):
    list_display=['title']
    def title(self,obj):
        return '活動設定'
admin.site.register(RecruitConfigs, RecruitConfigAdmin)

class RecruitSignupAdmin(admin.ModelAdmin):
    pass
admin.site.register(RecruitSignup, RecruitSignupAdmin)

class JobfairSlotAdmin(admin.ModelAdmin):
    list_display = ('serial_number',)

admin.site.register(JobfairSlot, JobfairSlotAdmin)

class JobfairInfoAdmin(admin.ModelAdmin):
    list_display = ('company',)


admin.site.register(JobfairInfo, JobfairInfoAdmin)