# Installation

> Language: [English](installation.md) | [Português](../primeiros-passos/instalacao.md)

This guide describes how to prepare a development environment for FluxOS.

## Requirements

| Software | Recommended version |
| --- | --- |
| Python | 3.14 or later |
| Git | Latest version |
| pip | Included with Python |
| PostgreSQL | 14 or later (recommended) |
| Node.js | Only for reinstalling frontend dependencies manually |

PostgreSQL is the recommended database and can be configured via `DATABASE_URL`. The project also works with SQLite for quick development.

The frontend libraries are already included in `static/`. There is no need to install Bootstrap, jQuery, DataTables, Chart.js, or Font Awesome separately, nor to run a frontend build.

## Clone the repository

```bash
git clone https://github.com/<user>/FluxOS.git
cd FluxOS
```

## Create the virtual environment

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

If PowerShell blocks activation, run this for the current session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

## Install the Python dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Alternatively, with `uv`:

```bash
uv sync
```

The dependencies include Django 6.0.6, django-environ, and django-widget-tweaks. For PostgreSQL, also install the `psycopg` driver:

```bash
pip install "psycopg[binary]"
```

The binary distribution does not require build tools. On systems where the driver is built from source, `libpq` must be installed.

## Configure the environment variables

Create the `.env` file from the example:

Linux/macOS:

```bash
cp .env.example .env
```

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Generate a new secret key:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Replace `SECRET_KEY` in `.env`. Then configure the database:

```env
# PostgreSQL (recommended)
DATABASE_URL=postgresql://user:password@127.0.0.1:5432/fluxos

# SQLite (development)
# DATABASE_URL=sqlite:///db.sqlite3
```

## Frontend dependencies

Bootstrap 4.6.0, SB Admin 2 4.1.3, jQuery 3.6.0, jQuery Easing, DataTables 1.10.24, Chart.js, and Font Awesome 5.15.3 are already versioned in the project.

To restore or update these libraries, download the official distributions and replace the files in `static/vendor/`. Optionally, use npm in a temporary directory:

```bash
npm install bootstrap@4.6.0 jquery@3.6.0 jquery.easing@1.4.1 datatables.net@1.10.24 datatables.net-bs4@1.10.24 chart.js@2.9.4 @fortawesome/fontawesome-free@5.15.3
```

Copy the distribution files from `node_modules/` to the corresponding folders in `static/vendor/`. There is no mandatory build step.

## Verify the installation

```bash
python manage.py check
```

Expected output:

```text
System check identified no issues (0 silenced).
```

## Next step

- [Configuration](configuration.md)
