# Benjamin - Translator Tab
Inteligentní překlad medicínské terminologie v rámci modálního okna Benjamina (záložka "Translator").

**Formát:** Tab view v rámci modálního okna (1200×800px) / Chrome Extension (800×600px)

**Layout:** Dvousloupcový (vstup | výstup) s centrálním tlačítkem

---

## Globální Kontext (Sdílený s Main Chat)

### Top Bar (Inherited from Main Modal)
- Logo "Benjamin"
- **Tab Navigation:**
  - 💬 Chat
  - 📋 Epikríza
  - 🌍 **Translator** (active)
  - ⚙️ Nastavení
- Close button ✕

---

## Header Sekce (Sticky)

### Page Title
- Nadpis: "🌍 Překlad Medicínského Obsahu"
- Podnázev: "Překlad mezi češtinou a angličtinou s podporou odborné terminologie"

### Translation Settings Bar (Horizontální)

**Layout:** Flex row, centered

**Components:**

1. **Vstupní Jazyk (Dropdown):**
   - 🇨🇿 Čeština
   - 🇬🇧 Angličtina
   - 🔍 Auto-detect (default)
   - Selected: zobrazuje vlajku + label

2. **Swap Button (Center):**
   - Ikona: ⇄ (obousměrná šipka)
   - Kliknutím prohodí směr překladu
   - Animovaný flip efekt

3. **Výstupní Jazyk (Dropdown):**
   - 🇬🇧 Angličtina (default)
   - 🇨🇿 Čeština

4. **Režim Překladu (Toggle Buttons):**
   - **Odborný** (default):
     - Ikona: 🩺
     - Tooltip: "Zachovává lékařskou terminologii"
   - **Zjednodušený**:
     - Ikona: 👤
     - Tooltip: "Převod na laicky srozumitelný jazyk"
   - Toggle styling (active = primary color)

---

## Main Content Area (Dual Panel)

### Layout Structure:
```
┌──────────────────────────────┬──────────────────────────────┐
│   Vstupní Panel (Left 48%)   │   Výstupní Panel (Right 48%) │
│                              │                              │
└──────────────────────────────┴──────────────────────────────┘
         Centrální tlačítko "Přeložit" (4% gap)
```

---

### Levý Panel - Vstupní Text

**Header:**
- Label: "📝 Text k překladu"
- Character counter: "0 / 5000 znaků"
- Detekovaný jazyk badge (dynamický):
  - "Detekováno: 🇨🇿 Čeština" (zelená)
  - "Detekováno: 🇬🇧 Angličtina" (modrá)
  - "⚠️ Neznámý jazyk" (oranžová)

**Textarea (Large Input Field):**
- Placeholder:
  ```
  Vložte text k překladu...

  Příklad:
  "Pacient přijat pro akutní infarkt myokardu..."
  ```
- Features:
  - Auto-resize (min 10 řádků, max full height)
  - Syntax highlighting pro lékařské termíny (subtle)
  - Spellcheck enabled
  - Maximální délka: 5000 znaků

**Toolbar (Above Textarea):**
- 📋 **Vložit ze schránky**
- 🗑️ **Vymazat vše**
- 📄 **Nahrát soubor**
  - Podporované formáty: .txt, .docx
  - Drag & drop area

**Quick Info Banner (Pod Textarea):**
- Auto-detekce typu obsahu (subtle display):
  - "Typ: Lékařská zpráva" (🏥)
  - "Typ: Laboratorní výsledky" (🧪)
  - "Typ: Lékový list" (💊)

---

### Pravý Panel - Přeložený Text

**Header:**
- Label: "✅ Překlad"
- Word count: "~250 slov"
- Quality indicator (badge):
  - ✅ "Vysoká kvalita" (zelená)
  - ⚠️ "Zkontrolujte manuálně" (oranžová)

**Display Area (Read-Only):**
- Formátované zobrazení (zachovává strukturu)
- Read-only textarea (scrollable)
- Syntax highlighting (subtle):
  - Lékařské termíny (modře)
  - Neúspěšně přeložené (žlutě s podtržítkem)

**Loading State (Během Překladu):**
- Skeleton loader:
  - Animované placeholder lines
  - Text: "🔄 Překládám..."
  - Progress bar:
    ```
    ⏳ Analyzuji text... (30%)
    🔍 Hledám terminologii... (60%)
    ✅ Dokončuji překlad... (90%)
    ```
  - Odhadovaný čas: "~2-5 sekund"

**Toolbar (Below Display Area):**
- 📋 **Kopírovat překlad**
  - Toast: "✅ Zkopírováno do schránky"
- 📄 **Stáhnout jako .txt**
- 📄 **Stáhnout jako .docx**
- ✏️ **Upravit překlad**
  - Přepne do edit mode (textarea editable)
- 📤 **Použít v dokumentaci**
  - Cross-integration s FONS Enterprise
  - Opens dialog: "Kam vložit? [Epikríza | Dekurz | ...]"

---

### Centrální Tlačítko "Přeložit"

**Umístění:** Mezi levým a pravým panelem (vertikálně centrované)

**Design:**
- Velké circular button (64×64px):
  - Ikona: 🌍 (globe)
  - Tooltip: "Přeložit (Enter)"
- Primary color gradient
- Hover efekt: scale + glow

**States:**
- **Default:** 🌍 "Přeložit"
- **Loading:** Spinner animace
- **Disabled:** Šedá, pokud vstup prázdný
- **Success:** ✅ check mark (1s, pak zpět)

**Keyboard Shortcut:**
- Enter (pokud focus v input textarea)
- Cmd/Ctrl + Enter (kdykoliv)

---

## Expandable Sections (Pod Main Panels)

### 1. Terminologický Slovník (Collapsible)

**Header:**
- "📚 Klíčové termíny v překladu"
- Badge: "5 termínů"
- Toggle: Collapsed by default

**Content (When Expanded):**
- Tabulka s 3 sloupci:

  | Původní Termín | Přeložený Termín | Alternativy |
  |----------------|------------------|-------------|
  | Epikríza | Discharge Summary | Clinical Summary, Hospital Summary |
  | Dekurz | Progress Note | Clinical Note, Daily Note |
  | Diferenciální diagnostika | Differential Diagnosis | DDx |

- Features:
  - Search box: "🔍 Hledat termín..."
  - Filter: "⚠️ Zobrazit pouze neobvyklé překlady"
  - Export: "📄 Exportovat slovník (.csv)"

### 2. Srovnání Režimů (Collapsible)

**Header:**
- "🔀 Porovnat: Odborný vs. Zjednodušený"
- Toggle: Collapsed by default

**Content:**
- Split view (50/50):
  - **Levá strana:** Odborný režim výstup
  - **Pravá strana:** Zjednodušený režim výstup
- Diff highlighting:
  - Zelená = odlišná terminologie
  - Zvýrazněné změny (odborný → laický termín)

---

## Sidebar - Historie Překladů (Collapsible Right Panel)

**Toggle Button:** "📜 Historie"

**Content:**
- Seznam posledních 10 překladů:
  - **Každý záznam:**
    - Preview vstupního textu (50 znaků, truncated)
    - Směr: 🇨🇿 → 🇬🇧 nebo 🇬🇧 → 🇨🇿
    - Režim badge: "Odborný" / "Zjednodušený"
    - Timestamp: "před 5 minutami"
    - **Quick Actions:**
      - 👁️ Zobrazit
      - 🔄 Znovu přeložit
      - 🗑️ Smazat

**Footer:**
- "Zobrazit kompletní historii" (link)
- "🗑️ Vymazat historii" (button)

**Search Box:**
- "🔍 Hledat v historii..."
- Real-time filtrování

---

## Prázdný Stav (Empty State)

**Zobrazuje se při prvním otevření tabu**

### Centrální Sekce (Místo Input/Output Panelů)
- Ikona: 🌍 (velká, animovaná)
- Nadpis: "Přeložte medicínský text"
- Podnázev: "Podporujeme překlad mezi češtinou a angličtinou s ohledem na odbornou terminologii."

### Ukázkové Příklady (Cards)

**Grid Layout (2×2):**

**Karta 1:**
- Název: "Propouštěcí zpráva"
- Direction: 🇨🇿 → 🇬🇧
- Preview: "Pacient přijat pro..."
- Button: "Vyzkoušet"

**Karta 2:**
- Název: "Zjednodušit termín"
- Mode: Odborný → Laický
- Příklad: "Akutní infarkt myokardu" → "Srdeční infarkt"
- Button: "Vyzkoušet"

**Karta 3:**
- Název: "Laboratorní výsledky"
- Direction: 🇬🇧 → 🇨🇿
- Preview: "Hemoglobin 12.5 g/dL..."
- Button: "Vyzkoušet"

**Karta 4:**
- Název: "Lékový list"
- Direction: 🇨🇿 → 🇬🇧
- Preview: "Amiodaron 200mg..."
- Button: "Vyzkoušet"

---

## Chybové a Edge Stavy

### 1. Prázdný Vstup
- Disabled "Přeložit" button
- Tooltip: "⚠️ Zadejte prosím text k překladu"

### 2. Příliš Dlouhý Text
- Warning banner (červený) v levém panelu:
  - "⚠️ Text přesahuje limit 5000 znaků"
  - "Aktuálně: **5234 znaků** (o 234 znaků více)"
  - CTA: "🗑️ Zkrátit text" (automatically trims to 5000)

### 3. Nepodporovaný Jazyk
- Error banner:
  - "❌ Tento jazyk zatím nepodporujeme"
  - "Dostupné: 🇨🇿 Čeština, 🇬🇧 Angličtina"
  - CTA: "🔄 Zkusit auto-detekci"

### 4. Selhání Překladu
- Error v pravém panelu:
  - "❌ Překlad se nezdařil"
  - "Důvod: [API timeout / Neznámý formát]"
  - Buttons:
    - "🔄 Zkusit znovu"
    - "🚨 Kontaktovat podporu"

### 5. Nekompletní Překlad
- Warning banner v pravém panelu:
  - "⚠️ Některé termíny nebyly přeloženy"
  - Highlight neúspěšných termínů (žlutá barva v textu)
  - CTA: "💡 Zobrazit neúspěšné termíny" (shows list)

---

## Dodatečné Funkce (Nice-to-Have)

### Batch Překlad
- Button v toolbar: "📂 Hromadný překlad"
- Modal dialog:
  - Upload multiple files (.txt, .docx)
  - Progress bar: "Překládám 3/10 souborů..."
  - Batch download výstupů (.zip)

### Integrace se Slovníky
- Links v bottom footer:
  - "📖 SNOMED CT lookup"
  - "📖 MeSH (MSHCZE)"
  - "📖 MKN-10 klasifikace"
- Quick lookup feature:
  - Highlight term → right-click → "Lookup in SNOMED CT"
  - Tooltip s definicí

### AI-Powered Suggestions
- Pokud detekován ambiguous termín:
  - Tooltip: "💡 Tento termín má více významů. Vyberte kontext:"
    - Option 1: Kardiologie → "Myocardial infarction"
    - Option 2: Obecné → "Heart attack"

---

## Responzivní Layout

### Desktop Modal (1200×800px)
- Dual panel (48% - 4% gap - 48%)
- Full sidebar visible
- Wide textareas

### Extension Mode (800×600px)
- Vertikální stack (vstup nad výstupem):
  - Input: 40% height
  - Output: 40% height
  - Gap: "Přeložit" button (centered, 10% height)
- Sidebar collapsed by default
- Narrow textareas

---

## Performance & UX

- **Real-time character counter** (debounced)
- **Auto-save draft** (každých 10s)
- **Cached translations** (no re-translate same input)
- **Keyboard shortcuts:**
  - `Cmd/Ctrl + Enter` - Přeložit
  - `Cmd/Ctrl + K` - Focus na input
  - `Cmd/Ctrl + C` - Kopírovat output
- **Undo/Redo** v edit mode (Cmd+Z / Cmd+Shift+Z)

---

## Cross-Tab Integration

### Z Chatu:
- Button "🌍 Přeložit" pod Benjamin response
- Automaticky otevře Translator tab
- Pre-fills input s textem z chatu

### Z Epikrízy:
- Button "📤 Přeložit do EN" v action buttons
- Otevře Translator tab
- Pre-fills s obsahem epikrízy

### Do FONS Enterprise:
- Button "📤 Použít v dokumentaci"
- Dialog s výběrem cílového pole v FONS
- Direct insertion bez copy-paste
