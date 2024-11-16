Project Overview
Live link: [*] in progress, will be provided soon
Doc link: [**] in progress, will be provided soon

This is a Django-based API designed for analytics services in areas such as sales performance, product profitability, and marketing conversion. The system offers detailed insights to help businesses track key performance metrics and optimize their strategies accordingly. Key features include advanced filtering, data aggregation, and reporting


Installation Instructions
Prerequisites
Before setting up the project locally, ensure you have the following prerequisites installed:

Python 3.8+
PostgreSQL
Virtualenv

How to Run API Locally
Clone the repository:

1. Clone the repository:
bash
git clone https://github.com/InternPulse/renergy-hub-django-backend.git

Navigate to the project directory:
cd renergy-hub-django-backend

Set up the virtual environment:

For Windows
python -m venv venv

For macOS/Linux
.\venv\Scripts\activate
python -m venv venv
source venv/bin/activate

Install the app dependencies:
pip install -r requirements.txt

Set up the database and run migrations:
python manage.py migrate

Start the API server:
python manage.py runserver

The API should now be running locally at http://localhost:8000/.

Commit Standards and Guidelines
Branches
dev → Use this branch for all backend-related work.
main → Do not touch this branch, as it represents the production version.
Contribution Guidelines
Fork the repository.

Set the origin branch:
bash
   git remote add origin https://github.com/InternPulse/renergy-hub-django-backend.git

Pull the latest changes from dev:
git pull origin dev

Create a new branch for your task:
git checkout -b TicketNumber/(Feat/Bug/Fix/Chore)/Ticket-title

After making changes, add and commit:
git add .
git commit -m "Your commit message"

Push your branch:
git push -u origin <dev>

Open a pull request to dev (not main).

Ensure your PR description is clear, especially if it introduces new functionality or requires testing


Project Structure
The project is organized as follows:

analytics_service/
├── analytics_service/           # Main project directory
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py             # Global settings
│   ├── urls.py                 # Root URL configuration
│   ├── wsgi.py
│   ├── sales_performance/      # App for Sales Performance Analytics
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py                 # App-specific URLs
│   ├── views.py
│   ├── product_performance/    # App for Product Performance Analytics
│   ├── (similar structure as sales_performance)
│   ├── marketing_conversion/   # App for Marketing & Conversion Analytics
│   ├── (similar structure as sales_performance)
│   ├── profitability_financial/ # App for Profitability & Financial Analytics
│   ├── (similar structure as sales_performance)
│   ├── shared/                  # Shared utilities and reusable components
│   ├── __init__.py
│   ├── filters.py               # Shared filters for all apps
│   ├── utils.py                 # Helper functions
│   ├── manage.py
└── requirements.txt             # Project dependencies


API Endpoints
Here are some of the key endpoints available:

GET /api/v1/financial/analytics/
Retrieves a list of all financial analytics records.

GET /api/v1/financial/analytics/top_products/
Retrieves a list of all top products with the highest profit records.

GET /api/v1/financial/analytics/?date=2024-11-12
Retrieves a list of financial analytics products by date.

GET /api/v1/financial/analytics/?day=28
Retrieves a list of financial analytics products by day.

GET /api/v1/financial/analytics/?year=2022
Retrieves a list of financial analytics products by year.

GET /api/v1/financial/analytics/?month=31
Retrieves a list of financial analytics products by exact month and day.

GET /api/v1/financial/analytics/?year=2022&month=12
Retrieves a list of financial analytics products by exact month, day, and year.

GET /api/v1/financial/analytics/?start_date=2023-01-01&end_date=2023-02-28
Retrieves a list of financial analytics products by a date range.

GET /api/v1/financial/analytics/profit_records/
Retrieves a list of financial analytics product records with profit alone.

GET /api/v1/financial/analytics/selling_at_loss/
Retrieves a list of financial analytics products with loss alone.

Environment Variables
You need to configure the following environment variables for the project to run locally:

bash
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost,.(*) # Allow localhost and all subdomains

# Database connection settings for PostgreSQL
DB_NAME=your-database-name
DB_USER=your-database-user
DB_PASSWORD=your-database-password
DB_HOST=your-database-host
DB_PORT=your-database-port

