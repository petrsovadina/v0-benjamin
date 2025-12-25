# Architektura systému

> **⚠️ Poznámka**: Detailní živá dokumentace je dostupná v `/app/docs` (Nextra) a hlavní README.

## Přehled
- **Frontend**: Next.js 16 (React 19), Shadcn/UI, TailwindCSS v4.
- **Backend**: FastAPI (Python 3.11+).
- **AI Orchestrace**: LangGraph (Chat, Epikríza, Překladač).
- **Databáze**: Supabase (PostgreSQL + pgvector).

## Klíčové Komponenty
1. **AI Chat**: Streamované odpovědi s citacemi (SÚKL, PubMed).
2. **VZP Navigator**: Vyhledávání úhrad a cen léků.
3. **Epikríza Generator**: Automatizovaná tvorba zpráv.
4. **Data Pipeline**: ETL procesy pro SÚKL data (viz `backend/README.md`).
