# ElectroMarket

Production-ready Django e-commerce application with i18n (es/en), custom admin dashboard, dark neon UI, and modular architecture.

## Stack
- Django 5+
- PostgreSQL (configurable via env)
- Session-based authentication
- Bootstrap + custom CSS

## Run
1. Create venv and install dependencies.
2. Copy `.env.example` to `.env`.
3. Run migrations and start server.

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
