from django.core.management.base import BaseCommand
from product_analytics.models import Product, SalesRecord, ProductEngagement
import uuid
import random

class Command(BaseCommand):
    help = "Create dummy data for testing"

    def handle(self, *args, **kwargs):
        # Create products
        for i in range(10):
            product = Product.objects.create(
                id=uuid.uuid4(),
                name=f"Product {i + 1}",
                description=f"Description for product {i + 1}",
                cost_price=random.uniform(10, 50),
                selling_price=random.uniform(60, 100),
            )
            self.stdout.write(f"Created Product: {product.name}")

            # Create sales records
            SalesRecord.objects.create(
                product=product,
                quantity=random.randint(1, 10),
            )

            # Create engagements
            for _ in range(random.randint(5, 15)):
                ProductEngagement.objects.create(
                    product=product,
                    engagement_type=random.choice(['view', 'click']),
                )
        self.stdout.write(self.style.SUCCESS("Dummy data created successfully!"))
