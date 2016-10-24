from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory
from . import views

# Create your tests here.

class PublicPageTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    def test_index(self):
        # Create an instance of a GET request.
        request = self.factory.get('/')
        # an AnonymousUser instance.
        request.user = AnonymousUser()
        # Test my_view() as if it were deployed at /customer/details
        response = views.Index(request)
        # Use this syntax for class-based views.
        self.assertEqual(response.status_code, 200)

    def test_general_news(self):
        # Create an instance of a GET request.
        request = self.factory.get('/general_news')
        # an AnonymousUser instance.
        request.user = AnonymousUser()
        # Test my_view() as if it were deployed at /customer/details
        response = views.GeneralNewsListing(request)
        # Use this syntax for class-based views.
        self.assertEqual(response.status_code, 200)

    def test_recruit_news(self):
        # Create an instance of a GET request.
        request = self.factory.get('/recruit')
        # an AnonymousUser instance.
        request.user = AnonymousUser()
        # Test my_view() as if it were deployed at /customer/details
        response = views.RecruitNewsListing(request)
        # Use this syntax for class-based views.
        self.assertEqual(response.status_code, 200)

# Create your tests here.
