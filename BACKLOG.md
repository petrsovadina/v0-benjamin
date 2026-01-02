# 📋 Czech MedAI - Backlog

> Vygenerováno: 2. ledna 2026
> Stav: Aktivní
> Prioritizace: MoSCoW (Must/Should/Could/Won't)

---

## 🚨 EPIC 1: Kritické bezpečnostní opravy
**Priorita:** 🔴 MUST HAVE | **Sprint:** 1 | **Estimate:** 8 SP

### US-1.1: Povolit RLS na všech veřejných tabulkách
**Jako** administrátor systému  
**Chci** mít RLS povoleno na všech tabulkách  
**Abych** zabránil neoprávněnému přístupu k datům přes PostgREST

#### Úkoly:
- [ ] **T-1.1.1** Povolit RLS na `drug_pricing` + přidat SELECT policy pro authenticated
- [ ] **T-1.1.2** Povolit RLS na `drug_atc`, `drug_spc`, `drug_pil` + public read policies
- [ ] **T-1.1.3** Povolit RLS na `drug_packages`, `drug_chunks`, `drug_interactions`
- [ ] **T-1.1.4** Povolit RLS na `active_substances`, `price_history`
- [ ] **T-1.1.5** Povolit RLS na `vzp_medicines`, `documents`
- [ ] **T-1.1.6** Povolit RLS na `api_logs` (pouze admin read)
- [ ] **T-1.1.7** Povolit RLS na `data_sync_log`, `search_synonyms`
- [ ] **T-1.1.8** Přidat RLS policies na `feedback` tabulku

**Acceptance Criteria:**
- [ ] Všechny tabulky mají `ENABLE ROW LEVEL SECURITY`
- [ ] Supabase Security Advisor nehlásí žádné ERROR
- [ ] Testy potvrzují, že anon user nemůže číst citlivá data

---

### US-1.2: Přidat autentizaci na nechráněné API endpointy
**Jako** bezpečnostní auditor  
**Chci** všechny API endpointy chráněné autentizací  
**Abych** zabránil zneužití AI služeb neautorizovanými uživateli

#### Úkoly:
- [ ] **T-1.2.1** Přidat `Depends(get_current_user)` na `/api/v1/ai/epicrisis`
- [ ] **T-1.2.2** Přidat `Depends(get_current_user)` na `/api/v1/ai/translate`
- [ ] **T-1.2.3** Přidat `Depends(get_current_user)` na `/api/v1/ai/transcribe`
- [ ] **T-1.2.4** Přidat `Depends(get_current_user)` na `/api/v1/drugs/vzp-search`
- [ ] **T-1.2.5** Přidat `Depends(get_current_user)` na `/api/v1/query/stream`
- [ ] **T-1.2.6** Přidat `Depends(get_current_user)` na `/api/v1/admin/upload-guideline`
- [ ] **T-1.2.7** Aktualizovat OpenAPI dokumentaci

**Acceptance Criteria:**
- [ ] Všechny POST endpointy vyžadují Bearer token
- [ ] 401 Unauthorized při chybějícím/neplatném tokenu
- [ ] Swagger UI zobrazuje auth requirements

---

### US-1.3: Opravit databázové funkce (search_path)
**Jako** DBA  
**Chci** mít všechny funkce s fixed search_path  
**Abych** zabránil SQL injection přes search_path manipulation

#### Úkoly:
- [ ] **T-1.3.1** Opravit `update_updated_at_column` - SET search_path = public
- [ ] **T-1.3.2** Opravit `update_updated_at` - SET search_path = public
- [ ] **T-1.3.3** Opravit `search_drugs` - SET search_path = public
- [ ] **T-1.3.4** Opravit `normalize_drug_name` - SET search_path = public
- [ ] **T-1.3.5** Opravit `handle_new_user` - SET search_path = public

**Acceptance Criteria:**
- [ ] Supabase Advisor nehlásí WARN pro function_search_path_mutable
- [ ] Funkce fungují správně po opravě

---

## 🔧 EPIC 2: Sjednocení Frontend-Backend komunikace
**Priorita:** 🟠 SHOULD HAVE | **Sprint:** 1-2 | **Estimate:** 13 SP

### US-2.1: Implementovat konzistentní proxy pattern
**Jako** frontend developer  
**Chci** volat všechna API přes Next.js routes  
**Abych** měl jednotný vzor komunikace a skryl backend URL

#### Úkoly:
- [ ] **T-2.1.1** Upravit `ChatInterface` - volat `/api/chat` místo přímého backendu
- [ ] **T-2.1.2** Upravit `VzpSearchInterface` - volat `/api/vzp-search` 
- [ ] **T-2.1.3** Upravit `HistoryInterface` - volat `/api/history`
- [ ] **T-2.1.4** Vytvořit nový Next.js route `/api/vzp-search/route.ts`
- [ ] **T-2.1.5** Vytvořit nový Next.js route `/api/history/route.ts`
- [ ] **T-2.1.6** Aktualizovat `/api/chat/route.ts` pro správné předávání auth

**Acceptance Criteria:**
- [ ] Žádná komponenta nevolá backend přímo
- [ ] Všechna volání jdou přes `/api/*` routes
- [ ] Backend URL není viditelný v browser DevTools

---

### US-2.2: Předávat autentizaci přes proxy
**Jako** uživatel  
**Chci** být automaticky autentizován při API voláních  
**Abych** nemusel manuálně spravovat tokeny

#### Úkoly:
- [ ] **T-2.2.1** Upravit Next.js API routes pro získání session z cookies
- [ ] **T-2.2.2** Předávat Bearer token z Next.js serveru do backendu
- [ ] **T-2.2.3** Odstranit manuální získávání tokenu v komponentách
- [ ] **T-2.2.4** Implementovat refresh token handling v proxy

**Acceptance Criteria:**
- [ ] Komponenty nezískávají token přímo
- [ ] Auth je řešena na úrovni Next.js middleware/routes
- [ ] Token refresh funguje transparentně

---

### US-2.3: Omezit CORS v produkci
**Jako** security engineer  
**Chci** CORS omezený pouze na povolené domény  
**Abych** zabránil cross-origin útokům

#### Úkoly:
- [ ] **T-2.3.1** Aktualizovat `Settings.CORS_ORIGINS` na konkrétní domény
- [ ] **T-2.3.2** Přidat environment-specific CORS konfigurace
- [ ] **T-2.3.3** Testovat CORS v staging prostředí

**Acceptance Criteria:**
- [ ] Produkce nemá `allow_origins=["*"]`
- [ ] Pouze frontend doména je povolena
- [ ] Preflight requesty fungují správně

---

## ⚡ EPIC 3: Implementace Streamingu
**Priorita:** 🟠 SHOULD HAVE | **Sprint:** 2 | **Estimate:** 8 SP

### US-3.1: Využít streaming endpoint v ChatInterface
**Jako** uživatel  
**Chci** vidět odpověď AI postupně, jak je generována  
**Abych** nemusel čekat na celou odpověď

#### Úkoly:
- [ ] **T-3.1.1** Vytvořit `/api/chat/stream/route.ts` jako streaming proxy
- [ ] **T-3.1.2** Implementovat ReadableStream parsing v `ChatInterface`
- [ ] **T-3.1.3** Aktualizovat state management pro postupné přidávání textu
- [ ] **T-3.1.4** Přidat indikátor "píše..." během streamování
- [ ] **T-3.1.5** Implementovat abort controller pro zrušení streamu

**Acceptance Criteria:**
- [ ] Text se zobrazuje token-by-token
- [ ] Uživatel může zrušit generování
- [ ] Metadata (citace) se zobrazí na konci
- [ ] Error handling pro přerušené streamy

---

### US-3.2: Optimalizovat UX během streamování
**Jako** uživatel  
**Chci** intuitivní feedback během generování odpovědi  
**Abych** věděl, že systém pracuje

#### Úkoly:
- [ ] **T-3.2.1** Animovaný typing indicator
- [ ] **T-3.2.2** Progress indikátor pro dlouhé operace
- [ ] **T-3.2.3** Disable input během generování
- [ ] **T-3.2.4** "Stop generating" tlačítko

**Acceptance Criteria:**
- [ ] Jasný vizuální feedback během generování
- [ ] Možnost zastavit generování
- [ ] Responsivní UI i během streamování

---

## 🏗️ EPIC 4: Refaktoring Backend architektury
**Priorita:** 🟡 COULD HAVE | **Sprint:** 3 | **Estimate:** 13 SP

### US-4.1: Konsolidovat AI grafy
**Jako** backend developer  
**Chci** mít jeden konzistentní AI workflow systém  
**Abych** snáze udržoval a rozšiřoval AI logiku

#### Úkoly:
- [ ] **T-4.1.1** Vytvořit `backend/app/core/ai/` adresář
- [ ] **T-4.1.2** Sloučit `agent_graph.py` a `graph.py` do `clinical_graph.py`
- [ ] **T-4.1.3** Přesunout `epicrisis_graph.py` do `core/ai/`
- [ ] **T-4.1.4** Přesunout `translator_graph.py` do `core/ai/`
- [ ] **T-4.1.5** Aktualizovat importy v endpointech
- [ ] **T-4.1.6** Smazat staré soubory z root backendu
- [ ] **T-4.1.7** Aktualizovat testy

**Acceptance Criteria:**
- [ ] Žádné `*_graph.py` v root `backend/` adresáři
- [ ] Jednotný import pattern: `from backend.app.core.ai import ...`
- [ ] Všechny testy projdou

---

### US-4.2: Centralizovat konfiguraci
**Jako** DevOps engineer  
**Chci** mít jednu source of truth pro konfiguraci  
**Abych** snadno spravoval environment proměnné

#### Úkoly:
- [ ] **T-4.2.1** Odstranit `load_dotenv()` z jednotlivých modulů
- [ ] **T-4.2.2** Všechny env vars načítat pouze přes `Settings`
- [ ] **T-4.2.3** Přidat validaci povinných env vars při startu
- [ ] **T-4.2.4** Dokumentovat všechny env vars v `.env.example`

**Acceptance Criteria:**
- [ ] `load_dotenv` se volá pouze jednou v `config.py`
- [ ] Aplikace padá při startu, pokud chybí povinné vars
- [ ] `.env.example` je kompletní

---

### US-4.3: Vylepšit error handling
**Jako** uživatel  
**Chci** dostávat srozumitelné chybové hlášky  
**Abych** věděl, co se pokazilo a jak to opravit

#### Úkoly:
- [ ] **T-4.3.1** Vytvořit custom exception classes
- [ ] **T-4.3.2** Implementovat global exception handler
- [ ] **T-4.3.3** Strukturované error responses (error code, message, details)
- [ ] **T-4.3.4** Lokalizovat error messages do češtiny
- [ ] **T-4.3.5** Logovat errory do `api_logs` tabulky

**Acceptance Criteria:**
- [ ] Všechny errory mají jednotný formát
- [ ] 500 errory neodhalují interní detaily
- [ ] Uživatel vidí českou hlášku, ne stack trace

---

## 📊 EPIC 5: Monitoring a Observability
**Priorita:** 🟡 COULD HAVE | **Sprint:** 4 | **Estimate:** 8 SP

### US-5.1: Implementovat metriky
**Jako** SRE  
**Chci** sledovat klíčové metriky aplikace  
**Abych** mohl monitorovat zdraví systému

#### Úkoly:
- [ ] **T-5.1.1** Přidat Prometheus metriky endpoint
- [ ] **T-5.1.2** Měřit latenci API endpointů
- [ ] **T-5.1.3** Počítat úspěšné/neúspěšné requesty
- [ ] **T-5.1.4** Měřit token usage per user
- [ ] **T-5.1.5** Dashboard v Grafana/Supabase

**Acceptance Criteria:**
- [ ] `/metrics` endpoint vrací Prometheus formát
- [ ] P50, P95, P99 latence jsou měřeny
- [ ] Token usage je trackován

---

### US-5.2: Audit logging
**Jako** compliance officer  
**Chci** mít audit trail všech operací  
**Abych** mohl splnit regulatorní požadavky

#### Úkoly:
- [ ] **T-5.2.1** Logovat všechna API volání do `api_logs`
- [ ] **T-5.2.2** Zahrnout user_id, endpoint, payload hash, response_status
- [ ] **T-5.2.3** Implementovat log retention policy
- [ ] **T-5.2.4** Admin UI pro prohlížení logů

**Acceptance Criteria:**
- [ ] Každé API volání je zalogováno
- [ ] Logy jsou uchovávány 90 dní
- [ ] Admin může filtrovat a vyhledávat v logech

---

## 🎨 EPIC 6: UX Vylepšení
**Priorita:** 🟡 COULD HAVE | **Sprint:** 4-5 | **Estimate:** 13 SP

### US-6.1: Optimistické UI aktualizace
**Jako** uživatel  
**Chci** okamžitou zpětnou vazbu při akcích  
**Abych** měl pocit rychlé aplikace

#### Úkoly:
- [ ] **T-6.1.1** Okamžité zobrazení odeslané zprávy v chatu
- [ ] **T-6.1.2** Skeleton loading pro citace
- [ ] **T-6.1.3** Optimistický update pro historie

**Acceptance Criteria:**
- [ ] Zpráva se zobrazí okamžitě po odeslání
- [ ] Loading states jsou vizuálně přívětivé

---

### US-6.2: Offline podpora
**Jako** lékař v terénu  
**Chci** přístup k historii i offline  
**Abych** mohl prohlížet předchozí dotazy bez internetu

#### Úkoly:
- [ ] **T-6.2.1** Implementovat Service Worker
- [ ] **T-6.2.2** Cache pro historii dotazů
- [ ] **T-6.2.3** Offline banner/indikátor
- [ ] **T-6.2.4** Sync při obnovení spojení

**Acceptance Criteria:**
- [ ] Historie je dostupná offline
- [ ] Jasný indikátor offline stavu
- [ ] Automatická synchronizace při reconnect

---

## 📈 Prioritizovaný přehled

| Sprint | Epic | Story | SP | Status |
|--------|------|-------|----|----|
| **1** | E1 | US-1.1 RLS tabulky | 3 | 🔴 TODO |
| **1** | E1 | US-1.2 Auth endpointy | 3 | 🔴 TODO |
| **1** | E1 | US-1.3 DB funkce | 2 | 🔴 TODO |
| **1-2** | E2 | US-2.1 Proxy pattern | 5 | 🟡 TODO |
| **1-2** | E2 | US-2.2 Auth proxy | 5 | 🟡 TODO |
| **1-2** | E2 | US-2.3 CORS | 3 | 🟡 TODO |
| **2** | E3 | US-3.1 Streaming | 5 | 🟡 TODO |
| **2** | E3 | US-3.2 UX streaming | 3 | 🟡 TODO |
| **3** | E4 | US-4.1 AI grafy | 5 | ⚪ TODO |
| **3** | E4 | US-4.2 Config | 3 | ⚪ TODO |
| **3** | E4 | US-4.3 Errors | 5 | ⚪ TODO |
| **4** | E5 | US-5.1 Metriky | 5 | ⚪ TODO |
| **4** | E5 | US-5.2 Audit | 3 | ⚪ TODO |
| **4-5** | E6 | US-6.1 Optimistic UI | 5 | ⚪ TODO |
| **4-5** | E6 | US-6.2 Offline | 8 | ⚪ TODO |

**Celkem:** ~63 Story Points

---

## 🏃 Sprint Planning

### Sprint 1 (Týden 1-2)
**Cíl:** Kritické bezpečnostní opravy + začátek proxy pattern
- US-1.1, US-1.2, US-1.3
- US-2.1 (částečně)
**Kapacita:** 13 SP

### Sprint 2 (Týden 3-4)
**Cíl:** Dokončit komunikaci + streaming
- US-2.1 (dokončení), US-2.2, US-2.3
- US-3.1, US-3.2
**Kapacita:** 16 SP

### Sprint 3 (Týden 5-6)
**Cíl:** Backend refaktoring
- US-4.1, US-4.2, US-4.3
**Kapacita:** 13 SP

### Sprint 4-5 (Týden 7-10)
**Cíl:** Monitoring a UX
- US-5.1, US-5.2
- US-6.1, US-6.2
**Kapacita:** 21 SP

---

## 📝 Definition of Done

- [ ] Kód prošel code review
- [ ] Unit testy pokrývají novou funkcionalitu
- [ ] Dokumentace aktualizována
- [ ] Žádné nové Supabase Security Advisor warnings
- [ ] Merge do main branch
- [ ] Deployment do staging
- [ ] QA sign-off

---

## 🔗 Související dokumenty

- [CLAUDE.md](CLAUDE.md) - AI agent instrukce
- [README.md](README.md) - Projektová dokumentace
- [ROADMAP.md](ROADMAP.md) - Dlouhodobá vize
- [docs/architecture/](docs/architecture/) - Architektonická dokumentace
