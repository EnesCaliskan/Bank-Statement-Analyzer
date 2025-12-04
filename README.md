# Bank Statement Analyzer
---

<a name="english"></a>

### Project Overview
This project is a REST API developed with Django and Django REST Framework. It allows users to upload bank statement CSV files, automatically normalizes the data, prevents duplicate entries, and generates financial KPI reports (Income vs. Expense, Net Cash Flow, Top Categories).

### Key Features
* **Atomic CSV Upload:** Validates and saves transaction data transactionally. If one row fails, the entire file is rejected to ensure data integrity.
* **Duplicate Prevention:** Uses a cryptographic hash (`SHA256`) of transaction details to prevent the same row from being uploaded twice (Idempotency).
* **Auto-Categorization:** Automatically assigns categories (e.g., "Rent", "Groceries") based on transaction descriptions.
* **KPI Reporting:** Optimized SQL aggregation for financial summaries.
* **Swagger Documentation:** Interactive API documentation.

### Technology Stack
* **Language:** Python 3.10+
* **Framework:** Django 4.2, Django REST Framework
* **Database:** SQLite (Default) / PostgreSQL (Ready)
* **Documentation:** drf-yasg (Swagger/OpenAPI)
* **Testing:** Django Test Framework

### Installation & Setup

#### 1. Clone & Environment
```bash
git clone <your-repo-link>
cd bank_case_study

# Create Virtual Environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Dependencies
pip install -r requirements.txt
```

#### 2. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser  # Create admin user for login
```

#### 3. Run Server
```bash
python manage.py runserver
```

#### API Documentation (Swagger)

Once the server is running, visit: ```http://127.0.0.1:8000/swagger/```

#### How to Use: 
* **Authorize:** Log in via the `/admin` panel or use the Authorize button.
* **Upload:** use `POST /api/transactions/upload/` with a CSV file.
* **Report:** use `GET /api/transactions/reports/summary/` with `start_date` and `end_date`.

#### Running Tests

To verify data integrity and logic: 
```bash
python manage.py test
```

#### NOTES

The requirements.txt file should list all Python libraries that your notebooks depend on, and they will be installed using:
```bash
pip install -r requirements.txt
```
