from django.test import TestCase, Client
from .models import URLMapping

class URLShortenerTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_url_creation(self):
        # Ensure trailing slash is present to avoid 301 redirect
        url = '/api/shorten/' 
        data = {'url': 'https://www.google.com'}
        response = self.client.post(url, data, content_type='application/json')
        
        # We expect 201 Created
        self.assertEqual(response.status_code, 201)

    def test_redirection(self):
        obj = URLMapping.objects.create(original_url="https://www.uber.com")
        # Assuming your redirect path is '<str:short_code>/'
        response = self.client.get(f'/{obj.short_code}/')
        
        # URL shorteners should use 302 to maintain analytics tracking
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "https://www.uber.com")
        