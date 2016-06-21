from django.db import models
CATEGORYS = (
		(u'半導體', u'半導體'),
		(u'消費電子', u'消費電子'),
		(u'網路通訊', u'網路通訊'),
		(u'光電光學', u'光電光學'),
		(u'資訊軟體', u'資訊軟體'),
		(u'集團', u'集團'),
		(u'綜合', u'綜合'),
		(u'人力銀行', u'人力銀行'),
		(u'機構', u'機構'),
		(u'通用', u'通用')
		)

class RdssConfigs(models.Model):
	signup_start = models.DateTimeField(u'廠商註冊開始時間')
	signup_end = models.DateTimeField(u'廠商註冊結束時間')
	rdss_signup_start = models.DateTimeField(u'研替報名開始時間')
	rdss_signup_end = models.DateTimeField(u'研替報名結束時間')

	#說明會相關
	seminar_start_date = models.DateField(u'說明會開始日期')
	seminar_end_date = models.DateField(u'說明會結束日期')
	session_1_start = models.TimeField(u'說明會場次1_開始時間')
	session_1_end = models.TimeField(u'說明會場次1_結束時間')
	session_2_start = models.TimeField(u'說明會場次2_開始時間')
	session_2_end = models.TimeField(u'說明會場次2_結束時間')
	session_3_start = models.TimeField(u'說明會場次3_開始時間')
	session_3_end = models.TimeField(u'說明會場次3_結束時間')
	#費用
	session_1_fee = models.IntegerField(u'說明會場次1_費用')
	session_2_fee = models.IntegerField(u'說明會場次2_費用')
	session_3_fee = models.IntegerField(u'說明會場次3_費用')

	#就博會相關
	jobfair_start = models.DateTimeField(u'就博會開始時間')
	jobfair_end = models.DateTimeField(u'就博會結束時間')
	jobfair_booth_fee = models.IntegerField(u'就博會攤位費用(每攤)')

	class Meta:
		managed = True

		verbose_name = u"研替活動設定"
		verbose_name_plural =u"研替活動設定"

class Activity(models.Model):
	id = models.AutoField(primary_key=True)
	cid = models.CharField(u'公司統一編號',unique=True,max_length=8)
	seminar_noon = models.BooleanField(u'說明會中午')
	seminar_night = models.BooleanField(u'說明會晚上')
	enterprise_day= models.BooleanField(u'專屬企業日')
	job_fair = models.IntegerField(u'徵才展示會攤位數量')
	career_tutor = models.BooleanField(u'企業職場導師')
	visit = models.BooleanField(u'企業參訪')
	lecture = models.BooleanField(u'就業力講座')
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

#以下為就博會

class Jobfair_Slot(models.Model):

	id = models.AutoField(primary_key=True)
	serial_no = models.CharField(u'攤位編號',max_length=10)
	category = models.CharField(u'類別',max_length=37,choices=CATEGORYS)
	cid=models.OneToOneField('Activity',to_field='cid',on_delete=models.CASCADE)
	updated = models.DateTimeField(u'更新時間',auto_now=True)

	class Meta:
		managed = True
		verbose_name = u"就博會攤位"
		verbose_name_plural =u"就博會攤位"
	def __str__(self):
		return self.cid

class Jobfair_Order(models.Model):
	id = models.AutoField(primary_key=True)
	time = models.DateTimeField(u'選位開始時間')
	cid=models.OneToOneField('Activity',to_field='cid',on_delete=models.CASCADE)
	updated = models.DateTimeField(u'更新時間',auto_now=True)

	class Meta:
		managed = True
		verbose_name = u"就博會選位順序"
		verbose_name_plural =u"就博會選位順序"

class Jobfair_Info(models.Model):
	id = models.AutoField(primary_key=True)
	cid=models.OneToOneField('Activity',to_field='cid',on_delete=models.CASCADE)
	signname = models.CharField(u'攤位招牌名稱',max_length=30)
	contact = models.CharField(u'聯絡人',max_length=30)
	contact_mobile = models.CharField(u'聯絡人手機',max_length=16)
	contact_email = models.EmailField(u'聯絡人Email',max_length=254)
	parking_tickets = models.SmallIntegerField(u'停車證數量')
	power_req = models.CharField(u'用電需求',max_length=256)
	ps = models.EmailField(u'其它需求',max_length=254)
	updated = models.DateTimeField(u'更新時間',auto_now=True)

	class Meta:
		managed = True
		verbose_name = u"就博會資訊"
		verbose_name_plural =u"就博會資訊"

class Sponsor_Items(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(u'贊助品名稱',max_length=64,unique=True)
	description = models.CharField(u'贊助品說明',max_length=64)
	price = models.IntegerField(u'價格')
	limit = models.IntegerField(u'數量限制')
	pic =models.ImageField(u"贊助品預覽圖",upload_to = 'sponsor_items',null=True,help_text='''提供過去做的贊助品圖片，做為參考''')
	class Meta:
		managed = True
		verbose_name = u"贊助品"
		verbose_name_plural =u"贊助品"

class Sponsorship(models.Model):
	id = models.AutoField(primary_key=True)
	cid = models.ForeignKey('Activity',to_field='cid',on_delete=models.CASCADE)
	item = models.ForeignKey('Sponsor_Items',to_field='name',on_delete=models.CASCADE)


