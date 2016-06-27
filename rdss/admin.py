from django.contrib import admin
from rdss import models

class Seminar_SlotAdmin(admin.ModelAdmin):
	list_display = ('date', 'session', 'cid')

# Register your models here.
admin.site.register(models.Activity)
admin.site.register(models.RdssConfigs)

admin.site.register(models.Seminar_Info)
admin.site.register(models.Seminar_Slot,Seminar_SlotAdmin)
admin.site.register(models.Seminar_Order)
admin.site.register(models.Jobfair_Order)
admin.site.register(models.Jobfair_Slot)
admin.site.register(models.Jobfair_Info)
admin.site.register(models.Sponsor_Items)
