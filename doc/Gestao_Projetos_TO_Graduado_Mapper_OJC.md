

# ESPECIFICAÇÃO E ANÁLISE DE REQUISITOS DO PROJETO MAPPER \- UTILITÁRIO DE GERENCIAMENTO DO ARMAZENAMENTO DE MÍDIAS

**Elaboração**  
*Adriano Carneiro Rosa*   
*Diana Lopes da Silva*  
*Guthemberg B. Alves*   
*Kauãn Kelvin Mendes da Costa*

**Aprovação Técnica**  
*Leandra Cristina Cavina Piovesan Soares*  
*Joelson de Araújo Delfino*

**Responsável operacional**  
*Centro Norte de Comunicação ltda \- TV Anhanguera Tocantins*

**Palmas – TO**  
**2026**

**Lista de distribuição**

| Nome | Cargo | E-mail | Fone |
| ----- | ----- | ----- | ----- |
| *Adriano Carneiro Rosa* | Desenvolvedor de Software */ add mais* |  |  |
| *Bruno Vieira de Melo Aguiar* | Desenvolvedor de Software */ add mais* |  |  |
| *Diana Lopes da Silva* | Desenvolvedor de Software */add mais* |  |  |
| *Guthemberg B. Alves* | Gerente do Projeto/Desenvolvedor de Software  |  |  |
| *Kauãn Kelvin Mendes da Costa*  | Desenvolvedor de Software  |  |  |
| *Rede Anhanguera* | Cliente |  |  |

# HISTÓRICO DE REVISÕES

| data | versão | Comentário | autor |
| ----- | :---: | ----- | ----- |
| **19-11-2024** | **1.0** | **criação do documento** | *Diana Lopes da Silva* |
| **06-12-2024** | **1.1** | **Edição pós revisão** | *Kauãn Kelvin Mendes da Costa* |
| **23-02-2026** | **1.2** | **Edição pós revisão** | *Diana Lopes da Silva* |
| **11-05-2026** | **1.3** | **Refatoração Arquitetural e Tecnológica (DDD/Web UI)** | *Guthemberg B. Alves* |
| **08-06-2026** | **1.4** | **Extração dos RNFs para documento dedicado; correção bcrypt e critérios de performance** | *Guthemberg B. Alves* |

# SUMÁRIO 

[HISTÓRICO DE REVISÕES](#histórico-de-revisões)

[**1**	**Introdução**](#1-introdução)

[**2**	**Situação atual e justificativa do projeto**](#2-situação-atual-e-justificativa-do-projeto)

[**3**	**Escopo do Projeto**](#3-escopo-do-projeto)

[**4**	**Dependências do Projeto**](#4-dependências-do-projeto)

[**5**	**Restrições do Projeto**](#5-restrições-do-projeto)

[**6**	**Premissas do Projeto**](#6-premissas-do-projeto)

[**7**	**Gestão dos Riscos e Problemas do Projeto**](#7-gestão-dos-riscos-e-problemas-do-projeto)

[**8**	**Estimativas Iniciais**](#8-estimativas-iniciais)

[**9**	**Recursos Utilizados**](#9-recursos-utilizados)

[**10**	**Requisitos Específicos do Projeto**](#10-requisitos-específicos-do-projeto)

[10.1 Lista dos Requisitos Funcionais](#101-lista-dos-requisitos-funcionais)  
[10.2 Lista dos Requisitos Não Funcionais](#102-lista-dos-requisitos-não-funcionais)

[**11**	**Detalhamento dos Casos de Uso**](#11-detalhamento-dos-casos-de-uso-core-flows)

[**12**	**Atores e Perfis de Acesso**](#12-atores-e-perfis-de-acesso)

[**13**	**Modelagem de Processos e Casos de Uso**](#13-modelagem-de-processos-e-casos-de-uso)

[**14**	**Arquitetura do Sistema e Modelo de Domínio**](#14-arquitetura-do-sistema-e-modelo-de-domínio)

[**15**	**Projeto de Banco de Dados**](#15-projeto-de-banco-de-dados-relacional)

[**16**	**Cronograma**](#16-cronograma-e-entregas-base-sprints)

[**17**	**Aprovações**](#17-aprovações)

# 1. Introdução

O gerenciamento eficaz de unidades de rede é um aspecto crucial na otimização de processos de produção, especialmente em ambientes que dependem de armazenamento compartilhado e colaboração em tempo real. No contexto da edição de vídeo, onde a organização e o acesso rápido a arquivos são fundamentais, a implementação de um utilitário que facilite essa gestão se torna indispensável.   
Pensando nessa necessidade, a Rede Anhanguera, mantida pela empresa Centro Norte de Comunicação Ltda, com sede em Palmas-TO, busca soluções que modernizem os fluxos de trabalho de produção audiovisual. O projeto MAPPER visa desenvolver um software que possibilite o mapeamento intuitivo de pastas em um ambiente de rede compartilhado, permitindo que as ilhas de edição tenham acesso a um repositório que mesmo centralizado permita o acesso a todos os vídeos disponíveis nesse compartilhamento. As soluções já implantadas buscando uma alta disponibilidade de todo o conteúdo da emissora como sistema de armazenamento Storage Quantum (Stornext 5), ferramentas de edição AVID Media Composer e NewsCutter, representam um avanço significativo na modernização dos fluxos de trabalho de produção audiovisual.

# 2. Situação atual e justificativa do projeto

Este documento é baseado em estatísticas colhidas durante estudos realizados com objetivos específicos de implantar um novo fluxo de edição na emissora de Palmas. Com os levantamentos chegou-se a conclusão do uso médio de 4TB por semana de dados do jornalismo, sendo 12TB por mês. Destes dados, verificou-se que 92% são mídias provenientes de “ingest” (processo/rotina que armazena de forma permanente os vídeos) e editadas e 8% são as mídias de arquivo (CEDOC).   
Baseado nisso, a proposta deste projeto além de inserir um workflow para rotina da captura ao arquivamento deve inserir uma nova ferramenta para que seja possível melhorar a forma dos editores terem acesso aos projetos que estão armazenados no Storage. Idealizando uma ecoistema que permita uma edição compartilhada e centralizada onde devem ser seguidas as regras que serão apresentadas também neste documento para o perfeito funcionamento do sistema e também a manutenção dos dados dentro do fluxo correto para as mídias, evitando assim perda de dados e problemas futuros não previstos pela engenharia.   
A necessidade de um gerenciamento adequado das unidades de rede se torna evidente quando se considera a complexidade dos projetos de edição de vídeo. A falta de organização pode resultar em perda de tempo e recursos, dificultando a localização de materiais e o acompanhamento do estado de produção. Estudos demonstram que um fluxo de trabalho bem estruturado é fundamental para garantir a eficiência e a produtividade em ambientes colaborativos. A implementação do MAPPER não apenas atenderá a essa necessidade, mas também proporcionará um ambiente mais coeso para a equipe de edição, permitindo que os projetos sejam compartilhados de maneira organizada e de maneira simplificada.  
Além disso, a integração do MAPPER com o sistema de armazenamento Quantum é um passo significativo para a modernização das práticas de trabalho. A utilização de tecnologias inovadoras, como a proposta de um sistema de gerenciamento de dados que separe a gestão de estado dos dados de armazenamento, pode aumentar a flexibilidade e a eficiência do sistema. O projeto MAPPER, portanto, não é apenas uma resposta a uma necessidade imediata, mas também uma contribuição para a evolução das práticas de gerenciamento de dados em ambientes de edição de vídeo, alinhando-se com as tendências atuais de digitalização e colaboração em um curto espaço de tempo.  
Através da combinação de conhecimentos e habilidades, o projeto não só visa resolver problemas práticos, mas também fomentar um ambiente de aprendizado contínuo e adaptação às novas tecnologias.

# 3. Escopo do Projeto

O projeto MAPPER é uma solução de engenharia de software desenvolvida para otimizar o gerenciamento de unidades de rede em infraestruturas de produção audiovisual. A solução foca na integração harmoniosa entre o repositório central (Quantum Storage) e as ilhas de edição (AVID Media Composer), garantindo que o acesso aos dados seja ágil, seguro e escalável.

O desenvolvimento utiliza uma abordagem de **Arquitetura Limpa (Clean Architecture)** com **Domain-Driven Design (DDD)**, garantindo que as regras de negócio sejam independentes da interface de usuário e do banco de dados.

**Metodologia de Desenvolvimento:**

* **Análise e Domínio:** Modelagem das entidades centrais (Projetos, Usuários, Configurações) para garantir consistência operacional.
* **Arquitetura em Camadas:**
    * **Domain:** Regras fundamentais e interfaces.
    * **Application:** Casos de uso e lógica de serviços.
    * **Infrastructure:** Implementação técnica de mapeamento (Windows Shell), persistência (SQLite) e Interface (Flask).
* **Interface Moderna:** Desenvolvimento de uma interface Web simulando experiência Desktop (Chromeless) com foco em UX (User Experience).
* **Implantação via Artefatos:** Geração de executáveis únicos (.exe) via PyInstaller para facilitar a distribuição Windows.

4. **Dependências do Projeto** 

O sucesso do projeto depende da disponibilidade da infraestrutura de rede local e do acesso ao Storage Quantum.

| Número de ordem | Dependência | De quem depende | Data Limite |
| :---: | :---: | :---: | :---: |
| 1 | Treinamento | Cliente | 30/07/2026 |
| 2 | Homologação em Estação Real | Engenharia técnica | 15/05/2026 |

5. **Restrições do Projeto** 

O OJCMapper opera sob as seguintes condições técnicas e gerenciais:
* **Ambiente de Execução:** Destinado exclusivamente ao sistema operacional Windows (7 SP1 a 11), devido à dependência de comandos de sistema para mapeamento de drives.
* **Stack Tecnológica:** Python 3.12+ para garantir longevidade e compatibilidade com bibliotecas modernas de segurança.
* **Interface:** Interface baseada em tecnologias Web (HTML5/CSS3/JS), porém executada localmente para evitar latência.
* **Cronograma Acadêmico:** Submetido aos prazos estabelecidos pelo programa TO Graduado (UNITINS).

# 6. Premissas do Projeto

* O sistema será utilizado em rede local controlada, mitigando riscos de ataques externos massivos.
* O banco de dados SQLite será local, garantindo performance de leitura para listagem de projetos.
* As permissões de mapeamento (`net use`) devem estar habilitadas no perfil do usuário Windows que executará o software.

# 7. Gestão dos Riscos e Problemas do Projeto

* **Compatibilidade Retroativa:** Garantir suporte ao Windows 7 SP1 utilizado em algumas ilhas de edição.
* **Persistência de Conexões:** Tratar falhas de rede no mapeamento para evitar travamentos na interface Flask.
* **Segurança de Credenciais:** Implementação de *hashing* de senhas para proteger o acesso administrativo às configurações.

8. **Estimativas Iniciais** 

|  | Estimativa |
| :---- | ----- |
| Data de Início | 24/09/2024 |
| Data de Término | 30/07/2026 |
| Custos de Licença | R$ 0,00 (Open Source / Internal Use) |

9. **Recursos Utilizados** 

A stack foi modernizada para eliminar dependências legadas e garantir alta fidelidade visual.

| Tipo de Recurso | Identificação do Recurso | Nome do Responsável |
| :--- | :--- | :--- |
| **Humano** | *Analista/Dev* | *Equipe TADS - TO Graduado* |
| | *Administrador de Redes* | *Adriano Carneiro Rosa* |
| | *Gerente de Projetos* | *Diana Lopes da Silva* |
| | *Product Owner* | *Guthemberg B. Alves* |
| **Tecnológico** | *Python 3.12+* | Core Logic |
| | *Flask* | Web Interface |
| | *PyWebView* | Desktop Window Native Bridge |
| | *SQLite 3* | Persistence |
| | *HTML5 / CSS3 (Vanilla)* | UI / Rich Aesthetics |
| | *PyInstaller* | Packaging |
| | *Visual Studio Code* | IDE |
| **Infraestrutura** | *Stornext 5 / UNC* | Network Storage |
| | *Windows Shell* | Drive Mapping |
| | *Windows 10/11* | Ambiente Operacional Alvo |
| | *Infra de Rede Local* | Rede Anhanguera |

# 10. Requisitos Específicos do Projeto

## 10.1 Lista dos Requisitos Funcionais

| ID | Nome do Requisito | Descrição | Escopo | Prioridade |
| :--- | :--- | :--- | :--- | :---: |
| RF01 | Listagem scope-based | Listar projetos filtrados por ONLINE (recentes) ou GAVETA (arquivados). | Aplicação | **Essencial** |
| RF02 | Busca Incremental | Pesquisar nomes de projetos dinamicamente na lista ativa. | UI | **Essencial** |
| RF03 | Mapeamento Híbrido | Montar unidade de rede via `net use` (UNC) ou local via `subst`. | Infra | **Essencial** |
| RF04 | Monitoramento de Unidades | Listar mapeamentos ativos reconhecidos pelo Windows. | Infra | **Essencial** |
| RF05 | Desmontagem Dinâmica | Desmontar unidades mapeadas (individuais ou em lote). | Infra | **Essencial** |
| RF06 | Gestão de Configurações | Interface para alteração de caminhos base (Online, Gaveta, Logs). | Gestão | **Importante** |
| RF07 | Gestão de Matérias | Seleção e deleção permanente de metadados e mídias. | Gestão | **Importante** |
| RF08 | Autenticação Multi-Role | Login com níveis de permissão (Gerente, Editor, Default). | Segurança | **Essencial** |
| RF09 | Exportação de Relatório | Exportar a lista vigente de projetos em formato **TXT**. | Aplicação | **Desejável** |
| RF10 | Gestão de Usuários | Cadastro, edição e exclusão de perfis de acesso. | Gestão | **Importante** |

## 10.2 Lista dos Requisitos Não Funcionais

A lista completa e revisada dos requisitos não funcionais encontra-se no documento dedicado:

**[Requisitos_Nao_Funcionais_OJCMapper.md](Requisitos_Nao_Funcionais_OJCMapper.md)**

Resumo (17 itens — versão 1.0, 08/06/2026):

| ID | Categoria | Descrição resumida | Prioridade |
| :--- | :--- | :--- | :---: |
| RNF01 | Usabilidade | Interface moderna com glassmorphism e feedback visual | **Essencial** |
| RNF02 | Usabilidade | Experiência desktop via PyWebView (janela 500×800) | **Essencial** |
| RNF03 | Performance | Mapeamento ≤ 2 s (rede estável); timeout máx. 10 s | **Essencial** |
| RNF04 | Performance | Listagem e busca incremental fluidas | **Importante** |
| RNF05 | Segurança | Senhas com hash bcrypt (com salt) | **Essencial** |
| RNF06 | Segurança | Controle de acesso por perfis (RBAC) | **Essencial** |
| RNF07 | Segurança | Sessões Flask com autenticação | **Essencial** |
| RNF08 | Portabilidade | Executável único `.exe` via PyInstaller | **Essencial** |
| RNF09 | Compatibilidade | Windows 7 SP1 a 11 (`net use` / `subst`) | **Essencial** |
| RNF10 | Robustez | Tratamento de erros em mapeamento e rede | **Essencial** |
| RNF11 | Robustez | Recuperação graciosa em indisponibilidade | **Importante** |
| RNF12 | Manutenibilidade | Clean Architecture + DDD + Hexagonal | **Essencial** |
| RNF13 | Manutenibilidade | Bounded contexts no domínio | **Importante** |
| RNF14 | Persistência | SQLite local sem servidor externo | **Essencial** |
| RNF15 | Operacionalidade | Execução em rede local (sem internet) | **Essencial** |
| RNF16 | Auditabilidade | Log de ações críticas por arquivo diário | **Importante** |
| RNF17 | Escalabilidade | Adequação ao volume operacional da emissora | **Desejável** |

# 11. Detalhamento dos Casos de Uso (Core Flows)

### [UC01] - Gerenciar Unidades de Rede
* **Ator:** Todos os usuários.
* **Fluxo Principal:** 
    1. Usuário seleciona o escopo (Online/Gaveta).
    2. Sistema lista projetos disponíveis no diretório configurado.
    3. Usuário seleciona o projeto e clica em "Mapear".
    4. Sistema identifica a primeira letra disponível no Windows.
    5. Sistema executa comando de mapeamento e atualiza a interface.

### [UC02] - Exportação de Projetos (RF09)
* **Ator:** Gerente / Admin.
* **Fluxo Principal:**
    1. Usuário acessa o painel de exportação.
    2. Seleciona o escopo desejado.
    3. Sistema gera um arquivo `.txt` contendo a lista formatada com nomes e caminhos.

### [UC03] - Controle de Configurações
* **Ator:** Admin.
* **Fluxo Principal:**
    1. Admin altera `online_path` ou `gaveta_path`.
    2. Sistema valida a existência do caminho.
    3. Sistema persiste a nova configuração no banco SQLite.

# 12. Atores e Perfis de Acesso

| Perfil | Descrição e Permissões |
| :--- | :--- |
| **Admin** | Acesso total: Mapeamento, Configurações, Gestão de Usuários e Deleção. |
| **Gerente** | Permissões de Mapeamento, Deleção e Exportação de Relatórios. |
| **Editor** | Permissão de Mapeamento e visualização de listas. (Modo Guest/Padrão) |
| **Default** | Perfil com permissões mínimas, configurado conforme necessidade contratual. |

# 13. Modelagem de Processos e Casos de Uso

A visualização detalhada dos processos encontra-se no arquivo anexo desenvolvido para alta fidelidade:
* **Legenda:** [Figura 1 - Diagrama de Casos de Uso](file:///d:/GIT/OJCMapper/doc/diagrams/Figura_1_Diagrama_de_Casos_de_Uso.html)

# 14. Arquitetura do Sistema e Modelo de Domínio

O OJCMapper utiliza uma arquitetura baseada em **Camadas de Responsabilidade**, permitindo que a lógica de mapeamento de unidades (Infraestrutura) seja isolada das regras de projeto (Domínio).

**Diagramas Técnicos:**
* **Estrutura de Container:** [Figura 2 - Arquitetura C4 do Sistema](file:///d:/GIT/OJCMapper/doc/diagrams/Figura_2_Arquitetura_C4_Sistema.html)
* **Modelo de Classes:** [Figura 3 - Diagrama de Classes de Domínio](file:///d:/GIT/OJCMapper/doc/diagrams/Figura_3_Diagrama_de_Classes_Dominio.html)
* **Fluxo de Trabalho:** [Figura 5 - Fluxo de Mapeamento (Sequência)](file:///d:/GIT/OJCMapper/doc/diagrams/Figura_5_Fluxo_de_Mapeamento_Sequencia.html)

# 15. Projeto de Banco de Dados (Relacional)

O sistema utiliza **SQLite 3** para garantir portabilidade absoluta sem necessidade de servidores de banco de dados externos.

* **Diagrama Entidade-Relacionamento:** [Figura 4 - Modelo de Entidade Relacionamento (ERD)](file:///d:/GIT/OJCMapper/doc/diagrams/Figura_4_Modelo_Entidade_Relacionamento_ERD.html)

**Esquema Físico (DDL):**

```sql
-- OJCMapper — esquema SQLite
-- Espelha SQLiteRepository._init_db em sqlite_repository.py
--
-- Criar base vazia (exemplo):
--   sqlite3 ojcmapper.db < schema.sql
-- Apenas DDL: copie só os três blocos CREATE TABLE.

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key TEXT UNIQUE NOT NULL,
    value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    path TEXT NOT NULL
);

-- ---------------------------------------------------------------------------
-- Dados iniciais (a aplicação só insere isto quando a tabela users está vazia).
-- users/settings: INSERT OR IGNORE evita erro se voltar a correr. projects: sem UK
-- em name — não volte a executar os INSERT de projects na mesma base ou haverá duplicados.
-- ---------------------------------------------------------------------------

INSERT OR IGNORE INTO users (username, password, role) VALUES ('admin', 'admin', 'Gerente');
INSERT OR IGNORE INTO users (username, password, role) VALUES ('editor', 'editor', 'Editor');
INSERT OR IGNORE INTO users (username, password, role) VALUES ('user', 'user', 'Default');

INSERT OR IGNORE INTO settings (key, value) VALUES ('online_path', 'Z:/Online');
INSERT OR IGNORE INTO settings (key, value) VALUES ('gaveta_path', 'Y:/Gaveta');
INSERT OR IGNORE INTO settings (key, value) VALUES ('av_medias_a_path', 'X:/Media');
INSERT OR IGNORE INTO settings (key, value) VALUES ('lista_path', 'W:/Lists');
INSERT OR IGNORE INTO settings (key, value) VALUES ('online_gaveta_status', 'OFFLINE');
INSERT OR IGNORE INTO settings (key, value) VALUES ('log_path', './app.log');

INSERT INTO projects (name, type, path) VALUES ('Projeto A', 'ONLINE', 'Z:/Online/ProjetoA');
INSERT INTO projects (name, type, path) VALUES ('Projeto B', 'GAVETA', 'Y:/Gaveta/ProjetoB');
```

# 16. Cronograma e Entregas (Base Sprints)
| Sprint | Meta Técnica | Duração | Status | Responsável |
| :---: | :--- | :--- | :---: | :--- |
| **1** | Mapeamento Core (net use/subst) e Infra DDD | 15 dias | **Concluído** | Equipe Dev |
| **2** | Interface Flask Premium e Autenticação SHA-256 | 15 dias | **Concluído** | Equipe Dev |
| **3** | Gestão de Usuários e Dashboards de Configuração | 15 dias | **Em Progresso** | Equipe Dev |
| **4** | Exportação TXT (RF09) e Homologação Final | 10 dias | **Planejado** | Equipe Dev |

# 17. Aprovações

| Participante | Assinatura | Data |
| :--- | :--- | :--- |
| Adriano Carneiro Rosa | _________________________________ | ___/___/2026 |
| Bruno Vieira de Melo Aguiar | _________________________________ | ___/___/2026 |
| Diana Lopes da Silva | _________________________________ | ___/___/2026 |
| Guthemberg B. Alves | _________________________________ | ___/___/2026 |
| Kauãn Kelvin Mendes da Costa | _________________________________ | ___/___/2026 |
| Joelson de Araújo Delfino | _________________________________ | ___/___/2026 |
| Leandra C. C. Piovesan Soares | _________________________________ | ___/___/2026 |
| Centro Norte de Comunicação ltda | _________________________________ | ___/___/2026 |

# Referências Bibliográficas

* CÂNDIDO, Carlos Henrique. **Modelagem de Dados Transformando Modelo Conceitual em Modelo Lógico**. 2020.
* FOWLER, Martin. **Patterns of Enterprise Application Architecture**. Addison-Wesley Professional, 2002.
* EVANS, Eric. **Domain-Driven Design: Tackling Complexity in the Heart of Software**. 2003.
* PYTHON SOFTWARE FOUNDATION. **Python 3.12 documentation**. 2024.
* FLASK. **Pallets Projects Documentation**. 2024.
* SOMMERVILLE, Ian. **Engenharia de Software**. 8ª Ed. Pearson, 2007.