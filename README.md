
## Features

- User authentication and profile management
- Virtual currency balance management
- Product browsing, searching, and filtering
- Shopping cart and checkout system
- Order tracking and fulfillment
- Seller inventory management
- Product and seller reviews
- Optional messaging system

## Setup Instructions

1. Clone the repository:
```bash
git clone <repository-url>
cd mini-amazon
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the project root with the following content:
```
SECRET_KEY=your_secret_key
DEBUG=True
DB_NAME=miniamazon
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

5. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Run the server:
```bash
python manage.py runserver
```

8. Access the site at http://127.0.0.1:8000/

## Project Structure

- `users`: User authentication, profiles, and balance management
- `products`: Product listings, categories, and search
- `carts`: Shopping cart and order processing
- `sellers`: Inventory management and order fulfillment
- `social`: Reviews, ratings, and messaging

