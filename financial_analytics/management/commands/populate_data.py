
from django.core.management.base import BaseCommand
from financial_analytics.utils import generate_mock_product_data

class Command(BaseCommand):
    help = 'Populates fake financial data for testing purposes'

    def handle(self, *args, **kwargs):
        self.stdout.write('Generating mock product data...')
        
        data = generate_mock_product_data()
        
        for record in data:
            self.stdout.write(str(record))  # Print the data to the console for checking
        
        self.stdout.write('Mock data generation complete.')