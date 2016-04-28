from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager,Group
from django.core.validators import RegexValidator,MinLengthValidator,validate_email
from django.utils import timezone

def validate_all_num(string):
	if not string.isdigit():
		raise ValidationError('必需都是數字')

def validate_mobile(string):
	RegexValidator(regex='^\d{4}-\d{6}$',message='格式：0987-654321')(string)

def validate_phone(string):
	RegexValidator(regex='^\d+-\d+(#\d+)?$',message='格式：區碼-號碼#分機')(string)


class Staff(AbstractBaseUser):
	GENDER = (('M', u'男生'), ('F', u'女生'))
	ROLE = (
			(u'就輔組',         u'就輔組'       ),
			(u'行政組 - 總召',  u'行政組 - 總召'),
			(u'行政組 - 副召',  u'行政組 - 副召'),
			(u'行政組 - 執秘',  u'行政組 - 執秘'),

			(u'廠聯組 - 組長',  u'廠聯組 - 組長'),
			(u'廠聯組 - 組員',  u'廠聯組 - 組員'),

			(u'設計組 - 組長',  u'設計組 - 組長'),
			(u'設計組 - 組員',  u'設計組 - 組員'),

			(u'活動組 - 組長',  u'活動組 - 組長'),
			(u'活動組 - 組員',  u'活動組 - 組員'),

			(u'資訊組 - 組長',  u'資訊組 - 組長'),
			(u'資訊組 - 組員',  u'資訊組 - 組員'),

			(u'專刊組 - 組長',  u'專刊組 - 組長'),
			(u'專刊組 - 組員',  u'專刊組 - 組員'),

			)

	id = models.AutoField(primary_key=True)
	username = models.CharField(u'學號',unique=True,max_length=10)
	name = models.CharField(u'姓名',max_length=10)
	gender = models.CharField(u'性別', choices=GENDER, max_length=1)
	birthday = models.DateField(u'出生年月日', default=timezone.now)
	idno= models.CharField(u'身份證字號',max_length=10)
	role = models.CharField(u'職位', choices=ROLE, blank=True, max_length=10)
	mobile = models.CharField(u'手機',max_length=12,validators=[validate_mobile],help_text='格式: 0912-345678')
	email = models.CharField(u'Email',max_length=64,validators=[validate_email])
	fb_url = models.URLField(u'FB個人首頁連結', default='')
	account = models.CharField(u'郵局或玉山帳號', max_length=15,help_text='必需為自己的名字')
	groups = models.ManyToManyField(Group, blank=True, related_name='staff_groups' ,
			related_query_name='staff_groups')
	last_update= models.DateTimeField(u'更新時間',auto_now=True,null=True)
	date_joined = models.DateTimeField(u'date joined', auto_now_add=True)
	is_active = models.BooleanField(u'啟用', default=False)
	is_superuser= models.BooleanField(u'最高權限', default=False)
	is_staff = models.BooleanField(u'後台權限', default=False)
	objects=UserManager()

	USERNAME_FIELD='username'
	REQUIRED_FIELDS = ['email']

	class Meta:
		managed = True
		db_table = 'staff'

		verbose_name = u"OpenHouse 工作人員"
		verbose_name_plural =u"OpenHouse 工作人員" #上面的複數ZZZ

	def __str__(self):
		return self.get_full_name()

	def get_full_name(self):
		return self.name

	def get_short_name(self):
		return self.name

	def get_username(self): #for get cid
		return self.username

	def has_module_perms(self, app_label):
		"""
		Returns True if the user has any permissions in the given app label.
		Uses pretty much the same logic as has_perm, above.
		"""
		# Active superusers have all permissions.
		if self.is_active and self.is_superuser:
			return True
		return False

	def has_perm(self,perm, obj=None):
		return False
