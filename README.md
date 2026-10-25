# FluxOS

> Idioma: [Português](README.md) | [English](README.en.md)

O **FluxOS** é um sistema open source de gestão comercial criado para centralizar clientes, pedidos, produtos e estoque em uma única aplicação. O projeto oferece uma base modular em Django, com autenticação, controle de acesso por perfil, painel administrativo, interface responsiva e suporte a português e inglês.

O sistema está em desenvolvimento ativo e já possui os fluxos principais de operação comercial implementados.

## Visão Geral

O FluxOS foi pensado para pequenos e médios negócios que precisam acompanhar o ciclo comercial sem depender de planilhas separadas. A aplicação reúne:

- cadastro e histórico de clientes;
- pedidos com múltiplos itens e controle de status;
- catálogo de produtos, categorias e disponibilidade;
- movimentações de estoque com validação de saldo;
- indicadores de faturamento, pedidos e estoque no dashboard;
- gestão de usuários e perfil com separação entre usuários comuns e equipe administrativa.

## Objetivos

### Objetivos de negócio

- Centralizar a operação comercial em um único sistema.
- Melhorar a visibilidade sobre vendas, clientes e estoque.
- Reduzir erros manuais em pedidos e movimentações de estoque.
- Apoiar decisões com indicadores atualizados de receita, pedidos e produtos em falta.
- Manter um histórico confiável de clientes, pedidos e alterações de estoque.

### Objetivos técnicos

- Oferecer uma arquitetura modular, com cada domínio em um app Django.
- Aplicar autenticação, autorização e validações no backend.
- Manter testes automatizados para os fluxos críticos.
- Ser simples de instalar e executar em ambiente de desenvolvimento.
- Permitir evolução gradual para relatórios, integrações e novos módulos.

## Funcionalidades Implementadas

### Dashboard

- Receita mensal e anual considerando pedidos concluídos e enviados.
- Contagem de pedidos pendentes.
- Lista de produtos com estoque baixo.
- Últimos pedidos cadastrados.
- Ranking dos clientes com maior valor gasto.
- Alertas globais de estoque baixo e pedidos pendentes.

### Clientes

- Cadastro, edição, listagem e exclusão de clientes.
- Endereço, gênero, estado civil e data de nascimento.
- Página de detalhes com histórico de pedidos.
- Total de pedidos e valor total gasto por cliente.
- Exclusão protegida por requisição POST.

### Pedidos

- Cadastro, edição, listagem, detalhes e exclusão de pedidos.
- Itens de pedido com produto e quantidade.
- Cálculo automático de subtotal e total.
- Status: pendente, concluído, cancelado, enviado e devolvido.
- Filtro de pedidos por status.
- Atualização automática das estatísticas do cliente.
- Pré-seleção do cliente ao criar um pedido a partir da página do cliente.

### Estoque

- Cadastro, edição e exclusão de produtos.
- Cadastro, edição e exclusão de categorias.
- Controle de disponibilidade e limite de estoque baixo.
- Filtro de produtos com estoque baixo.
- Movimentações de entrada e saída de estoque.
- Validação de quantidade e de saldo disponível.
- Registro do usuário responsável por cada movimentação.
- Bloqueio de edição de movimentações já registradas.

### Usuários e Segurança

- Login e logout.
- Gestão de usuários restrita à equipe administrativa.
- Criação e edição de usuários com validação de senha.
- Proteção contra autoativação, autodesativação e autoexclusão indevidas.
- Perfil do usuário limitado a nome, sobrenome, e-mail e nome de usuário.
- Rotas protegidas por autenticação.
- Exclusões e alterações sensíveis via POST.

### Interface e Internacionalização

- Interface responsiva com Bootstrap e SB Admin 2.
- Tabelas com DataTables.
- Gráficos e indicadores com Chart.js.
- Ícones com Font Awesome.
- Mensagens de sucesso e erro centralizadas.
- Idiomas disponíveis: inglês (`en-us`) e português do Brasil (`pt-br`).
- Traduções compiladas em `locale/pt_BR/LC_MESSAGES/`.

### Testes

A suíte cobre modelos, formulários, views, permissões, redirecionamentos, exclusões via POST, movimentações de estoque, estatísticas de clientes, dashboard, alertas, autenticação e troca de idioma.

## Roadmap

Itens ainda não implementados ou em evolução:

- fornecedores e pedidos de compra;
- contas a receber e conciliação financeira;
- relatórios avançados e exportação de dados;
- notificações por e-mail e lembretes;
- API para integrações externas;
- integração com WooCommerce;
- configuração de produção com Docker, Gunicorn e Nginx.

### Limitações atuais

- A criação de um pedido não baixa o estoque automaticamente; a baixa deve ser registrada como movimentação de saída.
- O dashboard considera receita somente para pedidos com status **Completed** ou **Shipped**.
- Os totais de clientes são mantidos de forma denormalizada e atualizados quando pedidos são criados, editados ou excluídos.
- O ambiente de produção ainda não está documentado neste repositório.

## Tecnologias e Dependências

### Backend

| Pacote | Versão | Finalidade |
| --- | --- | --- |
| Python | 3.14+ | Linguagem e runtime |
| Django | 6.0.6 | Framework web |
| django-environ | 0.14.0 | Leitura de variáveis de ambiente |
| django-widget-tweaks | 1.5.1 | Customização de widgets nos templates |
| psycopg | 3.x | Driver PostgreSQL |
| asgiref | 3.11.1 | Dependência do Django |
| sqlparse | 0.5.5 | Dependência do Django |
| tzdata | 2026.2 | Dados de fuso horário |

As versões do backend estão fixadas em `requirements.txt` e `pyproject.toml`. O driver `psycopg` deve ser instalado para usar PostgreSQL:

```bash
pip install "psycopg[binary]"
```

### Frontend

As bibliotecas de interface já estão incluídas no repositório, dentro de `static/`. Não é necessário executar `npm install` nem criar um build de frontend para rodar o projeto.

| Biblioteca | Versão | Local |
| --- | --- | --- |
| Bootstrap | 4.6.0 | `static/vendor/bootstrap/` |
| SB Admin 2 | 4.1.3 | `static/css/` e `static/js/` |
| jQuery | 3.6.0 | `static/vendor/jquery/` |
| jQuery Easing | 1.4.x | `static/vendor/jquery-easing/` |
| DataTables | 1.10.24 | `static/vendor/datatables/` |
| DataTables Bootstrap 4 | 1.10.24 | `static/vendor/datatables/` |
| Font Awesome Free | 5.15.3 | `static/vendor/fontawesome-free/` |
| Chart.js | 2.x | `static/vendor/chart.js/` |
| Google Fonts (Inter) | CDN | Carregado em `templates/head.html` |

O Bootstrap é a base do layout responsivo. O template SB Admin 2 fornece a estrutura visual do painel, e o DataTables adiciona ordenação, busca e paginação às tabelas.

#### Reinstalação opcional das dependências frontend

O projeto não exige Node.js. Caso seja necessário atualizar ou restaurar as bibliotecas, baixe as distribuições oficiais e mantenha a estrutura de pastas usada em `static/vendor/`:

- Bootstrap 4: https://getbootstrap.com/docs/4.6/getting-started/download/
- jQuery: https://jquery.com/download/
- DataTables: https://datatables.net/download/
- Font Awesome 5: https://fontawesome.com/v5/download
- Chart.js: https://www.chartjs.org/docs/
- SB Admin 2: https://startbootstrap.com/theme/sb-admin-2

Também é possível usar npm em um diretório temporário:

```bash
npm install bootstrap@4.6.0 jquery@3.6.0 jquery.easing@1.4.1 datatables.net@1.10.24 datatables.net-bs4@1.10.24 chart.js@2.9.4 @fortawesome/fontawesome-free@5.15.3
```

Depois, copie os arquivos necessários de `node_modules/` para as pastas correspondentes em `static/vendor/`. Não há etapa de compilação obrigatória.

## Estrutura do Projeto

```text
FluxOS/
├── apps/
│   ├── customers/          # Clientes
│   ├── dashboard/          # Dashboard e perfil
│   ├── members/            # Usuários e controle de acesso
│   ├── orders/             # Pedidos, itens e estatísticas
│   └── stock/              # Produtos, categorias e movimentações
├── core/                   # Configurações, URLs e context processors
├── docs/                   # Documentação complementar
├── locale/                 # Traduções (pt-BR e en-US)
├── static/
│   ├── css/                # Estilos globais e SB Admin 2
│   ├── img/                # Imagens
│   ├── js/                 # Scripts globais
│   └── vendor/             # Bootstrap, jQuery, DataTables, Chart.js etc.
├── templates/              # Templates globais e de autenticação
├── manage.py
├── requirements.txt
├── pyproject.toml
├── uv.lock
└── .env.example
```

## Instalação

### Pré-requisitos

- Python 3.14 ou superior
- Git
- `pip`
- PostgreSQL 14+ (recomendado; o projeto também funciona com SQLite para desenvolvimento)
- Node.js apenas se for reinstalar as bibliotecas de frontend manualmente

> Não é necessário instalar Bootstrap, jQuery, DataTables, Chart.js ou Font Awesome separadamente: os arquivos já estão versionados no projeto.

### 1. Clonar o repositório

```bash
git clone https://github.com/<usuario>/FluxOS.git
cd FluxOS
```

### 2. Criar e ativar o ambiente virtual

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

Se o PowerShell bloquear a ativação, execute apenas para a sessão atual:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### 3. Instalar as dependências Python

Atualize o `pip` e instale os pacotes:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Alternativamente, com `uv`:

```bash
uv sync
```

O `psycopg` é o driver utilizado quando `DATABASE_URL` aponta para PostgreSQL. Instale a distribuição binária, que não exige ferramentas de compilação:

```bash
pip install "psycopg[binary]"
```

Em sistemas onde o driver é compilado do código-fonte, é necessário ter a `libpq` instalada. Para desenvolvimento rápido com SQLite, não é preciso instalar um servidor de banco, mas o driver PostgreSQL ainda deve ser instalado para uso com PostgreSQL.

### 4. Configurar as variáveis de ambiente

Copie o arquivo de exemplo:

Linux/macOS:

```bash
cp .env.example .env
```

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Gere uma nova `SECRET_KEY`:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Edite `.env` e substitua o valor de `SECRET_KEY`.

Para PostgreSQL:

```env
DATABASE_URL=postgresql://usuario:senha@127.0.0.1:5432/fluxos
```

Para desenvolvimento rápido com SQLite:

```env
DATABASE_URL=sqlite:///db.sqlite3
```

Configurações opcionais:

```env
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
LANGUAGE_CODE=pt-br
TIME_ZONE=America/Sao_Paulo
```

O arquivo `.env` não é versionado.

### 5. Criar o banco de dados

Com SQLite, o banco é criado automaticamente na primeira migração.

Com PostgreSQL, crie o banco antes de migrar:

```sql
CREATE DATABASE fluxos
    WITH ENCODING 'UTF8'
    TEMPLATE template0;
```

### 6. Aplicar migrações

```bash
python manage.py migrate
```

### 7. Criar um superusuário

```bash
python manage.py createsuperuser
```

Informe nome de usuário, e-mail e senha.

### 8. Executar o servidor

```bash
python manage.py runserver
```

Acesse:

- Aplicação: http://127.0.0.1:8000/
- Painel administrativo: http://127.0.0.1:8000/admin/

### 9. Verificar a instalação

```bash
python manage.py check
python manage.py test
```

A suíte atual cobre os apps de clientes, pedidos, estoque, usuários, dashboard e o módulo core.

## Comandos Úteis

```bash
# Criar novas migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Abrir o shell do Django
python manage.py shell

# Executar todos os testes
python manage.py test

# Executar testes de um app específico
python manage.py test apps.stock

# Verificar o projeto
python manage.py check
```

## Internacionalização

O projeto inclui inglês e português do Brasil. O idioma pode ser alterado pelo seletor no topo da interface.

Arquivos de tradução:

```text
locale/
└── pt_BR/
    └── LC_MESSAGES/
        ├── django.po
        └── django.mo
```

Os arquivos `.mo` já estão compilados. Caso altere traduções e tenha o GNU gettext instalado:

```bash
python manage.py compilemessages
```

## Documentação Complementar

- [Índice da documentação](docs/README.md)
- [Instalação](docs/primeiros-passos/instalacao.md)
- [Configuração](docs/primeiros-passos/configuracao.md)
- [Primeira execução](docs/primeiros-passos/primeira-execucao.md)
- [Documentação em inglês](docs/getting-started/installation.md)

## Licença

Este projeto está licenciado sob a GNU General Public License v3.0. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.
