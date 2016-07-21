from django.db import models
from tinymce.models import HTMLField
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.

class News(models.Model):
	CATEGORYS = (
			(u'最新消息', u'最新消息'),
			(u'廠商專區', u'廠商專區')
			)
	id = models.AutoField(primary_key=True)
	title = models.CharField(u'標題',max_length=100)
	category = models.CharField(u'公告類別',max_length=5,choices=CATEGORYS)
	content = RichTextUploadingField(u'內容')
	created_time = models.DateTimeField(u'發佈時間',auto_now_add=True)
	updated_time = models.DateTimeField(u'更新時間',auto_now=True)

	class Meta:
		verbose_name = "公告"
		verbose_name_plural = "公告"
