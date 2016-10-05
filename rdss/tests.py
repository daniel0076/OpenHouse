from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse
from rdss.public_urls import urlpatterns as pub_urls
from rdss.internal_urls import urlpatterns as inter_urls

import rdss.views
import company.models
import rdss.models

class UrlsTest(TestCase):
    def setUp(self):
        data = {"register_start": "2016-07-05T15:17:00Z",
             "register_end": "2016-07-23T15:17:00Z",
             "rdss_signup_start": "2016-06-20T16:09:00Z",
             "rdss_signup_end": "2016-10-18T16:09:00Z",
             "survey_start": "2016-08-18T10:00:00Z",
             "survey_end": "2016-08-18T10:08:00Z",
             "seminar_start_date": "2016-09-27",
             "seminar_end_date": "2016-10-18",
             "session1_start": "12:20:00", "session1_end": "13:10:00",
             "session2_start": "17:00:00", "session2_end": "17:50:00",
             "session3_start": "18:10:00", "session3_end": "18:50:00",
             "session1_fee": 100, "session2_fee": 100, "session3_fee": 100,
             "jobfair_date": "2016-10-14",
             "jobfair_start": "10:00:00", "jobfair_end": "16:00:00",
             "jobfair_booth_fee": 200}
        init_configs = rdss.models.RdssConfigs(**data)
        init_configs.save()

    def test_public(self):
        print("Testing all public url accessibility")
        for url in pub_urls:
            response = self.client.get(reverse(url.name))
            self.assertEqual(response.status_code, 200)

    def test_internal(self):
        for url in inter_urls:
            response = self.client.get(reverse(url.name))
            # AnonymousUser can't login
            self.assertEqual(response.status_code, 302)

class LoginReqTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    def test_anony(self):
        # Create an instance of a GET request.
        request = self.factory.get('/rdss/status')
        # an AnonymousUser instance.
        request.user = AnonymousUser()
        # Test my_view() as if it were deployed at /customer/details
        response = rdss.views.Status(request)
        # Use this syntax for class-based views.
        self.assertEqual(response.status_code, 302)
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

class CompanyTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(self):
        super(CompanyTest, self).setUpClass()
        self.driver = webdriver.PhantomJS()
        self.driver.implicitly_wait(5)
        #self.base_url = "http://idaniel.me:8000ate/"
        self.base_url = self.live_server_url
        self.verificationErrors = []
        self.accept_next_alert = True

    @classmethod
    def tearDownClass(self):
        self.driver.quit()
        super(CompanyTest, self).tearDownClass()

    def company_create(self):
        driver = self.driver
        driver.get(self.base_url + "/company/create/")
        driver.find_element_by_id("id_cid").clear()
        driver.find_element_by_id("id_cid").send_keys("66666666")
        driver.find_element_by_id("id_name").clear()
        driver.find_element_by_id("id_name").send_keys("test")
        driver.find_element_by_id("id_shortname").clear()
        driver.find_element_by_id("id_shortname").send_keys("test")
        driver.find_element_by_id("id_password1").clear()
        driver.find_element_by_id("id_password1").send_keys("test")
        driver.find_element_by_id("id_password2").clear()
        driver.find_element_by_id("id_password2").send_keys("test")
        driver.find_element_by_id("id_phone").clear()
        driver.find_element_by_id("id_phone").send_keys("04-000000")
        #driver.find_element_by_id("id_logo").clear()
        driver.find_element_by_id("id_logo").send_keys(u"{}/tests/test_logo.jpg".format(settings.BASE_DIR))
        driver.find_element_by_xpath("//div[@id='full']/form/div[4]/div[2]/div").click()
        driver.find_element_by_xpath("//div[@id='full']/form/div[4]/div[2]/div/div[2]/div[4]").click()
        Select(driver.find_element_by_id("id_category")).select_by_visible_text(u"光電光學")
        driver.find_element_by_id("id_postal_code").clear()
        driver.find_element_by_id("id_postal_code").send_keys("400")
        driver.find_element_by_id("id_address").clear()
        driver.find_element_by_id("id_address").send_keys("sdafasfd")
        driver.find_element_by_id("id_website").clear()
        driver.find_element_by_id("id_website").send_keys("http://dsaf.com")
        driver.find_element_by_id("id_hr_name").clear()
        driver.find_element_by_id("id_hr_name").send_keys("test")
        driver.find_element_by_id("id_hr_fax").clear()
        driver.find_element_by_id("id_hr_fax").send_keys("test")
        driver.find_element_by_id("id_hr_mobile").clear()
        driver.find_element_by_id("id_hr_mobile").send_keys("0987-555555")
        driver.find_element_by_id("id_hr_phone").clear()
        driver.find_element_by_id("id_hr_phone").send_keys("04-5050")
        driver.find_element_by_id("id_hr_email").clear()
        driver.find_element_by_id("id_hr_email").send_keys("gg@gg.com")
        driver.find_element_by_id("id_brief").clear()
        driver.find_element_by_id("id_brief").send_keys("ggg")
        driver.find_element_by_id("id_recruit_info").clear()
        driver.find_element_by_id("id_recruit_info").send_keys("ggg")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        self.assertEqual("OpenHouse 企業校園徵才 廠商入口", driver.find_element_by_xpath("//div[@id='container']/h1").text)
        print("測試創建公司帳號…OK")


    def company_login(self):
        driver = self.driver
        driver.get(self.base_url + "/company/login/")
        driver.find_element_by_name("username").clear()
        driver.find_element_by_name("username").send_keys("66666666")
        driver.find_element_by_name("password").clear()
        driver.find_element_by_name("password").send_keys("test")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        try: self.assertNotEqual("帳號或密碼錯誤", driver.find_element_by_xpath("//div[@id='full']/form/div[3]").text)
        except NoSuchElementException: print("測試登入…OK")

    def register_rdss(self):
        driver = self.driver
        driver.get(self.base_url + "/company/rdss/signup/")
        driver.find_element_by_id("id_jobfair").clear()
        driver.find_element_by_id("id_jobfair").send_keys("2")
        driver.find_element_by_css_selector("label").click()
        driver.find_element_by_xpath("//button[@type='submit']").click()
        self.assertEqual(u"報名已完成，您也可以修改報名資料，再次送出。", driver.find_element_by_xpath("//div[@id='full']/div/div[2]/form/div").text)
        print("測試報名研替…OK")

    def seminar_info_valid(self):
        driver = self.driver
        driver.get(self.base_url + "/company/rdss/seminar/info")
        driver.find_element_by_id("id_topic").clear()
        driver.find_element_by_id("id_topic").send_keys("test")
        driver.find_element_by_id("id_speaker").clear()
        driver.find_element_by_id("id_speaker").send_keys("test")
        driver.find_element_by_id("id_speaker_title").clear()
        driver.find_element_by_id("id_speaker_title").send_keys("test")
        driver.find_element_by_id("id_speaker_email").clear()
        driver.find_element_by_id("id_speaker_email").send_keys("test@test.com")
        driver.find_element_by_id("id_contact").clear()
        driver.find_element_by_id("id_contact").send_keys("test")
        driver.find_element_by_id("id_contact_mobile").clear()
        driver.find_element_by_id("id_contact_mobile").send_keys("0987-111111")
        driver.find_element_by_id("id_contact_email").clear()
        driver.find_element_by_id("id_contact_email").send_keys("test@test.com")
        driver.find_element_by_id("id_attendees").clear()
        driver.find_element_by_id("id_attendees").send_keys("0")
        driver.find_element_by_id("id_snack_box").clear()
        driver.find_element_by_id("id_snack_box").send_keys("2")
        driver.find_element_by_id("id_ps").clear()
        driver.find_element_by_id("id_ps").send_keys("")
        driver.find_element_by_id("id_qa_prize").clear()
        driver.find_element_by_id("id_qa_prize").send_keys("a")
        driver.find_element_by_id("id_qa_prize_amount").clear()
        driver.find_element_by_id("id_qa_prize_amount").send_keys("2")
        driver.find_element_by_id("id_raffle_prize").clear()
        driver.find_element_by_id("id_raffle_prize").send_keys("s")
        driver.find_element_by_id("id_raffle_prize_amount").clear()
        driver.find_element_by_id("id_raffle_prize_amount").send_keys("2")
        driver.find_element_by_id("id_attend_prize").clear()
        driver.find_element_by_id("id_attend_prize").send_keys("a")
        driver.find_element_by_id("id_attend_prize_amount").clear()
        driver.find_element_by_id("id_attend_prize_amount").send_keys("4")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        self.assertEqual(u"說明會資訊填寫已完成，您也可以修改資訊，再次送出。", driver.find_element_by_xpath("//div[@id='full']/div/div[2]/form/div").text)
        print("測試填寫說明會資訊…OK")

    def jobfair_info_valid(self):
        driver = self.driver
        driver.get(self.base_url + "/company/rdss/jobfair/info")
        driver.find_element_by_id("id_signname").clear()
        driver.find_element_by_id("id_signname").send_keys("test")
        driver.find_element_by_id("id_contact").clear()
        driver.find_element_by_id("id_contact").send_keys("test")
        driver.find_element_by_id("id_contact_mobile").clear()
        driver.find_element_by_id("id_contact_mobile").send_keys("0987-777777")
        driver.find_element_by_id("id_contact_email").clear()
        driver.find_element_by_id("id_contact_email").send_keys("test@test.com")
        driver.find_element_by_id("id_vege_lunchbox").clear()
        driver.find_element_by_id("id_vege_lunchbox").send_keys("1")
        driver.find_element_by_id("id_meat_lunchbox").clear()
        driver.find_element_by_id("id_meat_lunchbox").send_keys("1")
        driver.find_element_by_id("id_parking_tickets").clear()
        driver.find_element_by_id("id_parking_tickets").send_keys("1")
        driver.find_element_by_id("id_power_req").clear()
        driver.find_element_by_id("id_power_req").send_keys("laptop")
        driver.find_element_by_id("id_ps").clear()
        driver.find_element_by_id("id_ps").send_keys("test")
        driver.find_element_by_xpath("//button[@type='submit']").click()
        self.assertEqual(u"就博會資訊填寫已完成，您也可以修改資訊，再次送出。", driver.find_element_by_xpath("//div[@id='full']/div/div[2]/form/div").text)
        print("測試填寫就博會資訊…OK")

    def test_company(self):
        self.company_create()
        self.company_login()
        self.register_rdss()
        self.seminar_info_valid()
        self.jobfair_info_valid()

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True

    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
