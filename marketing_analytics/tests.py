from django.test import TestCase
from django.urls import reverse
from marketing_analytics.models import Cart, Product, CartItem
from django.contrib.auth.models import User
from django.utils.timezone import now
from datetime import timedelta

class CartAbandonmentRateAPITest(TestCase):
    def setUp(self):
        user = User.objects.create(username="test_user")
        product = Product.objects.create(name="Test Product", price=100.00)
        
        # Create carts
        Cart.objects.create(user=user, created_at=now() - timedelta(hours=48), is_checked_out=False)
        Cart.objects.create(user=user, created_at=now() - timedelta(hours=12), is_checked_out=True)

    def test_abandonment_rate_api(self):
        response = self.client.get(reverse('api_cart_abandonment_rate'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('abandonment_rate', response.json())
