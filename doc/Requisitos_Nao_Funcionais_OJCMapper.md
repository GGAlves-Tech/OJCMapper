# Requisitos Não Funcionais — OJCMapper

**Projeto:** MAPPER — Utilitário de Gerenciamento do Armazenamento de Mídias  
**Documento relacionado:** [`Gestao_Projetos_TO_Graduado_Mapper_OJC.md`](Gestao_Projetos_TO_Graduado_Mapper_OJC.md)  
**Versão:** 1.0  
**Data:** 08/06/2026  
**Autor da revisão:** *Guthemberg B. Alves*

---

## Histórico de Revisões

| Data | Versão | Comentário | Autor |
| :--- | :---: | :--- | :--- |
| 08/06/2026 | 1.0 | Extração e correção da lista de RNFs; alinhamento com a implementação atual (bcrypt, Clean Architecture, PyInstaller) | *Guthemberg B. Alves* |

---

## 1. Objetivo

Este documento consolida os **requisitos não funcionais (RNFs)** do OJCMapper de forma independente do documento de gestão do projeto. A lista foi revisada para refletir o estado atual do sistema após a refatoração arquitetural (DDD, Clean Architecture e Hexagonal Architecture).

Os RNFs descrevem **como** o sistema deve se comportar em aspectos transversais — desempenho, segurança, usabilidade, portabilidade e manutenibilidade — sem detalhar funcionalidades de negócio (cobertas pelos RFs no documento principal).

---

## 2. Lista dos Requisitos Não Funcionais

| ID | Categoria | Descrição | Critério de Aceite | Prioridade |
| :--- | :--- | :--- | :--- | :---: |
| **RNF01** | Usabilidade | Interface web moderna com estética *glassmorphism*, layout responsivo dentro da janela fixa e feedback visual imediato (toasts, estados de carregamento). | Telas principais (login, dashboard, configurações, usuários) seguem o mesmo padrão visual; ações críticas exibem confirmação ou mensagem de resultado. | **Essencial** |
| **RNF02** | Usabilidade | Experiência de aplicativo desktop nativo via PyWebView, sem barra de endereço do navegador. | Aplicação abre em janela dedicada (500×800 px, não redimensionável) apontando para `http://127.0.0.1:5000`. | **Essencial** |
| **RNF03** | Performance | Operações de mapeamento e desmontagem de unidades devem responder em tempo aceitável para o fluxo de edição. | Em rede local estável, o retorno da operação ocorre em **até 2 segundos**; em falha ou indisponibilidade, o timeout máximo de subprocesso é de **10 segundos**, com mensagem clara ao usuário. | **Essencial** |
| **RNF04** | Performance | Listagem e busca incremental de projetos devem permanecer fluidas na interface. | A filtragem por texto na lista ativa não bloqueia a UI; a listagem de diretórios configurados é carregada sem travar a aplicação Flask. | **Importante** |
| **RNF05** | Segurança | Senhas de usuários devem ser armazenadas com hash criptográfico **com salt**, nunca em texto plano. | Persistência via **bcrypt** (`bcrypt.hashpw` / `bcrypt.checkpw`); credenciais iniciais do banco também são inseridas já hasheadas. | **Essencial** |
| **RNF06** | Segurança | Controle de acesso baseado em perfis (RBAC) para rotas e ações sensíveis. | Rotas administrativas protegidas por `@role_required`; perfis **Gerente**, **Editor** e **Default** com permissões diferenciadas conforme matriz de atores do projeto. | **Essencial** |
| **RNF07** | Segurança | Sessões de autenticação gerenciadas pelo Flask com chave secreta gerada na inicialização. | Login bem-sucedido persiste `user_id`, `username` e `user_role` na sessão; acesso não autenticado redireciona para `/login`. | **Essencial** |
| **RNF08** | Portabilidade | Distribuição como executável único Windows, sem exigir instalação de Python no posto de trabalho. | Build via PyInstaller (`--onefile`, `--noconsole`) gera `MAPPER_OJC.exe` com templates, estáticos e banco embutidos ou copiados ao lado do `.exe`. | **Essencial** |
| **RNF09** | Compatibilidade | Execução exclusiva em ambiente Windows, suportando estações de edição legadas e atuais. | Compatível com **Windows 7 SP1 a Windows 11**; mapeamento via comandos nativos `net use` e `subst`. | **Essencial** |
| **RNF10** | Robustez | Tratamento de erros para caminhos de rede inacessíveis, falhas de mapeamento e timeouts de subprocesso. | Operações retornam `(sucesso, mensagem)` ou JSON com `success: false`; exceções não derrubam o servidor Flask. | **Essencial** |
| **RNF11** | Robustez | Recuperação graciosa quando o storage ou a rede estiverem indisponíveis. | Interface permanece utilizável; usuário recebe mensagem descritiva (ex.: *"Timeout: servidor não respondeu"*, *"Erro ao mapear"*). | **Importante** |
| **RNF12** | Manutenibilidade | Arquitetura em camadas com regra de dependência unidirecional (Clean Architecture + DDD + Hexagonal). | Domínio (`src/domain/`) sem dependências de Flask, SQLite ou subprocess; use cases em `application/`; adaptadores em `infrastructure/`. | **Essencial** |
| **RNF13** | Manutenibilidade | Bounded contexts explícitos no domínio para evolução independente dos módulos. | Subcontextos `identity`, `projects`, `drives`, `shared` e `audit` com ports (interfaces) e eventos de domínio onde aplicável. | **Importante** |
| **RNF14** | Persistência | Banco de dados local embutido, sem servidor externo. | SQLite 3 para usuários, configurações e metadados; arquivo `.db` portável junto ao executável ou ao diretório de desenvolvimento. | **Essencial** |
| **RNF15** | Operacionalidade | Execução em rede local controlada, sem dependência de conectividade com a internet. | Servidor Flask e interface rodam em `127.0.0.1`; acesso ao Storage Quantum ocorre via UNC/rede interna da emissora. | **Essencial** |
| **RNF16** | Auditabilidade | Registro de ações críticas para rastreabilidade operacional. | `FileAuditLogger` grava entradas no formato `{data}_{ator}_{ação}` em arquivo diário por hostname, com diretório configurável via `log_path`. | **Importante** |
| **RNF17** | Escalabilidade operacional | Suporte ao volume de dados da operação jornalística da emissora. | Listagem baseada em diretórios configurados (Online/Gaveta), adequada ao fluxo de ~12 TB/mês sem exigir indexação centralizada em servidor dedicado. | **Desejável** |

---

## 3. Correções em relação à versão anterior

A tabela abaixo registra as principais divergências corrigidas em relação à seção 10.2 do documento de gestão (versão 1.3):

| ID (anterior) | Problema identificado | Correção aplicada |
| :--- | :--- | :--- |
| RNF03 | Citava hash **SHA-256** | Substituído por **bcrypt com salt**, conforme `auth_service.py` e `sqlite_repository.py` |
| RNF02 | Meta de 2 s sem limite superior | Incluído timeout de subprocesso de **10 s** (`windows_mapper.py`) |
| RNF01 | Descrição genérica | Detalhados critérios de UX desktop (PyWebView, dimensões fixas, feedback visual) |
| — | Lista incompleta (5 itens) | Expandida para cobrir arquitetura, RBAC, compatibilidade Windows, SQLite, auditoria e operação local |

---

## 4. Rastreabilidade com a Implementação

| ID | Evidência no código / build |
| :--- | :--- |
| RNF01 | `src/infrastructure/web/templates/*.html`, classes `glass`, Tailwind CSS |
| RNF02 | `main_desktop.py` — `webview.create_window(...)` |
| RNF03 | `src/infrastructure/system/windows_mapper.py` — `timeout=10` |
| RNF05 | `src/application/auth_service.py`, `src/infrastructure/persistence/sqlite_repository.py` |
| RNF06 | `src/infrastructure/web/decorators.py` — `role_required` |
| RNF07 | `src/infrastructure/web/app.py` — `secret_key`, controllers de auth |
| RNF08 | `build_exe.py` — PyInstaller `--onefile` |
| RNF09 | `windows_mapper.py` — `net use`, `subst`, verificação `platform.system()` |
| RNF10–RNF11 | Retornos estruturados em use cases e controllers |
| RNF12–RNF13 | `src/domain/`, `src/application/`, `src/infrastructure/` |
| RNF14 | `SQLiteRepository`, schema em `Gestao_Projetos_...md` §15 |
| RNF16 | `src/infrastructure/audit/file_audit_logger.py` |

---

## 5. Referências

* SOMMERVILLE, Ian. **Engenharia de Software**. 8ª Ed. Pearson, 2007.  
* EVANS, Eric. **Domain-Driven Design**. Addison-Wesley, 2003.  
* MARTIN, Robert C. **Clean Architecture**. Prentice Hall, 2017.  
* PYTHON SOFTWARE FOUNDATION. **bcrypt** e documentação Python 3.12. 2024.
