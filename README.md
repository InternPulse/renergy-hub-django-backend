Renergy Hub Express Backend API
Project Overview
The Renergy Hub Express Backend API is a Django-based analytics service designed to provide insights into critical business areas, including:

Sales Performance
Product Analytics
Marketing Conversions
Financial Analytics
It empowers businesses with advanced features such as filtering, data aggregation, and reporting to optimize strategies and monitor key metrics effectively.

Live Link : https://codebrewmaster.pythonanywhere.com/api/v1


Documentation Link : https://codebrewmaster.pythonanywhere.com/api/v1


Installation Instructions
Prerequisites
Ensure the following tools are installed:

Python (>= 3.9 recommended)
pip (Python package manager)
Git
Virtual environment tool (e.g., venv or virtualenv)
PostgreSQL
How to Run the API Locally
Clone the repository:

bash
Copy code
git clone https://github.com/InternPulse/renergy-hub-django-backend.git
cd renergy-hub-django-backend
Set up a virtual environment:
Windows:

bash
Copy code
python -m venv venv
.\venv\Scripts\activate
macOS/Linux:

bash
Copy code
python -m venv venv
source venv/bin/activate
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Set up the database:

bash
Copy code
python manage.py migrate
Start the server:

bash
Copy code
python manage.py runserver
The API will be available at http://127.0.0.1:8000/.

Features
Advanced Analytics: Provides insights into key performance metrics.
REST API: Enables querying and managing analytics data.
Filters: Supports filtering by dates, products, and profitability.
Data Aggregation: Converts raw data into actionable insights.
Reporting: Offers downloadable and visual reports.
Usage
Access the API locally at http://127.0.0.1:8000/ or via the Live Link.
Test endpoints using tools like Postman, cURL, or other API testing utilities.
Refer to the API Documentation for detailed instructions.
API Endpoints
Base URL: http://127.0.0.1:8000/api/v1/

Endpoint	Method	Description
/financial/analytics/	GET	Fetch all financial analytics records.
/financial/analytics/top_products/	GET	Get top products by profitability.
/financial/analytics/?year=2022	GET	Filter analytics by year.
/financial/analytics/?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD	GET	Filter analytics by date range.
/financial/analytics/profit_records/	GET	Fetch records with profit only.
/financial/analytics/selling_at_loss/	GET	Fetch records with losses only.
For a comprehensive list, refer to the API Documentation.

Project Structure
plaintext
Copy code
renergy-hub-django-backend/
├── analytics_service/
│   ├── sales_performance/      # Sales Performance Analytics
│   ├── product_performance/    # Product Performance Analytics
│   ├── marketing_conversion/   # Marketing Analytics
│   ├── profitability_financial/ # Financial Analytics
│   ├── shared/                 # Shared utilities and helpers
├── manage.py                   # Django entry point
├── requirements.txt            # Python dependencies
└── ...
Environment Variables
Create a .env file in the root directory with the following keys:

bash
Copy code
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# PostgreSQL
DB_NAME=your-database-name
DB_USER=your-database-user
DB_PASSWORD=your-database-password
DB_HOST=localhost
DB_PORT=5432
Contributions
Contributions are welcome! If you’re interested:

Create an issue or comment on the repository to let others know what you're working on to avoid overlapping efforts.
Follow the steps outlined below to contribute.
Contribution Guidelines
Clone the repository:

bash
Copy code
git clone https://github.com/InternPulse/renergy-hub-django-backend.git
Set the origin branch:

bash
Copy code
git remote add origin https://github.com/InternPulse/renergy-hub-django-backend.git
git pull origin dev
Create a new branch for your task:

bash
Copy code
git checkout -b BA-001/Feat/Sign-Up-Form
Make your changes and commit:

bash
Copy code
git add .
git commit -m "your commit message"
Sync with the dev branch to avoid conflicts:

bash
Copy code
git pull origin dev
Push your branch:

bash
Copy code
git push -u origin BA-001/Feat/Sign-Up-Form
Create a pull request to the dev branch. Ensure the PR description is clear and includes test instructions.

Commit Standards and Guidelines
Commit Cheat Sheet
Type	Description
feat	Features: A new feature
fix	Bug Fixes: A bug fix
docs	Documentation: Documentation-only changes
style	Styles: Formatting or cosmetic changes
refactor	Code Refactoring: Neither fixes a bug nor adds a feature
perf	Performance: Optimizes performance
test	Tests: Adding or updating tests
build	Builds: Changes to build tools or dependencies
ci	CI: Updates to CI configurations
chore	Chores: Maintenance or configuration tasks
revert	Reverts: Reverts a previous commit
Sample Commit Messages

chore: Update README file – Maintenance task.
feat: Add user registration endpoint – New feature added.
License
This project is licensed under the MIT License.











