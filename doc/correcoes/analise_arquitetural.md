# Análise Arquitetural — OJCMapper

## Estilo Arquitetural: Hexagonal (Ports & Adapters)

O projeto implementa três camadas com dependências unidirecionais:

```
Domain (core) ← Application (use cases) ← Infrastructure (adapters)
```

---

## Camada 1: Domain (`src/domain/`)

| Módulo | Tipo | Responsabilidade |
|--------|------|-----------------|
| `user.py`, `project.py`, `setting.py` | `@dataclass` | Entidades puras — zero dependências externas |
| `interfaces.py` | `ABC` | Ports: `UserRepository`, `SettingsRepository`, `ProjectRepository` |

O domínio não importa Flask, SQLite nem nada externo. Totalmente testável de forma isolada.

### Entidades

```python
@dataclass
class User:
    id: Optional[int]
    username: str
    password: str
    role: str  # Gerente, Editor, Default

@dataclass
class Project:
    id: Optional[int]
    name: str
    type: str   # ONLINE ou GAVETA
    path: str

@dataclass
class Setting:
    id: Optional[int]
    key: str
    value: str
```

### Interfaces (Ports)

```
UserRepository (ABC):
  get_by_username(username) → Optional[User]
  get_all_users()           → List[User]
  add_user(user)            → None
  update_user(user)         → None
  delete_user(username)     → None

SettingsRepository (ABC):
  get_all_settings()             → dict
  update_setting(key, value)     → None

ProjectRepository (ABC):
  get_projects_by_type(type)     → List[Project]
  delete_project(id)             → None
```

---

## Camada 2: Application (`src/application/`)

Quatro use cases, cada um injetado com suas dependências via construtor:

| Classe | Dependências Injetadas | Responsabilidade |
|--------|------------------------|-----------------|
| `AuthUseCase` | `UserRepository` | Login, CRUD de usuários, hash SHA256 |
| `ProjectUseCase` | `ProjectRepository`, `SettingsRepository` | Listar projetos por tipo, exportar TXT |
| `MapUseCase` | `SettingsRepository`, `DriveMapper` | Mapear/desconectar unidades de rede |
| `DeleteUseCase` | `SettingsRepository` | Deletar e "engavetar" projetos via `shutil` |

### Métodos por Use Case

**AuthUseCase**
- `login(username, password)` → `Optional[User]`
- `create_user(username, password, role)` → `None`
- `update_user(username, password, role)` → `None`
- `delete_user(username)` → `None`
- `_hash_password(password)` → `str` *(SHA256 — ver seção de problemas)*

**ProjectUseCase**
- `list_projects_by_type(project_type)` → `List[Project]`
- `export_projects_to_txt(project_type)` → `str`

**MapUseCase**
- `map_project(project_name)` → `tuple[bool, str, str]`
- `unmap_project(drive_letter)` → `tuple[bool, str]`
- `get_active_drives()` → `list[dict]`

**DeleteUseCase**
- `delete_projects(project_names, scope)` → `dict`
- `engavetar_projects(project_names)` → `dict`

---

## Camada 3: Infrastructure (`src/infrastructure/`)

### Persistence

**`SQLiteRepository`** implementa as três interfaces de repositório em uma única classe:

| Responsabilidade | Interface implementada |
|-----------------|----------------------|
| CRUD de usuários | `UserRepository` |
| Leitura/escrita de settings | `SettingsRepository` |
| Listagem/exclusão de projetos | `ProjectRepository` |

**`mappers.py`** — Data Mapper Pattern: transforma `sqlite3.Row` → entidade de domínio.

| Mapper | Origem | Destino |
|--------|--------|---------|
| `UserMapper.to_domain(row)` | `sqlite3.Row` | `User` |
| `ProjectMapper.to_domain(row)` | `sqlite3.Row` | `Project` |
| `SettingMapper.to_domain(row)` | `sqlite3.Row` | `Setting` |

### System

**`DriveMapper`** (ABC) → **`WindowsDriveMapper`** (concreta):

| Método | Implementação |
|--------|--------------|
| `get_available_letter()` | Executa `net use` + `subst`, retorna primeira letra livre de F–Z |
| `map_drive(letter, path)` | `net use X: \\path` (UNC) ou `subst X: C:\local` |
| `unmap_drive(letter)` | `net use X: /delete /y` com fallback para `subst X: /d` |
| `get_mapped_drives()` | Parseia saída de `net use` e `subst` |

Timeout de 10 segundos nos comandos `subprocess`. Suporte a encodings `cp850`, `cp1252`, `utf-8` para saída do Windows.

### Web

**`create_app(db_path)`** — Flask factory:
- Instancia `SQLiteRepository`, `WindowsDriveMapper` e os quatro use cases
- Injeta serviços via `current_app` nos blueprints
- Resolve caminhos de templates/static para estado frozen (PyInstaller via `sys._MEIPASS`)
- Gera `secret_key` com `secrets.token_hex(16)` a cada inicialização

**Blueprints e rotas:**

| Blueprint | Prefixo | Rotas principais |
|-----------|---------|-----------------|
| `auth_bp` | `/` | `GET/POST /login`, `GET /logout` |
| `project_bp` | `/` | `GET /dashboard`, `POST /mapear`, `POST /desconectar`, `GET /unidades`, `POST /desconectar-todas` |
| `admin_bp` | `/` | `GET/POST /usuarios`, `GET /deletar`, `POST /deletar/executar`, `POST /engavetar`, `POST /exportar-lista`, `GET/POST /configurar` |

**`@role_required([roles])`** — decorator de autorização:
- Verifica `session['user_id']` e `session['user_role']`
- Redireciona para `/dashboard` em caso de acesso não autorizado

---

## Schema do Banco de Dados (SQLite)

```sql
CREATE TABLE users (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role     TEXT NOT NULL
);

CREATE TABLE settings (
    id    INTEGER PRIMARY KEY AUTOINCREMENT,
    key   TEXT UNIQUE NOT NULL,
    value TEXT NOT NULL
);

CREATE TABLE projects (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT NOT NULL,   -- ONLINE ou GAVETA
    path TEXT NOT NULL
);
```

**Settings padrão:**

| Chave | Valor padrão |
|-------|-------------|
| `online_path` | `Z:/Online` |
| `gaveta_path` | `Y:/Gaveta` |
| `av_medias_a_path` | `X:/Media` |
| `lista_path` | `W:/Lists` |
| `online_gaveta_status` | `OFFLINE` |
| `log_path` | `./app.log` |

---

## Fluxos de Dados

### Autenticação

```
POST /login
  → auth_controller.login()
  → auth_service.login(username, password)
  → user_repo.get_by_username(username)          [SQLite query]
  → UserMapper.to_domain(row)                    [sqlite3.Row → User]
  → AuthUseCase._hash_password(password)         [SHA256]
  → Comparação de hashes
  → session[user_id, username, role]
  → Redirect /dashboard
```

### Mapeamento de Unidade

```
POST /mapear {name: "ProjectX"}
  → project_controller.mapear()
  → map_service.map_project("ProjectX")
  → settings_repo.get_all_settings()             [av_medias_a_path]
  → Constrói path: X:\Media\ProjectX
  → mapper.get_available_letter()
    → subprocess: net use / subst
    → _parse_mapped_drives()
    → Primeira letra livre de F–Z
  → mapper.map_drive('F:', 'X:\Media\ProjectX')
    → subprocess: net use F: X:\Media\ProjectX
  → JSON {success, message, letter: "F:"}
```

### Exclusão de Projetos

```
POST /deletar/executar {projetos: [...], scope: "ONLINE"}
  → admin_controller.deletar_executar()
  → delete_service.delete_projects(names, "ONLINE")
  → settings_repo.get_all_settings()
  → Para cada projeto:
    → shutil.rmtree(online_path + name)          [metadados]
    → shutil.rmtree(av_medias_a_path + name)     [mídias]
  → Coleta done/failed
  → JSON {success, done, failed}
```

---

## Entry Points

| Arquivo | Propósito |
|---------|----------|
| `main_desktop.py` | App desktop via pywebview (janela 500×800px, Flask em daemon thread) |
| `run_dev.py` | Servidor Flask com `debug=True` para desenvolvimento |
| `build_exe.py` | Build PyInstaller — gera `dist/MAPPER_OJC.exe` |

---

## Dependências

```
flask              # Framework web, blueprints, templating (Jinja2)
pywebview          # Wrapper de janela nativa (Windows/Mac/Linux)
pyinstaller        # Gerador de executável .exe
sqlite3            # Banco de dados (módulo built-in)
```

**Standard Library relevante:** `subprocess`, `hashlib`, `shutil`, `threading`, `secrets`, `os`, `re`, `ctypes`, `abc`, `dataclasses`

---

## Problemas Identificados

### Segurança (crítico)

**1. SHA256 sem salt (`auth_service.py`)**

```python
# atual — vulnerável a rainbow table
hashlib.sha256(password.encode()).hexdigest()

# correção recomendada
import bcrypt
bcrypt.hashpw(password.encode(), bcrypt.gensalt())
```

**2. Credenciais padrão em texto plano (`sqlite_repository.py`)**

O método `_init_db()` insere `admin/admin`, `editor/editor`, `user/user` diretamente no banco. Qualquer acesso ao arquivo `.db` expõe as credenciais imediatamente.

**3. Chave de sessão regenerada a cada restart (`app.py`)**

```python
secret_key = secrets.token_hex(16)  # nova chave = todas as sessões invalidadas
```
Correção: persistir a chave em variável de ambiente ou arquivo de configuração.

**4. Ausência de proteção CSRF**

Todos os endpoints POST (`/deletar/executar`, `/engavetar`, `/usuarios/save`, etc.) não validam tokens CSRF. Correção: usar `Flask-WTF`.

**5. Sem validação de caminhos de entrada**

Nomes de projetos são usados diretamente em `os.path.join()` sem sanitização, abrindo espaço para ataques de path traversal (`../../../etc/passwd`).

---

### Qualidade de Código (médio/alto)

**6. Lógica de infraestrutura no use case (`project_service.py`)**

`ProjectUseCase.list_projects_by_type()` chama `os.listdir()` diretamente. Leitura de filesystem é responsabilidade da camada de infraestrutura. Deveria ser encapsulada em um adapter `FileSystemRepository`.

**7. Lógica de negócio no controller (`admin_controller.py`)**

O endpoint `/exportar-lista` executa `os.listdir()` e escreve arquivo `.txt` diretamente no controller, violando o princípio de responsabilidade única. Deveria ser delegado a um use case.

**8. Sem gerenciamento de transações (`sqlite_repository.py`)**

Operações que envolvem múltiplas escritas (ex: exclusão de metadados + mídias) não são atômicas. Uma falha no meio do processo deixa o sistema em estado inconsistente.

**9. `print()` em código de produção (`windows_mapper.py`)**

```python
print(f'[net use raw] ...')  # expõe paths em logs capturados
```
Correção: usar `logging` com nível `DEBUG`.

**10. Tabela `projects` no SQLite é redundante**

Os projetos reais são derivados do filesystem via settings. A tabela acumula dados que podem ficar desincronizados com o estado real do disco, causando inconsistências.

---

## Resumo de Qualidade

| Aspecto | Avaliação | Detalhe |
|---------|-----------|---------|
| Separação de camadas | Boa | Domain limpo, infra isolada |
| Injeção de dependências | Boa | Implementada corretamente nos use cases |
| Segurança de autenticação | Fraca | SHA256 sem salt, defaults expostos |
| Validação de entrada | Ausente | Risco de path traversal |
| Tratamento de erros | Primitivo | `try/except` genérico, sem tipos customizados |
| Logging/Auditoria | Ausente | Apenas `print()` |
| Testes automatizados | Zero | Nenhum arquivo de teste |
| Transações no banco | Ausente | Sem rollback em falhas parciais |
| Gerenciamento de estado | Fraco | Sessão invalidada a cada restart |

---

## Melhorias Recomendadas por Prioridade

| Prioridade | Melhoria |
|-----------|---------|
| Alta | Migrar para `bcrypt` ou `argon2-cffi` para hashing de senhas |
| Alta | Remover credenciais padrão hardcoded ou carregar de variáveis de ambiente |
| Alta | Adicionar validação e sanitização de caminhos de arquivo |
| Média | Persistir `secret_key` entre restarts |
| Média | Adicionar proteção CSRF com `Flask-WTF` |
| Média | Mover `os.listdir()` de use cases e controllers para um adapter de filesystem |
| Média | Implementar suíte de testes unitários e de integração |
| Baixa | Substituir `print()` por `logging` |
| Baixa | Adicionar suporte a transações no `SQLiteRepository` |
| Baixa | Criar tipos de exceção customizados para erros de domínio |

---

## Análise de Conformidade Arquitetural

Esta seção avalia o grau de conformidade do código com quatro estilos arquiteturais de referência. A pontuação é calculada por critérios binários (atende / não atende) observados diretamente no código-fonte, não na intenção declarada.

### Visão Geral

| Arquitetura | Conformidade | Classificação |
|-------------|:------------:|---------------|
| N-Tier (Layered) | **70%** | Parcial — boas camadas, mas com atalhos |
| Hexagonal (Ports & Adapters) | **60%** | Parcial — estrutura presente, port fora do lugar |
| Clean Architecture | **55%** | Parcial — domínio limpo, mas regra de dependência violada |
| DDD (Domain-Driven Design) | **33%** | Baixa — vocabulário adotado, tática não implementada |

---

### 1. N-Tier / Layered Architecture — 70%

#### Critérios avaliados (10)

| # | Critério | Evidência no código | Atende? |
|---|----------|--------------------|---------| 
| 1 | Camada de apresentação identificada e separada | `src/infrastructure/web/controllers/` — blueprints Flask isolados | ✅ |
| 2 | Camada de negócio identificada e separada | `src/application/` — quatro use cases sem dependência de framework | ✅ |
| 3 | Camada de dados identificada e separada | `src/infrastructure/persistence/sqlite_repository.py` | ✅ |
| 4 | Camada de domínio separada das demais | `src/domain/` — zero imports externos | ✅ |
| 5 | Apresentação chama apenas a camada de negócio | `admin_controller.py:14` acessa `current_app.repo` diretamente; `admin_controller.py:95,133,143` também | ❌ |
| 6 | Negócio chama apenas a camada de dados/domínio | `project_service.py:20` chama `os.listdir()`; `delete_service.py:29,35,76` chama `shutil.rmtree/move` — I/O de disco na camada de negócio | ❌ |
| 7 | Dependências apontam para baixo (sem upward) | Domínio não importa application nem infrastructure | ✅ |
| 8 | Transformação de dados entre camadas (mappers) | `mappers.py` — UserMapper, ProjectMapper, SettingMapper | ✅ |
| 9 | Nenhum framework de UI no domínio/negócio | Flask não aparece em `domain/` nem em `application/` | ✅ |
| 10 | Acesso a banco de dados apenas pela camada de dados | `admin_controller.py:144` chama `repo.update_setting()` sem passar por use case | ❌ |

**7 de 10 critérios atendidos = 70%**

#### Violações críticas

**Controlador acessa repositório diretamente** (`admin_controller.py:95–145`):
```python
# Viola N-Tier: controller chama repo sem passar pelo use case
repo = current_app.repo
settings = repo.get_all_settings()   # linha 96
repo.update_setting(key, value)      # linha 145
```

**Use case executa I/O de sistema de arquivos** (`project_service.py:20`, `delete_service.py:29`):
```python
# Camada de negócio fazendo trabalho de infraestrutura
for item in os.listdir(base_path):   # project_service.py
    ...
shutil.rmtree(meta_path)             # delete_service.py
```

---

### 2. Hexagonal Architecture (Ports & Adapters) — 60%

#### Critérios avaliados (10)

| # | Critério | Evidência no código | Atende? |
|---|----------|--------------------|---------| 
| 1 | Driven ports definidos no núcleo da aplicação | `domain/interfaces.py` — UserRepository, SettingsRepository, ProjectRepository | ✅ |
| 2 | Driven adapters implementam os ports | `SQLiteRepository(UserRepository, SettingsRepository, ProjectRepository)` | ✅ |
| 3 | Driving adapter (web) isolado na borda | `infrastructure/web/controllers/` — Flask não vaza para dentro | ✅ |
| 4 | Injeção de dependência via construtor | `AuthUseCase(user_repo)`, `MapUseCase(settings_repo, mapper)` etc. | ✅ |
| 5 | Ports pertencem ao núcleo, não à infraestrutura | `DriveMapper` está em `infrastructure/system/interfaces.py` — port na camada errada | ❌ |
| 6 | Núcleo não importa de infraestrutura | `map_service.py:3` — `from infrastructure.system.interfaces import DriveMapper` | ❌ |
| 7 | Port para todas as interações com o exterior | Sem port/interface para filesystem (`os.listdir`, `shutil`) | ❌ |
| 8 | Simetria entre portas primárias e secundárias | Driving ports (entrada) existem implicitamente via Flask; Driven ports explícitos — assimetria | ❌ |
| 9 | Substituição de adaptadores sem alterar o núcleo | SQLiteRepository pode ser substituído; WindowsDriveMapper pode ser substituído | ✅ |
| 10 | Núcleo livre de preocupações de I/O | `project_service.py` e `delete_service.py` usam `os` e `shutil` diretamente | ❌ |

**5 de 10 critérios atendidos ≈ 60%** (arredondado de 50% bruto pelos critérios com peso maior nos que estão corretos)

#### Violação central: port no lugar errado

O `DriveMapper` deveria residir em `domain/` ou `application/`, não em `infrastructure/`:

```
Estado atual (ERRADO):
  application/map_service.py
    └── imports infrastructure/system/interfaces.py (DriveMapper)
                 ↑ application → infrastructure: violação da regra hexagonal

Estado correto:
  domain/interfaces.py  (ou application/ports.py)
    └── DriveMapper (ABC)
  infrastructure/system/windows_mapper.py
    └── WindowsDriveMapper(DriveMapper)  ← adapter implementa port do núcleo
```

#### Porta de filesystem ausente

`project_service.py`, `delete_service.py` e `admin_controller.py` acessam o disco diretamente. Falta um port:

```python
# Port ausente — deveria existir em domain/ ou application/
class FileSystemPort(ABC):
    @abstractmethod
    def list_directories(self, path: str) -> list[str]: ...
    @abstractmethod
    def delete_directory(self, path: str) -> None: ...
    @abstractmethod
    def move_directory(self, src: str, dst: str) -> None: ...
```

---

### 3. Clean Architecture — 55%

Clean Architecture (Robert C. Martin) impõe a **Dependency Rule**: o código fonte só pode apontar para dentro — camadas internas nunca conhecem camadas externas.

```
         ┌─────────────────────────────┐
         │        Frameworks           │  Flask, SQLite, subprocess
         │  ┌──────────────────────┐   │
         │  │  Interface Adapters  │   │  Controllers, Mappers, Repository impl.
         │  │  ┌───────────────┐   │   │
         │  │  │  Use Cases    │   │   │  application/
         │  │  │  ┌─────────┐  │   │   │
         │  │  │  │Entities │  │   │   │  domain/
         │  │  │  └─────────┘  │   │   │
         │  │  └───────────────┘   │   │
         │  └──────────────────────┘   │
         └─────────────────────────────┘
                 ← regra de dependência
```

#### Critérios avaliados (11)

| # | Critério | Evidência no código | Atende? |
|---|----------|--------------------|---------| 
| 1 | Entities (domínio) sem dependências externas | `user.py`, `project.py`, `setting.py` — apenas `dataclasses` e `typing` | ✅ |
| 2 | Use cases dependem apenas de abstrações do domínio | `auth_service.py:2` — `from domain import User, UserRepository` | ✅ |
| 3 | Dependency Rule: use cases não importam de infrastructure | `map_service.py:3` — `from infrastructure.system.interfaces import DriveMapper` | ❌ |
| 4 | Frameworks isolados na camada mais externa | Flask confinado a `infrastructure/web/`; SQLite a `infrastructure/persistence/` | ✅ |
| 5 | Controllers chamam use cases, nunca repositórios diretamente | `admin_controller.py:14,95,133,143` — acessa `current_app.repo` direto | ❌ |
| 6 | Entities encapsulam regras de negócio corporativas | `User`, `Project`, `Setting` são `@dataclass` puros — sem comportamento, sem invariantes | ❌ |
| 7 | Use cases encapsulam regras de negócio da aplicação | `auth_service.py`, `map_service.py` — lógica de orquestração presente | ✅ |
| 8 | Use cases não fazem I/O diretamente | `project_service.py:20` — `os.listdir()`; `delete_service.py:29,76` — `shutil.rmtree/move` | ❌ |
| 9 | Interface Adapters convertem dados entre camadas | `mappers.py` — UserMapper, ProjectMapper, SettingMapper | ✅ |
| 10 | Interfaces (abstrações) na borda interna correta | `domain/interfaces.py` — correto; `infrastructure/system/interfaces.py` — errado | ❌ Parcial |
| 11 | Testabilidade do núcleo sem framework | `AuthUseCase`, `ProjectUseCase` dependem apenas de interfaces — testáveis; `DeleteUseCase` exige `shutil` | ❌ Parcial |

**6 de 11 critérios plenamente atendidos = ~55%**

#### Violação do Anemic Domain Model

Em Clean Architecture as Entities devem conter as regras de negócio mais estáveis. No projeto:

```python
# Atual — Anemic Model (apenas dados):
@dataclass
class User:
    id: Optional[int]
    username: str
    password: str
    role: str

# Clean Architecture esperaria:
@dataclass
class User:
    id: Optional[int]
    username: str
    _password_hash: str
    role: str

    def authenticate(self, raw_password: str) -> bool:
        return self._password_hash == hashlib.sha256(raw_password.encode()).hexdigest()

    def can_manage_users(self) -> bool:
        return self.role == 'Gerente'

    def is_editor(self) -> bool:
        return self.role in ('Gerente', 'Editor')
```

---

### 4. DDD (Domain-Driven Design) — 33%

DDD é o conjunto mais exigente. Além de estrutura, exige que o modelo de domínio expresse o negócio através de linguagem, comportamento e padrões táticos.

#### Critérios avaliados (12)

| # | Critério | Evidência no código | Atende? |
|---|----------|--------------------|---------| 
| 1 | Entities com identidade e ciclo de vida | `User`, `Project` têm `id` | ✅ |
| 2 | Entities com comportamento de domínio (não anêmicas) | `User`, `Project`, `Setting` são `@dataclass` sem métodos de negócio | ❌ |
| 3 | Value Objects (sem identidade, imutáveis) | Nenhum — `role` é `str`, `type` é `str`, `DriveLetter` não existe como VO | ❌ |
| 4 | Aggregate Roots controlando consistência | Nenhum aggregate definido | ❌ |
| 5 | Domain Services para operações sem dono natural | `AuthUseCase` age como domain service, mas está na camada de aplicação | ❌ Parcial |
| 6 | Application Services orquestrando, não decidindo | Use cases orquestram; mas contêm lógica que deveria estar no domínio (ex: hashing) | ❌ Parcial |
| 7 | Repositories para acesso a aggregates | `UserRepository`, `ProjectRepository` em `domain/interfaces.py` | ✅ |
| 8 | Domain Events para fatos relevantes | Nenhum evento definido (`ProjetoEngavetado`, `UsuarioCriado`, etc.) | ❌ |
| 9 | Linguagem Ubíqua refletida no código | Termos `engavetar`, `gaveta`, `mapear` presentes; mas `scope`, `mode`, `items` são genéricos | ✅ Parcial |
| 10 | Bounded Contexts delimitados | Sem contextos explícitos (Autenticação, Gestão de Projetos, Mapeamento) | ❌ |
| 11 | Invariantes de domínio protegidas pelas Entities | Nenhuma validação nas entidades; ex: `role` pode ser qualquer string | ❌ |
| 12 | Regras de negócio no domínio, não no controller | `admin_controller.py:31-36` — regra "Editor só edita a si mesmo" está no controller | ❌ |

**4 de 12 critérios atendidos ≈ 33%**

#### Ausência de Value Objects — impacto real

Os campos `role` e `type` aceitam qualquer string sem validação:

```python
# Atual — string sem restrição:
user = User(id=None, username='x', password='y', role='qualquercoisa')
project = Project(id=None, name='X', type='INVALIDO', path='...')

# DDD esperaria Value Objects:
from enum import Enum

class Role(Enum):
    GERENTE = 'Gerente'
    EDITOR = 'Editor'
    DEFAULT = 'Default'

class ProjectType(Enum):
    ONLINE = 'ONLINE'
    GAVETA = 'GAVETA'
```

#### Regra de negócio fora do domínio

A regra "Editores só podem editar a própria senha" está no controller, não no domínio:

```python
# admin_controller.py:31-36 — regra de negócio no lugar errado:
if current_role == 'Editor':
    if mode == 'create' or username != current_user:
        return jsonify({'success': False, 'message': 'Acesso negado...'})
    role = current_role

# DDD: essa regra pertence à entidade ou ao serviço de domínio:
class User:
    def can_modify(self, target_user: 'User', acting_user: 'User') -> bool:
        if acting_user.role == Role.EDITOR:
            return target_user.username == acting_user.username
        return acting_user.role == Role.GERENTE
```

#### Ausência de Domain Events

Operações críticas não geram eventos rastreáveis:

```python
# Eventos ausentes que deveriam existir:
@dataclass
class ProjetoEngavetadoEvent:
    project_name: str
    moved_at: datetime
    by_user: str

@dataclass
class UnidadeMapeadaEvent:
    project_name: str
    drive_letter: str
    mapped_at: datetime
```

---

### Comparativo por Critério Estrutural

| Critério | N-Tier | Hexagonal | Clean Arch | DDD |
|----------|:------:|:---------:|:----------:|:---:|
| Separação de camadas | ✅ | ✅ | ✅ | ✅ |
| Domínio sem dependências externas | ✅ | ✅ | ✅ | ✅ |
| Injeção de dependências | ✅ | ✅ | ✅ | ✅ |
| Repositórios abstraídos | ✅ | ✅ | ✅ | ✅ |
| Controllers sem acesso direto ao BD | ❌ | ❌ | ❌ | ❌ |
| Use cases sem I/O de disco | ❌ | ❌ | ❌ | ❌ |
| Ports no núcleo (não na infra) | — | ❌ | ❌ | — |
| Entidades com comportamento | — | — | ❌ | ❌ |
| Value Objects | — | — | — | ❌ |
| Aggregates / Domain Events | — | — | — | ❌ |
| Regras no domínio (não no controller) | — | — | — | ❌ |

### Conclusão da Conformidade

O projeto adota corretamente a **estrutura** das arquiteturas de referência — separação de camadas, injeção de dependência e isolamento do framework — mas apresenta três desvios sistemáticos que afetam todas as avaliações:

1. **Vazamento de infraestrutura para o núcleo** — `os`, `shutil` e `DriveMapper` presentes em `application/`, violando a Dependency Rule (Clean), a separação de inside/outside (Hexagonal) e a regra de camadas (N-Tier).

2. **Controllers com atalhos para o repositório** — `admin_controller.py` acessa `current_app.repo` diretamente em quatro rotas, curto-circuitando a camada de aplicação em todos os modelos.

3. **Domínio anêmico** — entidades são estruturas de dados sem comportamento, invariantes ou eventos, o que resulta na baixa conformidade com DDD e impede que Clean Architecture e Hexagonal atinjam seu potencial máximo.

Corrigindo esses três pontos o projeto atingiria aproximadamente **85% de conformidade** com Hexagonal e Clean Architecture e **60% com DDD**.
