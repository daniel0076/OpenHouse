from django.db import models

# Create your models here.

class Configs(models.Model):
	signup_start = models.DateTimeField(u'廠商註冊開始時間')
	signup_end = models.DateTimeField(u'廠商註冊結束時間')
	rdss_signup_start = models.DateTimeField(u'研替報名開始時間')
	rdss_signup_end = models.DateTimeField(u'研替報名結束時間')
