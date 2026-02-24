# OJCMapper - Gestão de Mapeamentos de Rede

> [!IMPORTANT]
> **Aplicação Nativa Windows Desktop**
> Este software foi projetado exclusivamente para o sistema operacional Windows, utilizando comandos nativos de rede (`net use`) e interface `pywebview`.

Utilitário desktop para gerenciamento de mapeamentos de rede e organização de projetos (Online/Gaveta), desenvolvido como parte da Disciplana de Projeto Integrador TADS UNITINS/Anhanguera.

## 🚀 Sobre o Projeto


O **OJCMapper** é uma evolução do protótipo inicial, agora construído sobre uma base sólida de **Arquitetura Hexagonal (Ports and Adapters)**. O sistema permite que usuários conectem e gerenciem diretórios de rede de forma intuitiva, oferecendo uma interface desktop moderna baseada em tecnologias web.

### Principais Funcionalidades
- **Conexão Dinâmica**: Mapeamento de unidades de rede Windows via interface visual.
- **Gestão de Projetos**: Organização categorizada entre projetos ativos (Online) e arquivados (Gaveta).
- **Relatórios**: Exportação de dados consolidados para auditoria.
- **Segurança**: Controle de acesso baseado em perfis (Gerente, Editor, Default).
- **Interface Desktop**: Janela nativa leve utilizando `pywebview`.

## 🛠️ Stack Tecnológica

- **Linguagem**: Python 3.12+
- **Backend / Web Adapter**: Flask
- **Frontend**: HTML5, Tailwind CSS, JavaScript Vanilla
- **Desktop Wrapper**: pywebview
- **Persistência**: SQLite 3
- **Arquitetura**: Hexagonal (Clean Architecture)

## 🏗️ Arquitetura

O projeto segue os princípios da **Arquitetura Hexagonal** para garantir o desacoplamento total entre as regras de negócio e os componentes externos:

```text
src/
├── domain/            # Regras de Negócio e Entidades (Puro Python)
├── application/       # Casos de Uso (Orquestração do Sistema)
└── infrastructure/    # Implementações Técnicas (Adaptadores)
    ├── persistence/   # Mapeadores e Repositórios SQLite
    ├── system/        # Integração com Windows OS
    └── web/           # Flask App, Templates e Static Assets
```

## 🏁 Início Rápido

Siga os passos abaixo para rodar o projeto em ambiente de desenvolvimento:

### 1. Pré-requisitos
- Python 3.12 ou superior instalado.
- Sistema Operacional Windows (necessário para comandos de rede `net use`).

### 2. Instalação
Clone o repositório e acesse a pasta do projeto:
```bash
git clone <url-do-repositorio>
cd OJCMapper
```

Crie e ative um ambiente virtual (recomendado):
```bash
python -m venv venv
venv\Scripts\activate
```

Instale as dependências:
```bash
pip install -r requirements.txt
```

### 3. Execução
Para iniciar a aplicação em modo desktop:
```bash
python main_desktop.py
```

### 4. Credenciais de Teste (Padrão)
| Usuário | Senha | Perfil |
| :--- | :--- | :--- |
| `admin` | `admin` | Gerente |
| `editor` | `editor` | Editor |
| `user` | `user` | Default |

---

## 📦 Empacotamento

Para gerar o executável (.exe) standalone:
```bash
python build_exe.py
```
> O executável será gerado em `dist/MAPPER_OJC.exe`

## 📝 Licença
Este projeto é acadêmico e segue as diretrizes da instituição UNITINS/Anhanguera.

---
*Mantido por Guthemberg B. Alves - 2026*
