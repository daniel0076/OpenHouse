from __future__ import unicode_literals
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.core.validators import RegexValidator,MinLengthValidator,validate_email
from django.utils import timezone
from datetime import datetime

def validate_all_num(string):
	if not string.isdigit():
		raise ValidationError('必需都是數字')

def validate_mobile(string):
	RegexValidator(regex='^\d{4}-\d{6}$',message='手機格式為：0987-654321')(string)

def validate_phone(string):
	RegexValidator(regex='^\d+-\d+(#\d+)?$',message='電話/傳真格式為：區碼-號碼#分機')(string)


class Company(AbstractBaseUser):
	CATEGORYS = (
			(u'半導體', u'半導體'),
			(u'消費電子', u'消費電子'),
			(u'網路通訊', u'網路通訊'),
			(u'光電光學', u'光電光學'),
			(u'資訊軟體', u'資訊軟體'),
			(u'集團', u'集團'),
			(u'綜合', u'綜合'),
			(u'人力銀行', u'人力銀行'),
			(u'機構', u'機構')
			)

	id = models.AutoField(primary_key=True)
	cid = models.CharField(u'公司統一編號',unique=True,max_length=8)
	name = models.CharField(u'公司名稱',max_length=64)
	shortname = models.CharField(u'公司簡稱',max_length=20)
	category = models.CharField(u'類別',max_length=37,choices=CATEGORYS,help_text='公司主要事業類別')
	phone = models.CharField(u'公司電話',max_length=32,validators=[validate_phone],help_text='格式: 區碼-號碼#分機')
	postal_code = models.CharField(u'郵遞區號',max_length=5,validators=[validate_all_num])
	address = models.CharField(u'公司地址',max_length=128)
	website = models.CharField(u'公司網站',max_length=64)
	brief = models.CharField(u'公司簡介',max_length=110,help_text='為了印刷效果，限110字內')
	introduction = models.CharField(u'公司介紹',max_length=260,help_text='為了印刷效果，限260字內')
	hr_name = models.CharField(u'人資姓名',max_length=32)
	hr_phone = models.CharField(u'人資電話',max_length=32,validators=[validate_phone],help_text='格式: 區碼-號碼#分機')
	hr_fax = models.CharField(u'人資傳真',max_length=32,help_text='格式: 區碼-號碼#分機')
	hr_mobile = models.CharField(u'人資手機',max_length=32,validators=[validate_mobile],help_text='格式: 0912-345678')
	hr_email = models.CharField(u'人資Email',max_length=64,validators=[validate_email])
	logo=models.ImageField(u"公司LOGO",upload_to = 'company_logos',null=True,help_text='''網站展示、筆記本內頁公司介紹使用，僅接受 jpg, png, gif 格式。建議解析度為 300 dpi以上，以達到最佳效果。''')
	last_update= models.DateTimeField(u'更新時間',auto_now=True,null=True)
	date_join = models.DateTimeField(u'date joined', auto_now_add=True)
	objects=UserManager()
	USERNAME_FIELD='cid'

	class Meta:
		managed = True
		db_table = 'company'

		verbose_name = u"總廠商列表"
		verbose_name_plural =u"總廠商列表" #上面的複數ZZZ

	def __str__(self):
		return self.get_full_name()

	def get_full_name(self):
		return u'{0} - {1}'.format(self.cid, self.shortname)

	def get_short_name(self):
		return self.shortname

	def get_cid(self): #for get cid
		return self.cid

	@property
	def username(self):
		return self.cid

	@property
	def is_staff(self):
		return False

	@property
	def is_active(self):
		return True

	@property
	def is_superuser(self):
		return False

	def has_module_perms(self, app_label):
		return False

	def has_perm(self,perm, obj=None):
		return False
