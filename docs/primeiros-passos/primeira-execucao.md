# Primeira execução

> Idioma: [Português](primeira-execucao.md) | [English](../getting-started/first-run.md)

Depois de instalar as dependências e configurar o `.env`, execute os passos abaixo.

## 1. Ativar o ambiente virtual

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

## 2. Aplicar as migrações

```bash
python manage.py migrate
```

Com PostgreSQL, crie o banco antes de migrar (veja [Configuração](configuracao.md)). Com SQLite, o arquivo é criado automaticamente nessa etapa.

## 3. Criar o superusuário

```bash
python manage.py createsuperuser
```

Informe nome de usuário, e-mail e senha. Esse usuário poderá acessar o painel administrativo e gerenciar a equipe.

## 4. Executar o servidor

```bash
python manage.py runserver
```

## 5. Acessar a aplicação

Aplicação:

```text
http://127.0.0.1:8000/
```

Painel administrativo:

```text
http://127.0.0.1:8000/admin/
```

## 6. Verificar o funcionamento

```bash
python manage.py check
python manage.py test
```

Confirme também:

- login funcionando;
- arquivos estáticos carregando;
- dashboard acessível;
- cadastro de produtos, clientes e pedidos funcionando;
- painel administrativo acessível.

## Comandos úteis

```bash
# Criar migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Abrir o shell
python manage.py shell

# Executar todos os testes
python manage.py test

# Testar um app específico
python manage.py test apps.stock
```

## Próximos passos

A documentação principal do projeto, incluindo objetivos, funcionalidades, dependências e instalação, está no [README](../../README.md).
