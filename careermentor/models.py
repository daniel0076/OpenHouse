from django.db import models
from company import models as company

class CareerMentor(models.Model):
    id = models.AutoField(primary_key=True)
    company = models.CharField(u'廠商', max_length=100)
    cid = models.CharField(u'公司統一編號', unique=True, max_length=8, default='', blank=True)
    title = models.CharField(u'標題', max_length=100)
    abstract = models.TextField(u'大鋼')
    date = models.DateField(u'日期')
    start_time = models.TimeField(u'開始時間')
    end_time = models.TimeField(u'結束時間')
    mentor = models.CharField(u'導師', max_length=30, default='', blank=True)
    mentor_brief = models.TextField(u'導師介紹')
    mentor_title = models.CharField(u'導師稱謂', max_length=30, default='', blank=True)
    mentor_email = models.EmailField(u'導師Email', max_length=254, default='', blank=True)
    mode = models.CharField(u'進行方式', max_length=50, default='', blank=True)
    place = models.CharField(u'地點', max_length=50)
    limit = models.IntegerField(u'人數限制', help_text='0表不限')
    remark = models.CharField(u'備註', max_length=100, default='', blank=True)
    updated = models.DateTimeField(u'更新時間', auto_now=True)

    class Meta:
        managed = True
        verbose_name = u"企業職場導師/職涯教練"
        verbose_name_plural = u"企業職場導師/職涯教練"

class CareerMentorSignup(models.Model):
    id = models.AutoField(primary_key=True)
    career_mentor = models.ForeignKey(CareerMentor, to_field='id',
                                      verbose_name=u'場次',
                                      on_delete=models.CASCADE)
    name = models.CharField(u'姓名', max_length=64, blank=True)
    student_id = models.CharField(u'學號', max_length=7, blank=True)
    dep = models.CharField(u'系級', max_length=16, blank=True)
    phone = models.CharField(u'手機', max_length=20, blank=True,
                             help_text='格式：0987654321')
    email = models.EmailField(u'Email', max_length=64, blank=True)
    time_available = models.CharField(u'場次時段內可以的時間',max_length=100)
    question = models.CharField(u'諮詢的內容', max_length=100, default='', blank=True)
    remark = models.CharField(u'備註', max_length=100, default='', blank=True)
    cv_en = models.FileField(u'履歷(英文)上傳',upload_to='career_mentor', blank=True, null=True)
    cv_zh = models.FileField(u'履歷(中文)上傳',upload_to='career_mentor', blank=True, null=True)
    other = models.FileField(u'其它資料上傳',upload_to='career_mentor', blank=True, null=True)
    updated = models.DateTimeField(u'更新時間', auto_now=True)

    class Meta:
        managed = True
        verbose_name = u"學生登記"
        verbose_name_plural = u"學生登記"
