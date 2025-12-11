# Benjamin AI - Component Documentation

**Verze:** 1.0
**Datum:** 2026-Q1
**Design System:** Green Healthcare Identity
**Určeno pro:** Frontend vývojáře, UI designéry

---

## 📋 Obsah

1. [Přehled Component Library](#přehled-component-library)
2. [Design Principles](#design-principles)
3. [Core Components](#core-components)
4. [Specialized Components](#specialized-components)
5. [UI Component Libraries](#ui-component-libraries)
6. [Usage Guidelines](#usage-guidelines)
7. [Integration Examples](#integration-examples)
8. [Accessibility](#accessibility)

---

## Přehled Component Library

Benjamin AI Component Library obsahuje **23 production-ready komponent** v jednotné zelené healthcare identitě. Všechny komponenty jsou:

- ✅ **Konzistentní** - Jednotný design systém napříč všemi komponenty
- ✅ **Dostupné** - WCAG 2.1 Level AA compliance
- ✅ **Responzivní** - Optimalizované pro desktop (1200px) i kompaktní view (400px)
- ✅ **Production-ready** - Připravené k implementaci do React/Vue/Angular

### Struktura Souborů

```
workspace/paraflow/
├── Style Guide/
│   └── benjamin_green_healthcare.style-guide.md (Design System)
├── Screen & Prototype/
│   ├── Core Screens (6)
│   ├── Specialized Components (3)
│   ├── Critical Components (6)
│   ├── Enhancement Components (3)
│   └── UI Libraries (3)
└── Feature Plan/
    └── benjamin_component_documentation.md (tento dokument)
```

---

## Design Principles

### 1. Professional Healthcare Identity

**Primární barva:** `#5CB85C` (zelená healthcare)
**Rationale:** Evokuje zdraví, důvěru, profesionalitu v klinickém prostředí

### 2. Flat Design Philosophy

- **Minimální stíny** - Pouze subtilní elevation (0-8px shadows)
- **Sharp corners** - 0-4px border radius (profesionální, ne hravé)
- **Clean borders** - `1px solid #E0E0E0` pro hierarchii
- **No gradients** - Kromě primary button (výjimečně)

### 3. Information Density

**Cílová skupina:** Lékaři (power users) s vysokou IT gramotností
**Priorita:** Efektivita nad estetikou
**Spacing:** Compact (8px base unit) pro maximalizaci obsahu na obrazovce

### 4. Accessibility First

- **Kontrast:** Min. 4.5:1 pro body text, 7:1 pro malý text
- **Focus states:** Viditelné pro keyboard navigation
- **ARIA labels:** Na všech interaktivních prvcích
- **Touch targets:** Min. 44×44px

---

## Core Components

### 1. Chat Interface (Empty State)

**Soubor:** `benjamin_chat_green.html`
**Rozměr:** 1200×800px
**Purpose:** Výchozí obrazovka při otevření Benjamin modalu

#### Anatomy

```
┌─────────────────────────────────────────────────────┐
│ [Green Header: Logo + Tab Nav + User Menu + Close] │
├─────────────────────────────────────────────────────┤
│                                                       │
│           [Brain Icon - Gradient Animation]          │
│                                                       │
│              Dobrý den, doktore 👋                   │
│      Zeptejte se mě na cokoliv - jsem připojený...  │
│                                                       │
│     ┌───────┐  ┌───────┐  ┌───────┐                │
│     │ Card  │  │ Card  │  │ Card  │                 │
│     │   1   │  │   2   │  │   3   │                 │
│     └───────┘  └───────┘  └───────┘                 │
│     ┌───────┐  ┌───────┐  ┌───────┐                │
│     │ Card  │  │ Card  │  │ Card  │                 │
│     │   4   │  │   5   │  │   6   │                 │
│     └───────┘  └───────┘  └───────┘                 │
│                                                       │
├─────────────────────────────────────────────────────┤
│ [Input Bar: Textarea + Icons + Send Button]         │
│ ✅ Připojeno: PubMed • SÚKL • Semantic Scholar      │
└─────────────────────────────────────────────────────┘
```

#### Key Elements

**Green Header Bar:**
- Height: `64px`
- Background: `#5CB85C`
- Color: `#FFFFFF`
- Border radius top: `8px 8px 0 0`

**Tab Navigation:**
- Active tab: Green underline `border-bottom: 2px solid #5CB85C`
- Inactive: Gray text `#616161`, hover `#212121`

**Quick Start Cards (6):**
- Grid: `2×3`
- Size: `280×160px` each
- Border: `1px solid #E0E0E0`
- Hover: `box-shadow: 0 2px 8px rgba(0,0,0,0.08)`

**Input Bar:**
- Background: `#FFFFFF`
- Border top: `1px solid #E0E0E0`
- Textarea: Auto-expanding, max 150px height
- Send button: Green `#5CB85C`, 40×40px

#### Props (pro React implementaci)

```typescript
interface ChatEmptyStateProps {
  userName: string;              // "doktore" nebo konkrétní jméno
  quickStartCards: QuickStartCard[];
  connectionStatus: ConnectionStatus;
  onCardClick: (cardId: string) => void;
  onSendMessage: (message: string) => void;
}

interface QuickStartCard {
  id: string;
  icon: IconType;               // 'search' | 'pills' | 'document' | etc.
  title: string;
  category: string;             // "Diagnostika", "Léky", etc.
  prompt: string;               // Full prompt to send
}

interface ConnectionStatus {
  online: boolean;
  sources: Array<{
    name: string;               // "PubMed", "SÚKL", etc.
    status: 'online' | 'offline';
  }>;
}
```

#### Usage Example

```tsx
// React Example
import { ChatEmptyState } from '@/components/benjamin';

<ChatEmptyState
  userName="Dr. Nováková"
  quickStartCards={QUICK_START_CARDS}
  connectionStatus={{
    online: true,
    sources: [
      { name: 'PubMed', status: 'online' },
      { name: 'SÚKL', status: 'online' },
      { name: 'Semantic Scholar', status: 'online' }
    ]
  }}
  onCardClick={(cardId) => handleQuickStart(cardId)}
  onSendMessage={(msg) => handleSendMessage(msg)}
/>
```

#### Accessibility

- **ARIA labels:** `aria-label="Rychlý start - Diagnostika"` na každé kartě
- **Keyboard nav:** Tab pro pohyb mezi kartami, Enter pro aktivaci
- **Screen reader:** Announce card categories and descriptions

---

### 2. Active Chat Conversation

**Soubor:** `benjamin_active_chat.html`
**Rozměr:** 1200×800px
**Purpose:** Chat interface s aktivní konverzací

#### Anatomy

```
┌─────────────────────────────────────────────────────┐
│ [Green Header: Same as empty state]                 │
├─────────────────────────────────────────────────────┤
│                                                       │
│                         ┌─────────────────────────┐ │
│                         │ User Message Bubble     │ │
│                         │ (Right-aligned, gray)   │ │
│                         └─────────────────────────┘ │
│                                                       │
│  ┌──┐                                                │
│  │AI│  Benjamin Response Bubble                      │
│  └──┘  Lorem ipsum dolor sit amet... [1] [2] [3]   │
│                                                       │
│        📚 Zobrazit 3 zdroje ▼                        │
│                                                       │
│        🤔 Možná vás zajímá:                          │
│        [Chip 1] [Chip 2] [Chip 3]                   │
│                                                       │
├─────────────────────────────────────────────────────┤
│ [Input Bar + Connection Status]                     │
└─────────────────────────────────────────────────────┘
```

#### Message Bubble Specs

**User Message:**
- Align: Right (`margin-left: auto`)
- Max width: `70%`
- Background: `#F5F5F5`
- Border radius: `16px 16px 4px 16px`
- Padding: `12px 16px`
- Font size: `14px`
- Line height: `20px`

**AI Response:**
- Align: Left
- Max width: `80%`
- Background: `#FFFFFF`
- Border: `1px solid #E0E0E0`
- Border radius: `4px 16px 16px 16px`
- Padding: `16px 20px`
- Avatar: 32×32px circle, green gradient

**Citations `[1]` `[2]`:**
- Color: `#5CB85C`
- Font weight: `600`
- Clickable: Opens Sources Panel
- Hover: Underline

#### Props

```typescript
interface ActiveChatProps {
  messages: Message[];
  isStreaming: boolean;
  onSendMessage: (message: string) => void;
  onCitationClick: (citationId: string) => void;
}

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  citations?: Citation[];
  followUpSuggestions?: string[];
  timestamp: Date;
}

interface Citation {
  id: string;
  number: number;           // [1], [2], [3]
  source: 'pubmed' | 'sukl' | 'guidelines';
  title: string;
  authors?: string;
  journal?: string;
  year: number;
  pmid?: string;
  doi?: string;
  url: string;
}
```

#### Streaming State

Když `isStreaming: true`:
- Zobrazit typewriter effect (postupné objevování textu)
- Loading indicator na avatar (animated gradient)
- Disable input textarea

---

### 3. Sources Citation Panel

**Soubor:** `benjamin_sources_panel.html`
**Rozměr:** 920×auto px
**Purpose:** Expandable panel zobrazující detaily citací

#### States

**Collapsed (Default):**
```
┌─────────────────────────────────────────┐
│ 📚 Zobrazit 5 zdrojů ▼                  │
└─────────────────────────────────────────┘
```
- Height: `40px`
- Background: `#F5F5F5`
- Border: `1px solid #E0E0E0`
- Cursor: `pointer`
- Hover: Background `#EEEEEE`

**Expanded:**
```
┌──────────────────────────────────────────────────────┐
│ 📚 Zdroje (5) | Filtr: ○ Všechny ⦿ České [▲ Zavřít]│
├──────────────────────────────────────────────────────┤
│ [1] PubMed - PMID: 12345678                         │
│     Effect of SGLT2 inhibitors on cardiovascular... │
│     Zinman B, et al. • N Engl J Med • 2024          │
│     🔗 https://pubmed.ncbi.nlm.nih.gov/12345678     │
├──────────────────────────────────────────────────────┤
│ [2] SÚKL - Databáze léků                            │
│     Empagliflozin (Jardiance) - Souhrn údajů...     │
│     SÚKL • Aktualizace: 15.1.2025                   │
│     🔗 https://www.sukl.cz/...                      │
├──────────────────────────────────────────────────────┤
│ [3] ČLS JEP - České guidelines                      │
│     ...                                              │
└──────────────────────────────────────────────────────┘
```

#### Citation Entry Anatomy

```
┌────────────────────────────────────────────┐
│ [#] [Icon] Source Type - ID                │ ← Header line
│     Title (truncated to 80 chars)          │ ← Title line
│     Authors • Journal • Year               │ ← Meta line
│     🔗 External link                        │ ← Link line
└────────────────────────────────────────────┘
```

**Spacing:**
- Padding: `16px`
- Gap between entries: `12px`
- Border between: `1px solid #EEEEEE`

#### Props

```typescript
interface SourcesPanelProps {
  citations: Citation[];
  isExpanded: boolean;
  onToggle: () => void;
  onCitationClick: (citationId: string) => void;
  filterCzechOnly?: boolean;
}
```

---

### 4. Epikríza Tab

**Soubor:** `benjamin_epicrisis_green.html`
**Rozměr:** 1200×800px
**Purpose:** Automatické generování epikríz

#### Workflow States

**State 1: Ready to Generate**
- Patient Context Banner (zelený checkmark)
- Data source checkboxes (☑️ Dekurzy, Lab, Medikace, Vyšetření)
- Large green button "🤖 Generovat Epikrízu"

**State 2: Generating (15-30s)**
- Multi-stage progress bar (3 stages)
- Current stage highlighted
- Time estimate "~15s zbývá"

**State 3: Generated**
- Rich text editor s vygenerovaným textem
- Toolbar s formátovacími nástroji
- Buttons: "Generovat jinak" | "📤 Exportovat do FONS"

#### Patient Context Banner

```
┌────────────────────────────────────────────────────────────┐
│ 👤 Jan Novák, *15.3.1965 (58 let) | Oddělení: Kardiologie │
│    Hospitalizace: 15.1.2026 - 20.1.2026 (5 dní)           │
│    ✅ Data dostupná                                         │
└────────────────────────────────────────────────────────────┘
```

#### Props

```typescript
interface EpicrisisTabProps {
  patientContext: PatientContext | null;
  dataSources: DataSource[];
  onGenerate: (sources: string[]) => void;
  onExport: (content: string) => void;
  onRegenerate: () => void;
}

interface PatientContext {
  name: string;
  birthDate: Date;
  department: string;
  hospitalizationStart: Date;
  hospitalizationEnd: Date;
  dataAvailable: boolean;
}

interface DataSource {
  id: 'dekurzy' | 'lab' | 'medikace' | 'vysetreni';
  label: string;
  count: number;        // Počet záznamů
  enabled: boolean;     // Checkbox state
}
```

---

### 5. FAB Widget (Floating Action Button)

**Soubor:** `benjamin_fab_widget_states.html`
**Purpose:** Entry point pro otevření Benjamin modalu z FONS systému

#### States (8 variants)

**1. Idle (Default):**
- Size: `56×56px`
- Shape: Circle
- Background: `#5CB85C`
- Icon: Brain (white)
- Shadow: `0 2px 8px rgba(92, 184, 92, 0.3)`
- Animation: Subtle breathing (scale 1.0 → 1.02)

**2. Hover:**
- Scale: `1.05`
- Shadow: `0 4px 12px rgba(92, 184, 92, 0.4)`
- Cursor: `pointer`

**3. Active (Pressed):**
- Background: `#45A049` (darker)
- Scale: `0.98`

**4. Modal Open:**
- Icon: Checkmark or minimize icon
- Background: `#45A049`

**5. Notification Badge:**
- Red circle `16×16px` top-right
- Background: `#F44336`
- Color: `#FFFFFF`
- Content: Number "3" or dot

**6. Loading:**
- Spinning animation
- Loading indicator inside
- Opacity: `0.8`

**7. Error:**
- Background: `#F44336` (red)
- Icon: Alert/exclamation
- Pulse animation

**8. Minimized:**
- Size: `40×40px` (smaller)
- Same styling but scaled down

#### Positioning

```css
.benjamin-fab {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 9998; /* Below modal (9999) */
}
```

#### Props

```typescript
interface FABWidgetProps {
  state: 'idle' | 'hover' | 'active' | 'open' | 'loading' | 'error' | 'minimized';
  notificationCount?: number;
  onClick: () => void;
  onMinimize?: () => void;
}
```

---

## Specialized Components

### 6. Patient Context Banner

**Soubor:** `benjamin_patient_banner.html`
**Purpose:** Reusable banner zobrazující patient context v Epikríza tab

#### States

**Success (Data Available):**
```css
background: rgba(76, 175, 80, 0.08); /* Light green */
border-left: 4px solid #4CAF50;
```

**Loading:**
```css
background: rgba(255, 193, 7, 0.08); /* Light yellow */
border-left: 4px solid #FFC107;
```

**Error:**
```css
background: rgba(244, 67, 54, 0.08); /* Light red */
border-left: 4px solid #F44336;
```

#### Props

```typescript
interface PatientBannerProps {
  status: 'loading' | 'success' | 'error';
  patient?: {
    name: string;
    birthDate: Date;
    department: string;
    hospitalization: {
      start: Date;
      end: Date;
      days: number;
    };
  };
  errorMessage?: string;
  onRetry?: () => void;
}
```

---

### 7. MCP Connection Status Bar

**Soubor:** `benjamin_connection_status.html`
**Purpose:** Bottom bar zobrazující real-time connection status k MCP tools

#### States

**All Online (Green):**
```
✅ Připojeno: PubMed • SÚKL • Semantic Scholar • MEDLINE • ČLS JEP
```

**Partial Online (Yellow):**
```
⚠️ 4/5 zdrojů připojeno: PubMed • SÚKL • Semantic Scholar • MEDLINE • ❌ ČLS JEP offline
```

**All Offline (Red):**
```
❌ Žádné zdroje dostupné. Zkontrolujte připojení k internetu. [🔄 Zkusit znovu]
```

**Degraded Mode (Orange):**
```
⚡ Omezený režim: Odpovídám z cache. Některé zdroje nedostupné.
```

#### Visual Style

```css
.connection-status {
  padding: 8px 16px;
  font-size: 13px;
  border-top: 1px solid #E0E0E0;
}

.status-online {
  background: rgba(76, 175, 80, 0.08);
  color: #2E7D32;
}

.status-partial {
  background: rgba(255, 193, 7, 0.08);
  color: #F57C00;
}

.status-offline {
  background: rgba(244, 67, 54, 0.08);
  color: #C62828;
}
```

#### Props

```typescript
interface ConnectionStatusProps {
  sources: Array<{
    name: string;
    status: 'online' | 'offline';
    responseTime?: number; // ms
  }>;
  mode: 'online' | 'partial' | 'offline' | 'degraded';
  onRetry?: () => void;
}
```

---

## UI Component Libraries

### 8. Loading States

**Soubor:** `benjamin_loading_states_green.html`
**Purpose:** Reusable loading indicators pro různé use cases

#### Variants

**1. Streaming AI Response Skeleton:**
```
┌──────────────────────────────────────┐
│ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │
│ ░░░░░░░░░░░░░░░░░░░░░░░░░░░         │
│ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░      │
│ ░░░░░░░░░░░░░░░░ ▊                  │ ← Blinking cursor
└──────────────────────────────────────┘
```

**CSS:**
```css
.skeleton-line {
  background: linear-gradient(
    90deg,
    #E0E0E0 25%,
    #F5F5F5 50%,
    #E0E0E0 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}
```

**2. Multi-Stage Progress:**
```
Načítám data... ● ○ ○
              [████░░░░░░░░░░░░] 33%
```

**3. Circular Spinner:**
```
    ⟳
```
Green spinning circle, 24×24px

#### Props

```typescript
interface LoadingStateProps {
  variant: 'skeleton' | 'progress' | 'spinner';
  stage?: number;      // For multi-stage
  totalStages?: number;
  percentage?: number;
  message?: string;
}
```

---

### 9. Error States

**Soubor:** `benjamin_error_states_green.html`
**Purpose:** Error & empty state messaging

#### Variants

**API Rate Limit:**
```
┌──────────────────────────────────────────┐
│ ⚠️ Denní limit dotazů vyčerpán           │
│                                           │
│ Využili jste všech 50 dotazů dnes.       │
│ Limit se obnoví: Zítra v 00:00          │
│                                           │
│ [Upgrade na Premium]                     │
└──────────────────────────────────────────┘
```

**No Connection:**
```
┌──────────────────────────────────────────┐
│ ❌ Nepodařilo se připojit k PubMed       │
│                                           │
│ Zkontrolujte připojení k internetu       │
│ a zkuste to znovu.                       │
│                                           │
│ [🔄 Zkusit znovu]                        │
└──────────────────────────────────────────┘
```

**Empty State:**
```
┌──────────────────────────────────────────┐
│           🔍                              │
│                                           │
│     Žádné výsledky nenalezeny            │
│                                           │
│ Zkuste upravit vyhledávací dotaz         │
│                                           │
│ [Vymazat filtry]                         │
└──────────────────────────────────────────┘
```

#### Props

```typescript
interface ErrorStateProps {
  type: 'rate-limit' | 'connection' | 'generation-failed' | 'empty';
  title: string;
  message: string;
  action?: {
    label: string;
    onClick: () => void;
  };
}
```

---

## Usage Guidelines

### Color Usage

**DO:**
- ✅ Use `#5CB85C` green for primary actions, success states, active elements
- ✅ Use `#F44336` red only for errors, destructive actions
- ✅ Use `#FFC107` yellow/amber for warnings, loading states
- ✅ Use `#212121` for primary text, `#616161` for secondary

**DON'T:**
- ❌ Don't use green for error states
- ❌ Don't use red for success confirmations
- ❌ Don't use low-contrast colors (below 4.5:1)

### Spacing

**8px Base Unit System:**
```
4px  - Micro spacing (icon-text gap)
8px  - Tight spacing (inline elements)
12px - Compact spacing (button padding)
16px - Default spacing (card padding)
24px - Medium spacing (section gaps)
32px - Large spacing (major sections)
```

### Typography

**Font Stack:**
```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto',
             'Helvetica Neue', Arial, sans-serif;
```

**Hierarchy:**
```
24px / 600 - Page title
20px / 600 - Section header
18px / 600 - Card title
14px / 400 - Body text (default)
13px / 400 - Secondary text
12px / 500 - Labels (uppercase)
```

---

## Integration Examples

### React Component Integration

```tsx
// 1. Import components
import {
  ChatInterface,
  EpicrisisTab,
  TranslatorTab,
  SettingsTab,
  FABWidget
} from '@/components/benjamin';

// 2. Main App Layout
function BenjaminApp() {
  const [activeTab, setActiveTab] = useState('chat');
  const [modalOpen, setModalOpen] = useState(false);

  return (
    <>
      {/* FAB Widget - Entry Point */}
      <FABWidget
        state={modalOpen ? 'open' : 'idle'}
        onClick={() => setModalOpen(true)}
      />

      {/* Modal Window */}
      {modalOpen && (
        <BenjaminModal
          activeTab={activeTab}
          onTabChange={setActiveTab}
          onClose={() => setModalOpen(false)}
        >
          {activeTab === 'chat' && <ChatInterface />}
          {activeTab === 'epicrisis' && <EpicrisisTab />}
          {activeTab === 'translator' && <TranslatorTab />}
          {activeTab === 'settings' && <SettingsTab />}
        </BenjaminModal>
      )}
    </>
  );
}
```

### CSS Variables Setup

```css
:root {
  /* Colors */
  --benjamin-primary: #5CB85C;
  --benjamin-primary-dark: #45A049;
  --benjamin-primary-light: #7CC47C;

  --benjamin-success: #4CAF50;
  --benjamin-warning: #FFC107;
  --benjamin-error: #F44336;
  --benjamin-info: #2196F3;

  --benjamin-text-primary: #212121;
  --benjamin-text-secondary: #616161;
  --benjamin-text-hint: #9E9E9E;

  --benjamin-bg-primary: #FFFFFF;
  --benjamin-bg-secondary: #F5F5F5;
  --benjamin-border: #E0E0E0;

  /* Spacing */
  --benjamin-space-xs: 4px;
  --benjamin-space-sm: 8px;
  --benjamin-space-md: 16px;
  --benjamin-space-lg: 24px;
  --benjamin-space-xl: 32px;

  /* Typography */
  --benjamin-font-body: 14px;
  --benjamin-font-small: 13px;
  --benjamin-font-caption: 12px;

  /* Borders */
  --benjamin-radius-sm: 3px;
  --benjamin-radius-md: 4px;
  --benjamin-radius-lg: 6px;

  /* Shadows */
  --benjamin-shadow-sm: 0 1px 3px rgba(0,0,0,0.06);
  --benjamin-shadow-md: 0 2px 8px rgba(0,0,0,0.08);
  --benjamin-shadow-lg: 0 4px 16px rgba(0,0,0,0.12);
}
```

---

## Accessibility

### Keyboard Navigation

**Tab Order:**
1. Header navigation (tabs)
2. Main content area (cards, messages, forms)
3. Input bar
4. Footer actions

**Shortcuts:**
- `Cmd/Ctrl + K` - Focus input
- `Cmd/Ctrl + /` - Show shortcuts
- `Escape` - Close modal
- `Tab` - Next element
- `Shift + Tab` - Previous element

### Screen Reader Support

**ARIA Labels Example:**
```html
<button
  aria-label="Odeslat zprávu do Benjamin AI"
  aria-disabled="false"
>
  <SendIcon />
</button>

<div
  role="region"
  aria-label="Chat konverzace"
  aria-live="polite"
>
  <!-- Messages -->
</div>
```

### Focus States

**Visual Indicator:**
```css
*:focus-visible {
  outline: 2px solid var(--benjamin-primary);
  outline-offset: 2px;
  border-radius: 4px;
}
```

### Color Contrast

**Minimum Ratios (WCAG 2.1 Level AA):**
- Body text (14px+): 4.5:1 ✅
- Large text (18px+): 3:1 ✅
- UI components: 3:1 ✅
- Green `#5CB85C` on white: 3.3:1 (suitable for large text only)
- Black `#212121` on white: 16.1:1 ✅

---

## Performance Guidelines

### Loading Strategy

**Critical Components (Above the fold):**
- Load immediately: Header, Chat empty state, Input bar

**Below the fold:**
- Lazy load: History cards, Settings panels

**Code Splitting:**
```tsx
// Lazy load tabs
const EpicrisisTab = lazy(() => import('./tabs/EpicrisisTab'));
const TranslatorTab = lazy(() => import('./tabs/TranslatorTab'));
```

### Image Optimization

- FAB icon: Inline SVG (< 1KB)
- User avatars: 32×32px WebP
- Quick Start icons: SVG sprites

### Animation Performance

**Use GPU-accelerated properties:**
```css
/* ✅ GOOD */
transform: translateY(10px);
opacity: 0.8;

/* ❌ AVOID */
top: 10px;
height: 100px;
```

---

## Testing Checklist

### Visual Regression
- [ ] Screenshot comparison všech komponent
- [ ] Cross-browser testing (Chrome, Firefox, Safari, Edge)
- [ ] Responsive breakpoints (1200px, 800px, 400px)

### Functionality
- [ ] Tab navigation funguje
- [ ] Form submission funguje
- [ ] Loading states správně
- [ ] Error states správně
- [ ] Keyboard navigation

### Accessibility
- [ ] WCAG 2.1 Level AA compliance
- [ ] Screen reader testování (NVDA, JAWS, VoiceOver)
- [ ] Keyboard-only navigation
- [ ] Color contrast check

### Performance
- [ ] First Contentful Paint < 1.5s
- [ ] Time to Interactive < 3s
- [ ] Lighthouse score > 90

---

## Changelog

**Version 1.0 (2026-Q1)**
- Initial release
- 23 components v zelené healthcare identitě
- Complete design system documentation
- Accessibility compliance
- Interactive prototype

---

## Support & Resources

**Documentation:**
- Style Guide: `/workspace/paraflow/Style Guide/benjamin_green_healthcare.style-guide.md`
- PRD: `/workspace/paraflow/Feature Plan/prd_mvp.md`
- Screen Plans: `/workspace/paraflow/Feature Plan/`

**Component Files:**
- Screens: `/workspace/paraflow/Screen & Prototype/`
- Prototype: `/workspace/paraflow/Screen & Prototype/benjamin_complete.prototype.html`

**Contact:**
- Product Team: Benjamin AI Development
- Design System Owner: Paraflow Design Team
