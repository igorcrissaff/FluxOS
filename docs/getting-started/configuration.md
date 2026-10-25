# Configuration

> Language: [English](configuration.md) | [Português](../primeiros-passos/configuracao.md)

After installing the project, configure the environment and the database before the first run.

## .env file

Copy the example file:

Linux/macOS:

```bash
cp .env.example .env
```

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

The `.env` file is not versioned and contains the local settings.

## Main variables

```env
SECRET_KEY=your-generated-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
LANGUAGE_CODE=pt-br
TIME_ZONE=America/Sao_Paulo
```

Generate a new `SECRET_KEY` with:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Database

The project reads the connection from `DATABASE_URL` using `django-environ`.

### SQLite

Recommended for development:

```env
DATABASE_URL=sqlite:///db.sqlite3
```

The database file is created automatically on the first migration.

### MySQL

Create the database:

```sql
CREATE DATABASE fluxos
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

Configure the URL:

```env
DATABASE_URL=mysql://user:password@127.0.0.1:3306/fluxos
```

The `mysqlclient` driver is already listed in `requirements.txt`.

## Django settings

The main configuration is in `core/settings.py`.

- `DEBUG`: enables development mode.
- `ALLOWED_HOSTS`: allowed hosts.
- `LOGIN_REDIRECT_URL`: redirects to `/` after login.
- `LOGOUT_REDIRECT_URL`: redirects to `/` after logout.
- `LANGUAGE_CODE`: default application language.
- `TIME_ZONE`: time zone used by Django.

## Languages

Available languages:

```python
LANGUAGES = [
    ('en-us', _('English')),
    ('pt-br', _('Portuguese (Brazil)')),
]
```

The translation files are in `locale/pt_BR/LC_MESSAGES/` and are already compiled. The language can be changed using the selector at the top of the interface.

## Static files

Static files are served by `runserver` in development:

```python
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
```

The frontend libraries are in `static/vendor/`.

## Next step

- [First run](first-run.md)
