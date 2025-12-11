# Benjamin - Settings Tab (Nastavení)

Záložka pro správu uživatelského profilu, historie konverzací (audit trail), připojených zdrojů a systémových preferencí.

**Formát:** Modální okno (1200×800px) / Chrome Extension popup (800×600px)

**Účel:** Poskytuje lékařům přístup k audit trail pro právní ochranu, správu historie konverzací, konfigurace MCP zdrojů a osobní preferences.

---

## Globální Struktura

### Top Bar (Sdílená s ostatními tabs)
- Logo/Branding: "Benjamin" + AI ikona
- Horizontal Tab Navigation:
  - 💬 Chat
  - 📋 Epikríza
  - 🌍 Translator
  - **⚙️ Nastavení** (active/highlighted)
- Utility Actions:
  - 👤 User avatar + menu
  - ✕ Close modal

### Content Area (Scrollable)
- Dvousloupcový layout:
  - **Left Sidebar (280px):** Settings navigation menu
  - **Right Panel (920px):** Content area pro vybranou sekci

---

## Left Sidebar Navigation

### Menu Struktura (Vertical List)

**📜 Historie & Audit**
- "Historie konverzací" (default selected)
- "Audit Trail Export"

**🔗 Připojené Zdroje**
- "MCP Nástroje Status"
- "Konfigurace Zdrojů"

**👤 Profil & Preferences**
- "Můj Profil"
- "Jazykové Nastavení"
- "Notifikace"

**ℹ️ O Aplikaci**
- "O Benjaminovi"
- "Co je nového"
- "Nápověda & Dokumentace"

### Vizuální Design Sidebaru
- Background: Jemný gradient nebo glassmorphism
- Active item: Fialové zvýraznění (primary color)
- Hover state: Subtle background change
- Icons: 20×20px, left-aligned

---

## Historie Konverzací (Default View)

### Page Header
- Nadpis: "📜 Historie Konverzací"
- Podnázev: "Kompletní záznam všech vašich interakcí s Benjaminem pro právní ochranu a zpětné dohledání."
- Actions:
  - 🔍 Search box: "Hledat v historii..." (full-text search)
  - 📅 Date range picker: "Tento měsíc ▾"
  - 📥 Export button: "Exportovat historii"

### Filter Bar
- Horizontal chips (toggleable):
  - "Vše" (default)
  - "💬 Chat"
  - "📋 Epikríza"
  - "🌍 Translator"
- Sort dropdown:
  - "Nejnovější první" (default)
  - "Nejstarší první"
  - "Nejčastěji používané"

### Conversation List
**Každá položka (Card Layout):**

```
┌──────────────────────────────────────────────────────┐
│ 💬 Chat Konverzace                     15.1.2026 14:32│
│─────────────────────────────────────────────────────│
│ "Jaké jsou guidelines pro léčbu diabetu 2. typu    │
│  u pacienta s kardiovaskulárním rizikem?"          │
│                                                      │
│ 📚 Zdroje: PubMed • SÚKL • ČLS JEP                 │
│ ⏱️ Délka: 2 minuty • 4 zprávy                       │
│                                                      │
│ [👁️ Zobrazit]  [📋 Kopírovat]  [📤 Exportovat]    │
└──────────────────────────────────────────────────────┘
```

**Komponenty každé položky:**
- **Type Badge:** 💬 Chat / 📋 Epikríza / 🌍 Translator
- **Timestamp:** Relativní ("Dnes 14:32") nebo absolutní ("15.1.2026")
- **Preview:** První dotaz/text (truncated to 120 chars)
- **Metadata:**
  - Použité zdroje (MCP tools ikony)
  - Délka konverzace (čas + počet zpráv)
  - Status: ✅ Úspěšné / ⚠️ Částečné / ❌ Selhalo
- **Action Buttons:**
  - 👁️ **Zobrazit:** Otevře detail konverzace (modal overlay nebo expansion)
  - 📋 **Kopírovat:** Copy celého threadu do schránky
  - 📤 **Exportovat:** Download jako PDF/JSON
  - 🗑️ **Smazat:** Odstranit ze záznamu (confirmation dialog)

### Pagination
- Load more button: "Načíst dalších 20 konverzací"
- Nebo: Infinite scroll s lazy loading
- Indikátor: "Zobrazeno 20 z 156 konverzací"

### Empty State (Žádná Historie)
- Ilustrace: Prázdný archiv
- Text: "Zatím jste neprovedli žádné konverzace s Benjaminem."
- CTA: "Začít konverzaci v Chat tabu →"

---

## Conversation Detail Modal (Po Kliknutí "Zobrazit")

### Modal Overlay (800×600px)
**Header:**
- "📜 Detail Konverzace"
- Timestamp: "15.1.2026, 14:32 - 14:34"
- Close button: ✕

**Content (Scrollable):**
- **Metadata Panel:**
  ```
  📊 Přehled:
  - Typ: Chat konverzace
  - Délka: 2 minuty, 4 zprávy
  - Použité zdroje: PubMed (3 citace), SÚKL (2 citace), ČLS JEP (1 citace)
  - User: Dr. Jana Nováková (jana.novakova@nemocnice.cz)
  ```

- **Full Conversation Thread:**
  - Zobrazení celého threadu (User + Benjamin messages)
  - Inline citace s odkazy: [1], [2], [3]
  - Sources Panel (expandable)
  - Zachováno původní formátování

- **Provenance Information (Pro Audit):**
  ```
  🔒 Audit Trail:
  - Conversation ID: conv_abc123xyz
  - AI Model: Claude Sonnet 4.5 (version: 20250115)
  - MCP Tools: PubMed API v2.3, SÚKL Scraper v1.1, Semantic Scholar v1.0
  - Data zpracování: EU datacenter (Frankfurt)
  - Compliance: GDPR ✓, Vyhláška 98/2012 Sb. ✓
  ```

**Footer Actions:**
- 📥 **Exportovat jako PDF:** Pro právní dokumentaci
- 📋 **Kopírovat jako Text:** Plain text format
- 📤 **Sdílet s kolegou:** Secure link (future feature)
- 🗑️ **Smazat konverzaci:** Confirmation required

---

## Audit Trail Export

### Page Header
- Nadpis: "📥 Audit Trail Export"
- Podnázev: "Exportujte kompletní audit trail všech AI asistovaných rozhodnutí pro právní ochranu nebo kontroly od pojišťovny."

### Export Configuration Form

**Časové Rozmezí:**
- Preset options (chips):
  - "Poslední týden"
  - "Poslední měsíc"
  - "Poslední kvartál"
  - "Celá historie"
- Custom date range picker:
  - Od: [Date picker]
  - Do: [Date picker]

**Typy Interakcí (Checkboxy):**
- ☑️ Chat konverzace (156 záznamů)
- ☑️ Generování epikríz (23 záznamů)
- ☑️ Překlady (45 záznamů)

**Formát Exportu (Radio Buttons):**
- ⚪ **PDF:** Kompletní formátovaný dokument s metadaty
  - ✓ Vhodné pro právní dokumentaci
  - ✓ Obsahuje kompletní citace a zdroje
- ⚪ **CSV:** Tabulkový formát pro analýzu v Excelu
  - ✓ Strukturovaná data (timestamp, query, response, sources)
- ⚪ **JSON:** Technický formát pro další zpracování
  - ✓ Plná struktura dat včetně metadat

**Metadata Inclusions (Checkboxy):**
- ☑️ Časová razítka (timestamps)
- ☑️ Použité MCP zdroje
- ☑️ AI model verze
- ☑️ User ID a credentials
- ☑️ Citace (PMID/DOI odkazy)
- ☑️ GDPR compliance metadata

### Export Preview
- Sample preview (první 3 řádky):
  ```
  Timestamp          | Type      | Query                           | Sources
  ─────────────────────────────────────────────────────────────────────────
  2026-01-15 14:32  | Chat      | Guidelines pro léčbu diabetu... | PubMed, SÚKL
  2026-01-14 09:15  | Epikríza  | Pacient: Jan Novák, *1965...    | FONS data
  2026-01-13 16:45  | Translator| "Adverse reactions: Headache..."| -
  ```

### Action Buttons
- **Primary:** "📥 Exportovat Audit Trail" (prominent button)
- **Secondary:** "👁️ Náhled před exportem" (opens preview modal)
- Loading state: "Generuji export... (15-30 sekund)"

### Legal Disclaimer
- Info box (subtle background):
  ```
  ℹ️ Právní Poznámka:
  Exportovaný audit trail je určen pro právní ochranu lékaře při kontrolách
  od pojišťovny nebo soudních sporech. Obsahuje kompletní provenance
  informace včetně použitých AI modelů, zdrojů a časových razítek dle
  vyhlášky č. 98/2012 Sb.
  ```

---

## MCP Nástroje Status

### Page Header
- Nadpis: "🔗 Připojené Zdroje (MCP Tools)"
- Podnázev: "Přehled stavů všech připojených medicínských zdrojů přes Model Context Protocol."

### Status Dashboard

**Každý MCP Tool (Card Layout):**

```
┌──────────────────────────────────────────────────────┐
│ ✅ PubMed                            Status: Online   │
│─────────────────────────────────────────────────────│
│ PubMed Central database pro medicínské studie       │
│                                                      │
│ 📊 Statistiky (poslední 30 dní):                    │
│ - Dotazů: 156                                       │
│ - Citací: 487                                       │
│ - Průměrná latence: 1.2s                            │
│                                                      │
│ 🔧 Konfigurace:                                     │
│ - API verze: v2.3                                   │
│ - Rate limit: 100/hour (73 zbývá)                  │
│ - Poslední update: 15.1.2026 14:00                 │
│                                                      │
│ [⚙️ Nastavit]  [🔄 Reconnect]  [ℹ️ Dokumentace]   │
└──────────────────────────────────────────────────────┘
```

**MCP Tools List:**
1. **PubMed** (✅ Online)
2. **SÚKL** (✅ Online)
3. **Semantic Scholar** (✅ Online)
4. **MEDLINE** (⚠️ Degraded - high latency)
5. **ČLS JEP Guidelines** (✅ Online)
6. **ScienceDirect** (❌ Offline - maintenance)

**Status Indicators:**
- ✅ **Online:** Zelená tečka, "Funguje normálně"
- ⚠️ **Degraded:** Žlutá tečka, "Zpomalené, ale funkční"
- ❌ **Offline:** Červená tečka, "Nedostupné"

**Global Actions:**
- "🔄 Aktualizovat všechny zdroje"
- "📊 Zobrazit detailní analytics"

### Connection Test
- Button: "🧪 Otestovat všechna připojení"
- Spustí health check pro všechny MCP tools
- Progress bar: "Testuji PubMed... 3/6 dokončeno"
- Result summary:
  ```
  ✅ 5 ze 6 zdrojů funguje správně
  ⚠️ ScienceDirect v údržbě (obnoví se 16.1.2026)
  ```

---

## Můj Profil

### Page Header
- Nadpis: "👤 Můj Profil"
- Podnázev: "Spravujte své osobní údaje a profesionální informace."

### Profile Form

**Osobní Údaje:**
- **Jméno:** Dr. Jana Nováková [Edit button]
- **Email:** jana.novakova@nemocnice.cz [Verified ✓]
- **Telefon:** +420 123 456 789 [Edit button]
- **Foto profilu:** [Avatar upload] (64×64px)

**Profesionální Informace:**
- **Specializace:** Praktické lékařství
- **Pracoviště:** Nemocnice Třebíč, Interní oddělení
- **Licence:** ČLK č. 123456 [Ověřeno ✓]
- **Zkušenosti:** 18 let praxe

**FONS Enterprise Integrace:**
- **FONS User ID:** user_abc123
- **Connected:** ✅ Ano (Naposledy synchronizováno: před 5 minutami)
- **Permissions:** Čtení dat pacientů, Epikríza generování
- Button: "🔄 Resynchronizovat s FONS"

**Account Actions:**
- "🔑 Změnit heslo"
- "🔐 Dvoufaktorová autentizace" (✅ Aktivní)
- "🚪 Odhlásit se ze všech zařízení"

---

## Jazykové Nastavení

### Page Header
- Nadpis: "🌍 Jazykové Nastavení"
- Podnázev: "Vyberte preferovaný jazyk pro interface a odpovědi Benjamina."

### Language Preferences

**Interface Language:**
- Radio buttons:
  - ⚪ **Čeština** (default)
  - ⚪ English
  - ⚪ Slovenčina (future)

**AI Response Language:**
- Radio buttons:
  - ⚪ **Vždy česky** (default)
  - ⚪ Match query language (odpovídá v jazyce dotazu)
  - ⚪ Vždy anglicky

**Translator Default Settings:**
- **Výchozí jazykový směr:** 🇨🇿 → 🇬🇧 [Dropdown]
- **Výchozí režim:** Odborný [Dropdown: Odborný / Zjednodušený]
- **Auto-detect jazyk:** ☑️ Ano

**Medical Terminology:**
- **Preferované terminologie:**
  - ☑️ Latinské názvy (např. "myocardial infarction")
  - ☑️ České ekvivalenty (např. "infarkt myokardu")
  - Priorita: České ekvivalenty s latinskými v závorkách

---

## Notifikace

### Page Header
- Nadpis: "🔔 Notifikace"
- Podnázev: "Spravujte, jak vás Benjamin upozorňuje na důležité události."

### Notification Settings (Toggles)

**Push Notifications (Chrome Extension):**
- ☑️ Nové zprávy v konverzaci
- ☑️ Dokončení generování epikrízy
- ☑️ Chybová hlášení (offline zdroje)
- ☐ Denní shrnutí aktivity

**Email Notifications:**
- ☑️ Týdenní audit trail report
- ☐ Novinky a aktualizace Benjamina
- ☐ Tips & tricks pro lepší používání

**In-App Alerts:**
- ☑️ MCP zdroje offline/degraded
- ☑️ Rate limit upozornění (90% dosaženo)
- ☐ Nové features a changelog

**Do Not Disturb:**
- Toggle: ☐ Zapnuto
- Schedule: "22:00 - 06:00" (quiet hours)

---

## O Benjaminovi

### Page Header
- Nadpis: "ℹ️ O Benjaminovi"
- Logo: Benjamin AI branding

### Product Information

**Verze:**
- Benjamin MVP v1.0
- Build: 2026.01.15.001
- Poslední aktualizace: 15.1.2026

**Technology Stack:**
- AI Model: Claude Sonnet 4.5
- Backend: Supabase (PostgreSQL + pgvector + Edge Functions)
- MCP Tools: PubMed, SÚKL, Semantic Scholar, MEDLINE, ČLS JEP

**Legal & Compliance:**
- ✅ GDPR compliant (EU datacenter - Frankfurt)
- ✅ Vyhláška č. 98/2012 Sb. § 21 (epikríza requirements)
- ⏳ MDR Class IIa certification (Fáze 3)

**Credits:**
- Vytvořil: Paraflow Team
- AI Partner: Anthropic (Claude)
- Data Sources: PubMed, SÚKL, ČLS JEP, Semantic Scholar

**Links:**
- 📄 Privacy Policy
- 📜 Terms of Service
- 🔐 Security & GDPR
- 🐛 Report Bug
- 💡 Feature Request

---

## Co je Nového (Changelog)

### Page Header
- Nadpis: "🆕 Co je Nového"
- Podnázev: "Nejnovější aktualizace a vylepšení Benjamina."

### Changelog Timeline

**Verze 1.0 (15.1.2026) - MVP Launch** 🎉
- ✨ **Nové funkce:**
  - Conversational AI asistent s MCP tools připojením
  - Automatické generování epikríz (Epikríza 0.1)
  - Jazykový překladač (CZ ↔ EN)
  - Chrome Extension (popup + side panel)
  - Audit trail pro právní ochranu
- 🐛 **Opravy:**
  - N/A (první release)
- 🔧 **Vylepšení:**
  - Optimalizovaná latence odpovědí (<5 sekund p95)

**Plánované (Fáze 2 - Q2 2026):**
- 🔮 Upcoming features:
  - Real-time notifications (Supabase Realtime)
  - Offline režim pro Chrome Extension
  - Více jazyků v Translatoru (SK, PL, DE)
  - DeepConsult (hloubková rešerše s full-text studiemi)

---

## Nápověda & Dokumentace

### Page Header
- Nadpis: "❓ Nápověda & Dokumentace"
- Podnázev: "Vše, co potřebujete vědět pro efektivní práci s Benjaminem."

### Help Categories (Cards)

**💡 Rychlý Start**
- "Jak začít s Benjaminem"
- "Psaní efektivních dotazů"
- "Interpretace AI odpovědí a citací"

**🔍 Funkce**
- "Chat: Dotazy na klinické informace"
- "Epikríza: Automatické generování dokumentace"
- "Translator: Překládání medicínského textu"

**🔒 Bezpečnost & Audit**
- "Export audit trail pro právní ochranu"
- "GDPR a ochrana dat pacientů"
- "MCP nástroje a ověřené zdroje"

**🚀 Tipy & Triky**
- "Používání inline citací [1], [2]"
- "Zkratky klávesnice"
- "Integrace s FONS Enterprise"

**📞 Podpora**
- Email: support@benjamin-ai.cz
- Chat podpora: 8:00 - 18:00 (Po-Pá)
- Knowledge Base: help.benjamin-ai.cz

### Search Documentation
- Search box: "Hledat v nápovědě..."
- Populární dotazy:
  - "Jak exportovat audit trail?"
  - "Co dělat, když je PubMed offline?"
  - "Jak citovat Benjamin v epikríze?"

---

## Chybové Stavy

### Nelze Načíst Historie
- Error banner:
  - "⚠️ Nepodařilo se načíst historii konverzací."
  - "Důvod: [Timeout databáze / RLS permissions error]"
  - Button: "Zkusit znovu"

### Export Selhal
- Error modal:
  - "❌ Export audit trail se nezdařil"
  - "Možné příčiny: Příliš velký rozsah dat (zkuste kratší období)"
  - Actions: "Zkusit menší rozsah" / "Kontaktovat podporu"

### MCP Tool Connection Failed
- Warning v status dashboard:
  - "⚠️ Nepodařilo se připojit k PubMed"
  - "Poslední pokus: před 2 minutami"
  - Button: "🔄 Zkusit znovu"

---

## Responzivní Behavior

### Modal Mode (Desktop - 1200×800px)
- Dvousloupcový layout (sidebar + content)
- Full-featured view
- Všechny sekce viditelné

### Extension Mode (Chrome - 800×600px)
- Kompaktnější sidebar (240px)
- Scrollable content area
- Reduced padding

### Minimized Extension (400×600px)
- Sidebar collapsible (hamburger menu)
- Single column content
- Priority na nejdůležitější settings (Historie, Profil)

---

## Keyboard Shortcuts

- `Cmd/Ctrl + ,` - Otevřít Settings tab
- `Cmd/Ctrl + H` - Jump to Historie konverzací
- `Cmd/Ctrl + E` - Export audit trail
- `Cmd/Ctrl + P` - Jump to Profil
- `Esc` - Zavřít Settings, návrat na Chat

---

## Performance Optimizations

- Lazy loading historie (virtualized list, 20 items per page)
- Debounced search (300ms delay)
- Cached MCP status (5 min TTL)
- Progressive image loading v profile avatars
- Background sync pro audit trail

---

## Accessibility

- ARIA landmarks pro navigation menu
- Keyboard navigation support (Tab, Arrow keys)
- Screen reader friendly labels
- Focus indicators na všech interaktivních prvcích
- High contrast mode support
