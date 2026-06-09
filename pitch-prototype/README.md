# OJCMapper.prototipo

Protótipo interativo do **OJCMapper** para apresentações e gravação de pitch em aba do navegador.

Desenvolvido com **Vite + Tailwind CSS**, simula a interface do utilitário de mapeamento de unidades de rede da TV Anhanguera (Palmas-TO), sem depender de Flask, Windows Shell ou Storage físico.

## Início rápido

```bash
npm install
npm run dev
```

Abre em `http://localhost:5173` — login de demonstração: **admin / admin**.

Outras credenciais: `editor/editor`, `user/user`.

## Páginas do protótipo

| Tela | Rota | Perfis |
|------|------|--------|
| Login | `#/login` | Todos |
| Conectar | `#/dashboard` | Todos |
| Deletar | `#/deletar` | Gerente, Editor |
| Usuários | `#/usuarios` | Gerente, Editor |
| Configurar | `#/configurar` | Gerente |
| Relatórios | `#/relatorios` | Gerente, Editor (rota direta) |

## Funcionalidades simuladas

| Recurso | Comportamento |
|---------|---------------|
| Login | Credenciais demo: admin/admin, editor/editor, user/user |
| Mapeamento | Mock com letras F, G, H… e delay ~1 s |
| Unidades Ativas | Tabela 3 colunas: Letra, Caminho, Ação |
| Deletar / Engavetar | Atualiza listas mock em memória |
| Usuários | CRUD simulado + modal criar/editar |
| Configurações | Formulário editável com persistência em memória |
| Exportar relatório | Toast de confirmação (TXT simulado) |

O mapeamento simula delay de rede (~1 s) e atribui letras de drive (F:, G:, H:…).

## Build para apresentação

```bash
npm run build
npm run preview
```

Gera arquivos estáticos em `dist/` para uso offline ou hospedagem.

## Deploy na Vercel

O projeto é **100% estático** (SPA com rotas em hash `#/login`, `#/dashboard`) — não precisa de backend nem variáveis de ambiente.

1. Acesse [vercel.com](https://vercel.com) e importe o repositório `GGAlves-Tech/OJCMapper.prototipo`.
2. A Vercel detecta **Vite** automaticamente; confirme:
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
   - **Install Command:** `npm install`
3. Clique em **Deploy**.

Também funciona via CLI:

```bash
npm i -g vercel
vercel
```

Após o deploy, acesse a URL gerada (ex.: `https://ojcmapper-prototipo.vercel.app`) e faça login com `admin` / `admin`.

## Repositório principal

Aplicação completa (Flask, DDD, mapeamento real Windows):

[GGAlves-Tech/OJCMapper](https://github.com/GGAlves-Tech/OJCMapper)

## Equipe

Projeto TADS UNITINS — TV Anhanguera Palmas-TO.
