# Configuração

Após instalar o projeto é necessário configurar o ambiente.

---

## Arquivo .env

Copie o arquivo de exemplo.

Linux

```bash
cp .env.example .env
```

Windows

```powershell
copy .env.example .env
```

---

## Configuração básica

Exemplo:

```env
SECRET_KEY=troque-esta-chave

DEBUG=True

DB_NAME=fluxos

DB_USER=root

DB_PASSWORD=senha

DB_HOST=localhost

DB_PORT=3306
```

---

## Configuração do banco

Crie um banco MySQL.

```sql
CREATE DATABASE fluxos
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

---

## Configurações Django

O projeto utiliza configurações separadas por ambiente.

```
config/

    settings/

        base.py

        development.py

        production.py

        testing.py
```

### Ambiente de desenvolvimento

```
DEBUG = True
```

### Produção

```
DEBUG = False
```

---

## Timezone

```
LANGUAGE_CODE = "pt-br"

TIME_ZONE = "America/Sao_Paulo"
```

---

## Arquivos estáticos

```
STATIC_URL = "static/"

STATICFILES_DIRS = [
    BASE_DIR / "static"
]

STATIC_ROOT = BASE_DIR / "staticfiles"
```

---

## Próximo passo

Continue para:

- primeira-execucao.md