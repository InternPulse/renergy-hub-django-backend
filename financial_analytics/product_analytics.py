from collections import defaultdict
from datetime import datetime

class ProductAnalytics:
    def calculate_product_analytics(self, products):
        product_analytics = defaultdict(lambda: {
            "product_id": "",
            "category_id": "",
            "user_id": "",
            "name": "",
            "description": "",
            "image": "",
            "created_at": "",
            "total_revenue": 0,
            "total_cost": 0,
            "total_quantity_sold": 0,
            "total_profit": 0,
            "average_stock": 0,
            "sales_data": [],
            "profit_margin": 0,
            "average_price": 0,
            "stock_turnover_rate": 0,
            "is_profitable": False,
            "profit_per_unit": 0
        })

        for product in products:
            p_id = product['id']
            product_analytics[p_id]['product_id'] = p_id
            product_analytics[p_id]['category_id'] = product['categoryId']
            product_analytics[p_id]['user_id'] = product['userId']
            product_analytics[p_id]['name'] = product['name']
            product_analytics[p_id]['description'] = product['description']
            product_analytics[p_id]['image'] = product['image']
            product_analytics[p_id]['created_at'] = product['createdAt']
            
            price = float(product['price'])
            stock = product['stock']
            revenue = price * stock
            cost = price * 0.7 * stock  # Assuming cost is 70% of price
            
            product_analytics[p_id]['total_revenue'] += revenue
            product_analytics[p_id]['total_cost'] += cost
            product_analytics[p_id]['total_quantity_sold'] += stock
            product_analytics[p_id]['average_stock'] += stock
            product_analytics[p_id]['sales_data'].append({
                "date": product['createdAt'],
                "price": price,
                "quantity_sold": stock,
                "revenue": revenue,
                "cost": cost,
                "profit": revenue - cost
            })

        for p_id, data in product_analytics.items():
            data['total_profit'] = data['total_revenue'] - data['total_cost']
            data['average_stock'] = data['average_stock']
        
            if data['total_revenue'] > 0:
                data['profit_margin'] = (data['total_profit'] / data['total_revenue']) * 100
            else:
                data['profit_margin'] = 0
        
            if data['total_quantity_sold'] > 0:
                data['average_price'] = data['total_revenue'] / data['total_quantity_sold']
                data['profit_per_unit'] = data['total_profit'] / data['total_quantity_sold']
            else:
                data['average_price'] = 0
                data['profit_per_unit'] = 0
        
            if data['average_stock'] > 0:
                data['stock_turnover_rate'] = data['total_quantity_sold'] / data['average_stock']
            else:
                data['stock_turnover_rate'] = 0

            data['is_profitable'] = data['total_profit'] > 0

        sorted_products = sorted(product_analytics.values(), key=lambda x: x['total_profit'], reverse=True)
        return sorted_products
    
    
    def get_top_selling_products(self, products, limit=10):
        product_analytics = self.calculate_product_analytics(products)
        return sorted(product_analytics, key=lambda x: x['total_quantity_sold'], reverse=True)[:limit]

    def get_top_profit_products(self, products, limit=10):
        product_analytics = self.calculate_product_analytics(products)
        return sorted(product_analytics, key=lambda x: x['total_profit'], reverse=True)[:limit]

    def get_loss_making_products(self, products):
        product_analytics = self.calculate_product_analytics(products)
        return [p for p in product_analytics if p['total_profit'] < 0]

    def get_profit_making_products(self, products):
        product_analytics = self.calculate_product_analytics(products)
        return [p for p in product_analytics if p['total_profit'] > 0]
    

    def filter_products_by_date(self, products, **params):
        start_date = params.get('start_date')
        end_date = params.get('end_date')
        day = params.get('day')
        month = params.get('month')
        year = params.get('year')
        date = params.get('date')

        filtered_products = products

        if start_date and end_date:
            start = datetime.strptime(start_date[0], "%Y-%m-%d")
            end = datetime.strptime(end_date[0], "%Y-%m-%d")
            filtered_products = [p for p in filtered_products if start <= datetime.strptime(p['createdAt'][:10], "%Y-%m-%d") <= end]
        elif date:
            target_date = datetime.strptime(date[0], "%Y-%m-%d")
            filtered_products = [p for p in filtered_products if datetime.strptime(p['createdAt'][:10], "%Y-%m-%d").date() == target_date.date()]
        elif day and month and year:
            filtered_products = [p for p in filtered_products if 
                                datetime.strptime(p['createdAt'][:10], "%Y-%m-%d").day == int(day[0]) and
                                datetime.strptime(p['createdAt'][:10], "%Y-%m-%d").month == int(month[0]) and
                                datetime.strptime(p['createdAt'][:10], "%Y-%m-%d").year == int(year[0])]
        elif month and year:
            filtered_products = [p for p in filtered_products if 
                                datetime.strptime(p['createdAt'][:10], "%Y-%m-%d").month == int(month[0]) and
                                datetime.strptime(p['createdAt'][:10], "%Y-%m-%d").year == int(year[0])]
        elif month:
            if not 1 <= int(month[0]) <= 12:
                raise ValueError("Invalid month. Must be between 1 and 12.")
            filtered_products = [p for p in filtered_products if datetime.strptime(p['createdAt'][:10], "%Y-%m-%d").month == int(month[0])]
        elif day:
            if not 1 <= int(day[0]) <= 31:
                raise ValueError("Invalid day. Must be between 1 and 31.")
            filtered_products = [p for p in filtered_products if datetime.strptime(p['createdAt'][:10], "%Y-%m-%d").day == int(day[0])]
        elif year:
            filtered_products = [p for p in filtered_products if datetime.strptime(p['createdAt'][:10], "%Y-%m-%d").year == int(year[0])]
            
        if not filtered_products:
            if start_date and end_date:
                raise ValueError("No records found for the specified date range.")
            elif month:
                raise ValueError("No records found for the specified month.")
            elif year:
                raise ValueError("No records found for the specified year.")
            elif day:
                raise ValueError("No records found for the specified day.")
            else:
                raise ValueError("No records found for the specified criteria.")

        return filtered_products