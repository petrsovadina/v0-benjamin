# Benjamin - VZP Navigator Feature (Screen Plan)

**Feature Type:** Inline enhancement pro Chat Interface

**Platform:** Web (Modal 1200×800px) + Chrome Extension (800×600px)

**Priority:** 🔥 MUST HAVE (Fáze 2)

**User Problem:** Lékaři musí ručně kontrolovat VZP web pro ověření hrazení léků, což zabírá 5+ minut a přerušuje workflow.

---

## Feature Overview

VZP Navigator je **MCP tool integrace**, která automaticky zobrazuje VZP úhradové informace přímo v Benjamin Chat odpovědích, když lékař klade dotazy týkající se léků. Feature se vykresluje jako **inline enriched content** v existujícím Chat UI, nikoliv jako samostatná stránka.

### Klíčové Principy
- **Zero friction:** Data VZP se zobrazují automaticky bez potřeby explicitního "VZP mode"
- **Contextual awareness:** AI detekuje, kdy je úhradová informace relevantní
- **Trust through transparency:** Vždy zobrazit zdroj dat (datum aktualizace VZP databáze)
- **Actionable:** Umožnit přímé follow-up akce (žádost o IU, cenové srovnání)

---

## Design Integration do Existujícího Chat UI

### Trigger Scénáře

VZP Navigator se aktivuje, když lékař:
1. Přímo se ptá na hrazení: *"Je empagliflozin hrazený VZP?"*
2. Ptá se na doporučení léku: *"Jaký SGLT2 inhibitor pro diabetes?"* → AI zmíní lék → automaticky přidá VZP status
3. Porovnává léky: *"Empagliflozin vs dapagliflozin"* → pro oba zobrazí VZP data
4. Follow-up na předchozí odpověď: *"A kolik to stojí pacienta?"*

### Kde se VZP Data Zobrazují

VZP informace se vykreslují **uvnitř Benjamin Response Bubble** jako strukturovaná sekce mezi hlavním textem odpovědi a Sources Panel.

---

## Visual Design - VZP Info Card

### Layout Structure

```
┌─────────────────────────────────────────────────────────────┐
│ Benjamin Response (Main Text)                                │
│                                                               │
│ Empagliflozin (Jardiance) je SGLT2 inhibitor doporučený     │
│ pro pacienty s T2DM a vysokým kardiovaskulárním rizikem...  │
│                                                               │
│ ┌───────────────────────────────────────────────────────┐   │
│ │ 💊 VZP ÚHRADOVÉ INFORMACE                              │   │
│ │ ─────────────────────────────────────────────────────  │   │
│ │                                                         │   │
│ │ 📦 Empagliflozin (Jardiance 10mg, 25mg)               │   │
│ │                                                         │   │
│ │ ✅ HRAZENÍ                                              │   │
│ │ • Standardní úhrada VZP                                │   │
│ │ • Indikace: Diabetes mellitus 2. typu (E11)           │   │
│ │ • Podmínky: HbA1c ≥ 53 mmol/mol po selhání metforminu│   │
│ │                                                         │   │
│ │ 💰 DOPLATEK PACIENTA                                   │   │
│ │ • 30 Kč (recept s plnou úhradou)                      │   │
│ │                                                         │   │
│ │ 📋 KÓDY PRO PŘEDPIS                                    │   │
│ │ • Kód omezení: H013 (Endokrinologie/Interní)          │   │
│ │ • ICD-10 diagnóza: E11 (Diabetes mellitus 2. typu)    │   │
│ │                                                         │   │
│ │ ⚠️ UPOZORNĚNÍ                                           │   │
│ │ • Pokud HbA1c < 53 → žádost o IU nutná                │   │
│ │   [📄 Jak podat žádost o IU]                          │   │
│ │                                                         │   │
│ │ 🔄 Aktualizace: 15.1.2025 | 🔗 VZP Seznam LP          │   │
│ └───────────────────────────────────────────────────────┘   │
│                                                               │
│ 📚 Zobrazit 3 zdroje (PubMed, SÚKL, ČLS JEP)                │
└─────────────────────────────────────────────────────────────┘
```

### Component Breakdown

#### 1. Header Section
- **Icon + Label:** `💊 VZP ÚHRADOVÉ INFORMACE`
- **Visual Style:**
  - Light purple/blue background `rgba(139, 92, 246, 0.08)`
  - Border: `1px solid rgba(139, 92, 246, 0.2)`
  - Border radius: `12px`
  - Padding: `16px`
  - Font: Inter Medium, 14px

#### 2. Drug Name
- **Text:** `📦 Empagliflozin (Jardiance 10mg, 25mg)`
- **Style:** Semi-bold, 15px, dark gray `#1F2937`

#### 3. Hrazení Status (Primary Info)
**Green Indicator pro hrazené léky:**
```
✅ HRAZENÍ
• Standardní úhrada VZP
• Indikace: Diabetes mellitus 2. typu (E11)
• Podmínky: HbA1c ≥ 53 mmol/mol po selhání metforminu
```

**Red Indicator pro nehrazené:**
```
❌ NENÍ HRAZENO
• Lék není na Seznamu kategorizovaných LP
• Úhrada: Pacient platí plnou cenu (~1,200 Kč/měsíc)
• Možnost: Žádost o individuální úhradu (IU)
  [📄 Jak podat žádost o IU]
```

**Yellow Indicator pro částečné hrazení:**
```
⚠️ ČÁSTEČNÉ HRAZENÍ
• Lék hrazen pouze pro specifické indikace
• Vaše indikace: Srdeční selhání (off-label)
• Žádost o IU nutná
  [📄 Template žádosti o IU]
```

#### 4. Doplatek Pacienta
- **Icon:** `💰 DOPLATEK PACIENTA`
- **Content:**
  - `30 Kč (recept s plnou úhradou)`
  - nebo: `50 Kč (50% úhrada)` nebo `350 Kč (pacient doplácí rozdíl)`

#### 5. Kódy pro Předpis (Prescribing Codes)
- **Icon:** `📋 KÓDY PRO PŘEDPIS`
- **Content:**
  - `Kód omezení: H013 (Endokrinologie/Internista)`
  - `ICD-10 diagnóza: E11 (Diabetes mellitus 2. typu)`
- **Purpose:** Kopírovatelné kódy pro e-recept systém

#### 6. Upozornění (Warnings/Special Conditions)
- **Icon:** `⚠️ UPOZORNĚNÍ`
- **Use Cases:**
  - Off-label použití
  - Dodatečné podmínky (lab hodnoty, předchozí terapie)
  - Link na žádost o IU

#### 7. Footer (Data Freshness)
- **Text:** `🔄 Aktualizace: 15.1.2025 | 🔗 VZP Seznam LP`
- **Style:** Small gray text, 12px, clickable link k VZP zdroji

---

## Interactive States

### 1. Collapsed State (Default)
Když Benjamin zmíní lék v odpovědi, zobrazí se kompaktní badge:

```
💊 Empagliflozin • ✅ Hrazeno VZP (30 Kč) [Zobrazit detaily ▼]
```

**Click action:** Expanduje na plnou VZP Info Card

### 2. Expanded State
Plná VZP Info Card s všemi sekcemi (viz Layout Structure výše)

### 3. Multiple Drugs Comparison
Pokud lékař porovnává 2+ léky, zobrazit VZP data side-by-side:

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

### 4. Loading State
Během fetchování VZP dat (1-2 sekundy):

```
┌─────────────────────────────────────────┐
│ 💊 VZP ÚHRADOVÉ INFORMACE               │
│ ─────────────────────────────────────   │
│                                          │
│ ⏳ Kontroluji VZP databázi...           │
│ [Animated spinner]                       │
└─────────────────────────────────────────┘
```

### 5. Error State
Pokud VZP data nejsou dostupná:

```
┌─────────────────────────────────────────┐
│ 💊 VZP ÚHRADOVÉ INFORMACE               │
│ ─────────────────────────────────────   │
│                                          │
│ ⚠️ VZP data dočasně nedostupná          │
│                                          │
│ [🔄 Zkusit znovu] [🔗 Otevřít VZP web] │
└─────────────────────────────────────────┘
```

---

## Follow-up Actions (Interactive Buttons)

Pod VZP Info Card zobrazit **akční tlačítka** pro rychlé follow-up:

```
[📄 Jak podat žádost o IU] [💰 Srovnat ceny alternativ] [📋 Kopírovat kódy]
```

### Button Actions

#### 1. "Jak podat žádost o IU"
**Trigger:** Click opens expandable section s step-by-step guide:

```
📄 ŽÁDOST O INDIVIDUÁLNÍ ÚHRADU (IU)

1. Formulář:
   • VZP Žádost o individuální úhradu (Formulář č. 12345)
   • Ke stažení: [🔗 VZP web]

2. Potřebná dokumentace:
   • Lékařská zpráva s odůvodněním
   • Dokumentace o selhání standardní terapie
   • Literatura podporující off-label použití

3. Doporučené odůvodnění:
   "Pacient s T2DM a NYHA II srdečním selháním, kde empagliflozin
    prokázal kardiorenal benefit (EMPA-REG OUTCOME, DAPA-HF studie).
    Metformin kontraindikován kvůli GFR 25 ml/min."

4. Čekací doba:
   • Standardní: 30 dnů
   • Urgentní: 7 dnů (při akutní indikaci)

[📋 Vygenerovat template žádosti pro tohoto pacienta]
```

#### 2. "Srovnat ceny alternativ"
**Trigger:** Opens price comparison table:

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

#### 3. "Kopírovat kódy"
**Trigger:** Kopíruje prescribing codes do clipboardu:

```
✅ Zkopírováno do schránky:

Kód omezení: H013
ICD-10: E11
SÚKL kód: 0123456
Dávkování: 10mg 1x denně
```

---

## Advanced Use Cases

### Scenario A: Off-label Prescribing

**User Query:** *"Je empagliflozin hrazený pro srdeční selhání?"*

**Benjamin Response with VZP Data:**

```
Empagliflozin (Jardiance) prokázal benefit u pacientů se srdečním
selháním ve studiích EMPEROR-Reduced a EMPEROR-Preserved [1][2].

┌─────────────────────────────────────────────────────────────┐
│ 💊 VZP ÚHRADOVÉ INFORMACE                                    │
│ ─────────────────────────────────────────────────────────   │
│                                                               │
│ ⚠️ OFF-LABEL POUŽITÍ                                          │
│                                                               │
│ • Indikace: Srdeční selhání (I50.x)                         │
│ • VZP hrazení: ❌ NE (registrován pouze pro T2DM)           │
│ • Doplatek pacienta: ~1,200 Kč/měsíc (plná cena)            │
│                                                               │
│ 💡 MOŽNOSTI:                                                  │
│ • Žádost o individuální úhradu (IU)                          │
│   → Evidence: EMPEROR-Reduced (2020), ESC guidelines 2021    │
│   → Success rate: ~60% (high evidence base)                  │
│                                                               │
│ • Alternativa: Dapagliflozin (Forxiga)                       │
│   → ✅ Hrazeno VZP pro srdeční selhání od 2023              │
│   → Doplatek: 50 Kč                                          │
│                                                               │
│ [📄 Vygenerovat žádost o IU] [🔄 Použít dapagliflozin]      │
└─────────────────────────────────────────────────────────────┘
```

### Scenario B: Price Comparison with Generic

**User Query:** *"Jaký je nejlevnější ACE inhibitor pro pacienta?"*

**Benjamin Response:**

```
Pro pacienty s hypertenzí nebo po infarktu myokardu jsou ACE inhibitory
první volbou. Nejlevnější opcí jsou generika ramipril nebo perindopril.

┌─────────────────────────────────────────────────────────────┐
│ 💊 VZP CENOVÉ SROVNÁNÍ - ACE INHIBITORY                      │
│ ─────────────────────────────────────────────────────────   │
│                                                               │
│ 💰 NEJLEVNĚJŠÍ PRO PACIENTA:                                 │
│                                                               │
│ 1. Ramipril (generikum)                                      │
│    • Doplatek: 15 Kč/měsíc                                   │
│    • Dávkování: 5mg 1x denně                                 │
│    • Kód: C09AA (bez omezení)                                │
│                                                               │
│ 2. Perindopril (generikum)                                   │
│    • Doplatek: 20 Kč/měsíc                                   │
│    • Dávkování: 5mg 1x denně                                 │
│                                                               │
│ 3. Enalapril (generikum)                                     │
│    • Doplatek: 18 Kč/měsíc                                   │
│    • Dávkování: 10mg 2x denně (⚠️ 2x denně compliance)      │
│                                                               │
│ ⚠️ ORIGINÁLY (DRAŽŠÍ):                                        │
│ • Tritace (ramipril): 85 Kč/měsíc (+70 Kč vs generikum)     │
│ • Prestarium (perindopril): 95 Kč/měsíc                      │
│                                                               │
│ 💡 Doporučení: Ramipril generikum - nejnižší cena + 1x denně│
│                                                               │
│ [📋 Předepsat ramipril 5mg] [💰 Detail všech ACE inhibitorů]│
└─────────────────────────────────────────────────────────────┘
```

### Scenario C: Drug Not Registered in Czech Republic

**User Query:** *"Je tirzepatide hrazený v ČR?"*

**Benjamin Response:**

```
Tirzepatide (Mounjaro) je duální GIP/GLP-1 agonista s výrazným efektem
na glykemickou kontrolu a hmotnost [1].

┌─────────────────────────────────────────────────────────────┐
│ 💊 VZP ÚHRADOVÉ INFORMACE                                    │
│ ─────────────────────────────────────────────────────────   │
│                                                               │
│ ❌ NENÍ REGISTROVÁN V ČR                                      │
│                                                               │
│ • SÚKL registrace: ❌ NE (k 15.1.2025)                       │
│ • EMA approval: ✅ ANO (2022)                                │
│ • Očekávaná registrace ČR: Q3 2025 (předběžné)              │
│                                                               │
│ 💡 AKTUÁLNÍ SITUACE:                                          │
│ • Lék není dostupný v českých lékárnách                      │
│ • Import ze zahraničí: Možný, ale bez VZP úhrady            │
│ • Náklady: ~8,000 Kč/měsíc (pacient platí vše)              │
│                                                               │
│ 🔄 HRAZENÉ ALTERNATIVY:                                       │
│ • Semaglutide (Ozempic) - ✅ Hrazeno VZP                     │
│   Doplatek: 150 Kč, podobný efekt (GLP-1 agonista)          │
│ • Dulaglutide (Trulicity) - ✅ Hrazeno VZP                   │
│   Doplatek: 120 Kč, 1x týdně aplikace                        │
│                                                               │
│ [📋 Detail semaglutide] [🔔 Upozornit na registraci]        │
└─────────────────────────────────────────────────────────────┘
```

---

## Suggested Follow-ups (Conversational AI)

Po zobrazení VZP Info Card AI automaticky navrhne follow-up otázky:

```
🤔 Možná vás zajímá:
• Jaké jsou podmínky pro předpis empagliflozinu?
• Jaké alternativy jsou hrazené?
• Jak napsat žádost o individuální úhradu?
```

---

## Responzivní Layout

### Desktop Modal (1200×800px)
- VZP Info Card: Full width (90% of chat area)
- Side-by-side comparison: 2 columns

### Chrome Extension (800×600px)
- VZP Info Card: Full width (95% of chat area)
- Comparison mode: Stacked vertically (scrollable)

### Mobile/Tablet (400×600px)
- VZP Info Card: Full width
- Collapsed by default (pouze badge)
- Comparison: Vertical tabs (swipeable)

---

## Edge Cases & Error Handling

### Case 1: VZP Data Stará (>3 měsíce)
```
⚠️ Upozornění: Data VZP starší než 90 dní (poslední aktualizace: 15.10.2024)
Doporučujeme ověřit aktuální status na VZP web.
[🔗 Otevřít VZP Seznam LP]
```

### Case 2: Lék Má Více Indikací s Různým Hrazením
```
⚠️ HRAZENÍ ZÁVISÍ NA INDIKACI

• Diabetes 2. typu (E11): ✅ Hrazeno (30 Kč doplatek)
• Srdeční selhání (I50): ❌ Není hrazeno (žádost o IU)
• Chronické onemocnění ledvin: ✅ Hrazeno od 2024

💡 Vyberte indikaci pro detail hrazení:
[E11 Diabetes] [I50 Srdeční selhání] [N18 CKD]
```

### Case 3: VZP API Nedostupné
```
⚠️ VZP databáze dočasně nedostupná

Zobrazuji cached data (aktualizace: 10.1.2025).
Pro nejnovější informace navštivte VZP web.

[🔄 Zkusit znovu] [🔗 VZP web]
```

---

## Accessibility

- **ARIA Labels:** `aria-label="VZP úhradové informace pro empagliflozin"`
- **Keyboard Navigation:**
  - `Tab` pro přesun mezi sekcemi
  - `Enter` pro expand/collapse
  - `Cmd+C` pro kopírování kódů
- **Screen Reader:** Announce VZP status při zobrazení card
- **High Contrast Mode:** Green/Red status indicators mají ikony (✅/❌)

---

## Performance Optimizations

- **Pre-fetching:** Pokud AI detekuje zmínku o léku, začne fetchovat VZP data paralelně během generování odpovědi
- **Caching:** VZP data pro populární léky (top 100) cached in Supabase (TTL 30 dní)
- **Lazy Load:** VZP Info Card se renderuje až po dokončení main response text (ne během streamingu)

---

## Success Metrics (KPIs)

- **Adoption:** 70% lékařů používá VZP Navigator ≥5x týdně
- **Time Savings:** 5 min (manuální VZP kontrola) → 0 min = 100% úspora
- **Accuracy:** 95%+ přesnost VZP dat vs oficiální VZP web
- **User Satisfaction:** "Pomohlo mi VZP Navigator?" → 85%+ ANO
- **Conversion:** 20% lékařů upgraduje na Pro plan kvůli VZP Navigator

---

## Technical Notes (pro Backend)

### MCP Tool: VZP Navigator

**Input:**
```json
{
  "drug_name": "empagliflozin",
  "indication": "E11", // Optional ICD-10 code
  "patient_context": { // Optional
    "age": 65,
    "insurance": "VZP" // Future: other insurers
  }
}
```

**Output:**
```json
{
  "reimbursement_status": "reimbursed",
  "copay_czk": 30,
  "restriction_code": "H013",
  "indications": ["E11"],
  "conditions": "HbA1c ≥ 53 mmol/mol po selhání metforminu",
  "off_label_note": null,
  "last_updated": "2025-01-15",
  "source_url": "https://www.vzp.cz/..."
}
```

### Database Schema (Supabase)
```sql
CREATE TABLE vzp_reimbursement (
  id UUID PRIMARY KEY,
  drug_name TEXT NOT NULL,
  atc_code TEXT,
  reimbursement_status TEXT, -- 'reimbursed', 'not_reimbursed', 'conditional'
  copay_czk INTEGER,
  restriction_code TEXT,
  indication_icd10 TEXT[],
  conditions TEXT,
  last_updated TIMESTAMP,
  source_url TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);
```

---

## Závěr

VZP Navigator je **high-impact, low-friction feature**, která poskytuje unikátní competitive advantage (žádný konkurent nemá VZP data). Implementuje se jako inline enhancement existujícího Chat UI, takže nevyžaduje nové obrazovky nebo UX flows — pouze obohacení stávajících odpovědí o strukturovaná VZP data.
