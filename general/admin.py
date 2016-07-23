from django.contrib import admin
from django.conf.urls import url,include
from general import models
import rdss.models

@admin.register(models.News)
class NewsAdmin(admin.ModelAdmin):
	list_display=('title','category','created_time','updated_time')

@admin.register(rdss.models.Files)
class RDSSFilesAdmin(admin.ModelAdmin):
	list_display=('title','category','upload_file','updated_time')

# Register your models here.
