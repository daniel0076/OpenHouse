from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.

class News(models.Model):
	CATEGORYS = (
			(u'最新消息', u'最新消息'),
			(u'徵才專區', u'徵才專區')
			)
	PERM = (
			(u'index_only', u'只顯示於首頁'),
			(u'company_only', u'只顯示於廠商'),
			(u'both', u'顯示於首頁及廠商'),
			)
	id = models.AutoField(primary_key=True)
	title = models.CharField(u'標題',max_length=100)
	category = models.CharField(u'公告類別',max_length=5,choices=CATEGORYS)
	perm = models.CharField(u'誰能看到這則公告',max_length=15,choices=PERM)
	content = RichTextUploadingField(u'內容')
	created_time = models.DateTimeField(u'發佈時間',auto_now_add=True)
	updated_time = models.DateTimeField(u'更新時間',auto_now=True)

	class Meta:
		verbose_name = "公告系統"
		verbose_name_plural = "公告系統"
