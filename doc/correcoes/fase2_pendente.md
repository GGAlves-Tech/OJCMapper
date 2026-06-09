# Fase 2 — Comportamento nas Entidades (Pendente)

## Decisão

A Fase 2 foi intencionalmente excluída da execução corrente.
O projeto seguirá a ordem **Fase 1 → Fase 3 → Fase 4**.

A Fase 2 pode ser encaixada após a conclusão da Fase 4 sem retrabalho
nas camadas já corrigidas, desde que a Fase 1 esteja concluída
(dependência de `Role` e `ProjectType` como enums).

---

## O que é a Fase 2

Elimina o **Anemic Domain Model** — o padrão onde entidades são apenas
estruturas de dados sem comportamento. Em DDD, as entidades devem
encapsular as regras de negócio que naturalmente lhes pertencem,
em vez de delegar essa responsabilidade para use cases e controllers.

---

## O que deve ser implementado

### 2.1 — Hashing de senha dentro de `User`

**Problema atual:**

`AuthUseCase._hash_password()` em `auth_service.py:9` aplica SHA256 na senha.
Isso é uma regra de negócio do `User` — decidir como sua senha é armazenada
e verificada é responsabilidade da entidade, não do serviço de aplicação.

**O que fazer:**

Adicionar em `src/domain/user.py`:

```python
def set_password(self, raw: str) -> None:
    self.password = hashlib.sha256(raw.encode()).hexdigest()

def check_password(self, raw: str) -> bool:
    return self.password == hashlib.sha256(raw.encode()).hexdigest()
```

Remover `_hash_password` de `AuthUseCase` e atualizar:

```python
# auth_service.py — antes:
hashed_password = self._hash_password(password)
if user and user.password == hashed_password:

# auth_service.py — depois:
if user and user.check_password(password):
```

**Arquivo principal:** `src/domain/user.py`
**Arquivo secundário:** `src/application/auth_service.py`

---

### 2.2 — Regra de autorização dentro de `User`

**Problema atual:**

`admin_controller.py:31–36` contém a regra "Editor só pode editar a própria senha":

```python
if current_role == 'Editor':
    if mode == 'create' or username != current_user:
        return jsonify({'success': False, 'message': 'Acesso negado...'})
    role = current_role
```

Esta é uma regra de negócio sobre o que um usuário pode fazer a outro.
Qualquer nova interface (CLI, API externa) que não passe por esse controller
não teria essa proteção. A regra pertence ao domínio.

**O que fazer:**

Adicionar em `src/domain/user.py`:

```python
def can_manage_users(self) -> bool:
    return self.role == Role.GERENTE

def can_modify(self, target: 'User') -> bool:
    if self.role == Role.GERENTE:
        return True
    if self.role == Role.EDITOR:
        return self.username == target.username
    return False

def can_change_role(self) -> bool:
    return self.role == Role.GERENTE
```

Atualizar `admin_controller.py` para delegar ao domínio:

```python
# antes — lógica no controller:
if current_role == 'Editor':
    if mode == 'create' or username != current_user:
        return jsonify({'success': False, ...})

# depois — controller delega ao domínio:
acting_user = current_app.auth_service.get_by_username(session['username'])
target_user = current_app.auth_service.get_by_username(username)
if not acting_user.can_modify(target_user):
    return jsonify({'success': False, 'message': 'Acesso negado.'})
```

**Arquivo principal:** `src/domain/user.py`
**Arquivo secundário:** `src/infrastructure/web/controllers/admin_controller.py`

---

### 2.3 — Estado e apresentação dentro de `Project`

**O que fazer:**

Adicionar em `src/domain/project.py`:

```python
def is_online(self) -> bool:
    return self.type == ProjectType.ONLINE

def is_in_gaveta(self) -> bool:
    return self.type == ProjectType.GAVETA

def display_label(self) -> str:
    return f"{self.type.value}/{self.name}"
```

**Arquivo principal:** `src/domain/project.py`

---

## Dependências para execução

| Pré-requisito | Motivo |
|--------------|--------|
| Fase 1 concluída | Os métodos de `User` usam `Role(Enum)` e os de `Project` usam `ProjectType(Enum)`. Sem os enums da Fase 1, os métodos seriam escritos com strings literais e quebrariam quando a Fase 1 fosse aplicada. |

---

## Ganho ao implementar

### Conformidade arquitetural

| Arquitetura | Sem Fase 2 | Com Fase 2 | Ganho |
|-------------|:----------:|:----------:|:-----:|
| DDD | ~55% | ~70% | +15% |
| Clean Architecture | ~78% | ~85% | +7% |
| Hexagonal | ~85% | ~85% | — |
| N-Tier | ~90% | ~90% | — |

### Ganhos qualitativos

**Segurança por design:** A regra de autorização de `User.can_modify()` passa a valer
para qualquer ponto de entrada — HTTP, CLI ou testes. Hoje, uma rota esquecida sem
o `@role_required` deixa o sistema sem proteção.

**Testabilidade:** É possível testar as regras de negócio sem instanciar Flask,
banco de dados ou qualquer infraestrutura:

```python
def test_editor_nao_pode_modificar_outro_usuario():
    editor = User(id=1, username='ed', password='x', role=Role.EDITOR)
    outro  = User(id=2, username='jo', password='y', role=Role.DEFAULT)
    assert editor.can_modify(outro) == False

def test_editor_pode_modificar_a_si_mesmo():
    editor = User(id=1, username='ed', password='x', role=Role.EDITOR)
    assert editor.can_modify(editor) == True
```

**Coesão:** Toda a lógica sobre `User` fica em `user.py`. Quem lê o arquivo
entende completamente o que um usuário pode ou não fazer — sem precisar
vasculhar controllers ou use cases.

**Eliminação do Anemic Model:** O domínio passa a expressar o negócio,
não apenas transportar dados. Isso é o núcleo do DDD tático.
