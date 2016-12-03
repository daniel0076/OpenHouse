from django.contrib import admin
from . import models

class SignupInline(admin.TabularInline):
    model = models.Signup
    extra = 0
# Register your models here.
@admin.register(models.Mentor)
class CareerMentorAdmin(admin.ModelAdmin):
    inlines = (SignupInline,)
    search_fields= ('company',)
    list_filter = ('category','company')
    list_display=('title','category', 'company', 'date','start_time','end_time',
                  'mentor', 'place','limit', 'updated' )

@admin.register(models.Signup)
class CareerSignupAdmin(admin.ModelAdmin):
    list_filter = ('mentor','mentor__category')
    list_display=('mentor', 'name', 'student_id','dep','phone',
                  'email', 'time_available','question','cv_en','cv_zh','other', 'updated' )

