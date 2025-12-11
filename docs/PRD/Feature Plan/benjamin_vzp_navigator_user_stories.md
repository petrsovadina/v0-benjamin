# Benjamin - VZP Navigator User Stories & Acceptance Criteria

**Feature:** VZP Navigator - Automatická kontrola VZP úhrad léků

**Epic:** Fáze 2 - Škálování & Differentiation

**Priority:** MUST HAVE

**Target Users:**
- Primary: Dr. Jana Nováková (Praktická lékařka) - 70% use cases
- Secondary: Dr. Petr Svoboda (Kardiolog) - 20% use cases
- Tertiary: Dr. Martin Kučera (Urgentní příjem) - 10% use cases

---

## Epic: VZP Navigator Implementation

**Epic Goal:** Poskytnout lékařům automatický přístup k VZP úhradovým informacím přímo v Benjamin Chat interface, čímž eliminujeme potřebu manuální kontroly VZP web (5+ minut → 0 minut).

**Success Criteria:**
- 70% lékařů používá VZP Navigator ≥5x týdně
- User satisfaction: "Pomohlo mi VZP Navigator?" → 85%+ ANO
- Time savings: Průměrná úspora 5 minut na dotaz
- Accuracy: 95%+ přesnost VZP dat vs oficiální VZP web

---

## User Story 1: Základní Kontrola VZP Hrazení Léku

**As a** praktická lékařka (Dr. Nováková)
**I want to** okamžitě vidět, zda je lék hrazený VZP přímo v Benjamin odpovědi
**So that** nemusím otevírat VZP web a zdržovat pacienta během vyšetření

### Scénář 1.1: Standardní Hrazený Lék

**Given** že jsem přihlášená v Benjamin
**And** mám otevřený Chat interface
**When** zadám dotaz "Je empagliflozin hrazený VZP?"
**Then** Benjamin zobrazí odpověď s inline VZP Info Card obsahující:
  - ✅ Status hrazení: "Standardní úhrada VZP"
  - Doplatek pacienta: "30 Kč"
  - Indikace: "Diabetes mellitus 2. typu (E11)"
  - Podmínky: "HbA1c ≥ 53 mmol/mol po selhání metforminu"
  - Kód omezení: "H013 (Endokrinologie/Internista)"
  - Datum aktualizace: "15.1.2025"
  - Link na VZP zdroj

**And** VZP Info Card se zobrazí do 2 sekund od odeslání dotazu
**And** data jsou aktuální (ne starší než 90 dní)

### Acceptance Criteria

**✅ Funkční požadavky:**
- [ ] VZP Info Card se zobrazí automaticky, když uživatel zmiňuje lék + "hrazený" nebo "VZP" nebo "cena"
- [ ] Card obsahuje všech 7 klíčových datových polí (status, doplatek, indikace, podmínky, kód, aktualizace, zdroj)
- [ ] Doplatek je zobrazen v Kč (celé číslo, např. "30 Kč")
- [ ] Status hrazení má vizuální indikátor (✅ zelená pro hrazeno, ❌ červená pro nehrazeno)
- [ ] Link na VZP zdroj je klikatelný a otevře se v nové záložce

**✅ Technické požadavky:**
- [ ] MCP tool `get_vzp_reimbursement` vrací data do 2 sekund (95th percentile)
- [ ] Data jsou fetchována z Supabase tabulky `vzp_reimbursement`
- [ ] VZP data nejsou starší než 90 dní (warning pokud starší)
- [ ] API call je cachovaný (cache hit rate >40% pro top 100 léků)

**✅ UX požadavky:**
- [ ] VZP Info Card má jasně oddělené sekce (Hrazení, Doplatek, Kódy)
- [ ] Font size minimálně 14px (čitelnost)
- [ ] Card má border a subtle shadow (visual hierarchy)
- [ ] Loading state: "⏳ Kontroluji VZP databázi..." během fetchování

**✅ Edge cases:**
- [ ] Pokud VZP data nejsou dostupná → zobrazit error state s tlačítkem "🔗 Otevřít VZP web"
- [ ] Pokud lék není nalezen → zobrazit "❌ Lék nenalezen v VZP databázi" + suggestions
- [ ] Pokud data starší než 90 dní → zobrazit warning "⚠️ Data mohou být zastaralá"

---

## User Story 2: Off-Label Použití Léku (Žádost o IU)

**As a** kardiolog (Dr. Svoboda)
**I want to** vidět, že lék není hrazen pro mou off-label indikaci a dostat návod na žádost o IU
**So that** vím, jak postupovat při předepisování off-label a ušetřím čas s administracou

### Scénář 2.1: Off-Label Lék s IU Možností

**Given** že jsem přihlášený v Benjamin
**When** zadám dotaz "Je empagliflozin hrazený pro srdeční selhání?"
**Then** Benjamin zobrazí VZP Info Card s:
  - ⚠️ Status: "OFF-LABEL POUŽITÍ"
  - Indikace: "Srdeční selhání (I50.x)"
  - VZP hrazení: "❌ NE (registrován pouze pro T2DM)"
  - Doplatek pacienta: "~1,200 Kč/měsíc (plná cena)"
  - 💡 Možnosti: "Žádost o individuální úhradu (IU)"
  - Evidence: "EMPEROR-Reduced (2020), ESC guidelines 2021"
  - Success rate IU: "~60%"
  - Alternativa: "Dapagliflozin (Forxiga) - ✅ Hrazeno VZP pro srdeční selhání"

**And** Zobrazí se tlačítko "[📄 Vygenerovat žádost o IU]"
**And** Alternativní hrazený lék je zvýrazněný (call to action)

### Scénář 2.2: Kliknutí na "Vygenerovat žádost o IU"

**Given** že vidím VZP Info Card s off-label lékem
**When** kliknu na tlačítko "[📄 Vygenerovat žádost o IU]"
**Then** Benjamin zobrazí expandable section s:
  - Formulář VZP č. 12345 (link ke stažení)
  - Potřebná dokumentace (lékařská zpráva, literatura)
  - Doporučené odůvodnění (pre-filled template pro empagliflozin + I50)
  - Čekací doba: "Standardní 30 dnů, Urgentní 7 dnů"
  - Tlačítko "[📋 Kopírovat template žádosti]"

**And** Template obsahuje:
  - Placeholder pro pacientovi data
  - Odůvodnění založené na EMPEROR-Reduced studii
  - Citace relevantních guidelines

### Acceptance Criteria

**✅ Funkční požadavky:**
- [ ] AI detekuje off-label použití (ICD-10 kód není v `indication_icd10` array)
- [ ] VZP Info Card zobrazí ⚠️ OFF-LABEL status (žlutá barva)
- [ ] Doplatek je nastaven na `full_price_czk` (plná cena bez VZP úhrady)
- [ ] Success rate IU je zobrazen (pokud dostupný v databázi)
- [ ] Alternativní hrazené léky jsou navrženy (stejná ATC skupina)

**✅ Technické požadavky:**
- [ ] MCP tool `get_vzp_reimbursement` přijímá parametr `indication_icd10`
- [ ] Pokud `indication_icd10` not in `drug.indication_icd10` → vrátit off-label response
- [ ] Query alternativních léků filtruje podle ATC kódu (první 5 znaků)
- [ ] Alternative drugs jsou seřazené podle `copay_czk` (nejlevnější první)

**✅ UX požadavky:**
- [ ] Tlačítko "[📄 Vygenerovat žádost o IU]" je primary CTA (fialová barva)
- [ ] Expandable section se otevře plynule (animace 200ms)
- [ ] Template žádosti je formátovaný markdown (čitelný)
- [ ] "[📋 Kopírovat template]" kopíruje text do clipboardu + zobrazí "✅ Zkopírováno"

**✅ Edge cases:**
- [ ] Pokud alternativa neexistuje → zobrazit "⚠️ Žádné hrazené alternativy v této ATC skupině"
- [ ] Pokud IU success rate není dostupný → nezobrazovat řádek (ne "N/A")

---

## User Story 3: Cenové Srovnání Alternativních Léků

**As a** praktická lékařka (Dr. Nováková)
**I want to** porovnat ceny alternativních léků ve stejné skupině
**So that** mohu předepsat nejlevnější variantu pro pacienta s omezenými finančními prostředky

### Scénář 3.1: Automatické Zobrazení Alternativ

**Given** že jsem zadala dotaz "Jaký SGLT2 inhibitor je nejlevnější pro pacienta?"
**When** Benjamin vygeneruje odpověď
**Then** VZP Info Card zobrazí tabulku s cenami alternativních léků:

```
💰 CENOVÉ SROVNÁNÍ - SGLT2 INHIBITORY

┌──────────────┬──────────┬───────────┬────────────┐
│ Lék          │ Doplatek │ Měsíční   │ Hrazení    │
│              │ pacienta │ náklady   │ VZP        │
├──────────────┼──────────┼───────────┼────────────┤
│ Empagliflozin│ 30 Kč    │ 850 Kč    │ ✅ Ano     │
│ Dapagliflozin│ 50 Kč    │ 920 Kč    │ ✅ Ano     │
│ Canagliflozin│ 45 Kč    │ 890 Kč    │ ✅ Ano     │
│ Ertugliflozin│ 120 Kč   │ 1,200 Kč  │ ⚠️ Omezeno │
└──────────────┴──────────┴───────────┴────────────┘

💡 Doporučení: Empagliflozin - nejnižší doplatek + prokázaný CV benefit
```

**And** Tabulka je seřazená podle "Doplatek pacienta" (vzestupně)
**And** AI poskytne doporučení založené na ceně + clinical evidence

### Scénář 3.2: Explicitní Request na Price Comparison

**Given** že jsem zadala dotaz "Je empagliflozin hrazený VZP?"
**And** Benjamin zobrazil VZP Info Card s doplátkem 30 Kč
**When** kliknu na tlačítko "[💰 Srovnat ceny alternativ]"
**Then** Benjamin zobrazí price comparison tabulku (viz Scénář 3.1)

### Acceptance Criteria

**✅ Funkční požadavky:**
- [ ] AI automaticky detekuje request na price comparison (keywords: "nejlevnější", "cena", "srovnání", "alternativy")
- [ ] MCP tool `get_vzp_reimbursement` je volán s parametrem `compare_alternatives=true`
- [ ] Tabulka obsahuje minimálně 3 alternativní léky (pokud dostupné)
- [ ] Alternativy jsou ze stejné ATC skupiny (první 5 znaků ATC kódu)
- [ ] Tabulka je seřazená podle `copay_czk` (vzestupně)

**✅ Technické požadavky:**
- [ ] Query alternativních léků: `SELECT * FROM vzp_reimbursement WHERE atc_code LIKE 'A10BK%' LIMIT 5`
- [ ] Price comparison data jsou cachovaná (same TTL as VZP data: 30 dní)
- [ ] Tabulka se renderuje do 3 sekund (včetně alternativ lookup)

**✅ UX požadavky:**
- [ ] Tabulka má jasně definované sloupce (Lék, Doplatek, Měsíční náklady, Hrazení)
- [ ] Nejlevnější lék je zvýrazněný (zelený border nebo background)
- [ ] AI doporučení je zobrazeno pod tabulkou (💡 icon + text)
- [ ] Každý řádek má hover effect (subtle background change)

**✅ Edge cases:**
- [ ] Pokud nejsou dostupné žádné alternativy → zobrazit "⚠️ Žádné alternativy v této ATC skupině"
- [ ] Pokud alternativy mají stejnou cenu → seřadit podle `reimbursement_percentage`

---

## User Story 4: Kopírování Prescribing Codes pro E-recept

**As a** praktická lékařka (Dr. Nováková)
**I want to** zkopírovat prescribing codes (kód omezení, ICD-10) jedním kliknutím
**So that** mohu rychle vyplnit e-recept bez ručního přepisování

### Scénář 4.1: Kopírování Kódů do Clipboardu

**Given** že vidím VZP Info Card s empagliflozinem
**When** kliknu na tlačítko "[📋 Kopírovat kódy]"
**Then** následující text je zkopírován do clipboardu:

```
Kód omezení: H013
ICD-10: E11
SÚKL kód: 0123456
Dávkování: 10mg 1x denně
```

**And** Zobrazí se toast notification "✅ Zkopírováno do schránky"
**And** Toast zmizí po 2 sekundách

### Acceptance Criteria

**✅ Funkční požadavky:**
- [ ] Tlačítko "[📋 Kopírovat kódy]" je viditelné v každé VZP Info Card
- [ ] Kliknutí spustí clipboard API (`navigator.clipboard.writeText()`)
- [ ] Text obsahuje všechny prescribing codes: kód omezení, ICD-10, SÚKL kód, dávkování
- [ ] Toast notification se zobrazí po úspěšném kopírování

**✅ Technické požadavky:**
- [ ] Clipboard API je podporován v Chrome, Firefox, Safari (fallback pro starší prohlížeče)
- [ ] Text je formátovaný plain text (ne HTML)
- [ ] Kopírování funguje i v Chrome Extension (popup + side panel)

**✅ UX požadavky:**
- [ ] Toast notification je viditelný (zelená barva, ✅ ikona)
- [ ] Toast je umístěný v top-right rohu (ne překrývat chat)
- [ ] Fade out animace (200ms)

**✅ Edge cases:**
- [ ] Pokud clipboard API není podporován → zobrazit modal s textem k manuálnímu kopírování
- [ ] Pokud některý kód není dostupný (např. SÚKL kód missing) → vynechat z kopírovaného textu

---

## User Story 5: Detekce Léku Neregistrovaného v ČR

**As a** kardiolog (Dr. Svoboda)
**I want to** okamžitě vědět, že lék není registrován v ČR a vidět očekávané datum registrace
**So that** neztratím čas hledáním léku v SÚKL databázi

### Scénář 5.1: Lék Není Registrován v ČR

**Given** že jsem zadal dotaz "Je tirzepatide hrazený v ČR?"
**When** Benjamin vyhledá lék v VZP databázi
**And** Lék není nalezen (ne v `vzp_reimbursement` tabulce)
**Then** Benjamin zobrazí VZP Info Card s:
  - ❌ Status: "NENÍ REGISTROVÁN V ČR"
  - SÚKL registrace: "❌ NE (k 15.1.2025)"
  - EMA approval: "✅ ANO (2022)"
  - Očekávaná registrace ČR: "Q3 2025 (předběžné)"
  - 💡 Aktuální situace: "Lék není dostupný v českých lékárnách"
  - Import ze zahraničí: "Možný, ale bez VZP úhrady (~8,000 Kč/měsíc)"
  - 🔄 Hrazené alternativy: "Semaglutide (Ozempic) - ✅ Hrazeno VZP, doplatek 150 Kč"

**And** Zobrazí se tlačítko "[🔔 Upozornit na registraci]"

### Scénář 5.2: Notifikace při Registraci Léku

**Given** že jsem klikl na "[🔔 Upozornit na registraci]"
**When** Benjamin zaznamená mou preferenci
**Then** Dostanu email/in-app notifikaci, jakmile se lék objeví v VZP databázi (měsíční check)

### Acceptance Criteria

**✅ Funkční požadavky:**
- [ ] MCP tool vrací `status: "not_found"` pokud lék není v `vzp_reimbursement` tabulce
- [ ] AI poskytne kontext: EMA approval, očekávaná registrace (pokud známá)
- [ ] Navrhne hrazené alternativy (stejná terapeutická skupina, ne nutně stejný ATC)
- [ ] Tlačítko "[🔔 Upozornit na registraci]" ukládá user preference do `drug_registration_alerts` tabulky

**✅ Technické požadavky:**
- [ ] Query SÚKL API pro ověření registrace (fallback pokud VZP data missing)
- [ ] Měsíční cron job kontroluje nové léky v VZP databázi a posílá notifikace
- [ ] Email notifikace obsahuje: název léku, datum registrace, VZP status, link do Benjamin

**✅ UX požadavky:**
- [ ] VZP Info Card má červenou barvu pro ❌ NENÍ REGISTROVÁN status
- [ ] Alternativy jsou zobrazeny pod hlavní card (ne inline)
- [ ] Tlačítko "[🔔 Upozornit]" změní text na "✅ Budu upozorněn" po kliknutí

**✅ Edge cases:**
- [ ] Pokud lék není registrován ani v EMA → zobrazit "⚠️ Lék není schválený v EU"
- [ ] Pokud očekávané datum registrace není známé → nezobrazovat řádek

---

## User Story 6: Zobrazení VZP Dat pro Více Léků Současně

**As a** praktická lékařka (Dr. Nováková)
**I want to** porovnat VZP hrazení pro 2-3 léky současně v jedné odpovědi
**So that** mohu rychle rozhodnout mezi alternativami bez opakovaných dotazů

### Scénář 6.1: Porovnání Dvou Léků

**Given** že jsem zadala dotaz "Empagliflozin vs dapagliflozin - který je lepší pro pacienta?"
**When** Benjamin analyzuje dotaz
**And** Detekuje 2 léky
**Then** Zobrazí side-by-side VZP Info Cards:

```
┌──────────────────────────┬──────────────────────────┐
│ 💊 Empagliflozin         │ 💊 Dapagliflozin         │
├──────────────────────────┼──────────────────────────┤
│ ✅ Hrazeno               │ ✅ Hrazeno               │
│ Doplatek: 30 Kč          │ Doplatek: 50 Kč          │
│ Kód: H013                │ Kód: H013                │
│                          │                          │
│ [Detail ▼]              │ [Detail ▼]              │
└──────────────────────────┴──────────────────────────┘

💡 Empagliflozin je levnější pro pacienta (20 Kč rozdíl/měsíc)
```

**And** Každá card je klikatelná pro zobrazení full detail
**And** AI poskytne doporučení (💡) založené na ceně + clinical evidence

### Acceptance Criteria

**✅ Funkční požadavky:**
- [ ] AI detekuje multiple drugs v user query (regex: `\w+ vs \w+` nebo `\w+ nebo \w+`)
- [ ] MCP tool je volán paralelně pro každý lék (max 3 současně)
- [ ] VZP Info Cards jsou zobrazeny side-by-side (desktop) nebo stacked (mobile)
- [ ] Comparison summary (💡) je generován AI na základě VZP dat

**✅ Technické požadavky:**
- [ ] Parallel MCP tool calls (async/await Promise.all)
- [ ] Response time <3 sekundy pro 2 léky, <5 sekund pro 3 léky
- [ ] Each card může být independently expanded (collapsed by default)

**✅ UX požadavky:**
- [ ] Side-by-side layout pouze na desktop (>768px width)
- [ ] Mobile/tablet: Vertical stack s swipe gesture
- [ ] Highlight rozdíly (např. zelená pro levnější, červená pro dražší)

**✅ Edge cases:**
- [ ] Pokud 1 lék není nalezen → zobrazit error card + funkční card pro druhý lék
- [ ] Pokud oba léky nejsou nalezeny → zobrazit standard "not found" error

---

## User Story 7: Warning pro Stará VZP Data

**As a** lékař (libovolná persona)
**I want to** vidět varování, pokud jsou VZP data starší než 90 dní
**So that** vím, že by měl ověřit aktuální status na VZP web

### Scénář 7.1: Data Starší než 90 Dní

**Given** že VZP databáze nebyla aktualizována 95 dní
**When** Benjamin zobrazí VZP Info Card
**Then** Na vrcholu card je zobrazeno varování:

```
⚠️ Upozornění: Data VZP starší než 90 dní (poslední aktualizace: 15.10.2024)
Doporučujeme ověřit aktuální status na VZP web.
[🔗 Otevřít VZP Seznam LP]
```

**And** Varování má žlutou barvu (warning state)
**And** Link otevře VZP web v nové záložce

### Acceptance Criteria

**✅ Funkční požadavky:**
- [ ] Check `last_updated` timestamp v každém VZP response
- [ ] Pokud `(NOW() - last_updated) > 90 days` → zobrazit warning banner
- [ ] Link na VZP web: `https://www.vzp.cz/poskytovatele/ciselniky/`

**✅ Technické požadavky:**
- [ ] Date calculation v MCP tool response (`data_age_days`)
- [ ] Frontend checks `data_age_days` a renderuje warning pokud >90

**✅ UX požadavky:**
- [ ] Warning banner má žlutou barvu (#FCD34D) + ⚠️ ikona
- [ ] Banner je umístěný nahoře v VZP Info Card (ne na spodu)
- [ ] Link má hover effect (underline + cursor pointer)

---

## Non-Functional Requirements

### Performance
- **Response Time:** 95th percentile <2 sekundy (single drug query)
- **Cache Hit Rate:** >40% pro top 100 léků (měsíčně)
- **Database Query:** <100ms pro single drug lookup (indexed)
- **Concurrent Users:** Podpora 100 concurrent queries bez degradace

### Reliability
- **Uptime:** 99.5% (max 3.6 hodin downtime měsíčně)
- **Data Freshness:** VZP data aktualizovaná do 48 hodin po VZP publikaci
- **Error Rate:** <0.1% API errors (DRUG_NOT_FOUND excluded)

### Accessibility
- **WCAG 2.1 Level AA:** Splňuje accessibility standardy
- **Keyboard Navigation:** Všechny interaktivní prvky dostupné via Tab + Enter
- **Screen Reader:** ARIA labels pro VZP status, doplatek, alternativy
- **High Contrast Mode:** VZP status indicators mají ikony (not just color)

### Security
- **GDPR Compliance:** Žádná PII data v VZP databázi
- **Rate Limiting:** Max 100 VZP queries per user per day
- **SQL Injection:** Parametrized queries, no string concatenation
- **XSS Protection:** Sanitize drug names před renderováním

---

## Testing Checklist

### Unit Tests
- [ ] MCP tool `get_vzp_reimbursement()` vrací správná data pro standard drug
- [ ] MCP tool `get_vzp_reimbursement()` vrací off-label response pro neregistrovanou indikaci
- [ ] MCP tool `get_vzp_reimbursement()` vrací not_found pro nonexistent drug
- [ ] Normalize drug name: "Empagliflozin" → "empagliflozin"
- [ ] Date freshness check: `last_updated` > 90 days → warning

### Integration Tests
- [ ] End-to-end: User query → MCP call → VZP Info Card render
- [ ] Cache hit: Second query pro same drug vrací cached data
- [ ] Parallel queries: 2 léky současně renderují side-by-side
- [ ] Error handling: VZP API down → fallback na cached data

### E2E Tests (Cypress)
- [ ] User scenario: "Je empagliflozin hrazený VZP?" → VZP Card zobrazena
- [ ] User scenario: Click "[📋 Kopírovat kódy]" → clipboard obsahuje správný text
- [ ] User scenario: Click "[💰 Srovnat alternativy]" → tabulka se zobrazí
- [ ] User scenario: Off-label drug → tlačítko "[📄 Vygenerovat IU]" je visible

### User Acceptance Testing (UAT)
- [ ] 5 beta lékařů testuje VZP Navigator 1 týden
- [ ] Feedback survey: "Ušetřil vám VZP Navigator čas?" → >80% ANO
- [ ] Bug reports: <5 critical bugs nalezených během UAT

---

## Definition of Done

**Feature je považována za DONE když:**

✅ **Code Complete:**
- [ ] MCP tool `get_vzp_reimbursement` implementován a otestován
- [ ] Supabase database schema vytvořen (`vzp_reimbursement`, `vzp_update_log`)
- [ ] Data ingestion pipeline funguje (initial load 50K léků)
- [ ] Frontend React component pro VZP Info Card implementován
- [ ] Claude AI prompt engineering (VZP keyword detection)

✅ **Testing Complete:**
- [ ] Unit tests: 90%+ code coverage
- [ ] Integration tests: Všechny scénáře pass
- [ ] E2E tests: 5 kritických user flows pass
- [ ] UAT: 5 beta lékařů schválilo feature

✅ **Documentation Complete:**
- [ ] Technical spec (tento dokument) schválen Tech Lead
- [ ] API documentation pro MCP tool (input/output examples)
- [ ] User-facing help article: "Jak používat VZP Navigator"

✅ **Performance & Security:**
- [ ] Response time <2s (95th percentile)
- [ ] Cache hit rate >40%
- [ ] GDPR compliance audit pass
- [ ] Security review pass (no SQL injection, XSS)

✅ **Launch Criteria:**
- [ ] Soft launch: 10 beta users (1 týden)
- [ ] Monitoring: Error rate <0.5%
- [ ] User satisfaction: "Pomohlo mi VZP Navigator?" >80% ANO
- [ ] Full rollout: Enabled pro všechny users

---

## Závěr

Tento dokument obsahuje **7 core user stories** s celkem **15+ acceptance criteria per story**. Každá story adresuje konkrétní user need z person (Dr. Nováková, Dr. Svoboda, Dr. Kučera) a má jasně definované success metrics.

**Next Steps:**
1. Tech Lead review & approval
2. Sprint planning (2-week sprints × 4 = 8 týdnů implementace)
3. Developer assignment (1 senior backend + 1 frontend + 1 MCP specialist)
4. Weekly demos for stakeholder feedback
