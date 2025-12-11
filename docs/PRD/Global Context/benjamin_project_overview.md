# Benjamin AI - Project Overview

## Přehled Projektu

**Benjamin AI Klinický Asistent** je komplexní webová aplikace navržená pro české lékaře. Poskytuje AI-poháněné nástroje pro klinickou podporu s přímým přístupem k medicínským zdrojům (PubMed, SÚKL, Semantic Scholar, MEDLINE).

**Vizuální Identita:** Green Healthcare Design System
**Formát:** Modální okno (1200×800px) + Chrome Extension (400-800px)
**Technologie:** HTML/CSS/JavaScript, Claude AI, MCP (Model Context Protocol)

---

## 📁 Struktura Projektu

### Global Context
- `persona_prakticka_lekarka.md` - Primární persona (Dr. Jana Nováková)
- `benjamin_project_overview.md` - Tento dokument

### Feature Plan
- `benjamin_main_chat_screen_plan.md` - Detailní plán hlavního chat interface
- `benjamin_component_documentation.md` (28KB) - Kompletní vývojářská dokumentace

### Style Guide
- `benjamin_green_healthcare.style-guide.md` (12KB) - Vizuální design system
- `benjamin_design_tokens.css` (16KB) - CSS custom properties a utility classes

### Screen & Prototype
**22 HTML komponent + 1 interaktivní prototyp = 23 vizuálních deliverables**

---

## 🎨 Komponenty (22 HTML souborů)

### Core Screens (6 hlavních obrazovek)
1. **benjamin_chat_green.html** (1200px) - Výchozí prázdný stav s Quick Start kartami
2. **benjamin_active_chat.html** (1200px) - Aktivní konverzace s citacemi [1][2][3]
3. **benjamin_epicrisis_green.html** (1200px) - Generování epikríz
4. **benjamin_translator_green.html** (1200px) - Překladač medicínských textů
5. **benjamin_settings_green.html** (1200px) - Nastavení a historie konverzací
6. **benjamin_extension_green.html** (400px) - Kompaktní Chrome extension layout

### Specialized Components (3 originální komponenty)
7. **benjamin_epicrisis_editor_green.html** (670px) - Editor epikríz (podle editor.png)
8. **benjamin_sidebar_menu_green.html** (350px) - Boční menu (podle hamburger.png)
9. **benjamin_ai_modal_green.html** (1440px) - AI modal (podle modalni okno.png)

### Critical Components (6 klíčových komponent)
10. **benjamin_fab_widget_states.html** (920px) - 8 stavů FAB widgetu (Idle, Hover, Active, Open, Badge, Loading, Error, Minimized)
11. **benjamin_sources_panel.html** (920px) - Rozbalovací panel zdrojů s PMID/DOI citacemi
12. **benjamin_patient_banner.html** (1120px) - Banner kontextu pacienta (Success, Loading, Error)
13. **benjamin_connection_status.html** (1200px) - Status MCP připojení (Online, Partial, Offline, Degraded)
14. **benjamin_epicrisis_progress.html** (800px) - Multi-stage progress bar pro generování
15. **benjamin_quick_start_cards.html** (920px) - 6 návrhových karet pro prázdný stav

### Enhancement Components (3 vylepšující komponenty)
16. **benjamin_user_dropdown.html** (360px) - User profile dropdown menu
17. **benjamin_history_card.html** (800px) - Karta historie konverzace (Standard, Hover, Expanded)

### UI Component Libraries (3 knihovny stavů)
18. **benjamin_error_states_green.html** (920px) - 6 chybových/prázdných stavů
19. **benjamin_loading_states_green.html** (920px) - 6 loading variant
20. **benjamin_toasts_green.html** (420px) - 8 typů toast notifikací
21. **benjamin_vzp_demo_green.html** (1200px) - Demo VZP Navigator feature

### Interactive Prototype
22. **benjamin_complete.prototype.html** - Funkční klikatelný prototyp propojující všechny hlavní screeny

---

## 🎨 Design System - Klíčové Hodnoty

### Barvy
```css
Primary Green:   #5CB85C (hlavní zelená)
Hover Green:     #45A049 (hover stav)
Active Green:    #3D8B40 (aktivní stav)
Text Primary:    #212121 (hlavní text)
Background:      #FFFFFF (pozadí)
Border Default:  #E0E0E0 (ohraničení)
```

### Spacing Scale (8px base unit)
```css
--benjamin-space-xs:  4px
--benjamin-space-sm:  8px
--benjamin-space-md:  12px
--benjamin-space-lg:  16px
--benjamin-space-xl:  20px
--benjamin-space-2xl: 24px
--benjamin-space-3xl: 32px
```

### Typography
```css
Font Family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto'
Base Size:   14px
Line Height: 1.5
Weights:     400 (normal), 500 (medium), 600 (semibold), 700 (bold)
```

### Design Principles
1. **Professional & Clinical** - Čistý, minimalistický design
2. **Green Healthcare Identity** - Důvěra a asociace se zdravotnictvím
3. **Flat Design** - Minimální stíny, spoléhání na ohraničení
4. **Information Density** - Efektivita před estetikou pro power users

---

## 📋 Klíčové Features (z PRD)

### Fáze 1 - Core Features
**A. Hlavní Chat Interface s MCP Nástroji**
- Prázdný stav s Quick Start kartami ✅
- Aktivní konverzace s inline citacemi [1][2][3] ✅
- Rozbalovací Sources Panel s detaily ✅
- Connection Status Indicator ✅

**B. Generátor Epikríz**
- Patient Context Banner ✅
- Multi-stage progress bar (15-30s) ✅
- Rich text editor s formátovacími nástroji ✅

**C. Překladač Medicínských Textů**
- Dvousloupcový layout ✅
- Nastavení překladu ✅

**D. Nastavení a Historie**
- Conversation History Cards ✅
- User Profile Dropdown ✅

**E. Chrome Extension**
- FAB Widget (8 stavů) ✅
- Kompaktní layout (400px) ✅

### Fáze 2 - Planned Features
- DeepConsult (detailní konzultace)
- VZP Navigator (úhradová navigace) - Demo vytvořeno ✅
- Audit Trail (právní dokumentace)

---

## 🎯 Persona - Dr. Jana Nováková

**Role:** Praktická lékařka, 45 let, Třebíč
**Potřeby:**
- Rychlé odpovědi během vyšetření (< 30 sekund)
- Důvěryhodné zdroje s citacemi (právní ochrana)
- České rozhraní s přístupem k anglickým zdrojům
- Snížení administrativní zátěže

**Frustrace:**
- Fragmentace informací (3-4 různé weby)
- Jazyková bariéra (časová ztráta)
- 30% času na dokumentaci místo péče
- Nedostatek právní ochrany při kontrolách

**Typické Úkoly:**
- Kontrola lékových interakcí (warfarin + SSRI)
- Ověření guidelines (diabetes 2. typu)
- Kontrola VZP úhrady léků
- Generování epikríz po hospitalizaci
- Diferenciální diagnostika

---

## 📦 Deliverables - Kompletní Seznam

### Vizuální Komponenty (23 HTML souborů)
✅ 6 Core Screens (Chat, Epikríza, Translator, Settings, Extension, VZP Demo)
✅ 3 Specialized Components (Editor, Sidebar, AI Modal)
✅ 6 Critical Components (FAB, Sources, Patient Banner, Connection Status, Progress, Quick Start)
✅ 3 Enhancement Components (User Dropdown, History Card)
✅ 3 UI Libraries (Error States, Loading States, Toasts)
✅ 1 Interactive Prototype

### Dokumentace (3 soubory)
✅ Style Guide (12KB) - Vizuální design system
✅ Design Tokens (16KB) - CSS custom properties
✅ Component Documentation (28KB) - Vývojářská dokumentace

### Kontext (2 soubory)
✅ Persona - Dr. Jana Nováková
✅ Screen Plan - Detailní plán hlavního interface

**Celkem: 27 deliverables** (23 HTML + 3 dokumentace + 1 persona)

---

## 🚀 Jak Použít Tento Design System

### Pro Designéry
1. Otevřete **benjamin_complete.prototype.html** pro interaktivní demo
2. Prostudujte **benjamin_green_healthcare.style-guide.md** pro vizuální guidelines
3. Reference jednotlivé HTML komponenty pro detailní implementaci

### Pro Vývojáře
1. Importujte **benjamin_design_tokens.css** do vašeho projektu
2. Použijte CSS custom properties: `color: var(--benjamin-primary)`
3. Reference **benjamin_component_documentation.md** pro TypeScript interfaces a props
4. Použijte utility classes: `.benjamin-button-primary`, `.benjamin-p-md`

### Pro Product Managery
1. Otevřete **benjamin_main_chat_screen_plan.md** pro feature specifikaci
2. Reference **persona_prakticka_lekarka.md** pro uživatelské potřeby
3. Použijte **benjamin_complete.prototype.html** pro stakeholder demos

---

## 📊 Technické Specifikace

### Modal Window
- **Rozměry:** 1200×800px (desktop), 90vw×90vh (tablet), 100vw×100vh (mobile)
- **Layout:** Fixed header (64px) + scrollable content + fixed footer
- **Z-index:** 9999 (modal), 9998 (backdrop)

### Chrome Extension
- **Rozměry:** 400×600px (minimized), 800×600px (expanded)
- **Modes:** Popup, Side Panel
- **Layout:** Icon-only tabs, compact spacing

### Accessibility
- **WCAG Level:** 2.1 Level AA compliance
- **Keyboard Navigation:** Full support (Tab, Enter, Esc, Arrows)
- **Screen Readers:** ARIA labels, live regions, alt texts
- **High Contrast:** @media (prefers-contrast: high)
- **Reduced Motion:** @media (prefers-reduced-motion: reduce)

### Performance
- **Loading Time:** < 2s for initial load
- **Streaming:** Typewriter effect for AI responses
- **Caching:** Offline mode support
- **Lazy Loading:** Images and history virtualization

---

## 🔐 Compliance & Legal

### Czech Healthcare Regulations
- **Vyhláška 98/2012 Sb.** - Zdravotnická dokumentace
- **SÚKL** - Státní ústav pro kontrolu léčiv integration
- **VZP** - Všeobecná zdravotní pojišťovna API
- **ČLS JEP** - Česká lékařská společnost guidelines

### Data Protection
- **GDPR Compliance** - EU data protection
- **Medical Confidentiality** - Patient data encryption
- **Audit Trail** - Legal documentation of AI decisions

---

## 🎉 Status Projektu

**Design Phase:** ✅ COMPLETED
**Component Library:** ✅ COMPLETED (23 HTML components)
**Documentation:** ✅ COMPLETED (28KB developer docs)
**Design System:** ✅ COMPLETED (Style guide + CSS tokens)
**Interactive Prototype:** ✅ COMPLETED

**Next Steps:**
- Frontend Implementation (React/Vue/Svelte)
- MCP Tool Integration (PubMed, SÚKL APIs)
- Claude AI Backend Setup
- User Testing with Czech Doctors
- Regulatory Approval Process

---

## 📞 Contact & Resources

**Project:** Benjamin AI Klinický Asistent
**Platform:** Web (Modal) + Chrome Extension
**Target Users:** České praktické lékařky a lékaři
**Design System:** Green Healthcare Identity

**Key Files:**
- Interactive Demo: `Screen & Prototype/benjamin_complete.prototype.html`
- Style Guide: `Style Guide/benjamin_green_healthcare.style-guide.md`
- CSS Tokens: `Style Guide/benjamin_design_tokens.css`
- Dev Docs: `Feature Plan/benjamin_component_documentation.md`

---

*Poslední aktualizace: 22. listopadu 2025*
*Design System Version: 1.0*
*Všechny komponenty jsou připraveny pro production handoff*
