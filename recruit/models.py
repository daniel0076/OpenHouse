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
    recruit_signup_start = models.DateTimeField(u'校徵報名開始時間')
    recruit_signup_end = models.DateTimeField(u'校徵報名結束時間')

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
        (u'none', u'不參加說明會'),
        (u'noon', u'中午場'),
        (u'night', u'下午/傍晚場'),
    )
    cid = models.CharField(u'公司統一編號', max_length=8, unique=True)
    seminar = models.CharField(u'說明會場次', choices=SEMINAR_CHOICES, max_length=15, default='none')
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

class Files(models.Model):
    FILE_CAT = (
            ('企畫書', '企畫書'),
            ('報名說明書', '報名說明書'),
            ('選位相關', '選位相關'),
            ('就博會攤位圖', '就博會攤位圖'),
            ('其它', '其它'),
            )
    id = models.AutoField(primary_key=True)
    title = models.CharField(u'標題', max_length=30)
    category = models.CharField(u'類型', max_length=10, choices=FILE_CAT)
    upload_file = models.FileField(u'上傳檔案',
                                   upload_to='rdss_files', null=False)
    updated = models.DateTimeField(u'更新時間', auto_now=True)

    class Meta:
        verbose_name = u"活動檔案"
        verbose_name_plural = u"活動檔案"

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
    company = models.OneToOneField(RecruitSignup, verbose_name=u'公司')
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

class SeminarInfo(models.Model):
    company = models.OneToOneField(RecruitSignup)
    topic = models.CharField(max_length=40)
    speaker = models.CharField(max_length=5)
    speaker_title = models.CharField(max_length=10)
    speaker_email = models.EmailField()

class SeminarSlot(models.Model):

    class Meta:
        verbose_name = u'說明會場次'
        verbose_name_plural = u'說明會場次'

class SponsorItem(models.Model):
    name = models.CharField(u'贊助品名稱', max_length=20, unique=True)
    description = models.CharField(u'贊助品說明', max_length=100)
    spec = models.CharField(u'規格', blank=True, null=True, max_length=100)
    ps = models.CharField(u'備註', blank=True, null=True, max_length=100)
    price = models.IntegerField(u'價格')
    number_limit = models.IntegerField(u'數量限制')
    pic = models.ImageField(u'贊助品預覽圖', upload_to='recruit_sponsor_item', null=True)
    sponsors = models.ManyToManyField(RecruitSignup, through='SponsorShip')
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = u'贊助品'
        verbose_name_plural = u'贊助品'

class SponsorShip(models.Model):
    company = models.ForeignKey(RecruitSignup, to_field='cid', on_delete=models.CASCADE)
    sponsor_item = models.ForeignKey(SponsorItem, to_field='name', on_delete=models.CASCADE)
    updated = models.DateTimeField(u'更新時間', auto_now=True)
    class Meta:
        verbose_name = u'贊助情況'
        verbose_name_plural = u'贊助情況'
        unique_together = ('company', 'sponsor_item')

class CompanySurvey(models.Model):
    RATING = (
            (u'優', u'優'),
            (u'佳', u'佳'),
            (u'普通', u'普通'),
            (u'差', u'差'),
            (u'劣', u'劣'),
            )

    ee_bachelor     = models.IntegerField(u'電機學院-大學人數', default=0)
    ee_master       = models.IntegerField(u'電機學院-碩士人數', default=0)
    ee_phd          = models.IntegerField(u'電機學院-博士人數', default=0)
    ee_satisfaction = models.CharField(u'電機學院 - 平均滿意度', max_length=2, choices=RATING,
                                       null=True, blank=True
                                       )
    cs_bachelor     = models.IntegerField(u'資訊學院-大學人數', default=0)
    cs_master       = models.IntegerField(u'資訊學院-碩士人數', default=0)
    cs_phd          = models.IntegerField(u'資訊學院-博士人數', default=0)
    cs_satisfaction = models.CharField(u'資訊學院 - 平均滿意度', max_length=2, choices=RATING,
                                       null=True, blank=True)
    manage_bachelor = models.IntegerField(u'管理學院-大學人數', default=0)
    manage_master   = models.IntegerField(u'管理學院-碩士人數', default=0)
    manage_phd      = models.IntegerField(u'管理學院-博士人數', default=0)
    manage_satisfaction = models.CharField(u'管理學院 - 平均滿意度', max_length=2, choices=RATING,
                                           null=True, blank=True)
    bio_bachelor    = models.IntegerField(u'生科學院-大學人數', default=0)
    bio_master      = models.IntegerField(u'生科學院-碩士人數', default=0)
    bio_phd         = models.IntegerField(u'生科學院-博士人數', default=0)
    bio_satisfaction = models.CharField(u'生科學院 - 平均滿意度', max_length=2, choices=RATING,
                                        null=True, blank=True)
    sci_bachelor    = models.IntegerField(u'理學院-大學人數', default=0)
    sci_master      = models.IntegerField(u'理學院-碩士人數', default=0)
    sci_phd         = models.IntegerField(u'理學院-博士人數', default=0)
    sci_satisfaction = models.CharField(u'理學院 - 平均滿意度', max_length=2, choices=RATING,
                                        null=True, blank=True)
    eng_bachelor    = models.IntegerField(u'工學院-大學人數', default=0)
    eng_master      = models.IntegerField(u'工學院-碩士人數', default=0)
    eng_phd         = models.IntegerField(u'工學院-博士人數', default=0)
    eng_satisfaction = models.CharField(u'工學院 - 平均滿意度', max_length=2, choices=RATING,
                                        null=True, blank=True)
    hs_bachelor     = models.IntegerField(u'人社學院-大學人數', default=0)
    hs_master       = models.IntegerField(u'人社學院-碩士人數', default=0)
    hs_phd          = models.IntegerField(u'人社學院-博士人數', default=0)
    hs_satisfaction = models.CharField(u'人社學院 - 平均滿意度', max_length=2, choices=RATING,
                                       null=True, blank=True)
    haka_bachelor   = models.IntegerField(u'客家學院-大學人數', default=0)
    haka_master     = models.IntegerField(u'客家學院-碩士人數', default=0)
    haka_phd        = models.IntegerField(u'客家學院-博士人數', default=0)
    haka_satisfaction = models.CharField(u'客家學院 - 平均滿意度', max_length=2, choices=RATING,
                                         null=True, blank=True)
    overall_satisfaction = models.CharField(u'整體滿意度', max_length=2, choices=RATING, null=True, blank=True)

    #salary
    SALARY_MONTH=(
            (u'4萬以下', u'4萬以下'),
            (u'4~5萬', u'4~5萬'),
            (u'5~6萬', u'5~6萬'),
            (u'6萬以上', u'6萬以上'),
            )
    SALARY_YEAR=(
            (u'50萬以下', u'50萬以下'),
            (u'50~70萬', u'50~70萬'),
            (u'70~100萬', u'70~100萬'),
            (u'100萬以上', u'100萬以上'),
            )
    salary_avg_bachelor = models.CharField(u'大學平均月薪', max_length=8, choices =SALARY_MONTH)
    salary_avg_master   = models.CharField(u'碩士平均月薪', max_length=8, choices =SALARY_MONTH)
    salary_avg_phd      = models.CharField(u'博士平均月薪', max_length=8, choices =SALARY_MONTH)
    nctu_salary_avg_bachelor    = models.CharField(u'大學平均年薪', max_length=8, choices =SALARY_YEAR)
    nctu_salary_avg_master      = models.CharField(u'碩士平均年薪', max_length=8, choices =SALARY_YEAR)
    nctu_salary_avg_phd         = models.CharField(u'博士平均年薪', max_length=8, choices =SALARY_YEAR)

    #ability
    no_nctu_employee        = models.BooleanField(u'目前無交大畢業生在職')
    professional_skill_rate = models.CharField(u'專業知能', max_length=4, choices=RATING, null=True, blank=True)
    foreign_lang_rate       = models.CharField(u'外語能力', max_length=4, choices=RATING, null=True, blank=True)
    document_process_rate   = models.CharField(u'文書處理', max_length=4, choices=RATING, null=True, blank=True)
    info_literacy_rate      = models.CharField(u'資訊素養', max_length=4, choices=RATING, null=True, blank=True)
    problem_solving_rate    = models.CharField(u'發現及解決問題', max_length=4, choices=RATING, null=True, blank=True)
    attitude_rate           = models.CharField(u'工作態度', max_length=4, choices=RATING, null=True, blank=True)
    civic_duty_rate         = models.CharField(u'公民責任', max_length=4, choices=RATING, null=True, blank=True)
    pro_moral_rate          = models.CharField(u'專業倫理', max_length=4, choices=RATING, null=True, blank=True)
    humanities_rate         = models.CharField(u'人文及在地關懷', max_length=4, choices=RATING, null=True, blank=True)
    cultural_rate           = models.CharField(u'人文藝術陶冶', max_length=4, choices=RATING, null=True, blank=True)
    international_view_rate = models.CharField(u'國際視野', max_length=4, choices=RATING, null=True, blank=True)
    diverse_thinking_rate   = models.CharField(u'跨界多元思考', max_length=4, choices=RATING, null=True, blank=True)
    group_cognitive_rate        = models.CharField(u'群己平衡認知', max_length=4, choices=RATING, null=True, blank=True)

    #ability choice
    professional_skill  = models.BooleanField(u'專業知能')
    foreign_lang        = models.BooleanField(u'外語能力')
    document_process    = models.BooleanField(u'文書處理')
    info_literacy       = models.BooleanField(u'資訊素養')
    problem_solving     = models.BooleanField(u'發現及解決問題')
    attitude            = models.BooleanField(u'工作態度')
    civic_duty          = models.BooleanField(u'公民責任')
    pro_moral           = models.BooleanField(u'專業倫理')
    humanities          = models.BooleanField(u'人文及在地關懷')
    cultural            = models.BooleanField(u'人文藝術陶冶')
    international_view  = models.BooleanField(u'國際視野')
    diverse_thinking    = models.BooleanField(u'跨界多元思考')
    group_cognitive     = models.BooleanField(u'群己平衡認知')
    other               = models.CharField(u'其它', max_length=100, blank=True, null=True)

    #exp
    HELPFUL_RATE = (
            (u'無幫助', u'無幫助'),
            (u'略有幫助', u'略有幫助'),
            (u'有幫助', u'有幫助'),
            (u'頗有幫助', u'頗有幫助'),
            (u'極有幫助', u'極有幫助'),
            )

    major               = models.CharField(u'主修科系', max_length=4, choices=HELPFUL_RATE)
    graduation_school   = models.CharField(u'畢業學校', max_length=4, choices=HELPFUL_RATE)
    second_major        = models.CharField(u'輔系、雙學位、學程', max_length=4, choices=HELPFUL_RATE)
    club                = models.CharField(u'社團經驗', max_length=4, choices=HELPFUL_RATE)
    common_class        = models.CharField(u'通識教育', max_length=4, choices=HELPFUL_RATE)
    national_exam       = models.CharField(u'國家考試證書', max_length=4, choices=HELPFUL_RATE)
    cert                = models.CharField(u'證照', max_length=4, choices=HELPFUL_RATE)
    work_exp            = models.CharField(u'相關工作經驗（打工、習實）', max_length=4, choices=HELPFUL_RATE)
    travel_study        = models.CharField(u'遊學（如交換學生）', max_length=4, choices=HELPFUL_RATE)

    #ways to recruit
    hr_bank             = models.BooleanField(u'人力銀行')
    newspaper_ad        = models.BooleanField(u'報章廣告')
    website             = models.BooleanField(u'公司網頁')
    school              = models.BooleanField(u'學校宣傳')
    teacher_recommend   = models.BooleanField(u'老師推薦')
    campus_jobfair      = models.BooleanField(u'校園徵才')
    contest             = models.BooleanField(u'競賽活動')

    #receive info
    receive_info        = models.BooleanField(u'我希望定期接收校園徵才活動訊息')
    suggestions         = models.CharField(u'其它建議', max_length=150, blank=True, null=True)

    #basic info
    cid = models.CharField(u'公司統一編號', unique=True, max_length=8, null=False)
    company             = models.CharField(u'企業名稱', max_length=50)
    submiter_name           = models.CharField(u'填寫人姓名', max_length=20)
    submiter_phone      = models.CharField(u'填寫人電話', max_length=20)
    submiter_email      = models.CharField(u'填寫人Email', max_length=50)
    SIZE = (
            (u'1~100人', u'1~100人'),
            (u'101~500人', u'101~500人'),
            (u'500~1000人', u'500~1000人'),
            (u'1001~5000人', u'1001~5000人'),
            (u'5000~10000人', u'5000~10000人'),
            (u'10000~20000人', u'10000~20000人'),
            (u'30000人以上', u'30000人以上'),
            )
    company_size        = models.CharField(u'貴企業規模', max_length=20, choices=SIZE)
    nctu_employees      = models.IntegerField(u'交大校友人數')
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
    category            = models.CharField(u'企業類別', max_length=10, choices=CATEGORYS)
    updated = models.DateTimeField(u'更新時間', auto_now=True)

    class Meta:
        managed = True
        verbose_name = u"企業滿意度問卷"
        verbose_name_plural =u"企業滿意度問卷"
