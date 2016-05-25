from django.contrib import admin
from rdss import models

# Register your models here.
admin.site.register(models.Activity)
admin.site.register(models.Seminar_Info)
admin.site.register(models.Seminar_Slot)
admin.site.register(models.Seminar_Order)
