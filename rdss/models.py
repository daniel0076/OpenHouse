from django.db import models

class Activity(models.Model):
	id = models.AutoField(primary_key=True)
	cid = models.CharField(u'公司統一編號',unique=True,max_length=8)
	name = models.CharField(u'公司名稱',max_length=64)
	seminar_noon = models.BooleanField(u'說明會中午')
	seminar_night = models.BooleanField(u'說明會晚上')
	enterprise_day= models.BooleanField(u'專屬企業日')
	job_fair = models.BooleanField(u'徵才展示會')
	career_tutor = models.BooleanField(u'徵才展示會')
	post_ad = models.BooleanField(u'刊登廣告')
	payment = models.BooleanField(u'完成付款')
	added = models.DateTimeField(u'報名時間',auto_now_add=True)
	updated = models.DateTimeField(u'更新時間',auto_now=True)

	class Meta:
		managed = True

		verbose_name = u"研替活動狀況"
		verbose_name_plural =u"研替活動狀況"

	def __str__(self):
		return self.name
