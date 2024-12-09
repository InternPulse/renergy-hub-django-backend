from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

class CartAbandonmentRateAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_abandonment_rate(self):
        url = reverse('abandonment_rate')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(response.data['abandonment_rate'])
        self.assertEqual(response.data['total_carts'], 0)
        self.assertEqual(response.data['abandoned_carts'], 0)
        self.assertEqual(response.data['message'], 'Cart abandonment data is not available yet.')

    def test_get_abandonment_rate_slash(self):
        url = reverse('abandonment_rate_slash')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(response.data['abandonment_rate'])
        self.assertEqual(response.data['total_carts'], 0)
        self.assertEqual(response.data['abandoned_carts'], 0)
        self.assertEqual(response.data['message'], 'Cart abandonment data is not available yet.')

class UrlsTest(TestCase):
    def test_abandonment_rate_url(self):
        url = reverse('abandonment_rate')
        self.assertEqual(url, '/api/v1/marketing/abandonment-rate')

    def test_abandonment_rate_slash_url(self):
        url = reverse('abandonment_rate_slash')
        self.assertEqual(url, '/api/v1/marketing/abandonment-rate/')

