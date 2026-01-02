# Struktura Repozitáře

> Tento dokument slouží jako mapa projektu pro snazší orientaci vývojářů.
> 
> **Poslední aktualizace**: Leden 2026

## 📂 Kořenová struktura

| Adresář | Popis |
| :--- | :--- |
| **`/app`** | **Frontend (Next.js 16)**. Obsahuje stránky (`page.tsx`), layouty a Next.js API routes (`/api`). |
| **`/backend`** | **Backend (Python 3.x)**. FastAPI služba pro AI, RAG a těžkou logiku. |
| **`/components`** | **UI Komponenty**. React komponenty, většinou postavené na Shadcn UI. |
| **`/docs`** | **Dokumentace**. Všechna zadání a technické popisy. |
| **`/lib`** | **Utility**. Pomocné funkce, konfigurace Supabase klienta. |
| **`/supabase`** | **Databáze**. Migrace (`/migrations`) a konfigurace. |
| **`/scripts`** | **SQL skripty**. Inicializační SQL pro Supabase. |
| **`/public`** | **Assets**. Obrázky, ikony, fonty. |

---

## 🔙 Backend Struktura (`/backend`)

```
backend/
├── app/                          # Hlavní FastAPI aplikace
│   ├── api/v1/                   # Verzované API
│   │   ├── endpoints/            # Routery (ai.py, query.py, drugs.py, admin.py)
│   │   ├── deps.py               # Auth dependencies
│   │   └── api.py                # Router agregátor
│   ├── core/                     # Jádro
│   │   ├── config.py             # Pydantic Settings
│   │   ├── database.py           # Supabase client
│   │   ├── graph.py              # LangGraph RAG workflow
│   │   ├── state.py              # ClinicalState definice
│   │   └── llm.py                # LLM factory
│   ├── schemas/                  # Pydantic modely
│   └── services/                 # Business logika
├── services/                     # Sdílené služby
│   ├── sukl_api_client.py        # SÚKL API
│   ├── chat_history.py           # Historie chatu
│   └── logger.py                 # Strukturované logování
├── data_processing/              # ETL pipeline
├── pipeline/                     # SÚKL data pipeline
├── mcp_servers/                  # MCP servery (PubMed, SÚKL)
├── agent_graph.py                # AI agent (streaming, tools)
├── epicrisis_graph.py            # Epikríza generátor
├── translator_graph.py           # Překladač
├── main.py                       # Entry point
└── requirements.txt              # Python závislosti
```

---

## 🗄️ Databázové tabulky (Supabase)

**Hlavní tabulky:**
- `users` - Uživatelské profily (rozšíření auth.users)
- `queries` - Historie dotazů s metadaty
- `citations` - Citace k dotazům
- `chat_sessions`, `chat_messages` - Chat historie
- `drugs` - SÚKL databáze léčiv (~20k)
- `guidelines` - České klinické guidelines
- `feedback` - Zpětná vazba uživatelů

**Pomocné tabulky (léky):**
- `drug_pricing`, `drug_atc`, `drug_spc`, `drug_pil`
- `drug_packages`, `drug_chunks`, `drug_interactions`
- `active_substances`, `price_history`, `vzp_medicines`

**⚠️ Bezpečnost:** Některé tabulky nemají RLS - viz [BACKLOG.md](../BACKLOG.md).

---

## 📚 Dokumentace (`/docs`)

### 1. `/docs/product` (Produkt & Business)
- `main-prd.md` - **Hlavní PRD**
- `prd_mvp.md` - MVP specifikace
- `product-description/` - Detailní popisy funkcí

### 2. `/docs/technical` (Vývoj)
- Technické manuály, deployment návody

### 3. `/docs/architecture` (Architektura)
- Diagramy, ADR

---

## 🔗 Důležité soubory

| Soubor | Popis |
|--------|-------|
| `README.md` | Vstupní bod, rychlý start |
| `CLAUDE.md` | Pokyny pro AI agenty |
| `BACKLOG.md` | Detailní backlog úkolů |
| `ROADMAP.md` | Plán vývoje |
| `backend/requirements.txt` | Python závislosti |
| `package.json` | Node.js závislosti |
| `backend/app/core/graph.py` | LangGraph RAG workflow |
| `backend/agent_graph.py` | AI agent se streaming |
