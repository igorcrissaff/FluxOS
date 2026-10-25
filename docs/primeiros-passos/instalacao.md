# Instalação

> Idioma: [Português](instalacao.md) | [English](../getting-started/installation.md)

Este guia descreve como preparar um ambiente de desenvolvimento para o FluxOS.

## Requisitos

| Software | Versão recomendada |
| --- | --- |
| Python | 3.14 ou superior |
| Git | Última versão |
| pip | Incluído com o Python |
| MySQL | 8.0 ou superior (opcional) |
| Node.js | Apenas para reinstalar dependências frontend manualmente |

O projeto funciona com SQLite em desenvolvimento. O MySQL é opcional e pode ser configurado via `DATABASE_URL`.

As bibliotecas de frontend já estão incluídas em `static/`. Não é necessário instalar Bootstrap, jQuery, DataTables, Chart.js ou Font Awesome separadamente, nem executar um build de frontend.

## Clonar o repositório

```bash
git clone https://github.com/<usuario>/FluxOS.git
cd FluxOS
```

## Criar o ambiente virtual

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

Se o PowerShell bloquear a ativação, execute para a sessão atual:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

## Instalar as dependências Python

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Alternativamente, com `uv`:

```bash
uv sync
```

As dependências incluem Django 6.0.6, django-environ, django-widget-tweaks e mysqlclient. O `mysqlclient` é utilizado com MySQL; em Windows pode ser necessário instalar o MySQL Client/Connector C e as ferramentas de compilação C++ para concluir a instalação.

## Configurar as variáveis de ambiente

Crie o arquivo `.env` a partir do exemplo:

Linux/macOS:

```bash
cp .env.example .env
```

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Gere uma nova chave secreta:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Substitua `SECRET_KEY` no `.env`. Depois configure o banco:

```env
# SQLite (desenvolvimento)
DATABASE_URL=sqlite:///db.sqlite3

# MySQL (opcional)
# DATABASE_URL=mysql://usuario:senha@127.0.0.1:3306/fluxos
```

## Dependências frontend

Bootstrap 4.6.0, SB Admin 2 4.1.3, jQuery 3.6.0, jQuery Easing, DataTables 1.10.24, Chart.js e Font Awesome 5.15.3 já estão versionados no projeto.

Para restaurar ou atualizar essas bibliotecas, baixe as distribuições oficiais e substitua os arquivos em `static/vendor/`. Opcionalmente, use npm em um diretório temporário:

```bash
npm install bootstrap@4.6.0 jquery@3.6.0 jquery.easing@1.4.1 datatables.net@1.10.24 datatables.net-bs4@1.10.24 chart.js@2.9.4 @fortawesome/fontawesome-free@5.15.3
```

Copie os arquivos de distribuição de `node_modules/` para as pastas correspondentes em `static/vendor/`. Não há etapa de compilação obrigatória.

## Verificar a instalação

```bash
python manage.py check
```

Saída esperada:

```text
System check identified no issues (0 silenced).
```

## Próximo passo

- [Configuração](configuracao.md)
