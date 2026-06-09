# Planejamento de Correções Arquiteturais — OJCMapper

## Objetivo

Elevar a conformidade do projeto com DDD, Clean Architecture e Hexagonal Architecture
através de correções incrementais, sem quebrar o comportamento atual da aplicação.

---

## Resultado de Conformidade

| Arquitetura | Antes | Alcançado | Com Fase 2 |
|-------------|:-----:|:---------:|:----------:|
| DDD | 33% | **~60%** | ~70% |
| Clean Architecture | 55% | **~82%** | ~85% |
| Hexagonal | 60% | **~85%** | ~85% |
| N-Tier | 70% | **~90%** | ~90% |

> **Decisão:** A Fase 2 foi excluída da execução corrente. O ganho dela concentra-se
> no DDD (domínio anêmico → entidades com comportamento) e não impacta as correções
> de camada das Fases 3 e 4. Pode ser encaixada posteriormente sem retrabalho.
> Documentação completa: [`fase2_pendente.md`](fase2_pendente.md)

---

## Ordem de Execução

```
Fase 1 ──► Fase 3 ──► Fase 4      (Fase 2 pendente — encaixar após Fase 4)
```

---

## Status das Fases

| Fase | Status | Commit | Observações |
|------|:------:|--------|-------------|
| Fase 1 — Value Objects e Invariantes | ✅ Concluída | `7340652` | |
| Fase 2 — Comportamento nas Entidades | ⏸ Adiada | — | Ver [`fase2_pendente.md`](fase2_pendente.md) |
| Fase 3 — Correção das Violações de Camada | ✅ Concluída | `bb885d1` | |
| Fase 4 — Bounded Contexts e Domain Events | ✅ Concluída | `8298bcf` | |
| Limpeza — Remoção de re-exports redundantes | ✅ Concluída | `1b9ec87` | Não planejada; executada após Fase 4 |

---

## Fases

---

## Fase 1 — Value Objects e Invariantes de Domínio ✅

> Esforço: baixo | Risco: baixo | Impacto: DDD +15%, Clean +10%

Introduz tipos fortes no lugar de strings soltas, eliminando estados inválidos
antes mesmo de chegarem ao banco de dados.

### 1.1 — `Role` como Enum

**Arquivo criado:** `src/domain/shared/value_objects.py`

```
Role(Enum):
  GERENTE = 'Gerente'
  EDITOR  = 'Editor'
  DEFAULT = 'Default'
```

### 1.2 — `ProjectType` como Enum

**Arquivo criado:** `src/domain/shared/value_objects.py` (mesmo arquivo)

```
ProjectType(Enum):
  ONLINE = 'ONLINE'
  GAVETA = 'GAVETA'
```

### 1.3 — Invariantes com `__post_init__`

**Arquivos afetados:** `src/domain/identity/user.py`, `src/domain/projects/project.py`

```
User.__post_init__:
  - username não pode ser vazio
  - role deve ser instância de Role

Project.__post_init__:
  - name não pode ser vazio
  - type deve ser instância de ProjectType
```

**Arquivos afetados adicionais:**
- `src/infrastructure/persistence/sqlite_repository.py` — serializa `role.value` ao persistir
- `src/infrastructure/persistence/mappers.py` — converte string do banco para enum
- `src/application/auth_service.py` — converte `role: str` para `Role(role)` na criação
- `src/application/project_service.py`, `delete_service.py` — recebem `ProjectType`
- `src/infrastructure/web/controllers/` — convertem string HTTP para enum na fronteira

---

## Fase 2 — Comportamento nas Entidades ⏸

> Esforço: médio | Risco: baixo-médio | Impacto: DDD +10%

Ver documentação completa em [`fase2_pendente.md`](fase2_pendente.md).

**Pré-requisito:** Fase 1 concluída.

**Resumo do que deve ser feito:**
- `User.set_password()` / `User.check_password()` — hashing no domínio
- `User.can_manage_users()` / `User.can_modify(target)` — autorização no domínio
- `Project.is_online()` / `Project.is_in_gaveta()` / `Project.display_label()`

---

## Fase 3 — Correção das Violações de Camada ✅

> Esforço: médio | Risco: médio | Impacto: Clean +15%, Hexagonal +20%, N-Tier +15%

### 3.1 — `DriveMapper` movido para o domínio

- `infrastructure/system/interfaces.py` removido
- `DriveMapper` (ABC) adicionado a `domain/drives/interfaces.py`
- `WindowsDriveMapper` e `MapUseCase` passam a importar do domínio

### 3.2 — `FileSystemPort` criado no domínio

- `FileSystemPort` (ABC) em `domain/projects/interfaces.py`
- `LocalFileSystemAdapter` criado em `infrastructure/system/filesystem_adapter.py`
- `os`/`shutil` removidos de `project_service.py` e `delete_service.py`
- `ProjectUseCase`, `DeleteUseCase` e `ExportUseCase` recebem `FileSystemPort` via DI

### 3.3 — Acesso direto ao repositório eliminado nos controllers

- `SettingsUseCase` criado em `application/settings_service.py`
- `ExportUseCase` criado em `application/export_service.py`
- `AuthUseCase.get_all_users()` adicionado
- `admin_controller.py` sem nenhum `current_app.repo`
- `app.repo` e `app.mapper` removidos da exposição pública do Flask app

---

## Fase 4 — Bounded Contexts e Domain Events ✅

> Esforço: alto | Risco: médio-alto | Impacto: DDD +20%

### 4.1 — Bounded Contexts

Domínio reorganizado em subcontextos autônomos:

```
src/domain/
  __init__.py            ← único ponto de re-exportação pública
  shared/
    value_objects.py     Role, ProjectType
    setting.py           Setting
    interfaces.py        SettingsRepository
    events.py            DomainEvent, EventBus + 6 eventos
  identity/
    user.py              User
    interfaces.py        UserRepository
  projects/
    project.py           Project
    interfaces.py        ProjectRepository, FileSystemPort
  drives/
    interfaces.py        DriveMapper
```

### 4.2 — Domain Events

- `domain/shared/events.py` com `DomainEvent`, `EventBus` e 6 eventos imutáveis
- `AuthUseCase` emite `UsuarioCriado`, `UsuarioRemovido`
- `DeleteUseCase` emite `ProjetoDeletado`, `ProjetoEngavetado`
- `MapUseCase` emite `UnidadeMapeada`, `UnidadeDesconectada`

### Limpeza pós-Fase 4 (não planejada)

Arquivos planos redundantes removidos da raiz de `domain/`:
`user.py`, `project.py`, `setting.py`, `interfaces.py`, `value_objects.py`

Todos os imports downstream unificados para `from domain import ...` via `__init__.py`.

---

## Estrutura Final de Arquivos

### Criados

| Arquivo | Fase | Propósito |
|---------|:----:|-----------|
| `src/domain/shared/value_objects.py` | 1 | `Role`, `ProjectType` |
| `src/domain/shared/setting.py` | 4 | `Setting` no contexto correto |
| `src/domain/shared/interfaces.py` | 4 | `SettingsRepository` |
| `src/domain/shared/events.py` | 4 | `DomainEvent`, `EventBus`, 6 eventos |
| `src/domain/identity/user.py` | 4 | `User` no contexto correto |
| `src/domain/identity/interfaces.py` | 4 | `UserRepository` |
| `src/domain/projects/project.py` | 4 | `Project` no contexto correto |
| `src/domain/projects/interfaces.py` | 4 | `ProjectRepository`, `FileSystemPort` |
| `src/domain/drives/interfaces.py` | 4 | `DriveMapper` |
| `src/application/settings_service.py` | 3 | Use case de configurações |
| `src/application/export_service.py` | 3 | Use case de exportação de lista |
| `src/infrastructure/system/filesystem_adapter.py` | 3 | Adapter para `os`/`shutil` |

### Removidos

| Arquivo | Motivo |
|---------|--------|
| `src/infrastructure/system/interfaces.py` | `DriveMapper` movido para o domínio |
| `src/domain/user.py` | Conteúdo movido para `identity/user.py` |
| `src/domain/project.py` | Conteúdo movido para `projects/project.py` |
| `src/domain/setting.py` | Conteúdo movido para `shared/setting.py` |
| `src/domain/interfaces.py` | Dividido entre os subcontextos |
| `src/domain/value_objects.py` | Conteúdo movido para `shared/value_objects.py` |
