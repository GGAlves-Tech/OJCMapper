# Roteiro de Pitch — OJCMapper (3 minutos)

**Projeto:** MAPPER — Utilitário de Gerenciamento do Armazenamento de Mídias  
**Cliente:** Rede Anhanguera / Centro Norte de Comunicação Ltda — Palmas-TO  
**Equipe:** Adriano Carneiro Rosa, Diana Lopes da Silva, Guthemberg B. Alves, Kauãn Kelvin Mendes da Costa  
**Duração alvo:** 3:00 (tolerância até 3:10)  
**Palavras:** ~420 (~140 palavras/minuto com pausas naturais)  
**Versão:** 1.1 — 08/06/2026

---

## Ferramentas para a gravação

| Recurso | Uso no pitch |
| :--- | :--- |
| **Protótipo web (Vercel)** | Demo principal em aba do navegador — todas as telas, zero risco |
| **Repositório protótipo** | [github.com/GGAlves-Tech/OJCMapper.prototipo](https://github.com/GGAlves-Tech/OJCMapper.prototipo) |
| **App real (`run_pitch.py`)** | Mapeamento Windows real com NAS simulado — opcional |
| **Slides (Canva/PPT)** | Gancho com números + stack técnica + fechamento |

**Login da demo:** `admin` / `admin` (Gerente — vê todas as abas)

---

## Estrutura do pitch

| Bloco | Tempo | Foco |
| :--- | :--- | :--- |
| 1. Gancho — a dor | 0:00 – 0:25 | Problema vivido pelo editor |
| 2. Contexto — por que importa | 0:25 – 0:55 | Números e ecossistema enterprise |
| 3. A solução + demo | 0:55 – 1:45 | OJCMapper e telas principais |
| 4. Diferencial técnico | 1:45 – 2:20 | Stack, arquitetura, deploy |
| 5. Resultado e valor | 2:20 – 2:50 | Ganho operacional e acadêmico |
| 6. Fechamento | 2:50 – 3:00 | Frase final memorável |

> **Formato recomendado pelo orientador:** começar pela dor ("faca no pescoço") e terminar com o curativo (o software).

---

## Roteiro completo (1 apresentador)

### [0:00 – 0:25] Gancho — a dor

> *"Imagine um editor de vídeo com uma matéria urgente para o ar — e ele perde minutos preciosos só tentando achar onde o projeto está salvo na rede.*
>
> *Na TV Anhanguera de Palmas, isso não é exceção: é rotina. O jornalismo gera cerca de **4 terabytes por semana** — **12 terabytes por mês** — entre materiais de ingest e arquivo do CEDOC. Com esse volume, mapear pastas manualmente nas ilhas de edição AVID virou um gargalo que atrasa a produção e gera chamados diários para o suporte de TI."*

**[Pausa de 1 segundo]**

---

### [0:25 – 0:55] Contexto — por que isso importa

> *"O problema não é falta de tecnologia. A emissora já investe em infraestrutura de ponta: Storage Quantum Stornext 5, AVID Media Composer e NewsCutter.*
>
> *O que faltava era o elo entre o storage e o editor — uma ferramenta simples que organizasse o acesso sem exigir conhecimento técnico de rede. Hoje, **92%** dos dados são mídias ativas de ingest e edição; **8%** são arquivos do CEDOC. Sem organização, qualquer atraso na busca de arquivos pode custar uma matéria no ar."*

---

### [0:55 – 1:45] A solução — OJCMapper + demo

> *"Para resolver isso, desenvolvemos o **OJCMapper**: um utilitário desktop que automatiza o mapeamento de unidades de rede no Windows.*
>
> *Com um clique, o editor conecta o projeto certo na letra de drive disponível — sem prompt de comando, sem `net use` manual. A interface separa **Online** e **Gaveta**, mostra as **unidades ativas** em tabela com letra, caminho e ação, e ainda permite **engavetar**, **deletar** com confirmação, **gerenciar usuários** por perfil e **configurar** os caminhos do storage.*
>
> *Perfis Gerente, Editor e Default evitam exclusões acidentais. Ações críticas vão para log de auditoria, e falhas de rede não travam a aplicação."*

**[Demo na tela — roteiro visual abaixo, ~50 segundos]**

---

### [1:45 – 2:20] Diferencial técnico

> *"Por baixo, o OJCMapper foi construído em **Python 3.12** com **Clean Architecture**, **DDD** e **Hexagonal Architecture** — regras de negócio isoladas da interface e do banco.*
>
> *A UI é web moderna renderizada como app desktop via **PyWebView**. Persistência local em **SQLite**, senhas com **bcrypt**, e deploy como **executável único `.exe`**. Para apresentações, publicamos um **protótipo interativo na Vercel** com todas as telas do sistema."*

---

### [2:20 – 2:50] Resultado e valor

> *"O ganho não é só técnico — é operacional. Menos tempo caçando pasta, menos chamado para TI, mais foco na edição. O editor trabalha no conteúdo, não na infraestrutura.*
>
> *Para a equipe do TADS UNITINS, o projeto consolidou experiência real: requisitos medidos na emissora, integração com storage enterprise e entrega de software utilizável em produção."*

---

### [2:50 – 3:00] Fechamento

> *"O OJCMapper transforma um processo manual e frágil em um fluxo organizado, seguro e com um clique. **Menos atrito na rede. Mais produtividade na edição.** Obrigado."*

**[Sorria, pause 1 segundo, encerre a gravação]**

---

## Roteiro visual da demo (~50 s)

Use o **protótipo na Vercel** ou `npm run dev` em `pitch-prototype/`. Mouse devagar.

| Seg | Ação | O que falar (opcional) |
| :---: | :--- | :--- |
| 0–8 | **Login** → `admin` / `admin` | *"Acesso por perfil"* |
| 8–20 | **Conectar** → aba Online → **Mapear** um projeto → ver **Unidades Ativas** (3 colunas) | *"Um clique, letra atribuída automaticamente"* |
| 20–30 | **Deletar** → selecionar projeto → mostrar botões Engavetar/Deletar | *"Gestão segura com confirmação"* |
| 30–38 | **Usuários** → tabela de perfis | *"RBAC: Gerente, Editor, Default"* |
| 38–45 | **Configurar** → caminhos Online, Gaveta, Mídias | *"Parâmetros do Storage Quantum"* |
| 45–50 | Voltar **Conectar** ou encerrar demo | — |

> Se faltar tempo na demo, mostre só **Login → Conectar → Mapear**. Nunca pule o mapeamento com um clique.

---

## Versão ultra-curta do bloco técnico

Use se o ensaio passar de 3:10 — economiza ~20 segundos:

> *"Python com arquitetura em camadas, interface desktop moderna, bcrypt e `.exe` para as estações — com protótipo web na Vercel para demonstração."*

---

## Roteiro alternativo (2 apresentadores)

**Apresentador A** — problema, contexto e fechamento  
**Apresentador B** — solução, demo e técnico

| Tempo | Quem | Texto |
| :--- | :--- | :--- |
| 0:00 – 0:30 | **A** | Gancho + números (4 TB/semana, 12 TB/mês, chamados diários à TI) |
| 0:30 – 0:50 | **B** | Ecossistema (Quantum, AVID) + elo storage ↔ editor |
| 0:50 – 1:40 | **B** | OJCMapper + demo (Conectar, Deletar, Usuários) |
| 1:40 – 2:05 | **B** | Stack: Python, DDD, PyWebView, bcrypt, `.exe`, Vercel |
| 2:05 – 2:40 | **A** | Ganho operacional + experiência UNITINS |
| 2:40 – 3:00 | **A** | *"Menos atrito na rede. Mais produtividade na edição. Obrigado."* |

**Dica:** B controla o mouse na demo; A mantém contato visual com a câmera nos trechos sem tela.

---

## Slides / tela (recomendado)

| Tempo | O que mostrar |
| :--- | :--- |
| 0:00 – 0:55 | Câmera ou slide **"12 TB/mês · 92% ingest"** |
| 0:55 – 1:45 | Protótipo Vercel — fluxo Conectar + Deletar + Usuários |
| 1:45 – 2:20 | Slide: Python · DDD · PyWebView · SQLite · bcrypt · `.exe` |
| 2:20 – 3:00 | Câmera ou slide **Antes × Depois** |

---

## Dicas para a gravação

### Antes de gravar

1. **Ensaie 3 vezes** com cronômetro. Se passar de 3:10, use a versão ultra-curta do bloco técnico.
2. **Decore o gancho e o fechamento**; o meio pode ser mais natural.
3. **Post-it com números:** 4 TB/semana, 12 TB/mês, 92%/8%.
4. **Feche notificações** (WhatsApp, e-mail, Teams).
5. **Abra o protótipo antes** e teste login + mapeamento.

### Qual demo usar?

| Opção | Quando usar |
| :--- | :--- |
| **Vercel (protótipo)** | Gravação do pitch — mais seguro, todas as telas |
| **`npm run dev` local** | Sem internet ou customização de última hora |
| **`python run_pitch.py`** | Mostrar mapeamento real Windows (mais arriscado ao vivo) |

### Áudio (prioridade máxima)

- Fone com microfone ou **20–30 cm** do microfone do notebook.
- Ambiente silencioso; fale um pouco **mais devagar**.
- Teste de **10 segundos** antes da gravação final.

### Vídeo

- Câmera na altura dos olhos, luz de frente.
- Fundo limpo; camisa lisa.
- Olhe para a **câmera** nos trechos sem tela.

### Edição

- **CapCut** ou **DaVinci Resolve** (grátis).
- Título: *"OJCMapper — Gestão de Mídias TV Anhanguera"*.
- Evite música de fundo ou use volume muito baixo.

### O que cortar se estourar 3:10

1. Bloco técnico detalhado (DDD, Hexagonal)
2. Telas Deletar / Usuários / Configurar na demo
3. Frase sobre experiência acadêmica

**Nunca corte:** números (12 TB), dor do editor, demo do mapeamento, fechamento.

---

## Histórico de revisões

| Data | Versão | Alteração |
| :--- | :---: | :--- |
| 08/06/2026 | 1.0 | Criação do roteiro |
| 08/06/2026 | 1.1 | Protótipo Vercel, demo de todas as páginas, bcrypt, roteiro visual 50 s |

---

## Referências

- [`Gestao_Projetos_TO_Graduado_Mapper_OJC.md`](Gestao_Projetos_TO_Graduado_Mapper_OJC.md)
- [`Requisitos_Nao_Funcionais_OJCMapper.md`](Requisitos_Nao_Funcionais_OJCMapper.md)
- [`Avaliacao_Pitch_Professor.md`](Avaliacao_Pitch_Professor.md)
- [OJCMapper.prototipo](https://github.com/GGAlves-Tech/OJCMapper.prototipo) — protótipo pitch (Vercel)
