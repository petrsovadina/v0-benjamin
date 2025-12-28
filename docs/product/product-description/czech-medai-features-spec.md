# Czech MedAI — Product Features Specification

**Projekt:** Czech MedAI (kódové označení: Benjamin)  
**Verze:** 1.0  
**Datum:** 12.12.2025  
**Status:** Draft

---

## 📋 Přehled Features

| ID | Feature | Priorita | Fáze | Status |
|----|---------|----------|------|--------|
| F-001 | QuickConsult | P0 | MVP | Planned |
| F-002 | Multi-Source RAG Pipeline | P0 | MVP | Planned |
| F-003 | Citation System | P0 | MVP | Planned |
| F-004 | Czech Localization | P0 | MVP | Planned |
| F-005 | VZP Integration | P1 | MVP | Planned |
| F-006 | DeepConsult | P2 | v2.0 | Backlog |
| F-007 | Drug Interaction Checker | P2 | v2.0 | Backlog |
| F-008 | EHR Browser Extension | P2 | v2.0 | Backlog |

---

## F-001: QuickConsult — Rychlé Klinické Dotazy

### Popis
Primární rozhraní pro zadávání klinických dotazů v přirozeném jazyce. Systém poskytuje stručné, přesné odpovědi s inline citacemi během několika sekund.

### User Stories

| ID | User Story | Priorita |
|----|------------|----------|
| US-001 | Jako praktický lékař chci zadat klinický dotaz v češtině, abych rychle získal odpověď s citacemi bez nutnosti prohledávat více zdrojů. | P0 |
| US-002 | Jako lékař na urgentním příjmu chci získat odpověď do 5 sekund, abych mohl rychle rozhodovat během akutní péče. | P0 |
| US-003 | Jako specialista chci vidět zdroje odpovědi, abych mohl ověřit informace před aplikací v praxi. | P0 |

### Funkční požadavky

| Req ID | Požadavek | Kritérium |
|--------|-----------|-----------|
| FR-001.1 | Textový input pro dotazy | Max 2000 znaků, podpora českých znaků |
| FR-001.2 | Odpověď ve strukturovaném formátu | 3-5 vět + inline citace [1][2][3] |
| FR-001.3 | Zobrazení zdrojů | Seznam referencí s PMID/DOI/SÚKL odkazy |
| FR-001.4 | Historie dotazů | Posledních 50 dotazů s možností opakování |
| FR-001.5 | Suggested questions | 3 související follow-up dotazy |

### UI/UX Specifikace

```
┌─────────────────────────────────────────────────────────┐
│  🔍 Zadejte klinický dotaz...                      [→]  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Odpověď:                                               │
│  Lorem ipsum dolor sit amet [1], consectetur            │
│  adipiscing elit [2]. Sed do eiusmod tempor [3].       │
│                                                         │
│  ────────────────────────────────────────────────────  │
│  📚 Zdroje:                                             │
│  [1] Smith et al. (2024) - PMID: 12345678              │
│  [2] SÚKL - Metformin SPC                              │
│  [3] ČDS Guidelines 2024                               │
│                                                         │
│  💡 Související dotazy:                                 │
│  • Jaké jsou kontraindikace metforminu?                │
│  • Dávkování u pacientů s renální insuficiencí?        │
│  • Alternativy při intoleranci?                        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Technická implementace

| Komponenta | Technologie | Popis |
|------------|-------------|-------|
| Frontend | Next.js + Shadcn/UI | Modal/popup interface |
| API Endpoint | FastAPI | `POST /api/v1/query` |
| LLM | Claude Sonnet 4.5 | Generování odpovědi |
| Orchestrace | LangGraph | Conditional routing |

### Acceptance Criteria

- [ ] Odpověď obsahuje minimálně 2 relevantní citace s PMID/DOI
- [ ] Latence odpovědi < 5 sekund pro 95% dotazů
- [ ] Odpověď je v češtině s korektní lékařskou terminologií
- [ ] Citace jsou klikatelné odkazy na původní zdroj
- [ ] UI je responzivní (desktop, tablet, mobile)

### Metriky úspěchu

| Metrika | Target | Měření |
|---------|--------|--------|
| Response Time (p95) | < 5s | APM monitoring |
| Citation Accuracy | > 90% | Manual audit |
| User Satisfaction | > 4.0/5 | In-app rating |
| Daily Active Queries | > 50/user | Analytics |

---

## F-002: Multi-Source RAG Pipeline

### Popis
Backend systém pro inteligentní vyhledávání a syntézu informací z více heterogenních zdrojů. Využívá conditional routing pro optimální výběr retrieval strategie podle typu dotazu.

### Architektura

```
                    ┌─────────────────┐
                    │   User Query    │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │    Classifier   │
                    │  (Query Type)   │
                    └────────┬────────┘
                             │
           ┌─────────────────┼─────────────────┐
           │                 │                 │
    ┌──────▼──────┐   ┌──────▼──────┐   ┌──────▼──────┐
    │  Drug Info  │   │  Guidelines │   │  Clinical   │
    │   Router    │   │   Router    │   │   Router    │
    └──────┬──────┘   └──────┬──────┘   └──────┬──────┘
           │                 │                 │
    ┌──────▼──────┐   ┌──────▼──────┐   ┌──────▼──────┐
    │    SÚKL     │   │  ČLS JEP    │   │   PubMed    │
    │  Retriever  │   │  Retriever  │   │  Retriever  │
    └──────┬──────┘   └──────┬──────┘   └──────┬──────┘
           │                 │                 │
           └─────────────────┼─────────────────┘
                             │
                    ┌────────▼────────┐
                    │   Re-ranker     │
                    │ (Cross-encoder) │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │   Generator     │
                    │ (Claude + Cit.) │
                    └─────────────────┘
```

### Query Types & Routing

| Query Type | Trigger Keywords | Primary Source | Secondary |
|------------|------------------|----------------|-----------|
| `drug_info` | lék, dávkování, kontraindikace, SPC | SÚKL | PubMed |
| `guidelines` | guidelines, doporučení, postup, léčba | ČLS JEP | ESC/ADA |
| `diagnosis` | diagnóza, symptomy, diferenciální | PubMed | Guidelines |
| `reimbursement` | úhrada, VZP, pojišťovna, cena | VZP/SÚKL | — |
| `interaction` | interakce, kombinace, kontraindikace | SÚKL | DrugBank |
| `general` | (default) | PubMed | All |

### Funkční požadavky

| Req ID | Požadavek | Kritérium |
|--------|-----------|-----------|
| FR-002.1 | Query classification | Accuracy > 95% na test setu |
| FR-002.2 | Multi-source retrieval | Paralelní dotazy, timeout 3s |
| FR-002.3 | Semantic search | Top-10 dokumentů, similarity > 0.7 |
| FR-002.4 | Re-ranking | Cross-encoder, top-3 relevance > 0.8 |
| FR-002.5 | Source attribution | 100% odpovědí s traceable sources |

### Retriever Specifications

#### SÚKL Retriever
```yaml
type: vector_store
database: supabase_pgvector
embedding_model: text-embedding-3-small
chunk_size: 512
overlap: 50
index: ivfflat
sources:
  - DLP (databáze léčivých přípravků)
  - SPC (souhrny údajů o přípravku)
  - PIL (příbalové informace)
update_frequency: weekly
```

#### PubMed Retriever
```yaml
type: api_hybrid
api: ncbi_e-utilities
search: semantic + keyword
max_results: 20
filters:
  - publication_date: last_10_years
  - language: [eng, cze]
  - article_type: [clinical_trial, meta_analysis, review]
cache_ttl: 24h
```

#### Guidelines Retriever
```yaml
type: vector_store
database: supabase_pgvector
sources:
  - cls_jep: České odborné společnosti
  - esc: European Society of Cardiology
  - ada: American Diabetes Association
chunk_size: 1024
overlap: 100
update_frequency: quarterly
```

### Acceptance Criteria

- [ ] Query classifier dosahuje > 95% accuracy
- [ ] Semantic search vrací top-10 relevantních dokumentů
- [ ] Re-ranking zajišťuje relevanci > 0.8 pro top-3 výsledky
- [ ] Paralelní retrieval z 3+ zdrojů < 3s
- [ ] Fallback strategie při výpadku zdroje

---

## F-003: Citation System

### Popis
Automatické generování inline citací s referencemi. Zajišťuje transparentnost a ověřitelnost každé odpovědi.

### Formát citací

#### Inline citace
```
Text odpovědi s tvrzením [1] a dalším faktem [2][3].
```

#### Reference list
```markdown
## Zdroje

[1] **Smith J, et al.** (2024) Title of the study. 
    Journal Name. PMID: 12345678
    🔗 https://pubmed.ncbi.nlm.nih.gov/12345678

[2] **SÚKL** - Metformin 500mg SPC
    Datum aktualizace: 2024-11-15
    🔗 https://www.sukl.cz/...

[3] **ČDS** - Doporučené postupy pro léčbu DM2 (2024)
    🔗 https://www.diab.cz/...
```

### Typy citací

| Typ | Prefix | Příklad |
|-----|--------|---------|
| PubMed | PMID | PMID: 12345678 |
| DOI | DOI | DOI: 10.1000/xyz123 |
| SÚKL | SÚKL | SÚKL-12345 |
| Guidelines | ČLS/ESC/ADA | ČDS-2024-DM2 |
| VZP | VZP | VZP-§15 |

### Funkční požadavky

| Req ID | Požadavek | Kritérium |
|--------|-----------|-----------|
| FR-003.1 | Inline citation generation | Každé faktické tvrzení má citaci |
| FR-003.2 | Reference formatting | Konzistentní formát dle typu zdroje |
| FR-003.3 | Clickable links | Všechny citace jsou klikatelné |
| FR-003.4 | Source verification | Link checker validuje dostupnost |
| FR-003.5 | Citation metadata | Autor, rok, titul, identifikátor |

### Acceptance Criteria

- [ ] 100% odpovědí obsahuje alespoň jednu citaci
- [ ] Citace jsou klikatelné odkazy na původní zdroj
- [ ] Formát citace je konzistentní a profesionální
- [ ] Broken links jsou detekovány a nahrazeny alternativou

---

## F-004: Czech Localization

### Popis
Plná podpora českého jazyka včetně lékařské terminologie, automatické překlady anglických zdrojů s uvedením originálu.

### Komponenty lokalizace

| Komponenta | Popis |
|------------|-------|
| UI Strings | Kompletní české rozhraní |
| Medical Terminology | Česká lékařská terminologie (MeSH CZ) |
| Abbreviations | Automatické vysvětlení zkratek |
| Translation Layer | Překlad anglických abstracts |
| Date/Number Format | České formátování |

### Terminologický slovník

```yaml
terminology_sources:
  - mesh_czech: MeSH české překlady
  - sukl_terminology: SÚKL terminologie
  - cls_glossary: ČLS JEP slovník
  
abbreviation_handling:
  first_use: "plný název (zkratka)"
  subsequent: "zkratka"
  
examples:
  - "diabetes mellitus 2. typu (DM2)" → "DM2"
  - "glomerulární filtrace (GFR)" → "GFR"
  - "akutní infarkt myokardu (AIM)" → "AIM"
```

### Translation Layer

```yaml
translation_config:
  source_detection: automatic
  target_language: cs
  preserve_original: true
  format: |
    [Překlad]: České znění
    [Originál]: English original
  
  excluded_from_translation:
    - proper_nouns
    - drug_names (use Czech registration)
    - study_names
    - acronyms
```

### Acceptance Criteria

- [ ] UI kompletně v češtině bez anglických fragmentů
- [ ] Lékařská terminologie odpovídá českým standardům
- [ ] Zkratky jsou vysvětleny při prvním použití
- [ ] Přeložené texty zachovávají odkaz na originál
- [ ] Podpora českých znaků (háčky, čárky)

---

## F-005: VZP Integration

### Popis
Zobrazení informací o úhradě léků a výkonů zdravotními pojišťovnami. Podmínky úhrady, omezení, preskripční limity.

### Data Sources

| Zdroj | Typ dat | Aktualizace |
|-------|---------|-------------|
| SÚKL LEK-13 | Ceny, úhrady, výdeje | Měsíčně |
| VZP číselníky | Výkony, body, omezení | Kvartálně |
| SÚKL přehledy | Preskripční omezení | Týdně |

### Zobrazované informace

```
┌─────────────────────────────────────────────────────────┐
│  💊 Metformin 500mg (SIOFOR)                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  💰 Úhrada VZP:                                         │
│  ├─ Základní úhrada: 45,50 Kč / 60 tbl                 │
│  ├─ Doplatek pacienta: 12,00 Kč                        │
│  └─ Maximální cena: 57,50 Kč                           │
│                                                         │
│  📋 Podmínky úhrady:                                    │
│  ├─ Indikační omezení: DM2 (E11)                       │
│  ├─ Preskripční omezení: Žádné                         │
│  └─ Množstevní limit: Bez omezení                      │
│                                                         │
│  ⚠️ Poznámky:                                           │
│  • Úhrada podmíněna diagnózou E11                      │
│  • Kombinace s jinými PAD bez omezení                  │
│                                                         │
│  📅 Platnost dat: 01.12.2025                           │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Funkční požadavky

| Req ID | Požadavek | Kritérium |
|--------|-----------|-----------|
| FR-005.1 | Drug price lookup | Cena + úhrada pro 90%+ běžných léků |
| FR-005.2 | Reimbursement conditions | Indikační omezení, preskripce |
| FR-005.3 | Patient copay calculation | Doplatek = cena - úhrada |
| FR-005.4 | Alternative suggestions | Generika, biosimilars |
| FR-005.5 | Data freshness indicator | Datum poslední aktualizace |

### Acceptance Criteria

- [ ] Zobrazení úhradových podmínek pro 90%+ běžných léků
- [ ] Data aktualizována minimálně měsíčně
- [ ] Jasné zobrazení doplatku pacienta
- [ ] Upozornění na preskripční omezení

---

## F-006: DeepConsult — Hloubková Analýza (v2.0)

### Popis
Rozšířený režim pro komplexní dotazy vyžadující hlubší analýzu, porovnání více zdrojů, syntézu guidelines.

### Klíčové funkce

| Funkce | Popis |
|--------|-------|
| Multi-source comparison | Porovnání CZ vs. mezinárodní guidelines |
| Evidence grading | GRADE hodnocení síly důkazů |
| Conflict resolution | Identifikace rozporů mezi zdroji |
| Extended reasoning | Chain-of-thought vysvětlení |
| Export | PDF report pro dokumentaci |

### UI Concept

```
┌─────────────────────────────────────────────────────────┐
│  🔬 DeepConsult                                         │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│                                                         │
│  📝 Dotaz:                                              │
│  "Optimální léčba DM2 u pacienta s CKD G3b"            │
│                                                         │
│  ⏳ Analyzuji... (15-30s)                               │
│  ├─ [✓] PubMed meta-analyses                           │
│  ├─ [✓] ČDS Guidelines 2024                            │
│  ├─ [✓] ADA Standards 2024                             │
│  ├─ [~] KDIGO Guidelines                               │
│  └─ [ ] SÚKL contraindications                         │
│                                                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  📊 Srovnání Guidelines:                                │
│  ┌──────────┬────────────┬────────────┐                │
│  │ Aspekt   │ ČDS 2024   │ ADA 2024   │                │
│  ├──────────┼────────────┼────────────┤                │
│  │ 1. volba │ Metformin* │ SGLT2i     │                │
│  │ eGFR <45 │ Redukce    │ Stop       │                │
│  │ ...      │ ...        │ ...        │                │
│  └──────────┴────────────┴────────────┘                │
│  * s úpravou dávky                                      │
│                                                         │
│  📈 Síla důkazů: ⭐⭐⭐⭐ (GRADE A)                       │
│                                                         │
│  [📄 Export PDF]  [📋 Kopírovat]  [🔄 Rozšířit]        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Acceptance Criteria (v2.0)

- [ ] Response time < 30s
- [ ] Minimálně 3 zdroje v analýze
- [ ] GRADE evidence rating
- [ ] Exportovatelný PDF report

---

## F-007: Drug Interaction Checker (v2.0)

### Popis
Kontrola lékových interakcí z SÚKL databáze a mezinárodních zdrojů (DrugBank).

### Funkce

| Funkce | Popis |
|--------|-------|
| Multi-drug input | Zadání seznamu léků pacienta |
| Interaction matrix | Vizualizace všech interakcí |
| Severity grading | Závažnost: mírná/střední/závažná/kontraindikace |
| Clinical relevance | Klinický dopad a doporučení |
| Alternative suggestions | Návrh alternativ bez interakce |

### Severity Levels

| Level | Barva | Akce |
|-------|-------|------|
| 🟢 Mírná | Zelená | Monitorovat |
| 🟡 Střední | Žlutá | Zvážit alternativu |
| 🟠 Závažná | Oranžová | Upravit dávkování |
| 🔴 Kontraindikace | Červená | Nekombinovat |

---

## F-008: EHR Browser Extension (v2.0)

### Popis
Browser extension pro integraci Czech MedAI přímo do existujících EHR/NIS systémů.

### Podporované systémy

| EHR Systém | Výrobce | Integrace |
|------------|---------|-----------|
| IKIS | ICZ | Overlay |
| Medicus | CGM | Overlay |
| STAPRO | STAPRO | Overlay |
| Galen | Galen | Overlay |

### Funkce

| Funkce | Popis |
|--------|-------|
| Context extraction | Automatické čtení diagnózy/léků z EHR |
| Floating widget | Plovoucí okno pro dotazy |
| Quick insert | Vložení odpovědi do EHR poznámky |
| Audit trail | Logování použití pro compliance |

### UI Concept

```
┌─────────────────────────────────────────┐
│ EHR SYSTÉM (IKIS)                       │
│ ─────────────────────────────────────── │
│ Pacient: Jan Novák (*1955)              │
│ Dg: E11.9, I10, E78.0                   │
│ Medikace: Metformin, Lisinopril, Ator.. │
│                                         │
│    ┌─────────────────────────┐          │
│    │ 🤖 Czech MedAI          │          │
│    │ ───────────────────────  │          │
│    │ Kontext: DM2, HTN, HLP  │          │
│    │                         │          │
│    │ 🔍 [Zadejte dotaz...]   │          │
│    │                         │          │
│    │ 💡 Doporučené:          │          │
│    │ • Cílová HbA1c?         │          │
│    │ • Kombinace léčby?      │          │
│    └─────────────────────────┘          │
│                                         │
└─────────────────────────────────────────┘
```

---

## 📊 Feature Prioritization Matrix

| Feature | Impact | Effort | Priority | Phase |
|---------|--------|--------|----------|-------|
| QuickConsult | 🔴 High | 🟡 Medium | P0 | MVP |
| RAG Pipeline | 🔴 High | 🔴 High | P0 | MVP |
| Citation System | 🔴 High | 🟢 Low | P0 | MVP |
| Czech Localization | 🔴 High | 🟡 Medium | P0 | MVP |
| VZP Integration | 🟡 Medium | 🟡 Medium | P1 | MVP |
| DeepConsult | 🟡 Medium | 🔴 High | P2 | v2.0 |
| Drug Interactions | 🟡 Medium | 🟡 Medium | P2 | v2.0 |
| EHR Extension | 🟢 Low | 🔴 High | P2 | v2.0 |

---

## 🎯 MVP Definition

### Included (Must Have)
- ✅ F-001: QuickConsult
- ✅ F-002: Multi-Source RAG Pipeline
- ✅ F-003: Citation System
- ✅ F-004: Czech Localization
- ✅ F-005: VZP Integration (basic)

### Excluded (v2.0+)
- ❌ F-006: DeepConsult
- ❌ F-007: Drug Interaction Checker
- ❌ F-008: EHR Browser Extension

### MVP Success Criteria
- [ ] 100 MAU po 3 měsících
- [ ] NPS > 40
- [ ] Response time < 5s (p95)
- [ ] Citation accuracy > 90%

---

*Dokument vytvořen: 12.12.2025*
