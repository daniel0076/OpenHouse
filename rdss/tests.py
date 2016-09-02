from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse
from rdss.public_urls import urlpatterns as pub_urls
from rdss.internal_urls import urlpatterns as inter_urls

import rdss.views
import company.models

class UrlsTest(TestCase):

    def test_public(self):
        for url in pub_urls:
            response = self.client.get(reverse(url.name))
            self.assertEqual(response.status_code, 200)

    def test_internal(self):
        for url in inter_urls:
            response = self.client.get(reverse(url.name))
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
