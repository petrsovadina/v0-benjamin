# Czech MedAI

## Klinický AI asistent pro české lékaře

---

## Co je Czech MedAI?

Czech MedAI je **inteligentní asistent**, který pomáhá českým lékařům rychle najít ověřené medicínské informace. Funguje jako zkušený kolega, který za vás prohledá stovky odborných zdrojů a během několika sekund vám podá stručnou odpověď s odkazy na původní studie.

---

## Jaký problém řešíme?

**Lékaři nemají čas hledat informace.**

- 📊 **30 % pracovní doby** tráví lékaři administrativou místo péče o pacienty
- 🔍 Vyhledání jedné informace vyžaduje otevřít **3–4 různé weby** (PubMed, SÚKL, guidelines)
- 🌍 Většina odborné literatury je **pouze v angličtině**
- ⏱️ Na jednoho pacienta je v průměru **15 minut** — není čas studovat nové studie

**Výsledek:** Frustrace, riziko chyb, vyhoření lékařů.

---

## Jak Czech MedAI funguje?

### 1. Zeptáte se česky
Napíšete svůj klinický dotaz přirozeným jazykem — stejně jako byste se zeptali kolegy.

> *„Jaká je první linie léčby hypertenze u pacienta s diabetem 2. typu?"*

### 2. AI prohledá důvěryhodné zdroje
Systém automaticky vyhledá relevantní informace ve:
- 🔬 **PubMed** — 36+ milionů vědeckých článků
- 💊 **SÚKL** — oficiální databáze léčiv v ČR
- 📋 **České guidelines** — doporučené postupy ČLS JEP
- 💰 **VZP** — informace o úhradách

### 3. Dostanete odpověď s citacemi
Za **méně než 5 sekund** obdržíte:
- ✅ Stručnou odpověď v češtině (3–5 vět)
- 📎 Inline citace s odkazy na původní zdroje [1][2][3]
- 🔗 Klikatelné odkazy na PubMed (PMID), SÚKL, guidelines

---

## Pro koho je Czech MedAI určen?

| Segment | Typický uživatel |
|---------|------------------|
| **Praktičtí lékaři** | Dr. Nováková, 25 pacientů denně, potřebuje rychlé odpovědi |
| **Specialisté** | MUDr. Svoboda, kardiolog, chce porovnat české a mezinárodní guidelines |
| **Nemocniční lékaři** | Dr. Kučera, urgentní příjem, potřebuje okamžité informace ve 3 ráno |

**Cílový trh:** ~50 000 lékařů v České republice

---

## Klíčové funkce

### 🚀 QuickConsult
Rychlé odpovědi na klinické dotazy do 5 sekund.

### 📚 Evidence-based
Každá odpověď obsahuje citace z primárních zdrojů — žádné vymyšlené informace.

### 🇨🇿 Plně v češtině
Česká lékařská terminologie, české guidelines, české úhradové podmínky.

### 💊 Informace o lécích
Přímý přístup k datům ze SÚKL — indikace, kontraindikace, interakce, úhrady VZP.

### 🔒 Bezpečné
Data v EU, GDPR compliant, ověření lékařské licence.

---

## Co Czech MedAI NENÍ

- ❌ **Nediagnostikuje** — neposkytuje diagnózy pacientů
- ❌ **Neordinuje léčbu** — nenahrazuje klinické rozhodnutí lékaře
- ❌ **Nenahrazuje EHR** — je doplňkem, ne náhradou nemocničních systémů
- ❌ **Není pro pacienty** — je určen výhradně pro zdravotnické profesionály

---

## Příklad použití

**Situace:** Dr. Nováková má pacienta s nově zjištěným diabetem 2. typu a hypertenzí. Potřebuje vědět, jaký antihypertenzivum zvolit.

**Dotaz v Czech MedAI:**
> „Jaké antihypertenzivum je první volbou u diabetika 2. typu?"

**Odpověď (za 4 sekundy):**
> U pacientů s diabetem 2. typu a hypertenzí jsou léky první volby **ACE inhibitory nebo sartany** [1][2], které kromě antihypertenzního účinku poskytují renoprotekci [3]. Dle českých guidelines ČDS je cílový TK < 130/80 mmHg [4]. Při intoleranci ACEi/ARB lze zvážit blokátory kalciových kanálů [2].
>
> **Citace:**
> [1] ESC Guidelines 2023 — PMID: 37622657
> [2] ČDS Doporučené postupy 2023
> [3] ADVANCE Trial — PMID: 17868116
> [4] ČKS Hypertenze guidelines 2022

---

## Technické pozadí

Czech MedAI využívá nejmodernější AI technologie:

- **Velký jazykový model (LLM)** — Claude od Anthropic pro generování odpovědí
- **RAG (Retrieval-Augmented Generation)** — kombinace vyhledávání a AI pro přesné odpovědi
- **Vektorová databáze** — rychlé sémantické vyhledávání v milionech dokumentů
- **MCP (Model Context Protocol)** — standardizované napojení na datové zdroje

---

## Časový plán

| Fáze | Období | Cíl |
|------|--------|-----|
| **Smoke Test** | Týden 1–2 | Ověření základní hypotézy s 5 beta testery |
| **MVP** | Týden 3–6 | Základní produkt s PubMed a SÚKL |
| **Beta** | Týden 7–12 | Rozšíření o guidelines, VZP, optimalizace |
| **Launch** | Q2 2025 | Veřejné spuštění pro české lékaře |

---

## Kontakt

**Projekt:** Czech MedAI (kódové označení: Benjamin)
**Autor:** Petr Sovadina
**Status:** V aktivním vývoji

---

*Czech MedAI — Váš AI kolega pro klinickou praxi* 🩺
