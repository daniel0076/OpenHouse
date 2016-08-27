from django.contrib import admin
from recruit import models

class RecruitConfigAdmin(admin.ModelAdmin):
    list_display=['title']
    def title(self,obj):
        return '活動設定'
admin.site.register(models.RecruitConfigs, RecruitConfigAdmin)

class RecruitSignup(admin.ModelAdmin):
    pass
admin.site.register(models.RecruitSignup, RecruitSignup)
