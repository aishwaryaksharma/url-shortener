from django.test import TestCase, Client
from django.contrib.messages import get_messages
from shortener.models import URLMapping

class HomeViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_home_page(self):
        """Test that GET request to home page renders the template successfully"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shortener/home.html')
        # Should not have short_url in context for GET request
        self.assertNotIn('short_url', response.context)

    def test_post_valid_url(self):
        """Test POST request with valid URL creates mapping and shows success"""
        url = 'https://www.example.com'
        response = self.client.post('/', {'url': url})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shortener/home.html')

        # Check that URLMapping was created
        mapping = URLMapping.objects.get(original_url=url)
        self.assertIsNotNone(mapping)
        self.assertEqual(mapping.original_url, url)

        # Check context contains the expected data
        self.assertIn('short_url', response.context)
        self.assertIn('original_url', response.context)
        self.assertEqual(response.context['original_url'], url)
        expected_short_url = f"http://localhost:8000/{mapping.short_code}"
        self.assertEqual(response.context['short_url'], expected_short_url)

    def test_post_empty_url(self):
        """Test POST request with empty URL shows error message"""
        response = self.client.post('/', {'url': ''})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shortener/home.html')

        # Check that no URLMapping was created
        self.assertEqual(URLMapping.objects.count(), 0)

        # Check error message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Please enter a URL')
        self.assertEqual(messages[0].level_tag, 'error')

    def test_post_invalid_url(self):
        """Test POST request with invalid URL format shows error message"""
        invalid_url = 'not-a-valid-url'
        response = self.client.post('/', {'url': invalid_url})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shortener/home.html')

        # Check that no URLMapping was created
        self.assertEqual(URLMapping.objects.count(), 0)

        # Check error message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Invalid URL format')
        self.assertEqual(messages[0].level_tag, 'error')

    def test_post_url_without_scheme(self):
        """Test POST request with URL missing scheme (should be invalid)"""
        url_without_scheme = 'www.example.com'
        response = self.client.post('/', {'url': url_without_scheme})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shortener/home.html')

        # Check that no URLMapping was created
        self.assertEqual(URLMapping.objects.count(), 0)

        # Check error message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Invalid URL format')

    def test_post_url_with_http_scheme(self):
        """Test POST request with valid HTTP URL"""
        url = 'http://www.example.com'
        response = self.client.post('/', {'url': url})

        self.assertEqual(response.status_code, 200)

        # Check that URLMapping was created
        mapping = URLMapping.objects.get(original_url=url)
        self.assertIsNotNone(mapping)
        self.assertEqual(mapping.original_url, url)

        # Check context
        self.assertIn('short_url', response.context)
        expected_short_url = f"http://localhost:8000/{mapping.short_code}"
        self.assertEqual(response.context['short_url'], expected_short_url)

    def test_post_url_with_https_scheme(self):
        """Test POST request with valid HTTPS URL"""
        url = 'https://www.example.com/path?query=value'
        response = self.client.post('/', {'url': url})

        self.assertEqual(response.status_code, 200)

        # Check that URLMapping was created
        mapping = URLMapping.objects.get(original_url=url)
        self.assertIsNotNone(mapping)
        self.assertEqual(mapping.original_url, url)

        # Check context
        self.assertIn('short_url', response.context)
        expected_short_url = f"http://localhost:8000/{mapping.short_code}"
        self.assertEqual(response.context['short_url'], expected_short_url)