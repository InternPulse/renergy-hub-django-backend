from faker import Faker
import random
from datetime import datetime, timedelta
import uuid


def generate_mock_product_data(num_products=10, years=3):
    random.seed(42)  # Use a fixed seed

def generate_mock_product_data(num_products=10, years=3):
    fake = Faker()
    
    start_date = datetime.now() - timedelta(days=years*365)
    end_date = datetime.now()

    products = []
    for _ in range(num_products):
        product_id = str(uuid.uuid4())
        category_id = str(uuid.uuid4())
        user_id = str(uuid.uuid4())
        name = fake.word() + " " + fake.word()  # Generate a two-word product name
        description = fake.sentence()
        base_price = round(random.uniform(10, 100), 2)
        created_at = fake.date_time_between(start_date=start_date, end_date=end_date)

        for _ in range(100):  # 100 data points per product
            date = fake.date_time_between(start_date=created_at, end_date=end_date)
            price = round(base_price * random.uniform(0.9, 1.1), 2)  # Slight price fluctuation
            cost_price = round(price * random.uniform(0.5, 0.9), 2)  # Cost price between 50% and 90% of selling price
            quantity_sold = random.randint(0, 100)
            
            products.append({
                "product_id": product_id,
                "category_id": category_id,
                "user_id": user_id,
                "name": name,
                "description": description,
                "price": price,
                "cost_price": cost_price,
                "stock": random.randint(0, 200),
                "image": f"https://example.com/images/{product_id}.jpg",  # Placeholder image URL
                "created_at": created_at,
                "updated_at": date,
                "sale_date": date,
                "quantity_sold": quantity_sold
            })

    return sorted(products, key=lambda x: x['sale_date'])