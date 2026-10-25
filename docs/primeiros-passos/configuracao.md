# Configuração

> Idioma: [Português](configuracao.md) | [English](../getting-started/configuration.md)

Após instalar o projeto, configure o ambiente e o banco de dados antes da primeira execução.

## Arquivo .env

Copie o arquivo de exemplo:

Linux/macOS:

```bash
cp .env.example .env
```

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

O `.env` não é versionado e contém as configurações locais.

## Variáveis principais

```env
SECRET_KEY=sua-chave-gerada
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
LANGUAGE_CODE=pt-br
TIME_ZONE=America/Sao_Paulo
```

Gere uma nova `SECRET_KEY` com:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Banco de dados

O projeto lê a conexão a partir de `DATABASE_URL` usando `django-environ`.

### SQLite

Recomendado para desenvolvimento:

```env
DATABASE_URL=sqlite:///db.sqlite3
```

O arquivo do banco é criado automaticamente na primeira migração.

### MySQL

Crie o banco:

```sql
CREATE DATABASE fluxos
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

Configure a URL:

```env
DATABASE_URL=mysql://usuario:senha@127.0.0.1:3306/fluxos
```

O driver `mysqlclient` já está em `requirements.txt`.

## Configurações do Django

A configuração principal está em `core/settings.py`.

- `DEBUG`: ativa o modo de desenvolvimento.
- `ALLOWED_HOSTS`: hosts permitidos.
- `LOGIN_REDIRECT_URL`: redireciona para `/` após o login.
- `LOGOUT_REDIRECT_URL`: redireciona para `/` após o logout.
- `LANGUAGE_CODE`: idioma padrão da aplicação.
- `TIME_ZONE`: fuso horário utilizado pelo Django.

## Idiomas

Idiomas disponíveis:

```python
LANGUAGES = [
    ('en-us', _('English')),
    ('pt-br', _('Portuguese (Brazil)')),
]
```

Os arquivos de tradução ficam em `locale/pt_BR/LC_MESSAGES/` e já estão compilados. O idioma pode ser alterado pelo seletor no topo da interface.

## Arquivos estáticos

Os arquivos estáticos são servidos pelo `runserver` em desenvolvimento:

```python
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
```

As bibliotecas de frontend ficam em `static/vendor/`.

## Próximo passo

- [Primeira execução](primeira-execucao.md)
