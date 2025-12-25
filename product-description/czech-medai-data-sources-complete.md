# Czech MedAI — Datové Zdroje & Technická Dokumentace

**Projekt:** Czech MedAI (kódové označení: Benjamin)  
**Verze:** 1.0  
**Datum:** 12.12.2025  
**Status:** Production-ready (všechny URL validovány)

---

## 📋 O Projektu

**Czech MedAI** je lokalizovaný AI-poháněný klinický asistent určený výhradně pro české zdravotnické profesionály. Poskytuje rychlé, přesné a ověřené odpovědi na klinické dotazy v češtině s důrazem na:

- **Transparentnost zdrojů** — inline citace, PMID/DOI odkazy
- **Lokalizaci** — česká lékařská terminologie, české guidelines, úhradové informace VZP
- **Evidence-based přístup** — každá odpověď obsahuje odkazy na primární zdroje
- **Integraci** — propojení českých (SÚKL, VZP, ČLS JEP) a mezinárodních zdrojů (PubMed, Cochrane)

**Cílový trh:** ~50 000 českých lékařů, zejména praktičtí lékaři v ambulantní péči

---

## 🔧 Technický Stack

| Vrstva | Technologie |
|--------|-------------|
| **Frontend** | Next.js, Shadcn/UI, TypeScript |
| **Backend** | FastAPI, LangGraph, LangChain, Langchain-DeepAgents |
| **Database** | Supabase (PostgreSQL + pgvector) + Supabase Auth |
| **LLM** | Claude Sonnet 4.5 (primary), OpenAI models (fallback) |
| **Infrastructure** | Vercel (frontend), Docker, Kubernetes |
| **Integrace** | MCP Servers pro PubMed, SÚKL a další klinické zdroje |

### RAG Architecture Flow
```
Query → Classification → Conditional Routing → Multi-Source Retrieval → Re-ranking → Generation + Citations
```

---

## 📚 VALIDOVANÉ DATOVÉ ZDROJE

> ⚠️ **Poznámka:** Všechny URL byly ověřeny 12.12.2025. Některé české zdroje změnily strukturu URL — níže jsou aktuální funkční adresy.

---

## 🇨🇿 1) SÚKL — Česká oficiální data o léčivech

**Primární zdroj pro léčiva v ČR**

### OpenData — CSV/ZIP datasety ke stažení a vektorizaci

| Dataset | URL | Popis |
|---------|-----|-------|
| Katalog otevřených dat | https://opendata.sukl.cz/?q=katalog-otevrenych-dat | Přehled všech dostupných datasetů |
| Databáze léčivých přípravků (DLP) | https://opendata.sukl.cz/?q=katalog/databaze-lecivych-pripravku-dlp | Kompletní seznam registrovaných léčiv |
| SPC — Souhrny údajů o přípravku | https://opendata.sukl.cz/?q=katalog/spc-souhrn-udaju-o-lecivem-pripravku-summary-product-characteristics | Odborné informace pro lékaře |
| PIL — Příbalové informace | https://opendata.sukl.cz/?q=katalog/pil-pribalove-informace-product-information-leaflet | Příbalové letáky pro pacienty |
| Obaly — Texty na obalu | https://opendata.sukl.cz/?q=katalog/obaly-texty-na-obalu | Informace z obalů léčiv |
| LEK-13 (výdeje, ceny, úhrady) | https://opendata.sukl.cz/?q=katalog/lek-13 | Měsíční data o výdejích a cenách |
| Seznam lékáren | https://opendata.sukl.cz/?q=katalog/seznam-lekaren | Registry lékáren v ČR |
| SPC/PIL týdenní změny | https://opendata.sukl.cz/?q=katalog/spc-pil-obaly-tydenni-zmeny | Týdenní aktualizace textů |

### Webové nástroje a aplikace

| Nástroj | URL | Popis |
|---------|-----|-------|
| Přehled léčiv (interaktivní) | https://prehledy.sukl.cz/prehled_leciv.html | Webový vyhledávač léčiv s filtry |
| Vyhledávání léčiv | https://www.sukl.cz/modules/medication/search.php | Základní vyhledávání na SÚKL |
| eRecept portál | https://www.epreskripce.cz | Informace o elektronické preskripci |

### 💡 Použití v projektu
→ **Core dataset** pro klinické odpovědi v ČR  
→ Léčiva, složení, indikace, kontraindikace, interakce, úhrady, preskripční omezení  
→ **Implementace:** Stáhnout CSV datasety, vektorizovat pro semantic search v Supabase pgvector

---

## 📊 2) ÚZIS ČR — Národní zdravotnické registry

**Zdroj epidemiologických dat a zdravotnických statistik**

### Národní zdravotní registry

| Registr | URL | Popis |
|---------|-----|-------|
| Přehled registrů | https://www.uzis.cz/index.php?pg=registry-sber-dat--narodni-zdravotni-registry | Kompletní seznam NZR |
| Národní onkologický registr (NOR) | https://www.uzis.cz/index.php?pg=registry-sber-dat--narodni-zdravotni-registry--narodni-onkologicky-registr | Data o nádorových onemocněních |
| Registr hospitalizovaných (NRHOSP) | https://www.uzis.cz/index.php?pg=registry-sber-dat--narodni-zdravotni-registry--narodni-registr-hospitalizovanych | Statistiky hospitalizací |
| Registr reprodukčního zdraví (NRRZ) | https://www.uzis.cz/index.php?pg=registry-sber-dat--narodni-zdravotni-registry--narodni-registr-reprodukcniho-zdravi | Perinatální data |
| Diabetologický registr | https://www.uzis.cz/index.php?pg=registry-sber-dat--narodni-zdravotni-registry--narodni-diabetologicky-registr | Epidemiologie diabetu |
| IS Infekční nemoci (ISIN) | https://www.uzis.cz/index.php?pg=registry-sber-dat--ochrana-verejneho-zdravi--informacni-system-infekcni-nemoci | Surveillance infekčních nemocí |

### Statistické výstupy

| Výstup | URL | Popis |
|--------|-----|-------|
| Souhrnné reporty | https://www.uzis.cz/index.php?pg=vystupy--souhrnne-reporty | Agregované zdravotnické statistiky |
| NZIP datový portál | https://www.nzip.cz | Národní zdravotnický informační portál |

### 💡 Použití v projektu
→ Incidence, prevalence, epidemiologie, demografie, hospitalizace  
→ **Evidence pro kontextové odpovědi** — když lékař potřebuje česká data  
→ **Implementace:** API integrace nebo periodický scraping reportů

---

## 🏛 3) MZ ČR — Standardy, doporučení, legislativa

**Závazné předpisy a klinické doporučené postupy**

| Zdroj | URL | Popis |
|-------|-----|-------|
| Klinické doporučené postupy | https://www.mzcr.cz/odbor-koncepci-a-legislativy/doporucene-postupy/ | Oficiální KDP schválené MZ |
| Zákon o zdravotním pojištění | https://www.zakonyprolidi.cz/cs/1997-48 | Zákon č. 48/1997 Sb. |

### 💡 Použití v projektu
→ Závazné předpisy, doporučené postupy, právní rámec, lokální specifika  
→ **Implementace:** PDF parsing + RAG indexace

---

## 🩺 4) České odborné společnosti — Lokální guidelines

**Klinické doporučené postupy specifické pro ČR — klíčová vrstva RAG**

| Společnost | Obor | URL |
|------------|------|-----|
| ČLS JEP | Umbrella organizace | https://www.cls.cz |
| Česká diabetologická společnost | Diabetologie | https://www.diab.cz/doporucene-postupy |
| Česká neurologická společnost | Neurologie | https://www.czech-neuro.cz |
| Česká onkologická společnost (Linkos) | Onkologie | https://www.linkos.cz/lekar-a-multidisciplinarni-tym/ |

> ⚠️ **Poznámka:** Některé weby (kardio-cz.cz, pneumologie.cz) mají nestabilní servery — implementovat retry logic.

### 💡 Použití v projektu
→ **Nejvyšší priorita** pro české lékaře — lokální standardy péče  
→ České guidelines mají přednost před mezinárodními  
→ **Implementace:** Scraping PDF guidelines, vektorizace, pravidelná aktualizace (kvartálně)

---

## 🌍 5) Mezinárodní klinické guidelines

**Komparace a fallback při absenci českých doporučení**

| Organizace | Obor | URL |
|------------|------|-----|
| ESC | Kardiologie (EU) | https://www.escardio.org/Guidelines |
| EASD | Diabetologie (EU) | https://easd.org/guidelines/ |
| ERS | Pneumologie (EU) | https://www.ersnet.org/guidelines/top-issues/ |
| IDSA | Infekční nemoci | https://www.idsociety.org/practice-guideline/ |
| WHO | Globální health | https://www.who.int/publications/who-guidelines |
| ADA | Diabetes (US) | https://professional.diabetes.org/content-page/practice-guidelines-resources |

### 💡 Použití v projektu
→ Komparace českých vs. mezinárodních postupů  
→ Klinická rozhodovací podpora **při absenci lokálních doporučení**  
→ Feature "DeepConsult" — porovnání guidelines  
→ **Implementace:** API integrace kde dostupné, jinak PDF parsing

---

## 📚 6) Evidence-based literatura — Studie, meta-analýzy

**Nejdůležitější vrstva pro evidence-based AI**

| Zdroj | Popis | URL |
|-------|-------|-----|
| PubMed | 36M+ biomedicínských článků | https://pubmed.ncbi.nlm.nih.gov |
| Europe PMC | Open access plné texty | https://europepmc.org |
| Cochrane | Systematic reviews, meta-analýzy | https://www.cochrane.org/evidence |
| ClinicalTrials.gov | Registr klinických studií | https://clinicaltrials.gov |
| NCBI | Biomedicínské databáze | https://www.ncbi.nlm.nih.gov |

### API pro real-time integraci

| API | Dokumentace | Popis |
|-----|-------------|-------|
| PubMed E-utilities | https://www.ncbi.nlm.nih.gov/books/NBK25501/ | REST API pro vyhledávání a stahování |
| Europe PMC REST API | https://europepmc.org/RestfulWebService | Open access články |

### 💡 Použití v projektu
→ **Primární zdroj citací** — každá odpověď musí obsahovat PMID/DOI  
→ Studie, důkazy, plné texty, meta-analýzy  
→ **Implementace:** MCP Server pro PubMed E-utilities, real-time semantic search

---

## 💊 7) Farmakologie — Klasifikace, interakce, dávkování

**Cross-walk mezi mezinárodními a českými názvy léčiv**

| Zdroj | Použití | URL |
|-------|---------|-----|
| WHO ATC/DDD | Klasifikace léčiv, definované denní dávky | https://www.who.int/tools/atc-ddd-toolkit |
| RxNorm | Standardizace názvů léčiv (US) | https://www.nlm.nih.gov/research/umls/rxnorm/index.html |
| DrugBank | Interakce, farmakologie, struktury | https://go.drugbank.com |

### 💡 Použití v projektu
→ Mapování mezi ATC kódy a českými názvy  
→ Kontrola interakcí (future feature)  
→ **Implementace:** Integrace s SÚKL DLP pro lokální kontext

---

## 🏥 8) České EHR systémy — Kontext pro integraci

**Znalost ekosystému pro budoucí browser extension**

| Systém | Výrobce | URL |
|--------|---------|-----|
| ICZ Group | ICZ | https://www.iczgroup.cz |
| CGM/Medicus | CGM | https://www.cgm.com/cz |

### 💡 Použití v projektu
→ EHR kontext pro budoucí integraci (F-008: Browser Extension)  
→ Audit trail, kontextové dotazy  
→ **Implementace:** Post-MVP feature

---

## 📘 9) Vzdělávací zdroje (doplňkové)

| Zdroj | URL | Popis |
|-------|-----|-------|
| LibreTexts Medicine | https://med.libretexts.org | Open educational resources |

---

## 🔧 Implementační Plán

### Fáze 0: Smoke Test (Týden 1-2)
- [ ] PubMed E-utilities integrace (MCP server)
- [ ] Direct Claude API s kontextem
- [ ] 5 beta testerů

### Fáze 1: MVP Foundation (Týden 3-6)
- [ ] SÚKL OpenData download + vektorizace (Supabase pgvector)
- [ ] Basic RAG pipeline s LangGraph
- [ ] Citation system (PMID/DOI)

### Fáze 2: Core Features (Týden 7-10)
- [ ] České guidelines indexace
- [ ] VZP úhradové podmínky
- [ ] Conditional routing dle typu dotazu

### Fáze 3: Production (Týden 11-12)
- [ ] Monitoring (Langfuse)
- [ ] Health check endpoint pro zdroje
- [ ] Beta launch

---

## 📅 Periodicita aktualizace dat

| Zdroj | Frekvence | Poznámka |
|-------|-----------|----------|
| SÚKL DLP | Měsíčně | Automatický download |
| SÚKL LEK-13 | Měsíčně | Ceny a úhrady |
| SPC/PIL změny | Týdně | Incremental update |
| PubMed | Real-time | API call |
| České guidelines | Kvartálně | Manuální review |
| Mezinárodní guidelines | Kvartálně | Při vydání nových verzí |

---

## 🎯 MCP Servery k implementaci

| MCP Server | Zdroj | Priorita |
|------------|-------|----------|
| `pubmed-mcp` | PubMed E-utilities | P0 (MVP) |
| `sukl-mcp` | SÚKL OpenData | P0 (MVP) |
| `guidelines-mcp` | ČLS JEP + mezinárodní | P1 |
| `vzp-mcp` | VZP úhrady | P1 |

---

*Dokument validován: 12.12.2025*  
*Všechny URL ověřeny a funkční*
