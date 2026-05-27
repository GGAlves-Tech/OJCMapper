# OJCMapper - Gestão de Mapeamentos de Rede

> [!IMPORTANT]
> **Aplicação Nativa Windows Desktop**
> Este software foi projetado exclusivamente para o sistema operacional Windows, utilizando comandos nativos de rede (`net use`) e interface `pywebview`.

Utilitário desktop para gerenciamento de mapeamentos de rede e organização de projetos (Online/Gaveta), desenvolvido como parte da Disciplina de Projeto Integrador TADS UNITINS/TV Anhanguera - Palmas-TO.

## 🚀 Sobre o Projeto

O **OJCMapper** é uma evolução do protótipo inicial, construído sobre **Arquitetura Hexagonal (Ports and Adapters)** com princípios de **DDD (Domain-Driven Design)**. O sistema permite que usuários conectem e gerenciem diretórios de rede de forma intuitiva, oferecendo uma interface desktop moderna baseada em tecnologias web.

### Principais Funcionalidades
- **Conexão Dinâmica**: Mapeamento de unidades de rede Windows via interface visual.
- **Gestão de Projetos**: Organização categorizada entre projetos ativos (Online) e arquivados (Gaveta).
- **Relatórios**: Exportação de listas de projetos consolidadas em arquivo `.txt`.
- **Segurança**: Controle de acesso baseado em perfis (Gerente, Editor, Default).
- **Auditoria**: Registro automático de ações por usuário em arquivos de log diários.
- **Interface Desktop**: Janela nativa leve utilizando `pywebview`.

## 🛠️ Stack Tecnológica

- **Linguagem**: Python 3.12+
- **Backend / Web Adapter**: Flask
- **Frontend**: HTML5, Tailwind CSS, JavaScript Vanilla
- **Desktop Wrapper**: pywebview
- **Persistência**: SQLite 3
- **Logging**: módulo `logging` da biblioteca padrão Python
- **Arquitetura**: Hexagonal + DDD (Bounded Contexts, Domain Events, Ports & Adapters)

## 🏗️ Arquitetura

O projeto segue **Arquitetura Hexagonal** com **Bounded Contexts** do DDD. O domínio é puro Python sem dependências externas; toda integração com infraestrutura ocorre via interfaces abstratas (ports) implementadas por adapters.

```
Domain (núcleo) ← Application (use cases) ← Infrastructure (adapters)
```

### Bounded Contexts

```text
src/
├── domain/
│   ├── identity/          # Usuários: User, UserRepository, UsuarioCriado, UsuarioRemovido
│   ├── projects/          # Projetos: Project, ProjectRepository, ProjetoEngavetado, ProjetoDeletado
│   ├── drives/            # Drives: DriveMapper, UnidadeMapeada, UnidadeDesconectada
│   ├── audit/             # Auditoria: AuditPort
│   └── shared/            # Compartilhado: Setting, Role, ProjectType, DomainEvent,
│                          #               EventBus, FileSystemPort, SettingsRepository
│
├── application/           # Casos de uso (orquestração, sem I/O direto)
│   ├── auth_service.py
│   ├── project_service.py
│   ├── map_service.py
│   ├── delete_service.py
│   ├── settings_service.py
│   └── export_service.py
│
└── infrastructure/        # Adapters (implementações concretas)
    ├── audit/             # FileAuditLogger — {hostname}_{data}.log
    ├── persistence/       # SQLiteRepository + mappers (User, Project, Setting)
    ├── system/            # WindowsDriveMapper, LocalFileSystemAdapter
    └── web/               # Flask app, blueprints, templates, static
```

### Domain Events

Operações críticas publicam eventos no `EventBus`, permitindo reações desacopladas:

| Evento | Contexto | Disparado por |
|--------|----------|---------------|
| `UsuarioCriado` | identity | criação de usuário |
| `UsuarioRemovido` | identity | remoção de usuário |
| `ProjetoEngavetado` | projects | mover projeto Online → Gaveta |
| `ProjetoDeletado` | projects | exclusão de projeto |
| `UnidadeMapeada` | drives | mapeamento de drive |
| `UnidadeDesconectada` | drives | desmapeamento de drive |

### Logs de Auditoria

Cada ação de escrita é registrada em `{diretório_configurado}/{hostname}_{data}.log`:

```
2026-05-26 14:30:00_admin_usuario-criado:joao
2026-05-26 14:35:00_admin_projeto-deletado:ProjetoX:ONLINE
2026-05-26 14:40:00_joao_unidade-mapeada:F:ProjetoY
```

O diretório é configurável em **Configurações → Diretório de Logs de Auditoria** e a mudança tem efeito imediato, sem necessidade de reiniciar a aplicação.

Erros de sistema são registrados no terminal via `logging` padrão Python.

## 🏁 Início Rápido

### 1. Pré-requisitos
- Python 3.12 ou superior instalado.
- Sistema Operacional Windows (necessário para comandos de rede `net use`).

### 2. Instalação
Clone o repositório e acesse a pasta do projeto:
```bash
git clone <url-do-repositorio>
cd OJCMapper
```

Crie e ative um ambiente virtual:
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

Para iniciar em modo desenvolvimento (Flask com debug):
```bash
python run_dev.py
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
Este projeto é acadêmico e segue as diretrizes da instituição UNITINS/TV Anhanguera - Palmas-TO.

---
*Mantido por Guthemberg B. Alves - 2026*
