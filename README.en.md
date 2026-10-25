# FluxOS

> Language: [English](README.en.md) | [Português](README.md)

**FluxOS** is an open source business management system built to centralize customers, orders, products, and inventory in a single application. The project provides a modular Django foundation with authentication, role-based access control, an admin panel, a responsive interface, and support for Portuguese and English.

The system is under active development and already includes the main commercial operation flows.

## Overview

FluxOS is designed for small and medium businesses that need to track the commercial cycle without relying on separate spreadsheets. The application brings together:

- customer records and history;
- orders with multiple items and status tracking;
- product catalog, categories, and availability;
- inventory movements with balance validation;
- revenue, order, and inventory indicators on the dashboard;
- user and profile management with separation between regular users and administrative staff.

## Goals

### Business goals

- Centralize the commercial operation in a single system.
- Improve visibility into sales, customers, and inventory.
- Reduce manual errors in orders and inventory movements.
- Support decisions with up-to-date revenue, order, and out-of-stock product indicators.
- Keep a reliable history of customers, orders, and inventory changes.

### Technical goals

- Provide a modular architecture, with each domain in a Django app.
- Apply authentication, authorization, and validation on the backend.
- Keep automated tests for critical flows.
- Be simple to install and run in a development environment.
- Allow gradual evolution toward reports, integrations, and new modules.

## Implemented Features

### Dashboard

- Monthly and annual revenue considering completed and shipped orders.
- Pending order count.
- List of products with low stock.
- Latest registered orders.
- Ranking of customers with the highest amount spent.
- Global alerts for low stock and pending orders.

### Customers

- Create, edit, list, and delete customers.
- Address, gender, marital status, and date of birth.
- Details page with order history.
- Total orders and total amount spent per customer.
- Deletion protected by POST request.

### Orders

- Create, edit, list, view details, and delete orders.
- Order items with product and quantity.
- Automatic subtotal and total calculation.
- Status: pending, completed, canceled, shipped, and returned.
- Filter orders by status.
- Automatic update of customer statistics.
- Customer preselection when creating an order from the customer page.

### Inventory

- Create, edit, and delete products.
- Create, edit, and delete categories.
- Availability control and low-stock threshold.
- Filter products with low stock.
- Inventory inbound and outbound movements.
- Quantity and available balance validation.
- Record of the user responsible for each movement.
- Editing of already recorded movements is blocked.

### Users and Security

- Login and logout.
- User management restricted to administrative staff.
- User creation and editing with password validation.
- Protection against improper self-activation, self-deactivation, and self-deletion.
- User profile limited to first name, last name, email, and username.
- Routes protected by authentication.
- Deletions and sensitive changes via POST.

### Interface and Internationalization

- Responsive interface with Bootstrap and SB Admin 2.
- Tables with DataTables.
- Charts and indicators with Chart.js.
- Icons with Font Awesome.
- Centralized success and error messages.
- Available languages: English (`en-us`) and Brazilian Portuguese (`pt-br`).
- Translations compiled in `locale/pt_BR/LC_MESSAGES/`.

### Tests

The suite covers models, forms, views, permissions, redirects, POST deletions, inventory movements, customer statistics, dashboard, alerts, authentication, and language switching.

## Roadmap

Items not yet implemented or in progress:

- suppliers and purchase orders;
- accounts receivable and financial reconciliation;
- advanced reports and data export;
- email notifications and reminders;
- API for external integrations;
- WooCommerce integration;
- production configuration with Docker, Gunicorn, and Nginx.

### Current limitations

- Creating an order does not automatically reduce inventory; the reduction must be recorded as an outbound movement.
- The dashboard counts revenue only for orders with status **Completed** or **Shipped**.
- Customer totals are denormalized and updated when orders are created, edited, or deleted.
- The production environment is not yet documented in this repository.

## Technologies and Dependencies

### Backend

| Package | Version | Purpose |
| --- | --- | --- |
| Python | 3.14+ | Language and runtime |
| Django | 6.0.6 | Web framework |
| django-environ | 0.14.0 | Environment variable reading |
| django-widget-tweaks | 1.5.1 | Widget customization in templates |
| psycopg | 3.x | PostgreSQL driver |
| asgiref | 3.11.1 | Django dependency |
| sqlparse | 0.5.5 | Django dependency |
| tzdata | 2026.2 | Time zone data |

Backend versions are pinned in `requirements.txt` and `pyproject.toml`. The `psycopg` driver must be installed to use PostgreSQL:

```bash
pip install "psycopg[binary]"
```

### Frontend

The interface libraries are already included in the repository under `static/`. There is no need to run `npm install` or create a frontend build to run the project.

| Library | Version | Location |
| --- | --- | --- |
| Bootstrap | 4.6.0 | `static/vendor/bootstrap/` |
| SB Admin 2 | 4.1.3 | `static/css/` and `static/js/` |
| jQuery | 3.6.0 | `static/vendor/jquery/` |
| jQuery Easing | 1.4.x | `static/vendor/jquery-easing/` |
| DataTables | 1.10.24 | `static/vendor/datatables/` |
| DataTables Bootstrap 4 | 1.10.24 | `static/vendor/datatables/` |
| Font Awesome Free | 5.15.3 | `static/vendor/fontawesome-free/` |
| Chart.js | 2.x | `static/vendor/chart.js/` |
| Google Fonts (Inter) | CDN | Loaded in `templates/head.html` |

Bootstrap is the foundation of the responsive layout. The SB Admin 2 template provides the visual structure of the panel, and DataTables adds sorting, search, and pagination to tables.

#### Optional reinstallation of frontend dependencies

The project does not require Node.js. If you need to update or restore the libraries, download the official distributions and keep the folder structure used in `static/vendor/`:

- Bootstrap 4: https://getbootstrap.com/docs/4.6/getting-started/download/
- jQuery: https://jquery.com/download/
- DataTables: https://datatables.net/download/
- Font Awesome 5: https://fontawesome.com/v5/download
- Chart.js: https://www.chartjs.org/docs/
- SB Admin 2: https://startbootstrap.com/theme/sb-admin-2

You can also use npm in a temporary directory:

```bash
npm install bootstrap@4.6.0 jquery@3.6.0 jquery.easing@1.4.1 datatables.net@1.10.24 datatables.net-bs4@1.10.24 chart.js@2.9.4 @fortawesome/fontawesome-free@5.15.3
```

Then copy the required files from `node_modules/` to the corresponding folders in `static/vendor/`. There is no mandatory build step.

## Project Structure

```text
FluxOS/
├── apps/
│   ├── customers/          # Customers
│   ├── dashboard/          # Dashboard and profile
│   ├── members/            # Users and access control
│   ├── orders/             # Orders, items, and statistics
│   └── stock/              # Products, categories, and movements
├── core/                   # Settings, URLs, and context processors
├── docs/                   # Additional documentation
├── locale/                 # Translations (pt-BR and en-US)
├── static/
│   ├── css/                # Global styles and SB Admin 2
│   ├── img/                # Images
│   ├── js/                 # Global scripts
│   └── vendor/             # Bootstrap, jQuery, DataTables, Chart.js, etc.
├── templates/              # Global and authentication templates
├── manage.py
├── requirements.txt
├── pyproject.toml
├── uv.lock
└── .env.example
```

## Installation

### Prerequisites

- Python 3.14 or later
- Git
- `pip`
- PostgreSQL 14+ (recommended; the project also works with SQLite for development)
- Node.js only if you reinstall the frontend libraries manually

> There is no need to install Bootstrap, jQuery, DataTables, Chart.js, or Font Awesome separately: the files are already versioned in the project.

### 1. Clone the repository

```bash
git clone https://github.com/<user>/FluxOS.git
cd FluxOS
```

### 2. Create and activate the virtual environment

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Windows CMD:

```bat
python -m venv .venv
.venv\Scripts\activate.bat
```

If PowerShell blocks activation, run this for the current session only:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### 3. Install the Python dependencies

Update `pip` and install the packages:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Alternatively, with `uv`:

```bash
uv sync
```

`psycopg` is the driver used when `DATABASE_URL` points to PostgreSQL. Install the binary distribution, which does not require build tools:

```bash
pip install "psycopg[binary]"
```

On systems where the driver is built from source, `libpq` must be installed. For quick development with SQLite, no database server is required, but the PostgreSQL driver must still be installed to use PostgreSQL.

### 4. Configure the environment variables

Copy the example file:

Linux/macOS:

```bash
cp .env.example .env
```

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Generate a new `SECRET_KEY`:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Edit `.env` and replace the value of `SECRET_KEY`.

For PostgreSQL:

```env
DATABASE_URL=postgresql://user:password@127.0.0.1:5432/fluxos
```

For quick development with SQLite:

```env
DATABASE_URL=sqlite:///db.sqlite3
```

Optional settings:

```env
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
LANGUAGE_CODE=pt-br
TIME_ZONE=America/Sao_Paulo
```

The `.env` file is not versioned.

### 5. Create the database

With SQLite, the database is created automatically on the first migration.

With PostgreSQL, create the database before migrating:

```sql
CREATE DATABASE fluxos
    WITH ENCODING 'UTF8'
    TEMPLATE template0;
```

### 6. Apply migrations

```bash
python manage.py migrate
```

### 7. Create a superuser

```bash
python manage.py createsuperuser
```

Enter username, email, and password.

### 8. Run the server

```bash
python manage.py runserver
```

Access:

- Application: http://127.0.0.1:8000/
- Admin panel: http://127.0.0.1:8000/admin/

### 9. Verify the installation

```bash
python manage.py check
python manage.py test
```

The current suite covers the customers, orders, inventory, users, dashboard, and core apps.

## Useful Commands

```bash
# Create new migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Open the Django shell
python manage.py shell

# Run all tests
python manage.py test

# Run tests for a specific app
python manage.py test apps.stock

# Check the project
python manage.py check
```

## Internationalization

The project includes English and Brazilian Portuguese. The language can be changed using the selector at the top of the interface.

Translation files:

```text
locale/
└── pt_BR/
    └── LC_MESSAGES/
        ├── django.po
        └── django.mo
```

The `.mo` files are already compiled. If you change translations and have GNU gettext installed:

```bash
python manage.py compilemessages
```

## Additional Documentation

- [Documentation index](docs/README.md)
- [Installation](docs/getting-started/installation.md)
- [Configuration](docs/getting-started/configuration.md)
- [First run](docs/getting-started/first-run.md)
- [Portuguese documentation](docs/primeiros-passos/instalacao.md)

## License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for more details.
