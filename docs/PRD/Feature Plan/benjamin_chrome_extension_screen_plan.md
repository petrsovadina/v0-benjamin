# Benjamin - Chrome Extension View
Benjamin jako Google Chrome rozšíření s kompaktním UI optimalizovaným pro browser popup a side panel.

**Formáty:**
- 🪟 **Browser Popup:** 400×600px (kliknutím na ikonu v toolbar)
- 📱 **Side Panel:** 400×full height (Chrome Side Panel API)
- 🔲 **Floating Widget:** Overlay na FONS Enterprise stránce

---

## Architektura Extension

### Deployment Modes

**1. Browser Popup (Default)**
- Kliknutí na Benjamin ikonu v Chrome toolbar
- Fixní velikost: 400×600px
- Always-on-top overlay
- Quick access všem funkcím

**2. Side Panel Mode**
- Chrome Side Panel API (Chrome 114+)
- Šířka: 400px, Výška: full viewport
- Persistent across tabs
- Anchor: pravá strana browseru

**3. Content Script Injection (FONS Integration)**
- Floating button/widget na FONS Enterprise stránce
- Kliknutím otevře modal (podobně jako hlavní modal view)
- Context-aware (detekuje pacientská data z FONS)

---

## Browser Popup View (400×600px)

### Global Layout Structure

```
┌────────────────────────────────────┐
│  Top Bar (40px)                    │  ← Fixed header
├────────────────────────────────────┤
│                                    │
│  Content Area (scrollable)         │  ← Main view (520px)
│                                    │
│                                    │
├────────────────────────────────────┤
│  Bottom Input Bar (40px)           │  ← Fixed footer (pouze pro Chat)
└────────────────────────────────────┘
```

---

### Top Bar (40px, Fixed Header)

**Layout:** Horizontal flex

**Left Side:**
- Logo + Title:
  - "Benjamin" text (12px, bold)
  - AI ikona (16×16px)

**Center:**
- **Compact Tab Switcher:**
  - Icon-only tabs (save space):
    - 💬 (Chat) - active
    - 📋 (Epikríza)
    - 🌍 (Translator)
    - ⚙️ (Settings)
  - Tooltip na hover (label názvu)
  - Active tab: primary color + underline

**Right Side:**
- Utility icons (16×16px):
  - 📌 Pin (toggle always-on-top)
  - ⤢ Expand (opens full modal in new tab)
  - ⚙️ Quick settings
  - ✕ Close

---

## Content Area Views (Scrollable, 520px height)

### 1. Chat View (💬 Tab - Default)

#### Empty State (Compact)
- Mini hero section:
  - Small AI icon (32×32px)
  - Text: "Dobrý den 👋"
  - Compact prompt: "Zeptejte se na cokoliv..."

- **Quick Prompts (Compact Cards):**
  - 2-column grid, smaller cards:
    - "💊 Interakce léků"
    - "🔍 Diagnostika"
    - "📋 Guidelines"
    - "🧪 Lab výsledky"
  - Kliknutím pre-fills input

#### Active Chat View
- **Message Bubbles (Compact):**
  - User messages: right-aligned, max 70% width
  - Benjamin responses: left-aligned, max 80% width
  - Smaller avatars (20×20px)
  - Compact padding (8px vs 16px)
  - Font size: 13px (vs 15px v modalu)

- **Sources Section (Minimal):**
  - Collapsed by default: "📚 3 zdroje"
  - Expanded: slim list (no icons, just links)

- **Action Buttons:**
  - Icon-only (to save space):
    - 👍 👎 📋 📤 🔄
  - Tooltip on hover

#### Bottom Input Bar (40px, Fixed)
- Compact textarea (auto-expand to max 80px)
- Placeholder: "Zeptejte se..."
- Send button (icon-only: ➤)
- Utility:
  - 📎 Attach (icon-only)
  - Character limit: 500 chars (vs 2000 v modalu)

---

### 2. Epikríza View (📋 Tab)

**Optimalizovaný pro Popup:**

#### Header (Compact)
- Title: "📋 Epikríza" (16px)
- Patient context (minimal):
  - Jméno + věk (single line)
  - Collapsible detail (▼ expand)

#### Form (Vertical Stack)
- **Data sources (Simplified):**
  - Checkboxes (smaller, 1 column):
    - ☑️ Dekurzy (12)
    - ☑️ Lab (23)
    - ☑️ Vyšetření (8)
    - ☑️ Medikace (15)
  - "Vše" toggle (select/deselect all)

- **Diagnózy (Compact):**
  - Hlavní: zobrazuje kód + název (truncated)
  - Vedlejší: collapsed list ("+ 3 další")

- **Generate Button:**
  - Full-width button
  - Prominent styling
  - "🤖 Generovat"

#### Output (After Generation)
- Scrollable textarea (read-only)
- Compact formatting
- Action buttons (icon-only):
  - 💾 📋 📄 ✏️

---

### 3. Translator View (🌍 Tab)

**Simplified Layout for Popup:**

#### Settings Bar (Compact)
- Horizontal row:
  - 🇨🇿 [dropdown] ⇄ 🇬🇧 [dropdown]
  - Mode toggle: "Odborný" | "Laický" (small chips)

#### Input/Output (Vertical Stack)
- **Input textarea:**
  - Height: 150px (fixed)
  - Character limit: 1000 (vs 5000)
  - Placeholder: "Text k překladu..."

- **Translate button:**
  - Full-width
  - "🌍 Přeložit"

- **Output display:**
  - Height: 150px (fixed, scrollable)
  - Read-only
  - Copy button (top-right corner)

#### Minimal Toolbar
- Icon-only actions:
  - 📋 Copy
  - 📄 Download
  - 🔄 Swap input/output

---

### 4. Settings View (⚙️ Tab)

**Compact Settings Panel:**

#### Quick Settings
- **Model selection:**
  - Radio buttons:
    - ⚪ Claude Sonnet 4.5
    - ⚪ GPT-4o

- **Language preference:**
  - Toggle: Czech (default) / English

- **Data sources:**
  - Checkboxes (which to enable):
    - ☑️ PubMed
    - ☑️ SÚKL
    - ☑️ Semantic Scholar
    - ☑️ MEDLINE

- **Privacy:**
  - Toggle: "Ukládat historii"
  - Toggle: "Anonymizovat data"

- **Appearance:**
  - Theme: Light / Dark / Auto
  - Font size: Small / Medium / Large

#### Account
- User info (compact):
  - Avatar + Name
  - Email
- Buttons:
  - "Odhlásit se"
  - "Spravovat účet"

#### Footer
- Links:
  - "📖 Nápověda"
  - "🐛 Nahlásit problém"
  - "ℹ️ O aplikaci"
- Version: "v1.0.2"

---

## Side Panel View (400×full height)

**Podobný layout jako Browser Popup, ale:**

### Differences:
- **No height constraint** (využívá full viewport height)
- **Persistent state** (across tabs)
- **Sticky scroll position** (survives tab switches)
- **Enhanced Chat View:**
  - Longer message history visible (20+ messages)
  - No "load more" needed
  - Better for extended conversations

### Side Panel Specific Features:
- **Pin to side panel** button in Top Bar
- **Detach to popup** option (switch modes)
- **Minimize** button (collapses to thin bar with icon)

---

## Content Script Injection (Floating Widget na FONS)

### Entry Point: Floating Button

**Design:**
- Position: Fixed bottom-right (20px margin)
- Size: 56×56px (FAB style)
- Icon: Benjamin logo (AI brain/chip)
- Background: Primary gradient (fialová → modrá)
- Shadow: subtle elevation
- Badge: notification count (unread messages/alerts)

**Interactions:**
- **Click:** Opens modal overlay (800×600px)
- **Long press:** Quick action menu:
  - "💬 Nový chat"
  - "📋 Generovat epikrízu"
  - "🌍 Přeložit text"
- **Drag:** Repositionable (remembers position)

### Modal Overlay (on Click)

**Layout:**
- Size: 800×600px (larger than popup)
- Position: Centered on viewport
- Backdrop: Dark overlay (50% opacity)
- Close: ESC key / click outside / ✕ button

**Content:**
- **Full Tab Interface** (similar to main modal)
- **Context-aware:**
  - Detekuje pacientská data z aktuální FONS stránky
  - Pre-fills jméno, diagnózy v Epikríza tabu
  - Suggests relevant queries in Chat based on page content

**Persistence:**
- Minimized to FAB (doesn't close completely)
- Preserves conversation state
- Quick restore

---

## Keyboard Shortcuts (Extension-Specific)

### Global (Browser-level)
- `Alt + B` - Toggle Benjamin popup
- `Alt + Shift + B` - Open in Side Panel

### Within Extension
- `Cmd/Ctrl + K` - Focus input
- `Cmd/Ctrl + 1/2/3/4` - Switch tabs (Chat/Epikríza/Translator/Settings)
- `Cmd/Ctrl + N` - New chat
- `Esc` - Close popup (if not in input)

---

## Offline Mode

**When Internet Connection Lost:**
- Banner: "⚠️ Offline - připojuji se..."
- **Cached Data:**
  - Last 10 conversations available (read-only)
  - Last used translations visible
  - Settings still editable
- **Degraded Functions:**
  - No new chat queries
  - No new translations
  - Epikríza generování disabled

---

## Notifications & Badges

### Extension Badge (on Icon)
- **Number badge:** Unread messages count
- **Color indicator:**
  - Zelená: Connected
  - Červená: Error/Offline
  - Oranžová: Rate limit warning

### In-Extension Notifications
- Toast messages (top of content area):
  - Success: "✅ Epikríza uložena"
  - Error: "❌ Selhání generování"
  - Warning: "⚠️ Zbývá 5 dotazů dnes"
- Auto-dismiss (3s)

---

## Performance Optimizations (Extension-Specific)

### Size & Loading
- Bundle size: <2MB (minified)
- Lazy load tabs (not all at once)
- Service Worker for background tasks
- IndexedDB for local storage (cache)

### Memory Management
- Limit history to 50 messages (vs unlimited in web)
- Purge old cache after 7 days
- Throttle API calls (max 1 req/sec)

---

## Chrome Extension Manifest (Key Features)

**Permissions Required:**
```json
{
  "permissions": [
    "storage",           // Cache conversations
    "sidePanel",         // Side Panel API
    "activeTab",         // Detect FONS page
    "notifications"      // Desktop notifications
  ],
  "host_permissions": [
    "https://*.digimedic.dev/*"  // FONS Enterprise
  ],
  "background": {
    "service_worker": "background.js"
  },
  "content_scripts": [{
    "matches": ["https://*.digimedic.dev/*"],
    "js": ["content-script.js"]
  }]
}
```

---

## Cross-Platform Sync (Future)

**Sync Across Devices:**
- Chrome Sync API integration
- Sync settings, history, bookmarks
- Real-time updates (WebSocket)
- Conflict resolution (last-write-wins)

---

## Security & Privacy (Extension-Specific)

### Content Security Policy
- No inline scripts
- Strict CSP headers
- HTTPS only

### Data Handling
- Local storage encrypted (IndexedDB)
- Sensitive data (patient info) never cached
- Session timeout (30 min inactivity)
- Auto-logout on browser close

### Permissions Transparency
- Install screen explains why each permission needed
- Settings to revoke permissions
- Audit log (user can see all API calls)

---

## Installation & Onboarding

### First Install Flow
1. Welcome screen (in new tab):
   - "👋 Vítejte v Benjaminovi"
   - Feature highlights (carousel)
   - Login/Sign up

2. Permissions request:
   - Explain each permission
   - "Povolit vše" / "Nastavit později"

3. Quick tour (interactive):
   - "Klikněte na ikonu pro chat"
   - "Zkuste zadat dotaz"
   - "Přepněte mezi funkcemi"

4. FONS Integration setup:
   - "Propojit s FONS Enterprise"
   - OAuth flow / API key input

### Onboarding Tooltips
- First 3 uses: highlight key features
- Dismissable (don't show again)

---

## Update & Maintenance

### Auto-Updates
- Chrome Web Store automatic updates
- Silent updates (no interruption)
- Changelog notification (optional toast)

### Version Migration
- Migrate local storage schema if changed
- Preserve user settings across versions
- Rollback support (if critical bug)

---

## Analytics & Telemetry (Privacy-Respecting)

### Metrics Collected (Opt-in)
- Feature usage counts (anonymous)
- Error rates (crash reports)
- Performance metrics (load times)
- NO patient data, NO query content

### User Control
- Settings toggle: "Sdílet anonymní telemetrii"
- Clear data button: "Smazat vše"
