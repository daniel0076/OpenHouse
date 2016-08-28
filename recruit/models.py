from django.db import models
from company.models import Company
CATEGORYS = (
            (u'半導體',  u'半導體'),
            (u'消費電子',  u'消費電子'),
            (u'網路通訊',  u'網路通訊'),
            (u'光電光學',  u'光電光學'),
            (u'資訊軟體',  u'資訊軟體'),
            (u'集團',  u'集團'),
            (u'綜合',  u'綜合'),
            (u'人力銀行',  u'人力銀行'),
            (u'機構',  u'機構'),
            (u'化工/化學',  u'化工/化學'),
            (u'傳產/製造',  u'傳產/製造'),
            (u'工商/服務',  u'工商/服務'),
            (u'教育、政府及團體',  u'教育、政府及團體'),
            (u'醫藥/農牧',  u'醫藥/農牧'),
            (u'民生消費',  u'民生消費'),
            (u'媒體/出版',  u'媒體/出版'),
            (u'貿易/流通',  u'貿易/流通'),
            (u'不動產相關',  u'不動產相關'),
)



class RecruitConfigs(models.Model):
    register_start = models.DateTimeField(u'廠商註冊開始時間')
    register_end = models.DateTimeField(u'廠商註冊結束時間')
    recruit_signup_start = models.DateTimeField(u'研替報名開始時間')
    recruit_signup_end = models.DateTimeField(u'研替報名結束時間')

    survey_start = models.DateTimeField(u'滿意度問卷開始填答')
    survey_end = models.DateTimeField(u'滿意度問卷結束填答')

    # 說明會相關
    seminar_start_date = models.DateField(u'說明會開始日期')
    seminar_end_date = models.DateField(u'說明會結束日期')
    session_1_start = models.TimeField(u'說明會場次1_開始時間')
    session_1_end = models.TimeField(u'說明會場次1_結束時間')
    session_2_start = models.TimeField(u'說明會場次2_開始時間')
    session_2_end = models.TimeField(u'說明會場次2_結束時間')
    session_3_start = models.TimeField(u'說明會場次3_開始時間')
    session_3_end = models.TimeField(u'說明會場次3_結束時間')
    session_4_start = models.TimeField(u'說明會場次4_開始時間')
    session_4_end = models.TimeField(u'說明會場次4_結束時間')
    # 費用
    session_1_fee = models.IntegerField(u'說明會場次1_費用')
    session_2_fee = models.IntegerField(u'說明會場次2_費用')
    session_3_fee = models.IntegerField(u'說明會場次3_費用')
    session_4_fee = models.IntegerField(u'說明會場次4_費用')

    jobfair_date = models.DateField(u'就博會日期')
    jobfair_start = models.TimeField(u'就博會開始時間')
    jobfair_end = models.TimeField(u'就博會結束時間')
    jobfair_booth_fee = models.IntegerField(u'就博會攤位費用(每攤)')

    class Meta:
       managed = True
       verbose_name = u'校徵活動設定'
       verbose_name_plural = u'校徵活動設定'


class RecruitSignup(models.Model):
    SEMINAR_CHOICES = (
        (u'', u'不參加說明會'),
        (u'noon', u'中午場'),
        (u'night', u'晚上場'),
        (u'company_day', u'專屬企業日'),
    )
    cid = models.CharField(u'公司統一編號',max_length=8)
    seminar = models.CharField(u'說明會場次', choices=SEMINAR_CHOICES, max_length=15, default='')
    jobfair = models.IntegerField(u'徵才展示會攤位數量', default=0)
    career_tutor = models.BooleanField(u'企業職場導師')
    company_visit = models.BooleanField(u'企業參訪')
    lecture = models.BooleanField(u'就業力講座')
    payment = models.BooleanField(u'完成付款', default=False)
    receipt_no = models.CharField(u'收據號碼', blank=True, null=True, max_length=50)
    ps = models.TextField(u'備註', blank=True, null=True)
    added = models.TimeField(u'報名時間', auto_now_add=True)
    updated = models.TimeField(u'更新時間',auto_now=True)
    def __str__(self):
        company = Company.objects.get(cid=self.cid)
        return company.name
    class Meta:
        managed = True
        verbose_name = u'活動報名情況'
        verbose_name_plural = u'活動報名情況'

class JobfairSlot(models.Model):
    id = models.AutoField(primary_key=True)
    serial_number = models.CharField(u'攤位編號', max_length=8)
    cid = models.ForeignKey(RecruitSignup, on_delete=models.CASCADE, verbose_name=u'公司')
    category = models.CharField(u'類別', max_length=15, choices=CATEGORYS)
    class Meta:
        managed = True
        verbose_name = u'就博會攤位'
        verbose_name_plural = u'就博會攤位'

class JobfairInfo(models.Model):
    id = models.AutoField(primary_key=True)
    cid = models.OneToOneField(RecruitSignup, verbose_name=u'公司')
    sign_name = models.CharField(u'攤位招牌名稱', max_length=20)
    contact_person = models.CharField(u'聯絡人', max_length=10)
    contact_mobile = models.CharField(u'聯絡人手機', max_length=10)
    contact_email = models.EmailField(u'聯絡人Email', max_length=20)
    packing_tickets = models.IntegerField(u'停車證數量')
    power_req = models.CharField(u'用電需求', max_length=30, blank=True, null=True)
    ps = models.CharField(u'備註', max_length=50, blank=True, null=True)
    class Meta:
        managed = True
        verbose_name = u'就博會資訊'
        verbose_name_plural = u'就博會資訊'

class SeminarSlot(models.Model):

    class Meta:
        verbose_name = u'說明會場次'
        verbose_name_plural = u'說明會場次'