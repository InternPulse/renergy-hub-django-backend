import requests
from django.conf import settings

class ProductManagementAPI:
    def __init__(self):
        self.base_url = settings.PRODUCT_MANAGEMENT_API_URL

    def get_products(self):
        response = requests.get(f"{self.base_url}/products")
        response.raise_for_status()
        return response.json()['data']