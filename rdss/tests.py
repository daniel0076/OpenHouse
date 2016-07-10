from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory

import rdss.views
import company.models

# Create your tests here.

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
		response = rdss.views.ControlPanel(request)
		# Use this syntax for class-based views.
		self.assertEqual(response.status_code, 302)
