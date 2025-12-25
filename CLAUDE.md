# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Projekt Overview

**Czech MedAI** (kódové označení *Benjamin*) je AI asistent pro české lékaře. Poskytuje evidence-based odpovědi na klinické otázky, ověřuje úhrady VZP a integruje data ze SÚKL, PubMed a českých doporučených postupů.

## Development Commands

### Frontend (Next.js)
```bash
pnpm dev              # Spustit dev server (http://localhost:3000)
pnpm build            # Build produkční verze
pnpm lint             # ESLint kontrola
pnpm start            # Spustit produkční server
```

### Backend (Python FastAPI)
**DŮLEŽITÉ:** Všechny Python příkazy se spouštějí z **kořenového adresáře projektu** (`v0-benjamin`), nikoliv z `backend/`.

```bash
# Vytvoření virtual environment
python -m venv backend/venv
source backend/venv/bin/activate  # macOS/Linux
# .\backend\venv\Scripts\activate  # Windows

# Instalace závislostí
pip install -r backend/requirements.txt

# Spuštění API serveru
uvicorn backend.main:app --reload --port 8000
# API: http://localhost:8000
# Docs: http://localhost:8000/docs
```

### SÚKL Data Pipeline
Pipeline pro stahování a zpracování dat ze SÚKL (léky, ceny, SPC dokumenty).

```bash
# Z kořenového adresáře (v0-benjamin):
python -m backend.pipeline.run_pipeline --all           # Celý pipeline
python -m backend.pipeline.run_pipeline --download      # Pouze stažení
python -m backend.pipeline.run_pipeline --drugs         # Zpracování léků
python -m backend.pipeline.run_pipeline --pricing       # Zpracování cen
python -m backend.pipeline.run_pipeline --documents     # Zpracování SPC/PIL

# Možnosti:
--limit <N>     # Zpracovat pouze N položek (pro testování)
--dry-run       # Běh bez zápisu do DB
```

### Testy
```bash
# Python testy
cd backend && pytest

# Frontend - momentálně není nakonfigurováno
```

## Architecture Overview

### Hybridní architektura (Next.js + Python)

**Frontend (Next.js 16 + TypeScript):**
- `app/` - Next.js App Router stránky
  - `app/dashboard/*` - Hlavní aplikace (Chat, History, Settings, VZP Navigator, Epikriza)
  - `app/api/*` - Frontend API routes (proxy pro backend)
  - `app/auth/*` - Autentizační stránky
- `components/` - React komponenty (Shadcn/UI)
- `lib/` - Shared utilities (Supabase client, auth actions)

**Backend (Python 3.11+ + FastAPI):**
- `backend/main.py` - FastAPI entry point s rate limitingem
- `backend/app/` - Modulární FastAPI aplikace
  - `app/core/` - **Klíčová logika**:
    - `graph.py` - LangGraph orchestrátor pro klasifikaci dotazů a RAG
    - `llm.py` - LLM providers (Anthropic Claude, OpenAI)
    - `database.py` - Supabase klient
    - `config.py` - Konfigurace
  - `app/api/v1/endpoints/` - API endpointy (`query.py`, `drugs.py`, `admin.py`)
  - `app/services/` - Business logika (search, chat history, cache)
  - `app/schemas/` - Pydantic modely
- `backend/data_processing/` - **ETL Pipeline pro SÚKL**:
  - `downloaders/` - Stahování dat ze SÚKL
  - `parsers/` - Parsování CSV/Excel dat
  - `loaders/` - Nahrávání do Supabase
  - `embeddings/` - Generování vektorových embeddingů
- `backend/pipeline/` - Orchestrace ETL procesu
- `backend/services/` - MCP servery a další služby

### Důležité koncepty

**LangGraph Flow (backend/app/core/graph.py):**
- Klasifikátor dotazů na typy: `drug_info`, `guidelines`, `clinical`, `urgent`, `reimbursement`
- Routing na základě typu dotazu
- RAG retrieval z Supabase Vector Store
- Generování odpovědí s citacemi

**Data Flow:**
1. Uživatel zadá dotaz (Next.js)
2. Požadavek jde přes `/api/chat` (frontend proxy) na backend
3. Backend klasifikuje dotaz (LangGraph)
4. Podle typu: vyhledá kontext (SÚKL, Guidelines, PubMed)
5. LLM vygeneruje odpověď s citacemi
6. Odpověď se uloží do `queries` tabulky
7. Historie chatu v `chat_sessions` a `chat_messages`

**Database (Supabase PostgreSQL):**
- `drugs` - SÚKL léky (DLP - Databáze léčivých přípravků)
- `pricing` - Cenové údaje a úhrady VZP
- `spc_documents` - Souhrny údajů o přípravku
- `guidelines` - Doporučené postupy (vektorizované)
- `queries` - Uživatelské dotazy a odpovědi
- `chat_sessions`, `chat_messages` - Historie konverzací
- Používá `pgvector` extension pro sémantické vyhledávání

## Environment Variables

**Frontend (`.env.local`):**
```bash
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
NEXT_PUBLIC_API_URL=http://localhost:8000  # Backend URL
```

**Backend (`backend/.env`):**
```bash
OPENAI_API_KEY=        # Pro embeddings (volitelné)
ANTHROPIC_API_KEY=     # Claude 3.5 Sonnet (POVINNÉ)
GOOGLE_API_KEY=        # Pro audio transkripci (POVINNÉ)
SUPABASE_URL=
SUPABASE_KEY=          # Service Role Key (pro pipeline)
```

## Známé problémy a specifika

1. **Module Resolution:** Python pipeline se MUSÍ spouštět z kořenového adresáře, ne z `backend/`. Používá importy typu `backend.pipeline.*`.

2. **Rate Limiting:** Backend má rate limit 60 požadavků/minutu na `/api/chat` endpoint.

3. **SÚKL Data:** Aplikace vyžaduje nahraná data v DB. První setup musí spustit `--all` pipeline.

4. **LangGraph State:** `ClinicalState` obsahuje `messages`, `query_type`, `retrieved_context`, `final_answer`. Veškerá logika orchestrace je v `backend/app/core/graph.py`.

5. **Caching:** Backend používá in-memory cache pro LLM odpovědi (`backend/services/cache.py`).

6. **MCP Integration:** Backend podporuje MCP servery pro nástroje jako PubMed search (`paper-search-mcp`).

## Import Paths

**Frontend:**
- Používá `@/` alias pro root (`tsconfig.json`)
- Příklad: `import { createClient } from '@/lib/supabase/client'`

**Backend:**
- Absolutní importy: `from backend.app.core.graph import app`
- Relativní importy POUZE v rámci stejného modulu

## Roadmap Status

- ✅ **Dokončeno:** Backend API, Chat UI, SÚKL Data Pipeline, LangGraph
- 🚧 **Probíhá:** Guidelines import (PDF → Vectors)
- 📅 **Plánováno:** Lékové interakce, Epikríza generator, E2E testy

## Tech Stack Details

- **Frontend:** Next.js 16, React 19, TypeScript 5.x, Tailwind CSS 4.x, Shadcn/UI
- **Backend:** Python 3.11+, FastAPI, LangGraph 1.0, LangChain
- **AI:** Anthropic Claude 3.5 Sonnet, OpenAI GPT-4o (fallback)
- **Database:** Supabase (PostgreSQL 15 + pgvector)
- **Embeddings:** OpenAI `text-embedding-3-small` nebo Anthropic
- **Data Processing:** Pandas, PyPDF, pdfplumber, BeautifulSoup
