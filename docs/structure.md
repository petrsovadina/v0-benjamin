# Struktura Repozitáře

Tento dokument slouží jako mapa projektu pro snazší orientaci vývojářů.

## 📂 Kořenová struktura

| Adresář | Popis |
| :--- | :--- |
| **`/app`** | **Frontend (Next.js)**. Obsahuje stránky (`page.tsx`), layouty a Next.js API routes (`/api`). |
| **`/backend`** | **Backend (Python)**. FastAPI služba pro AI, RAG a těžkou logiku. |
| **`/components`** | **UI Komponenty**. React komponenty, většinou postavené na Shadcn UI. |
| **`/docs`** | **Dokumentace**. Všechna zadání a technické popisy. Viz níže. |
| **`/lib`** | **Utility**. Pomocné funkce, konfigurace Supabase klienta (`supabase/client.ts`). |
| **`/supabase`** | **Databáze**. Migrace (`/migrations`), seed data a konfigurace pro lokální vývoj. |
| **`/public`** | **Assets**. Obrázky, ikony, fonty. |

---

## 📚 Dokumentace (`/docs`)

Dokumentace je rozdělena podle cílové skupiny a účelu:

### 1. `/docs/product` (Produkt & Business)
*   `main-prd.md` - **Hlavní zadání (Product Requirements Document)**. Zdroj pravdy pro funkčnost.
*   `prd_mvp.md` - Specifikace pro MVP (Minimum Viable Product).
*   Specifikace widgetů a rozšíření.

### 2. `/docs/technical` (Vývoj & Tech)
*   Technické manuály, API specifikace (bude doplněno).
*   Návody na deployment.

### 3. `/docs/architecture` (Architektura)
*   Diagramy toků dat.
*   Návrh databázového schématu.
*   ADR (Architecture Decision Records).

---

## 🔗 Důležité soubory
*   `README.md` - Vstupní bod, rychlý start.
*   `backend/requirements.txt` - Python závislosti.
*   `package.json` - Node.js závislosti a skripty.
*   `backend/agent_graph.py` - Definice LangGraph workflow (hlavní AI logika).
