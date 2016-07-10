from django.db import models
import company.models
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

		verbose_name = u"1. 研替活動設定"
		verbose_name_plural =u"1. 研替活動設定"



class Signup(models.Model):
	SEMINAR_CHOICES = (
			(u'', u'不參加說明會'),
			(u'noon', u'中午場'),
			(u'night', u'晚上場'),
			(u'company_day', u'專屬企業日'),
			)
	id = models.AutoField(primary_key=True)
	cid = models.CharField(u'公司統一編號',unique=True,max_length=8,null=False)
	seminar = models.CharField(u'說明會場次',max_length=6,choices=SEMINAR_CHOICES,default='',blank=True)
	jobfair = models.IntegerField(u'徵才展示會攤位數量',default=0)
	career_tutor = models.BooleanField(u'企業職場導師')
	visit = models.BooleanField(u'企業參訪')
	lecture = models.BooleanField(u'就業力講座')
	#post_ad = models.BooleanField(u'刊登廣告')
	payment = models.BooleanField(u'完成付款',default=False)
	added = models.DateTimeField(u'報名時間',auto_now_add=True)
	updated = models.DateTimeField(u'更新時間',auto_now=True)

	class Meta:
		managed = True
		verbose_name = u"3. 活動報名情況"
		verbose_name_plural =u"3. 活動報名情況"
	def __str__(self):
		return self.cid

# Proxy model for AdminSite company list item
class Company(Signup):
	class Meta:
		proxy = True
		verbose_name = u"2. 參加廠商"
		verbose_name_plural =u"2. 參加廠商"


class Seminar_Slot(models.Model):
	# (value in db,display name)
	SESSIONS =  (
			("noon","中午場"),
			("night1","晚上場1"),
			("night2","晚上場2"),
			)
	id = models.AutoField(primary_key=True)
	date = models.DateField(u'日期')
	session = models.CharField(u'時段',max_length=6,choices=SESSIONS)
	cid=models.OneToOneField('Signup',to_field='cid',verbose_name = u'公司統編',on_delete=models.CASCADE,null=True,blank=True)
	updated = models.DateTimeField(u'更新時間',auto_now=True)

	class Meta:
		managed = True
		verbose_name = u"說明會場次"
		verbose_name_plural =u"說明會場次"
	#def __str__(self):

class Seminar_Order(models.Model):
	id = models.AutoField(primary_key=True)
	time = models.DateTimeField(u'選位開始時間')
	cid=models.OneToOneField('Signup',to_field='cid',verbose_name = u'公司統編',on_delete=models.CASCADE)
	updated = models.DateTimeField(u'更新時間',auto_now=True)

	class Meta:
		managed = True
		verbose_name = u"說明會選位順序"
		verbose_name_plural =u"說明會選位順序"

class Seminar_Info(models.Model):
	id = models.AutoField(primary_key=True)
	cid=models.OneToOneField('Signup',to_field='cid',verbose_name = u'公司統編',on_delete=models.CASCADE)
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
	cid=models.OneToOneField('Signup',to_field='cid',verbose_name = u'公司統編',on_delete=models.CASCADE,blank=True,null=True)
	updated = models.DateTimeField(u'更新時間',auto_now=True)

	class Meta:
		managed = True
		verbose_name = u"就博會攤位"
		verbose_name_plural =u"就博會攤位"
	def __str__(self):
		return self.serial_no

class Jobfair_Order(models.Model):
	id = models.AutoField(primary_key=True)
	time = models.DateTimeField(u'選位開始時間')
	cid=models.OneToOneField('Signup',to_field='cid',verbose_name = u'公司統編',on_delete=models.CASCADE)
	updated = models.DateTimeField(u'更新時間',auto_now=True)

	class Meta:
		managed = True
		verbose_name = u"就博會選位順序"
		verbose_name_plural =u"就博會選位順序"

class Jobfair_Info(models.Model):
	id = models.AutoField(primary_key=True)
	cid = models.OneToOneField('Signup',to_field='cid',verbose_name = u'公司統編',on_delete=models.CASCADE)
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
	description = models.CharField(u'贊助品說明',max_length=250)
	spec = models.CharField(u'規格',max_length=100,null=True,blank=True)
	ps = models.CharField(u'備註',max_length=100,null=True,blank=True)
	price = models.IntegerField(u'價格')
	limit = models.IntegerField(u'數量限制')
	pic =models.ImageField(u"贊助品預覽圖",upload_to = 'sponsor_items',null=True,help_text='''提供過去做的贊助品圖片，做為參考''')
	class Meta:
		managed = True
		verbose_name = u"4. 贊助品"
		verbose_name_plural =u"4. 贊助品"

class Sponsorship(models.Model):
	id = models.AutoField(primary_key=True)
	cid = models.ForeignKey('Signup',to_field='cid',verbose_name = u'公司統編',on_delete=models.CASCADE)
	item = models.ForeignKey('Sponsor_Items',to_field='name',on_delete=models.CASCADE)
	class Meta:
		unique_together = ("cid", "item")
		verbose_name = u"5. 贊助情況"
		verbose_name_plural =u"5. 贊助情況"

#TODO names
class CompanyVisit(models.Model):
	id = models.AutoField(primary_key=True)
	cid = models.ForeignKey('Signup',to_field='cid',verbose_name = u'公司統編',on_delete=models.CASCADE)
	time = models.DateTimeField(u'')
	limit = models.IntegerField(u'限制')

	class Meta:
		managed = True
		verbose_name = u""
		verbose_name_plural =u""

#TODO names
class Lectures(models.Model):
	id = models.AutoField(primary_key=True)
	cid = models.ForeignKey('Signup',to_field='cid',verbose_name = u'公司統編',on_delete=models.CASCADE)
	time = models.DateTimeField(u'')
	limit = models.IntegerField(u'限制')

	class Meta:
		managed = True
		verbose_name = u""
		verbose_name_plural =u""

class CareerTutor(models.Model):
	id = models.AutoField(primary_key=True)
	cid = models.ForeignKey('Signup',to_field='cid',verbose_name = u'公司統編',on_delete=models.CASCADE)
	time = models.DateTimeField(u'')
	limit = models.IntegerField(u'限制')

	class Meta:
		managed = True
		verbose_name = u""
		verbose_name_plural =u""
