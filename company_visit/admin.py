from django.contrib import admin
from . import models

class CompanyVisitAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.CompanyVisit, CompanyVisitAdmin)

class StudentApplyAdmin(admin.ModelAdmin):
    list_display = ('event','name','date','SSN','mobile','email','student_id','department','gender','country')
    list_filter = ('event',)
admin.site.register(models.StudentApply,StudentApplyAdmin)
