# Planejamento de Correções Arquiteturais — OJCMapper

## Objetivo

Elevar a conformidade do projeto com DDD, Clean Architecture e Hexagonal Architecture
através de correções incrementais, sem quebrar o comportamento atual da aplicação.

**Meta de conformidade pós-correção:**

| Arquitetura | Antes | Meta |
|-------------|:-----:|:----:|
| DDD | 33% | 70% |
| Clean Architecture | 55% | 85% |
| Hexagonal | 60% | 85% |
| N-Tier | 70% | 90% |

---

## Fases

As correções estão organizadas em 4 fases, da mais simples e segura para a mais estrutural.
Cada fase é independente e pode ser entregue separadamente.

---

## Fase 1 — Value Objects e Invariantes de Domínio

> Esforço: baixo | Risco: baixo | Impacto: DDD +15%, Clean +10%

Introduz tipos fortes no lugar de strings soltas, eliminando estados inválidos
antes mesmo de chegarem ao banco de dados.

### 1.1 — Criar `Role` como Enum

**Arquivo a criar:** `src/domain/value_objects.py`

```
Role(Enum):
  GERENTE = 'Gerente'
  EDITOR  = 'Editor'
  DEFAULT = 'Default'
```

**Arquivos afetados:**
- `src/domain/user.py` — substituir `role: str` por `role: Role`
- `src/infrastructure/persistence/sqlite_repository.py` — serializar/deserializar Role
- `src/infrastructure/persistence/mappers.py` — `Role(row['role'])` no UserMapper
- `src/infrastructure/web/controllers/admin_controller.py` — comparar `Role.EDITOR` em vez de string

### 1.2 — Criar `ProjectType` como Enum

**Arquivo a criar:** `src/domain/value_objects.py` (mesmo arquivo)

```
ProjectType(Enum):
  ONLINE = 'ONLINE'
  GAVETA = 'GAVETA'
```

**Arquivos afetados:**
- `src/domain/project.py` — substituir `type: str` por `type: ProjectType`
- `src/infrastructure/persistence/mappers.py` — `ProjectType(row['type'])`
- `src/application/project_service.py` — usar `ProjectType.ONLINE` em vez de strings literais
- `src/application/delete_service.py` — mesmo

### 1.3 — Invariantes com `__post_init__`

Adicionar validação nas entidades para rejeitar dados inválidos no momento da criação.

**Arquivo afetado:** `src/domain/user.py`, `src/domain/project.py`

```
User.__post_init__:
  - username não pode ser vazio
  - role deve ser Role válido

Project.__post_init__:
  - name não pode ser vazio
  - type deve ser ProjectType válido
  - path não pode ser vazio
```

---

## Fase 2 — Comportamento nas Entidades (Fim do Anemic Model)

> Esforço: médio | Risco: baixo-médio | Impacto: DDD +20%, Clean +10%

Move lógica de negócio que hoje está espalhada em controllers e use cases
para dentro das entidades que naturalmente a possuem.

### 2.1 — Hashing de senha em `User`

**Problema:** `AuthUseCase._hash_password()` em `auth_service.py:9` — regra de negócio fora do domínio.

**O que fazer:**
- Adicionar `User.set_password(raw: str)` que aplica o hash internamente
- Adicionar `User.check_password(raw: str) -> bool` para verificar
- Remover `_hash_password` de `AuthUseCase`
- Atualizar `auth_service.py` para usar `user.check_password(password)`

**Arquivo principal:** `src/domain/user.py`
**Arquivo secundário:** `src/application/auth_service.py`

### 2.2 — Regra de autorização em `User`

**Problema:** `admin_controller.py:31–36` — "Editor só pode editar a própria senha" está no controller Flask.

**O que fazer:**
- Adicionar `User.can_manage_users() -> bool`
- Adicionar `User.can_modify(target: User) -> bool`
- Remover a lógica de autorização do controller
- Controller passa a chamar `acting_user.can_modify(target_user)`

**Arquivo principal:** `src/domain/user.py`
**Arquivo secundário:** `src/infrastructure/web/controllers/admin_controller.py`

### 2.3 — Estado do projeto em `Project`

**O que fazer:**
- Adicionar `Project.is_online() -> bool`
- Adicionar `Project.is_in_gaveta() -> bool`
- Adicionar `Project.display_label() -> str`

**Arquivo principal:** `src/domain/project.py`

---

## Fase 3 — Correção das Violações de Camada

> Esforço: médio | Risco: médio | Impacto: Clean +15%, Hexagonal +20%, N-Tier +15%

Elimina os três desvios estruturais que afetam todas as avaliações de conformidade.

### 3.1 — Mover `DriveMapper` para o domínio

**Problema:** `map_service.py:3` importa `from infrastructure.system.interfaces import DriveMapper` — application depende de infrastructure.

**O que fazer:**
- Mover `DriveMapper` (ABC) de `src/infrastructure/system/interfaces.py`
  para `src/domain/interfaces.py` (junto com os repositórios)
- Atualizar `WindowsDriveMapper` para importar do domínio
- Atualizar `map_service.py` para importar do domínio

**Arquivo a mover:** `src/infrastructure/system/interfaces.py` → `src/domain/interfaces.py`

### 3.2 — Criar `FileSystemPort` no domínio

**Problema:** `project_service.py:20` e `delete_service.py:29,35,76` chamam `os.listdir()`, `shutil.rmtree()`, `shutil.move()` diretamente — infraestrutura na camada de aplicação.

**O que fazer:**
- Criar `FileSystemPort` (ABC) em `src/domain/interfaces.py`
- Criar `LocalFileSystemAdapter` em `src/infrastructure/system/filesystem_adapter.py`
  implementando o port com `os` e `shutil`
- `ProjectUseCase` e `DeleteUseCase` recebem `FileSystemPort` por injeção de dependência
- `create_app()` instancia e injeta `LocalFileSystemAdapter`

```
FileSystemPort (ABC) — src/domain/interfaces.py:
  list_directories(path: str)      -> list[str]
  directory_exists(path: str)      -> bool
  delete_directory(path: str)      -> None
  move_directory(src, dst: str)    -> None
  write_text_file(path, content)   -> None
```

**Arquivo a criar:** `src/infrastructure/system/filesystem_adapter.py`
**Arquivos afetados:** `src/domain/interfaces.py`, `src/application/project_service.py`,
  `src/application/delete_service.py`, `src/infrastructure/web/app.py`

### 3.3 — Eliminar acesso direto ao repositório nos controllers

**Problema:** `admin_controller.py:14,95,133,143` acessa `current_app.repo` diretamente,
  bypassando a camada de aplicação.

**O que fazer:**
- Criar use case ou método no use case existente para cobrir cada acesso direto:
  - `repo.get_all_users()` → já existe `AuthUseCase` — adicionar `get_all_users()`
  - `repo.get_all_settings()` → criar `SettingsUseCase.get_settings()`
  - `repo.update_setting()` → `SettingsUseCase.update_setting(key, value)`
  - `repo.update_setting()` no loop do `save_configurar` → `SettingsUseCase.update_all(dict)`
- Remover `app.repo` e `app.mapper` expostos no `current_app`
- Remover `exportar_lista` do controller e criar `ExportUseCase`

**Arquivo a criar:** `src/application/settings_service.py`, `src/application/export_service.py`
**Arquivo afetado:** `src/infrastructure/web/controllers/admin_controller.py`,
  `src/infrastructure/web/app.py`

---

## Fase 4 — Bounded Contexts e Domain Events

> Esforço: alto | Risco: médio-alto | Impacto: DDD +20%

Reorganiza o domínio em contextos explícitos e introduz rastreabilidade de eventos.

### 4.1 — Separar Bounded Contexts

**O que fazer:**
Reorganizar `src/domain/` em subcontextos:

```
src/domain/
  identity/          ← contexto de autenticação e usuários
    user.py
    interfaces.py    (UserRepository)
  projects/          ← contexto de gestão de projetos
    project.py
    interfaces.py    (ProjectRepository, FileSystemPort)
  drives/            ← contexto de mapeamento de unidades
    interfaces.py    (DriveMapper)
  shared/            ← tipos compartilhados entre contextos
    value_objects.py (Role, ProjectType)
```

**Arquivos afetados:** todos os imports de `domain/` em `application/` e `infrastructure/`

### 4.2 — Domain Events

**O que fazer:**
- Criar `src/domain/events.py` com dataclasses de eventos imutáveis
- Criar publicador simples `EventBus` (in-memory, sem dependências externas)
- Emitir eventos nas operações críticas dos use cases

```
Eventos a criar:
  UsuarioCriado(username, role, created_at)
  UsuarioRemovido(username, removed_at)
  ProjetoEngavetado(project_name, moved_at, by_user)
  ProjetoDeletado(project_name, scope, deleted_at, by_user)
  UnidadeMapeada(project_name, drive_letter, mapped_at)
  UnidadeDesconectada(drive_letter, unmapped_at)
```

---

## Ordem de Execução Recomendada

```
Fase 1  ──►  Fase 2  ──►  Fase 3  ──►  Fase 4
(VOs)        (Entidades)   (Camadas)    (Contextos)
 baixo risco               médio risco   alto risco
```

Cada fase pode ser mergeada e validada independentemente antes de iniciar a próxima.

---

## Arquivos Novos a Criar

| Arquivo | Fase | Propósito |
|---------|:----:|-----------|
| `src/domain/value_objects.py` | 1 | `Role`, `ProjectType` |
| `src/application/settings_service.py` | 3 | Use case de configurações |
| `src/application/export_service.py` | 3 | Use case de exportação de lista |
| `src/infrastructure/system/filesystem_adapter.py` | 3 | Adapter para `os`/`shutil` |
| `src/domain/events.py` | 4 | Domain Events |
| `src/domain/identity/` | 4 | Bounded Context de identidade |
| `src/domain/projects/` | 4 | Bounded Context de projetos |
| `src/domain/drives/` | 4 | Bounded Context de drives |

## Arquivos Modificados por Fase

| Arquivo | Fase 1 | Fase 2 | Fase 3 | Fase 4 |
|---------|:------:|:------:|:------:|:------:|
| `src/domain/user.py` | ✏️ | ✏️ | — | ✏️ |
| `src/domain/project.py` | ✏️ | ✏️ | — | ✏️ |
| `src/domain/interfaces.py` | — | — | ✏️ | ✏️ |
| `src/application/auth_service.py` | — | ✏️ | ✏️ | — |
| `src/application/project_service.py` | ✏️ | — | ✏️ | — |
| `src/application/delete_service.py` | ✏️ | — | ✏️ | — |
| `src/application/map_service.py` | — | — | ✏️ | — |
| `src/infrastructure/persistence/mappers.py` | ✏️ | — | — | — |
| `src/infrastructure/persistence/sqlite_repository.py` | ✏️ | — | — | — |
| `src/infrastructure/system/interfaces.py` | — | — | ✏️ | — |
| `src/infrastructure/web/app.py` | — | — | ✏️ | — |
| `src/infrastructure/web/controllers/admin_controller.py` | ✏️ | ✏️ | ✏️ | — |

---

## Status das Fases

| Fase | Status | Observações |
|------|:------:|-------------|
| Fase 1 — Value Objects e Invariantes | 🔲 Pendente | |
| Fase 2 — Comportamento nas Entidades | 🔲 Pendente | Depende da Fase 1 |
| Fase 3 — Correção das Violações de Camada | 🔲 Pendente | Depende da Fase 1 |
| Fase 4 — Bounded Contexts e Domain Events | 🔲 Pendente | Depende das Fases 2 e 3 |
