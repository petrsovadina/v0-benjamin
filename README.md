# Czech MedAI 🏥

> **AI asistent pro české lékaře** — Evidence-based odpovědi s citacemi z PubMed, SÚKL a českých guidelines.

[![Next.js](https://img.shields.io/badge/Next.js-16-black)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688)](https://fastapi.tiangolo.com/)
[![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL-3ECF8E)](https://supabase.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-AI-FF6B6B)](https://github.com/langchain-ai/langgraph)

---

## ⚡ Rychlý start

```bash
# 1. Klonovat repo
git clone <repository-url> && cd v0-benjamin

# 2. Frontend
pnpm install
cp .env.example .env.local  # nastavit SUPABASE credentials
pnpm dev                    # → http://localhost:3000

# 3. Backend (nový terminál)
python -m venv backend/venv && source backend/venv/bin/activate
pip install -r backend/requirements.txt
cp backend/.env.example backend/.env  # nastavit API klíče
uvicorn backend.main:app --reload --port 8000  # → http://localhost:8000/docs
```

---

## 🎯 Hlavní funkce

| Funkce | Popis | Status |
|--------|-------|--------|
| **AI Chat** | Klinické dotazy s citacemi (PubMed, SÚKL, Guidelines) | ✅ Ready |
| **VZP Navigator** | Vyhledávání úhrad a cen léků | ✅ Ready |
| **Epikríza** | Generování zpráv z poznámek | ✅ Ready |
| **Překladač** | Překlad lékařských textů | ✅ Ready |
| **Transkripce** | Audio → text (návštěvy pacientů) | ✅ Ready |

---

## 🏗️ Architektura

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│    Frontend     │────▶│     Backend     │────▶│    Supabase     │
│   Next.js 16    │     │    FastAPI      │     │  PostgreSQL     │
│   React 19      │     │   LangGraph     │     │   pgvector      │
│   Tailwind v4   │     │   Claude 3      │     │   Auth + RLS    │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

**Tech Stack:**
- **Frontend:** Next.js 16, React 19, TypeScript, Tailwind CSS, shadcn/ui
- **Backend:** FastAPI, LangGraph, LangChain, Claude 3 (Anthropic)
- **Database:** Supabase (PostgreSQL + pgvector pro RAG)
- **Auth:** Supabase Auth s Row Level Security

---

## 📁 Struktura projektu

```
v0-benjamin/
├── app/                    # Next.js App Router
│   ├── api/                # Proxy endpointy
│   ├── auth/               # Login, register, reset
│   ├── dashboard/          # Hlavní aplikace
│   └── docs/               # Nextra dokumentace
├── backend/                # FastAPI + LangGraph
│   ├── app/api/v1/         # REST endpointy
│   ├── app/core/           # Config, grafy, state
│   ├── pipeline/           # SÚKL ETL
│   └── README.md           # 📖 Backend dokumentace
├── components/             # React komponenty
├── lib/                    # Utils, Supabase klient
├── docs/                   # Architektura, struktura
├── BACKLOG.md              # 📋 Product backlog
├── ROADMAP.md              # 🗺️ Plán vývoje
└── CLAUDE.md               # 🤖 Pokyny pro AI agenty
```

---

## 🔧 Environment Variables

### Frontend (`.env.local`)
```env
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_PUBLISHABLE_DEFAULT_KEY=eyJ...
```

### Backend (`backend/.env`)
```env
ANTHROPIC_API_KEY=sk-ant-...      # Claude 3 (povinné)
OPENAI_API_KEY=sk-...              # Embeddings (povinné)
GOOGLE_API_KEY=...                 # Transkripce (povinné)
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=eyJ...                # Service role key
```

---

## 📚 Dokumentace

| Dokument | Obsah |
|----------|-------|
| [backend/README.md](backend/README.md) | API endpointy, SÚKL pipeline, testování |
| [docs/architecture/](docs/architecture/README.md) | Architektonické diagramy |
| [docs/structure.md](docs/structure.md) | Kompletní struktura + DB schéma |
| [BACKLOG.md](BACKLOG.md) | Product backlog (6 EPICs, ~63 SP) |
| [ROADMAP.md](ROADMAP.md) | Plán vývoje a milníky |
| [CLAUDE.md](CLAUDE.md) | Pokyny pro AI agenty |

---

## ⚠️ Známé problémy

> Viz [BACKLOG.md](BACKLOG.md) pro kompletní seznam a řešení.

- **Bezpečnost:** 14 tabulek bez RLS → Sprint 1
- **Auth:** Některé `/api/v1/ai/*` endpointy bez autentizace → Sprint 1
- **Streaming:** Backend ready, frontend nepoužívá → Sprint 2

---

## 🚀 Deployment

### Frontend → Vercel
```bash
vercel --prod
```

### Backend → Docker
```bash
docker build -t czech-medai-backend ./backend
docker run -p 8000:8000 --env-file backend/.env czech-medai-backend
```

Detaily v [docs/deployment.md](docs/deployment.md).

---

## 🧪 Testování

```bash
# Backend testy
cd backend && pytest -v

# Frontend (TBD)
pnpm test
```

---

## 📄 Licence

Proprietární software. Všechna práva vyhrazena.

---

**Vytvořeno s ❤️ pro české lékaře**

*Poslední aktualizace: Leden 2026*
