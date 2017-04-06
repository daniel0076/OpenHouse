from django.contrib import admin
from . import models

@admin.register(models.Participant)
class ParticipantAdmin(admin.ModelAdmin):
    pass

