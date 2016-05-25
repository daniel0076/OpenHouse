from django.db import models

class Activity(models.Model):
	id = models.AutoField(primary_key=True)
	cid = models.CharField(u'公司統一編號',unique=True,max_length=8)
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

		verbose_name = u"研替活動報名"
		verbose_name_plural =u"研替活動報名"

	def __str__(self):
		return self.shortname

class Seminar_Slot(models.Model):

	id = models.AutoField(primary_key=True)
	time = models.DateTimeField(u'場次時間')
	cid=models.OneToOneField('Activity',to_field='cid',on_delete=models.CASCADE)
	updated = models.DateTimeField(u'更新時間',auto_now=True)

	class Meta:
		managed = True
		verbose_name = u"說明會場次"
		verbose_name_plural =u"說明會場次"
	def __str__(self):
		return self.cid

class Seminar_Order(models.Model):
	id = models.AutoField(primary_key=True)
	time = models.DateTimeField(u'選位開始時間')
	cid=models.OneToOneField('Activity',to_field='cid',on_delete=models.CASCADE)
	updated = models.DateTimeField(u'更新時間',auto_now=True)

	class Meta:
		managed = True
		verbose_name = u"說明會選位順序"
		verbose_name_plural =u"說明會選位順序"

class Seminar_Info(models.Model):
	id = models.AutoField(primary_key=True)
	cid=models.OneToOneField('Activity',to_field='cid',on_delete=models.CASCADE)
	topic = models.CharField(u'說明會主題',max_length=30)
	speaker = models.CharField(u'主講人',max_length=30)
	speaker_title = models.CharField(u'主講人稱謂',max_length=30)
	speaker_email = models.EmailField(u'主講人Email',max_length=254)
	attendees = models.SmallIntegerField(u'廠商到場人數')
	raffle_prize = models.TextField(u'抽獎獎品')
	raffle_prize_amount = models.SmallIntegerField(u'抽獎獎品數量')
	qa_prize = models.TextField(u'QA獎獎品')
	qa_prize_amount = models.SmallIntegerField(u'QA獎獎品數量')
	attend_prize = models.TextField(u'參加獎獎品')
	attend_prize_amount = models.SmallIntegerField(u'參加獎獎品數量')
	snack_box = models.SmallIntegerField(u'加碼餐盒數量')
	contact = models.CharField(u'聯絡人',max_length=30)
	contact_mobile = models.CharField(u'聯絡人手機',max_length=16)
	contact_email = models.EmailField(u'聯絡人Email',max_length=254)
	ps = models.EmailField(u'其它需求',max_length=254)
	updated = models.DateTimeField(u'更新時間',auto_now=True)

	class Meta:
		managed = True
		verbose_name = u"說明會資訊"
		verbose_name_plural =u"說明會資訊"
