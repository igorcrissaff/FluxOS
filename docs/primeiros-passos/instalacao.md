# Instalação

Este guia descreve como preparar um ambiente de desenvolvimento para o FluxOS.

---

## Requisitos

Antes de iniciar, verifique se possui os seguintes softwares instalados:

| Software | Versão recomendada |
|-----------|-------------------|
| Python | 3.12 ou superior |
| Git | Última versão |
| MySQL | 8.0 ou superior |
| Docker | 28+ (Opcional) |
| Docker Compose | 2+ (Opcional) |

Também é recomendado utilizar um editor como:

- Visual Studio Code
- PyCharm Professional ou Community

---

## Clonando o repositório

```bash
git clone https://github.com/<usuario>/FluxOS.git

cd FluxOS
```

---

## Criando um ambiente virtual

### Linux/macOS

```bash
python3 -m venv .venv

source .venv/bin/activate
```

### Windows (PowerShell)

```powershell
python -m venv .venv

.venv\Scripts\Activate.ps1
```

---

## Atualizando o pip

```bash
python -m pip install --upgrade pip
```

---

## Instalando as dependências

```bash
pip install -r requirements/dev.txt
```

---

## Verificando a instalação

```bash
python manage.py check
```

Saída esperada:

```
System check identified no issues.
```

---

## Próximo passo

Após concluir a instalação, siga para:

- configuracao.md