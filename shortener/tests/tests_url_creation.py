from django.test import TestCase, Client
from shortener.models import URLMapping

class URLCreationTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_url_creation(self):
        # Ensure trailing slash is present to avoid 301 redirect
        url = '/api/shorten/' 
        data = {'url': 'https://www.google.com'}
        response = self.client.post(url, data, content_type='application/json')
        
        # We expect 201 Created
        self.assertEqual(response.status_code, 201)

        