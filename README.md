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

## Global migration recovery (Windows PowerShell)

Use this checklist when you get errors like `ProgrammingError: relation "catalog_product" does not exist` or `relation "cart_cart" does not exist`.

### 1) Activate your virtual environment and install dependencies

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2) Validate Django app loading and model discovery

```powershell
python manage.py check
python manage.py shell -c "from django.apps import apps; print(sorted(a.label for a in apps.get_app_configs()))"
```

### 3) Ensure migration packages exist for every local app

Expected folders:
- `catalog/migrations/__init__.py`
- `cart/migrations/__init__.py`
- `orders/migrations/__init__.py`
- `core/migrations/__init__.py`
- `users/migrations/__init__.py`
- `dashboard/migrations/__init__.py`

### 4) Generate migrations for all apps with models

```powershell
python manage.py makemigrations catalog cart orders
```

If you are unsure, run the global command too:

```powershell
python manage.py makemigrations
```

### 5) Apply every pending migration

```powershell
python manage.py migrate
python manage.py showmigrations
```

### 6) Confirm tables exist in PostgreSQL

```powershell
python manage.py dbshell
```

Inside `psql`:

```sql
\dt
\dt catalog_*
\dt cart_*
\dt orders_*
```

You should see at least these tables:
- `catalog_category`
- `catalog_product`
- `cart_cart`
- `cart_cartitem`
- `orders_order`
- `orders_orderitem`

### 7) Optional: inspect SQL for pending operations

```powershell
python manage.py sqlmigrate cart 0001
python manage.py sqlmigrate orders 0001
```

### 8) Common root causes to eliminate
- App missing from `INSTALLED_APPS`.
- App has models but no migration package.
- Models changed without generating new migrations.
- Wrong PostgreSQL connection in `.env` (wrong DB name/host/port/user/password).
- Running project with a different settings file or environment than expected.
