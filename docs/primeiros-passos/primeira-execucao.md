# Primeira execução

Após instalar e configurar o projeto, execute os passos abaixo.

---

## 1. Ative o ambiente virtual

Linux

```bash
source .venv/bin/activate
```

Windows

```powershell
.venv\Scripts\activate
```

---

## 2. Execute as migrações

```bash
python manage.py migrate
```

---

## 3. Crie um usuário administrador

```bash
python manage.py createsuperuser
```

Informe:

- usuário

- e-mail

- senha

---

## 4. Execute o servidor

```bash
python manage.py runserver
```

---

## 5. Acesse a aplicação

Aplicação

```
http://127.0.0.1:8000
```

Painel administrativo

```
http://127.0.0.1:8000/admin
```

---

## Verificações

Antes de iniciar o desenvolvimento confirme:

- Banco conectado

- Login funcionando

- Arquivos estáticos carregando

- Painel administrativo acessível

- Sem erros no terminal

---

## Comandos úteis

Criar migração

```bash
python manage.py makemigrations
```

Aplicar migrações

```bash
python manage.py migrate
```

Abrir shell

```bash
python manage.py shell
```

Executar testes

```bash
pytest
```

Executar lint

```bash
ruff check .
```

Formatar código

```bash
black .
```

---

## Próximos passos

Agora você pode começar a desenvolver novos módulos do FluxOS.

Recomenda-se ler a documentação:

- Architecture

- Style Guide

- Contributing