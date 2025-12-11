# Benjamin - FAB Widget (Floating Action Button) Specification

Entry point do Benjamin AI asistenta v rámci FONS Enterprise systému.

**Kontext:** Content script injected do FONS Enterprise stránek zobrazuje plovoucí FAB widget, který po kliknutí otevírá Benjamin modální okno.

**Účel:** Poskytuje lékaři okamžitý přístup k Benjamin AI asistentovi kdekoli v FONS Enterprise bez nutnosti opouštět aktuální pracovní kontext.

---

## Základní Specifikace

### Rozměry & Pozice
- **Velikost:** 56×56px (standardní Material Design FAB size)
- **Tvar:** Kruh (border-radius: 50%)
- **Pozice:** Fixed position
  - Bottom: 24px (od spodního okraje viewportu)
  - Right: 24px (od pravého okraje viewportu)
- **Z-index:** 1000 (nad většinou FONS Enterprise UI, ale pod modály)

### Visual Design
```css
/* Base State */
width: 56px;
height: 56px;
border-radius: 50%;
background: linear-gradient(135deg, #8B5CF6 0%, #3B82F6 100%);
box-shadow: 0 8px 24px 0 rgba(139, 92, 246, 0.3);
cursor: pointer;
transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
```

### Ikona
- **Icon Type:** AI sparkle/brain icon (white)
- **Icon Size:** 28×28px (centered)
- **Icon Color:** `#FFFFFF`
- **Animation:** Subtle pulse animation (1.5s infinite)

---

## Stavy (States)

### 1. Idle State (Default)
**Visual:**
- Gradient background (purple → blue)
- AI icon (static, white)
- Shadow: 0 8px 24px rgba(139, 92, 246, 0.3)
- Opacity: 1

**Behavior:**
- Visible vždy v pravém dolním rohu
- Breathing animation (subtle scale 1.0 → 1.02 → 1.0, 3s ease-in-out infinite)

### 2. Hover State
**Visual:**
- Shadow increase: 0 12px 32px rgba(139, 92, 246, 0.4)
- Scale: 1.1 (grow)
- Icon: Slight rotation (+5deg)
- Tooltip appears:
  - "Otevřít Benjamin AI" (above FAB)
  - Background: rgba(31, 41, 55, 0.9)
  - Text color: white
  - Padding: 8px 12px
  - Border-radius: 8px
  - Positioned: 8px above FAB

**Transition:**
- Duration: 0.2s
- Easing: cubic-bezier(0.4, 0, 0.2, 1)

### 3. Active/Pressed State
**Visual:**
- Scale: 0.95 (shrink)
- Shadow reduce: 0 4px 16px rgba(139, 92, 246, 0.25)
- Brightness: 90%

**Behavior:**
- Immediate visual feedback při kliknutí
- Duration: 0.1s

### 4. Modal Open State
**Visual:**
- FAB se změní na "minimize" button
- Icon change: AI icon → Minimize icon (― nebo ▼)
- Background: Semi-transparent rgba(139, 92, 246, 0.5)
- Size remains: 56×56px
- Position remains: bottom-right

**Behavior:**
- Kliknutí minimalizuje modal (ale nezavře jej)
- Hover tooltip: "Minimalizovat Benjamin"

**Alternative Design (Skrytí FAB):**
- FAB zmizí (fade out, 0.3s)
- Objeví se znovu až po zavření modalu

### 5. Notification Badge State
**Visual:**
- Red badge v pravém horním rohu FAB:
  - Size: 18×18px (nebo width auto pro 2+ digit numbers)
  - Background: #EF4444 (error red)
  - Text: "1" (počet notifikací)
  - Font: 11px, bold, white
  - Border: 2px solid white (pro contrast s FAB)
  - Position: top: -4px, right: -4px

**Use Cases:**
- Nová zpráva v otevřené konverzaci (ale modal není viditelný)
- Dokončeno generování epikrízy
- Chybová notifikace (zdroj offline)
- MCP tool degraded warning

**Animation:**
- Badge appears: Scale from 0 → 1.2 → 1 (bounce effect, 0.4s)
- Badge pulse: Subtle scale 1 → 1.1 → 1 každých 2s

### 6. Loading/Processing State
**Visual:**
- Icon: Spinning loader (circle segments)
- Background gradient animates (rotating gradient)
- Tooltip: "Benjamin zpracovává..."

**Use Cases:**
- Když uživatel klikne a modal se načítá
- Když probíhá dlouhá operace (export audit trail)

**Animation:**
- Spin: 360deg rotation, 1s linear infinite

### 7. Error/Offline State
**Visual:**
- Background: Grayscale (desaturated purple)
- Icon: Warning icon (⚠️) nebo offline icon (📡❌)
- Tooltip: "Benjamin je offline - zkontrolujte připojení"
- Opacity: 0.6

**Behavior:**
- Kliknutí zobrazí error dialog místo modalu:
  - "⚠️ Benjamin je momentálně nedostupný"
  - "Důvod: [Ztráta připojení k internetu / API timeout]"
  - Button: "Zkusit znovu"

### 8. Minimized State (Collapsed FAB)
**Visual:**
- Smaller size: 40×40px (compact)
- Semi-transparent: opacity 0.7
- Icon: Pouze AI symbol (bez textu)
- Tooltip: "Rozbalit Benjamin"

**Use Cases:**
- User má minimalizovaný modal (background work)
- Chce méně vizuálního clutteru

**Transition:**
- User může přetáhnout (drag) FAB do jiné pozice
- Double-click: Toggle mezi 56px ↔ 40px size

---

## Interakce & Chování

### Click Behavior
**Primary Click (První Otevření):**
1. User klikne na FAB
2. FAB scale animation (active state, 0.1s)
3. Modal fade-in animation (0.3s):
   - Modal appears: opacity 0 → 1
   - Modal scale: 0.95 → 1
   - Backdrop blur: 0px → 8px
4. FAB state changes to "Modal Open"

**Click při Otevřeném Modalu:**
- Závisí na nastavení (user preference):
  - **Option A:** Minimalizuje modal (modal shrinks to FAB)
  - **Option B:** Zavře modal (modal fade out)

### Drag Behavior (Optional)
**User může přetáhnout FAB:**
- Draggable area: Celý FAB
- Constraints:
  - Snap to edges (bottom-left, bottom-right, top-right, top-left)
  - Minimum distance from edge: 16px
  - Cannot overlap s FONS Enterprise kritickými UI prvky
- Memory:
  - Position se ukládá do localStorage
  - Při dalším načtení stránky FAB na stejné pozici

### Keyboard Shortcut
- **Global Shortcut:** `Cmd/Ctrl + Shift + B`
  - Opens Benjamin modal (stejně jako kliknutí na FAB)
  - Works anywhere in FONS Enterprise

---

## Animace & Transitions

### Idle Breathing Animation
```css
@keyframes breathe {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.02); }
}

animation: breathe 3s ease-in-out infinite;
```

### Hover Grow
```css
transition: transform 0.2s cubic-bezier(0.4, 0, 0.2, 1);
transform: scale(1.1);
```

### Click Ripple Effect
- Material Design ripple (expanding circle)
- Color: rgba(255, 255, 255, 0.3)
- Duration: 0.6s
- Origin: Click point

### Notification Badge Bounce
```css
@keyframes badgeBounce {
  0% { transform: scale(0); }
  60% { transform: scale(1.2); }
  100% { transform: scale(1); }
}

animation: badgeBounce 0.4s cubic-bezier(0.68, -0.55, 0.27, 1.55);
```

---

## Responzivní Chování

### Desktop (>1024px)
- Full size: 56×56px
- Position: bottom-right (24px, 24px)
- Tooltip above FAB

### Tablet (768px - 1024px)
- Slightly smaller: 48×48px
- Position: bottom-right (16px, 16px)
- Tooltip still visible

### Mobile (<768px)
- Compact size: 48×48px
- Position: bottom-right (16px, 16px)
- Tooltip hidden (tap to open directly)

---

## Accessibility

### ARIA Attributes
```html
<button
  aria-label="Otevřít Benjamin AI asistenta"
  aria-haspopup="dialog"
  aria-expanded="false"
  role="button"
  tabindex="0"
>
  <svg aria-hidden="true"><!-- AI icon --></svg>
</button>
```

### Keyboard Navigation
- **Tab:** Focus na FAB (když je v tab order)
- **Enter/Space:** Aktivuje FAB (open modal)
- **Esc:** Zavře modal (pokud je otevřený)

### Screen Reader
- Announces: "Tlačítko, Otevřít Benjamin AI asistenta"
- Při hover: "Pro otevření stiskněte Enter"
- Při notifikaci: "1 nová zpráva v Benjaminovi"

### Focus Indicator
```css
&:focus-visible {
  outline: none;
  box-shadow: 0 0 0 4px rgba(139, 92, 246, 0.3);
}
```

---

## Chybové Stavy & Edge Cases

### FONS Enterprise Not Detected
- FAB se nezobrazí
- Console warning: "Benjamin: FONS Enterprise context not detected"

### User bez Oprávnění
- FAB visible, ale disabled (opacity 0.4)
- Tooltip: "Nemáte oprávnění k Benjaminovi - kontaktujte správce"
- Click: Shows permission error dialog

### API Offline
- FAB in "Error/Offline State"
- Click: Shows retry dialog

### Multiple FONS Tabs Open
- FAB synchronizace:
  - Když user otevře modal v Tab A, FAB v Tab B shows "Modal Open" state
  - Uses localStorage event listener pro cross-tab communication

---

## Performance Optimizations

### Initial Load
- FAB appears po DOMContentLoaded (neblokuje initial render)
- Icon SVG: inline (žádný external request)
- CSS: critical styles inline, zbytek lazy loaded

### Animation
- Use `transform` and `opacity` (hardware accelerated)
- Avoid `width`, `height`, `left`, `right` animations
- `will-change: transform` pro smooth hover

### Memory
- Remove event listeners při unload
- Cleanup animations při modal close

---

## Technical Implementation Notes

### Content Script Injection
```javascript
// content-script.js
const fabWidget = document.createElement('div');
fabWidget.id = 'benjamin-fab-widget';
fabWidget.innerHTML = `
  <button class="benjamin-fab" aria-label="Otevřít Benjamin AI">
    <svg class="benjamin-fab-icon"><!-- AI icon --></svg>
    <span class="benjamin-fab-badge" hidden>0</span>
  </button>
`;
document.body.appendChild(fabWidget);

// Event listeners
fabWidget.querySelector('.benjamin-fab').addEventListener('click', openBenjaminModal);
```

### Modal Communication
- FAB click → sends message to background script
- Background script → opens modal (iframe or new window)
- Modal loaded → FAB state changes to "Modal Open"

---

## Visual Mockup Variants

### Variant 1: Classic FAB (Recommended)
- Single circular button
- Gradient background
- AI icon centered
- Material Design shadow

### Variant 2: FAB with Label
- FAB + text label "Benjamin"
- Pill shape when expanded (on hover)
- Collapsed: 56×56px circle
- Expanded: 120×56px pill

### Variant 3: Minimal FAB
- Smaller size: 48×48px
- No shadow (flat design)
- Monochrome icon (outline only)
- Subtle hover grow

**Recommendation:** Use Variant 1 (Classic FAB) pro konzistenci s Material Design a Benjamin brand (gradient).

---

## Integration with Modal

### FAB → Modal Relationship
1. **FAB Click:** Triggers modal open
2. **Modal Position:** Centers in viewport (1200×800px)
3. **Backdrop:** Blur(8px) + rgba(0,0,0,0.2)
4. **FAB State:** Changes icon to minimize (― )
5. **Modal Close:** FAB returns to idle state

### Minimize Behavior
**Option A (Recommended):**
- Modal minimizes to FAB position (animated shrink)
- FAB shows notification badge if new messages
- Click FAB to restore modal

**Option B:**
- Modal closes completely (fade out)
- FAB returns to idle state
- Click FAB to re-open modal (new session or restore)

---

## A/B Testing Considerations

### Test Variants:
1. **Position:** Bottom-right vs bottom-left vs top-right
2. **Size:** 56px vs 48px vs 64px
3. **Icon:** AI sparkle vs brain vs chat bubble vs "B" letter
4. **Behavior:** Minimize vs close při druhém kliknutí
5. **Tooltip:** Above vs below vs left side

### Metrics to Track:
- Click-through rate (FAB clicks / page views)
- Time to first interaction (page load → FAB click)
- Minimize vs close preference
- Position change requests (drag events)

---

## Future Enhancements (Post-MVP)

### Smart FAB (Context-Aware)
- **Patient Context Detection:**
  - Když lékař otevře patient detail v FONS Enterprise
  - FAB badge shows "📋 Epikríza ready"
  - Click → directly opens Epikríza tab (ne Chat)

- **Quick Actions Menu:**
  - Long-press FAB → opens radial menu:
    - 💬 Chat
    - 📋 Epikríza
    - 🌍 Translator
    - ⚙️ Settings

### Voice Activation
- "Hey Benjamin" wake word
- Opens modal s voice input ready

### Multi-FAB (Different Tools)
- FAB cluster: Benjamin + Other FONS tools
- Expandable/collapsible cluster

---

**Design Completion:** FAB Widget specification ready for HTML mockup generation.
