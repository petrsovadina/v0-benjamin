# Czech MedAI — Dokumentace projektu

> **Klinický AI asistent pro české lékaře**  
> Kódové označení: Benjamin

---

## 🎯 O projektu

Czech MedAI je AI-poháněný klinický asistent, který pomáhá ~50 000 českým lékařům rychle najít ověřené medicínské informace v češtině. Každá odpověď obsahuje citace z PubMed, SÚKL, českých guidelines a dalších důvěryhodných zdrojů.

**Klíčové funkce:**
- ⚡ Odpověď do 5 sekund s inline citacemi
- 🇨🇿 Plná lokalizace včetně české lékařské terminologie
- 💊 Integrace SÚKL databáze a VZP úhrad
- 📚 Evidence-based přístup s transparentními zdroji

---

## 📁 Struktura dokumentace

### Hlavní dokumenty (aktuální verze)

| # | Dokument | Popis | Velikost |
|---|----------|-------|----------|
| 1 | **[PRD v1.1](czech-medai-prd-v1.1.docx)** | Product Requirements Document | 19 KB |
| 2 | **[Product Description](czech-medai-product-description.md)** | Srozumitelný popis produktu | 5 KB |
| 3 | **[Use Cases & User Stories](czech-medai-use-cases-user-stories.md)** | 5 UC + 18 User Stories | 10 KB |
| 4 | **[Features Spec](czech-medai-features-spec.md)** | Detailní specifikace funkcí F-001 až F-008 | 23 KB |
| 5 | **[Tech Stack v2](czech-medai-tech-stack-v2.md)** | Technologie (Context7 verified) | 27 KB |
| 6 | **[Data Sources](czech-medai-data-sources-complete.md)** | 43 validovaných URL zdrojů | 12 KB |
| 7 | **[API Specification](czech-medai-api-specification.md)** | REST API dokumentace | 14 KB |
| 8 | **[System Prompt](czech-medai-system-prompt.md)** | Instrukce pro LLM | 12 KB |
| 9 | **[Database Schema](czech-medai-database-schema.md)** | SQL migrace pro Supabase | 27 KB |

### Archivní verze (nepoužívat)

- `czech-medai-prd.docx` — původní PRD
- `czech-medai-tech-stack.md` — zastaralé verze technologií
- `czech-medai-data-sources.md` — neúplný seznam zdrojů

---

## 🚀 Quick Start

### 1. Seznámení s projektem
```
Přečti: Product Description → PRD v1.1 → Use Cases
```

### 2. Technická příprava
```
Přečti: Tech Stack v2 → API Specification → Database Schema
```

### 3. Vývoj
```
Použij: System Prompt (pro LLM) + Data Sources (pro integraci)
```

---

## 🔧 Technology Stack

| Vrstva | Technologie | Verze |
|--------|-------------|-------|
| Frontend | Next.js + Shadcn/UI | 15.4+ |
| Styling | Tailwind CSS | 4.x |
| Backend | FastAPI + Python | 0.122+ |
| AI | LangGraph + Claude | 1.0.3 |
| Database | Supabase + pgvector | 1.25+ |
| Integrace | MCP Servers | latest |

---

## 📋 Roadmap

| Fáze | Týden | Cíl |
|------|-------|-----|
| **Smoke Test** | 1-2 | Validace hypotézy s 5 beta testery |
| **MVP** | 3-6 | PubMed + SÚKL + basic RAG |
| **Beta** | 7-10 | Guidelines + VZP + LangGraph routing |
| **Production** | 11-12 | Auth + monitoring + launch |

---

## 📊 Hodnocení dokumentace

### ✅ Silné stránky

| Dokument | Hodnocení | Poznámka |
|----------|-----------|----------|
| API Specification | ⭐⭐⭐⭐⭐ | Kompletní REST API, request/response, error codes |
| System Prompt | ⭐⭐⭐⭐⭐ | Modulární, bezpečnostní guardrails, příklady |
| Database Schema | ⭐⭐⭐⭐⭐ | 10 migrací, RLS, pgvector, funkce |
| Tech Stack | ⭐⭐⭐⭐⭐ | Context7 verified, production-ready kód |
| Data Sources | ⭐⭐⭐⭐ | 43 URL, validováno, peridicita aktualizací |

### 📝 Doporučení pro další fázi

1. **UI/UX Wireframes** — vizuální návrh rozhraní (Figma)
2. **Testing Strategy** — test cases, QA kritéria
3. **Deployment Guide** — CI/CD, env variables
4. **Security Audit** — GDPR checklist, penetrační testy

---

## 🏗️ Architektura

```
┌─────────────────────────────────────────────────────────┐
│                     FRONTEND                            │
│              Next.js 15 + Shadcn/UI                     │
└─────────────────────────┬───────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                     BACKEND                             │
│                    FastAPI                              │
│  ┌─────────────────────────────────────────────────┐   │
│  │              LangGraph Pipeline                  │   │
│  │  Query → Classify → Route → Retrieve → Generate │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────┬───────────────────────────────┘
                          │
          ┌───────────────┼───────────────┐
          ▼               ▼               ▼
    ┌──────────┐   ┌──────────┐   ┌──────────┐
    │  PubMed  │   │   SÚKL   │   │Guidelines│
    │   MCP    │   │   MCP    │   │   MCP    │
    └──────────┘   └──────────┘   └──────────┘
          │               │               │
          └───────────────┼───────────────┘
                          ▼
              ┌───────────────────────┐
              │       Supabase        │
              │  PostgreSQL+pgvector  │
              └───────────────────────┘
```

---

## 👥 Tým

| Role | Osoba |
|------|-------|
| Team Leader & AI Architect | Petr Sovadina |
| Product Manager | Miroslav Hutňan |
| AI Engineer | Martin Kostovčík |
| AI Developer | Juraj Dedič |

---

## 📞 Kontakt

**Projekt:** Czech MedAI  
**Organizace:** STAPRO  
**Status:** V aktivním vývoji

---

*Dokumentace aktualizována: 20.12.2025*
