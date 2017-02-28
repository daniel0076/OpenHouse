from django.contrib import admin
from . import models

class CompanyVisitAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.CompanyVisit, CompanyVisitAdmin)

class StudentApplyAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.StudentApply,StudentApplyAdmin)