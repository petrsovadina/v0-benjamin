# Benjamin - Hlavní Chat Interface
Primární view AI klinického asistenta s přímým přístupem k medicínským zdrojům přes MCP nástroje.

**Formát:** Modální okno (1200×800px) / Chrome Extension popup (800×600px)

**Design Inspirace:** Minimalistický, clean (podobně jako Morphic) s důrazem na chat konverzaci

---

## Globální Struktura Modálního Okna

### Top Bar (Fixed Header)
- Logo/Branding:
  - "Benjamin" text logo + AI ikona
  - Subtitle: "AI Klinický Asistent"
- Horizontal Tab Navigation (primární navigace):
  - 💬 **Chat** (active/default)
  - 📋 Epikríza
  - 🌍 Translator
  - ⚙️ Nastavení
- Utility Actions:
  - 🔍 Search v historii (quick search)
  - 👤 User avatar + menu
  - ✕ Close modal (návrat do FONS Enterprise)

### Content Area (Main View)
- Full-height scrollable oblast
- Responzivní layout (adapts to modal/extension size)

### Bottom Input Bar (Fixed Footer)
- Always visible vstupní pole
- Sticky na spodku modalu

---

## Prázdný Stav (Empty State)

**Zobrazuje se při prvním otevření nebo po vymazání konverzace**

### Centrální Hero Sekce
- Velké logo/icon (AI brain/chip):
  - Animovaný gradient (fialová → modrá)
  - Subtle breathing animation
- Nadpis:
  - "Dobrý den, doktore 👋"
  - Personalizované oslovení (jméno z FONS účtu)
- Podnázev:
  - "Zeptejte se mě na cokoliv - jsem připojený k PubMed, SÚKL, Semantic Scholar a dalším medicínským zdrojům."

### Quick Start Cards (Suggested Prompts)
- Grid layout (2×3 nebo 3×2 podle velikosti okna)
- Klikatelné karty s ukázkovými dotazy:

  **Karta 1: Diagnostika**
  - "🔍 Diferenciální diagnostika akutní bolesti břicha"
  - Kategorie badge: "Diagnostika"

  **Karta 2: Farmakologie**
  - "💊 Interakce warfarinu se SSRI antidepresivy"
  - Kategorie badge: "Léky"

  **Karta 3: Guidelines**
  - "📋 Aktuální guidelines pro léčbu diabetu 2. typu"
  - Kategorie badge: "Doporučení"

  **Karta 4: Laboratorní Hodnoty**
  - "🧪 Interpretace zvýšeného D-dimeru u starších pacientů"
  - Kategorie badge: "Lab"

  **Karta 5: Klinický Případ**
  - "🏥 45letá žena s palpitacemi a únavou - co vyšetřit?"
  - Kategorie badge: "Kazuistika"

  **Karta 6: Aktuální Výzkum**
  - "🆕 Co nového v léčbě fibrilace síní (2024-2025)?"
  - Kategorie badge: "Novinky"

### Tips Banner (Bottom of Empty State)
- Subtle info box:
  - "💡 **Tip:** Pište přirozeně v češtině. Mohu odpovídat na základě PubMed, SÚKL databáze, českých guidelines a dalších zdrojů."
  - Odkaz: "Jak efektivně komunikovat s Benjaminem"

---

## Konverzační Stav (Active Chat)

**Zobrazuje se po zadání prvního dotazu**

### Chat Thread (Scrollable Area)

#### User Message Bubble
- Pravá strana (right-aligned)
- Světlé pozadí (light blue/gray)
- Komponenty:
  - Text dotazu
  - Timestamp (relativní: "před 2 minutami")
  - User avatar (malý, 24×24px)
- Max width: 70% šířky content area

#### Benjamin Response Bubble
- Levá strana (left-aligned)
- Bílé/světle fialové pozadí
- Benjamin avatar (AI ikona, 32×32px)
- Komponenty:

  **1. Response Header:**
  - "Benjamin" label
  - Timestamp
  - Thinking indicator (při generování):
    - "💭 Hledám v PubMed..."
    - "🔍 Kontroluji SÚKL databázi..."
    - "📚 Analyzuji české guidelines..."
    - Animated dots (...)

  **2. Main Response Text:**
  - Markdown formátování:
    - **Tučné** pro důležité body
    - `Inline code` pro léky/diagnózy
    - Numbered lists pro postupy
    - Blockquotes pro citace
  - Inline citace: [1], [2], [3]
  - Strukturované sekce (pokud relevantní):
    ```
    📊 **Hlavní zjištění:**
    - Bod 1
    - Bod 2

    🇨🇿 **České implikace:**
    - VZP úhrada
    - SÚKL doporučení

    🤔 **Praktické doporučení:**
    - Action items
    ```

  **3. Sources Panel (Expandable):**
  - Collapsed by default: "📚 Zobrazit 5 zdrojů"
  - Expanded:
    - Seznam citací:
      ```
      [1] PubMed - PMID:12345678
          "Effect of warfarin on..."
          Nature Medicine, 2024
          🔗 Odkaz

      [2] SÚKL - Databáze léků
          "Interakce warfarinu s..."
          Aktualizace: 15.1.2025
          🔗 Odkaz
      ```
    - Filtr: "Zobrazit pouze české zdroje"

  **4. Action Buttons (Mini Toolbar):**
  - Horizontal row of icon buttons:
    - 👍 Helpful
    - 👎 Not helpful
    - 📋 Kopírovat
    - 📤 Použít v epikríze
    - 🔄 Regenerovat odpověď
    - 🚨 Nahlásit problém

#### Streaming Response (při generování)
- Typewriter efekt (streaming text)
- Loading skeleton pro sources panel
- Animated gradient na avatar během generování

#### Multi-turn Conversation
- Historie všech zpráv v threadu
- Smooth scroll to latest message
- Context awareness (Benjamin si pamatuje předchozí zprávy)

### Suggested Follow-ups (Po Každé Odpovědi)
- Sekce pod Benjamin response:
  - "🤔 Možná vás zajímá:"
  - Klikatelné chips s follow-up otázkami:
    - "Jaké jsou kontraindikace?"
    - "Dávkování u starších pacientů?"
    - "Dostupné alternativy v ČR?"
  - AI-generované na základě kontextu

---

## Bottom Input Bar (Fixed Footer)

### Input Field
- Large textarea (auto-expanding):
  - Placeholder: "Zeptejte se Benjamina..."
  - Max height: 150px (scrollable po překročení)
  - Character counter: "125 / 2000"
- Features:
  - Auto-focus při otevření modalu
  - Shift+Enter = nový řádek
  - Enter = odeslat
  - @ mentions (future: @PubMed, @SÚKL pro targeted search)

### Toolbar (Above Input)
- Left side:
  - 📎 Attach file (upload lab results, images)
  - 🎤 Voice input (speech-to-text)
  - 💡 Quick actions dropdown:
    - "Vygenerovat epikrízu"
    - "Přeložit text"
    - "Vyhledat lék v SÚKL"
- Right side:
  - 🗑️ Clear conversation
  - ⚙️ Model settings (Claude vs GPT toggle)
  - ➤ Send button (prominent, primary color)

### Active Connections Indicator
- Subtle status bar:
  - "✅ Připojeno: PubMed • SÚKL • Semantic Scholar • MEDLINE"
  - Zelená tečka = active
  - Červená tečka = offline (with error message)

---

## Sidebar Features (Optional - Collapsible)

### History Sidebar (Right Panel - Collapsible)
- Toggle button: "📜 Historie"
- Content:
  - **Recent Conversations (10 latest):**
    - Každá konverzace:
      - První dotaz (truncated, 50 chars)
      - Timestamp
      - Quick actions:
        - 👁️ Zobrazit
        - 🔄 Pokračovat
        - 🗑️ Smazat
  - Search box: "Hledat v historii..."
  - Filtr podle data: "Dnes", "Tento týden", "Tento měsíc"
  - Tlačítko: "Exportovat kompletní historii"

### Bookmarks Section
- Záložkované konverzace
- Star ikona pro označení důležitých threadů
- Organizace do složek (future)

---

## Chybové a Edge Stavy

### Žádné Připojení ke Zdrojům
- Error banner v top bar:
  - "⚠️ Některé zdroje jsou nedostupné (PubMed offline)"
  - Tlačítko: "Zkusit znovu"
- Benjamin může stále odpovídat (degraded mode):
  - "⚠️ Odpovídám na základě cache, některé zdroje nejsou aktuální."

### API Rate Limit
- Warning message:
  - "⏱️ Dosáhli jste denního limitu dotazů (50/50)"
  - "Upgrade na Premium pro neomezený přístup"

### Neúspěšná Generování
- Error v Benjamin response bubble:
  - "❌ Omlouvám se, nepodařilo se mi vygenerovat odpověď."
  - "Důvod: [API timeout / Nenalezeny relevantní zdroje]"
  - Tlačítko: "Zkusit znovu" / "Přeformulovat dotaz"

### Nepatřičný Obsah
- Validace user inputu:
  - "⚠️ Benjamin je určen pouze pro zdravotnické profesionály a klinické dotazy."
  - "Nemohu odpovídat na osobní zdravotní dotazy pacientů."

---

## Responzivní Layout

### Modal Mode (Desktop - 1200×800px)
- Full-featured view
- Sidebar visible
- Wide chat area (70% width)

### Extension Mode (Chrome - 800×600px)
- Kompaktní layout
- Sidebar collapsed by default
- Narrower chat bubbles (80% width)
- Bottom input bar vždy visible

### Minimized Extension (400×600px)
- Ultra-compact mode
- Single column
- Hidden toolbars (accessible via dropdown)
- Focus pouze na chat

---

## Keyboard Shortcuts

- `Cmd/Ctrl + K` - Focus na input pole
- `Cmd/Ctrl + /` - Zobrazit shortcuts
- `Cmd/Ctrl + N` - Nová konverzace
- `Cmd/Ctrl + H` - Toggle historie sidebar
- `Esc` - Zavřít modal
- `↑/↓` - Navigace v historii

---

## Performance Optimizations

- Lazy loading historie (virtualized list)
- Debounced typing indicator
- Cached responses (offline mode)
- Incremental streaming (typewriter)
- Image lazy loading v attachments

---

## Accessibility

- ARIA labels pro všechny interaktivní prvky
- Keyboard navigation support
- Screen reader friendly (alt texty, live regions)
- High contrast mode
- Focus indicators
