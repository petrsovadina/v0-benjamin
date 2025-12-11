# Benjamin - Epikríza Tab
Automatické generování epikrízy v rámci modálního okna Benjamina (záložka "Epikríza").

**Formát:** Tab view v rámci modálního okna (1200×800px) / Chrome Extension (800×600px)

**Layout:** Single-page form s vertikálním scrollem

---

## Globální Kontext (Sdílený s Main Chat)

### Top Bar (Inherited from Main Modal)
- Logo "Benjamin"
- **Tab Navigation:**
  - 💬 Chat
  - 📋 **Epikríza** (active)
  - 🌍 Translator
  - ⚙️ Nastavení
- Close button ✕

---

## Header Sekce (Sticky)

### Page Title
- Nadpis: "📋 Generování Epikrízy"
- Podnázev: "Automatická generování podle vyhlášky č. 98/2012 Sb. § 21"

### Patient Context Banner (Prominent)
- Compact info card (horizontální layout):
  - **Left side:**
    - 👤 Jméno pacienta (z FONS kontextu)
    - 📅 Datum narození (věk)
    - 🏥 Oddělení
  - **Center:**
    - 📆 Přijetí: 15.11.2024
    - 📆 Propuštění: 20.11.2024 (nebo "Hospitalizován: 5 dní")
  - **Right side:**
    - Status badge:
      - ✅ "Data dostupná" (zelená)
      - ⚠️ "Neúplná data" (oranžová)
    - Quick stats: "12 dekurzů • 8 vyšetření • 5 léků"
- Collapse/expand toggle (pro úsporu místa)

---

## Main Content Area (Scrollable)

### Sekce 1: Datové Zdroje

**Nadpis:** "📊 Vyberte datové zdroje"

**Layout:** Checkboxes + info badges (compact grid, 2 columns)

**Zdroje (všechny defaultně zaškrtnuté):**

- **Řádek 1:**
  - ☑️ **Dekurzy** (badge: "12 záznamů")
  - ☑️ **Laboratorní výsledky** (badge: "23 výsledků")

- **Řádek 2:**
  - ☑️ **Vyšetření** (badge: "8 vyšetření")
  - ☑️ **Medikace** (badge: "15 léků")

- **Řádek 3:**
  - ☑️ **Zákroky a operace** (badge: "2 zákroky")
  - ☑️ **Konzilia** (badge: "3 konzilia")

**Expandable detail view:**
- Link: "🔍 Zobrazit detaily zdrojů"
- Expanduje accordion s:
  - Seznam všech dekurzů (datum + autor)
  - Možnost individuálně odškrtnout konkrétní záznamy
  - Preview tooltip při hover

---

### Sekce 2: Diagnózy (MKN-10)

**Nadpis:** "🩺 Diagnózy"

**Hlavní diagnóza:**
- Display box (read-only, editable v FONS):
  - Kód: I21.0
  - Název: "Akutní transmurální infarkt myokardu přední stěny"
  - Tlačítko: "✏️ Upravit v FONS" (opens FONS form)

**Vedlejší diagnózy:**
- Scrollable list (max 5 visible, scroll for more):
  - I10 - Esenciální hypertenze
  - E11.9 - Diabetes mellitus 2. typu
  - I25.1 - Aterosklerotická choroba srdce
- Drag & drop reorder (čísla 1, 2, 3... pro pořadí)

**Validace:**
- ⚠️ Warning pokud chybí hlavní diagnóza:
  - "Hlavní diagnóza není zadána. Doplňte ji před generováním."

---

### Sekce 3: Generování (Primary Action)

**Layout:** Centrální, prominent

**Info Banner:**
- 💡 "Benjamin vygeneruje strukturovanou epikrízu podle legislativních požadavků (§21)."
- Link: "📄 Zobrazit požadované náležitosti"

**Primary Action Button:**
- Velké tlačítko (full-width nebo centered):
  - "🤖 Generovat Epikrízu"
  - Primary color (modré/fialové)
  - Disabled pokud:
    - Chybí hlavní diagnóza
    - Nejsou vybrány žádné zdroje

**Loading State (během generování):**
- Button přechod na loading:
  - Spinner + text: "Generuji..."
- Progress indicator pod tlačítkem:
  - Progress bar s kroky:
    ```
    ⏳ Načítám data pacienta... (30%)
    🔍 Analyzuji průběh hospitalizace... (60%)
    📝 Strukturuji obsah epikrízy... (90%)
    ✅ Dokončeno!
    ```
  - Odhadovaný čas: "~15-30 sekund"
- Možnost zrušit: "❌ Zrušit" button

---

### Sekce 4: Vygenerovaná Epikríza (Po Generování)

**Header:**
- Nadpis: "✅ Vygenerovaná Epikríza"
- Meta info:
  - Timestamp: "Vygenerováno: 20.11.2024 14:35"
  - Word count: "~450 slov"

**Editovatelné Textové Pole (Rich Text Editor):**
- Layout: Full-width textarea s formátováním
- Strukturované sekce (collapsible accordions):

  **1. Identifikační údaje** (pre-filled z FONS)
  ```
  Pacient: Jan Novák, nar. 15.5.1970 (54 let)
  Oddělení: Interní klinika, JIP
  Pobyt: 15.11.2024 - 20.11.2024 (5 dní)
  ```

  **2. Anamnestické údaje** (AI generované)
  ```
  RA: Arteriální hypertenze 10 let, DM 2. typu 5 let...
  OA: Otec zemřel na infarkt myokardu...
  ```

  **3. Diagnostická část** (z diagnóz)
  ```
  Hlavní diagnóza: I21.0 - Akutní transmurální...
  Vedlejší diagnózy:
  1. I10 - Esenciální hypertenze
  2. E11.9 - Diabetes mellitus 2. typu
  ```

  **4. Průběh hospitalizace** (AI shrnutí)
  ```
  Pacient přijat pro akutní bolest na hrudi...
  Provedeno akutní PCI s implantací stentu...
  ```

  **5. Provedená vyšetření a léčba** (strukturovaný přehled)
  ```
  - EKG: Elevace ST v V1-V4
  - Lab: Troponin I 45 ng/ml (↑)
  - Koronarografie: Oklúze LAD
  - PCI + stent LAD
  ```

  **6. Epikritické zhodnocení** (AI syntéza)
  ```
  Hospitalizace komplikovaná, stabilizován...
  ```

  **7. Doporučení** (AI generované)
  ```
  - Duální antiagregační léčba (ASA + clopidogrel)
  - Pokračovat v léčbě statinem, ACE-I, beta-blokátorem
  - Kontrola v kardiologické ambulanci za 4 týdny
  - Rehabilitace, dietní opatření, kontrola lipidogramu
  ```

**Formátovací Toolbar:**
- Minimalistický rich text editor:
  - **B** Tučné
  - _I_ Kurzíva
  - • Odrážky
  - 1. Číslovaný seznam
  - Undo/Redo

**Inline Editing:**
- Kliknutí do kterékoli sekce = edit mode
- Auto-save každých 10 sekund
- Indicator: "💾 Uloženo" / "💾 Ukládám..."

---

### Action Buttons (Bottom of Content)

**Primary Actions (Horizontal Row):**
- 💾 **Uložit do FONS Enterprise**
  - Primary button
  - Ukládá přímo do pole epikrízy v FONS
  - Success toast: "✅ Epikríza uložena"

- 📋 **Kopírovat do schránky**
  - Secondary button
  - Toast: "✅ Zkopírováno"

- 📄 **Export PDF**
  - Secondary button
  - Dropdown s opcemi:
    - "S hlavičkou instituce"
    - "Bez hlavičky (plain)"
  - Generates PDF s podpisem lékaře

**Secondary Actions:**
- 🔄 **Generovat jinak**
  - Link/tertiary button
  - Vygeneruje alternativní verzi
  - Možnost porovnat (side-by-side)

- ✏️ **Upravit manuálně**
  - Přepne do full edit mode (všechny sekce editovatelné)

- 📤 **Přeložit do EN**
  - Cross-tab integration
  - Otevře Translator tab s obsahem epikrízy

**Feedback:**
- 👍 Kvalitní / 👎 Nekvalitní
- 🚨 Nahlásit chybu

---

## Chybové a Edge Stavy

### Nedostatek Dat
- Error banner (červený):
  - "⚠️ **Nelze vygenerovat epikrízu** - chybí povinné údaje:"
  - Bulleted list:
    - ❌ Hlavní diagnóza není zadána
    - ❌ Nejsou dostupné žádné dekurzy
    - ❌ Chybí propouštěcí datum
  - CTA: "➡️ Doplnit v FONS Enterprise"

### Selhání Generování
- Error message v content area:
  - "❌ Nepodařilo se vygenerovat epikrízu."
  - "Důvod: [API timeout / Nedostatečná data]"
  - Tlačítko: "🔄 Zkusit znovu"

### Validace Výstupu
- Automatická kontrola po vygenerování:
  - ⚠️ Warning banner (pokud detekováno):
    - "Epikríza je neobvykle krátká (<200 slov). Zkontrolujte obsah."
    - "Chybí některé povinné sekce. Doplňte manuálně."

---

## Responzivní Behavior

### Desktop Modal (1200×800px)
- Full layout
- Dvousloupcový grid pro checkboxy (2 columns)
- Wide textarea (100% width)

### Extension Mode (800×600px)
- Single column layout
- Kompaktní checkboxy (1 column)
- Narrow textarea
- Scrollable content area

---

## Dodatečné Funkce (Nice-to-Have)

### Šablony Epikríz
- Dropdown nad "Generovat" tlačítkem:
  - "📄 Vyberte šablonu"
  - Podle typu oddělení:
    - Interní medicína
    - Chirurgie
    - ARO/JIP
    - Psychiatrie
  - Custom šablony (user-defined)

### Porovnání Verzí
- Pokud "Generovat jinak":
  - Split view (50/50):
    - Verze A | Verze B
  - Diff highlighting (zelená/červená pro rozdíly)
  - Tlačítko: "Vybrat tuto verzi"

### Historie Generování
- Collapsible sidebar (pravá strana):
  - "📜 Poslední 5 epikríz"
  - Každý záznam:
    - Jméno pacienta
    - Datum generování
    - Quick actions: 👁️ Zobrazit, 🔄 Re-use

### Auto-save Koncept
- Automatické ukládání draftu každých 30 sekund
- Možnost obnovit předchozí verzi:
  - "↩️ Obnovit poslední uloženou verzi"

---

## Integration s Chat Tabem

**Cross-feature Actions:**
- Z Chatu:
  - Button "📋 Použít v epikríze" pod Benjamin response
  - Automaticky otevře Epikríza tab
  - Pre-fills relevantní data z chat odpovědi

- Z Epikrízy:
  - Button "💬 Zeptat se Benjamina"
  - Otevře Chat tab s kontextem:
    - "Doplň prosím chybějící informace pro epikrízu pacienta X..."

---

## Performance

- Lazy load historie epikríz (virtualized)
- Cached patient data (no re-fetch)
- Debounced auto-save (10s interval)
- Optimistic UI updates (instant feedback)
