# Architektura systému Czech MedAI

> **Poslední aktualizace**: Leden 2026
> 
> Pro detailní backlog viz [BACKLOG.md](../../BACKLOG.md)

## Přehled

| Vrstva | Technologie |
|--------|-------------|
| **Frontend** | Next.js 16 (React 19), Shadcn/UI, TailwindCSS v4 |
| **Backend** | FastAPI (Python 3.11+), Uvicorn |
| **AI Orchestrace** | LangGraph, LangChain, Claude 3 (Anthropic) |
| **Databáze** | Supabase (PostgreSQL + pgvector) |
| **Auth** | Supabase Auth + RLS |

---

## Architektura - Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND (Next.js)                       │
├─────────────────────────────────────────────────────────────────┤
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌───────────┐ │
│  │ ChatInterface│  │VzpSearch   │  │Translator  │  │Epicrisis  │ │
│  └──────┬─────┘  └──────┬─────┘  └──────┬─────┘  └─────┬─────┘ │
│         │               │               │               │        │
│  ┌──────▼───────────────▼───────────────▼───────────────▼─────┐ │
│  │                    Next.js API Routes                       │ │
│  │         /api/chat  /api/vzp  /api/translate /api/epicrisis │ │
│  └────────────────────────────┬───────────────────────────────┘ │
└───────────────────────────────┼─────────────────────────────────┘
                                │ HTTP (Bearer Token)
┌───────────────────────────────▼─────────────────────────────────┐
│                         BACKEND (FastAPI)                        │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    /api/v1/ Endpoints                        ││
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────────┐││
│  │  │query.py  │ │ ai.py    │ │drugs.py  │ │ admin.py         │││
│  │  │- POST /  │ │-epicrisis│ │-search   │ │- upload-guideline│││
│  │  │- /stream │ │-translate│ │-vzp-srch │ │                  │││
│  │  │- /history│ │-transcribe│ │-detail  │ │                  │││
│  │  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────────┬─────────┘││
│  └───────┼────────────┼────────────┼────────────────┼──────────┘│
│          │            │            │                │           │
│  ┌───────▼────────────▼────────────▼────────────────▼──────────┐│
│  │                    LangGraph Workflows                       ││
│  │  ┌────────────────┐ ┌────────────┐ ┌────────────────────┐   ││
│  │  │ graph.py (RAG) │ │agent_graph │ │epicrisis/translator│   ││
│  │  │ - classifier   │ │ - streaming│ │    graphs          │   ││
│  │  │ - retriever    │ │ - tools    │ │                    │   ││
│  │  │ - synthesizer  │ │            │ │                    │   ││
│  │  └────────────────┘ └────────────┘ └────────────────────┘   ││
│  └─────────────────────────────────────────────────────────────┘│
└───────────────────────────────┬─────────────────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────────┐
│                         SUPABASE                                 │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │  Auth       │  │  PostgreSQL │  │  pgvector (embeddings)  │  │
│  │  - JWT      │  │  - 27 tables│  │  - drugs.embedding      │  │
│  │  - RLS      │  │  - RLS      │  │  - guidelines.embedding │  │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Klíčové Komponenty

### 1. AI Chat
- **Non-streaming**: `/api/v1/query/` → `graph.py` (RAG workflow)
- **Streaming**: `/api/v1/query/stream` → `agent_graph.py` (tool-based)
- Citace z SÚKL, PubMed, Guidelines

### 2. VZP Navigator
- Vyhledávání úhrad a cen léků
- Sémantické vyhledávání (pgvector)

### 3. Epikríza Generator
- `epicrisis_graph.py` - LangGraph pro strukturované reporty
- Input: raw poznámky → Output: formátovaná epikríza

### 4. Data Pipeline
- ETL procesy pro SÚKL data
- Viz `backend/pipeline/` a `backend/data_processing/`

---

## ⚠️ Známé problémy

1. **Bezpečnost**: 14 tabulek bez RLS - viz [BACKLOG.md](../../BACKLOG.md#us-11-povolit-rls-na-všech-veřejných-tabulkách)
2. **Auth**: Některé endpointy bez autentizace - viz [BACKLOG.md](../../BACKLOG.md#us-12-přidat-autentizaci-na-nechráněné-api-endpointy)
3. **Komunikace FE-BE**: Nekonzistentní vzory (proxy vs přímé volání)

---

## Další dokumentace

- [README.md](../../README.md) - Rychlý start
- [CLAUDE.md](../../CLAUDE.md) - Pokyny pro AI agenty
- [BACKLOG.md](../../BACKLOG.md) - Detailní backlog
- [data_pipeline.md](../data_pipeline.md) - SÚKL pipeline
