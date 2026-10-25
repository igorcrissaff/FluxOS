# First run

> Language: [English](first-run.md) | [Português](../primeiros-passos/primeira-execucao.md)

After installing the dependencies and configuring the `.env` file, follow the steps below.

## 1. Activate the virtual environment

Linux/macOS:

```bash
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Windows CMD:

```bat
.venv\Scripts\activate.bat
```

## 2. Apply migrations

```bash
python manage.py migrate
```

With SQLite, the database is created automatically at this step.

## 3. Create the superuser

```bash
python manage.py createsuperuser
```

Enter username, email, and password. This user will be able to access the admin panel and manage the team.

## 4. Run the server

```bash
python manage.py runserver
```

## 5. Access the application

Application:

```text
http://127.0.0.1:8000/
```

Admin panel:

```text
http://127.0.0.1:8000/admin/
```

## 6. Verify it works

```bash
python manage.py check
python manage.py test
```

Also confirm that:

- login is working;
- static files are loading;
- the dashboard is accessible;
- product, customer, and order registration is working;
- the admin panel is accessible.

## Useful commands

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Open the shell
python manage.py shell

# Run all tests
python manage.py test

# Test a specific app
python manage.py test apps.stock
```

## Next steps

The main project documentation, including goals, features, dependencies, and installation, is in the [README](../../README.en.md).
