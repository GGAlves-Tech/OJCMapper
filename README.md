# Base Architecture - Flask + PyWebView

Este é um boilerplate de aplicação desktop utilizando **Flask** para o backend/UI logic e **PyWebView** para a interface nativa, estruturado seguindo os princípios da **Arquitetura Hexagonal (Clean Architecture)**.

## 🚀 Tecnologias Utilizadas

- **Python 3.10+**: Linguagem base.
- **Flask**: Micro-framework web para gerenciar rotas, lógica e templates.
- **PyWebView**: Biblioteca para criar janelas desktop nativas que renderizam conteúdo web.
- **SQLite**: Banco de dados relacional leve (boilerplate de repositório incluído).
- **Jinja2**: Motor de templates para o frontend equilibrado.

## 🏗️ Padrões de Arquitetura

O projeto segue a **Arquitetura Hexagonal**, dividida em:

- **Domain (Domínio)**: Contém as regras de negócio puras e definições de interfaces (Ports). Não possui dependências externas.
- **Application (Aplicação)**: Casos de uso que orquestram a lógica do domínio e chamam os adaptadores.
- **Infrastructure (Infraestrutura)**: Implementações técnicas (Adapters).
    - **Web**: Servidor Flask, controladores e recursos estáticos.
    - **Persistence**: Acesso a dados (SQLite).

## 📂 Estrutura de Pastas

```text
/
├── main.py              # Ponto de entrada (Bootstrap)
├── requirements.txt     # Dependências do projeto
└── src/
    ├── application/     # Camada de Aplicação (Serviços/Cases)
    ├── domain/          # Camada de Domínio (Entidades/Interfaces)
    └── infrastructure/  # Camada de Infraestrutura (Drivers/Adapters)
        ├── persistence/ # Implementação de Repositórios
        └── web/         # Flask App, Controllers, Templates/Static
```

## 🛠️ Como Executar

### 1. Pré-requisitos
Certifique-se de ter o Python instalado em sua máquina.

### 2. Configuração do Ambiente
Clone o repositório e navegue até a pasta do projeto:

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual (Windows)
.\venv\Scripts\activate

# Ativar ambiente virtual (Linux/macOS)
source venv/bin/activate
```

### 3. Instalação de Dependências
```bash
pip install -r requirements.txt
```

### 4. Execução
```bash
python main.py
```

## 📦 Empacotamento (Build)
Para gerar um executável (.exe) utilizando o PyInstaller:

```bash
pyinstaller --noconfirm --onefile --windowed --add-data "src/infrastructure/web/templates;infrastructure/web/templates" --add-data "src/infrastructure/web/static;infrastructure/web/static" main.py
```
*(Nota: Ajuste os caminhos de `--add-data` conforme necessário para o seu sistema)*

---
Desenvolvido como uma base sólida para aplicações desktop modernas e modulares.
