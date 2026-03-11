from django.test import TestCase, Client
from shortener.models import URLMapping

class URLRedirectionTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_redirection(self):
        obj = URLMapping.objects.create(original_url="https://www.uber.com")
        # Assuming your redirect path is '<str:short_code>/'
        response = self.client.get(f'/{obj.short_code}/')
        
        # URL shorteners should use 302 to maintain analytics tracking
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "https://www.uber.com")
        