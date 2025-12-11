# PRD — Benjamin MVP (Fáze 1)

**Vlastník:** Product Team
**Status:** Draft → Review
**Verze:** 1.1
**Datum:** 2026-Q1
**Reference:** Product Charter, Supabase Technical Specification, Feature Inventory, User Flow, Screen Plans

---

## 1) Background

České zdravotnictví čelí kritické krizi personálu a produktivity — lékaři tráví 30% pracovní doby administrativou místo péče o pacienty, systém má minimální digitalizaci (12% ordinací), a informace jsou fragmentované napříč různými zdroji (PubMed, SÚKL, české guidelines). Dr. Nováková, typická praktická lékařka, musí při každém dotazu otevřít 3-4 různé weby, strávit 10+ minut hledáním a překladem anglických zdrojů, což vede k frustraci, chybám v rozhodování a burnoutu. Tento problém adresuje Product Charter v sekci "Core Problem / JTBD" — fragmentace informací, jazyková bariéra a časový deficit.

Benjamin MVP je první iterace AI asistenta pro české lékaře, který poskytuje conversational interface s přímým přístupem k medicínským zdrojům prostřednictvím MCP (Model Context Protocol) nástrojů, automatizuje generování epikríz a překládá medicínskou terminologii. Produkt je dostupný jako modální okno (1200×800px overlay) integrované do FONS Enterprise a jako Chrome Extension (popup 400×600px + side panel 400×full height). Zaměřujeme se na tři primární persony: Dr. Nováková (praktická lékařka, časová tíseň), Dr. Svoboda (kardiolog, potřeba hloubkové rešerše) a Dr. Kučera (urgentní příjem, kritická rozhodnutí). MVP validuje základní product-market fit s 50 pilotními lékaři v Q2 2026, před škálováním na 500+ uživatelů v Fázi 2.

Nyní je správný čas, protože české zdravotnictví prochází legislativní podporou digitalizace (Národní strategie elektronizace 2025-2035, NPO fondy 3 mld Kč), AI technologie dosáhly medical-grade kvality (Claude Sonnet 4.5, RAG architektury), a konkurence je minimální (žádný lokalizovaný AI asistent v ČR). První pilotní projekty (OZP s AI mamografií) ukazují připravenost trhu.

---

## 2) Objectives & Desired Outcomes

- **Outcome A - Úspora času**: Lékaři ušetří minimálně 80% času věnovaného hledání informací — z průměrných 80 minut/den na 5 minut/den (= 312 hodin ročně, ekvivalent 39 pracovních dní). Měřeno: průměrný čas od dotazu k rozhodnutí.

- **Outcome B - Důvěra v AI odpovědi**: Minimálně 90% lékařů hodnotí AI odpovědi jako "helpful" nebo "very helpful" s tím, že inline citace s DOI/PMID zvyšují důvěru v rozhodování. Měřeno: NPS >50, retention >60% po 3 měsících.

- **Outcome C - Snížení administrativní zátěže**: Automatické generování epikríz zkrátí čas na dokumentaci z 20 minut na 2 minuty na hospitalizaci. Lékaři věnují více času přímé péči o pacienty místo manuálnímu vyplňování formulářů. Měřeno: průměrný čas na vytvoření epikrízy, počet manuálních úprav.

- **Outcome D - Bezproblémová integrace do workflow**: Lékaři používají Benjamin přirozeně jako součást svého denního workflow prostřednictvím modálního okna v FONS Enterprise nebo Chrome Extension, bez nutnosti přepínat mezi aplikacemi. Měřeno: průměrně >5 dotazů/den/user, DAU/WAU >40%.

- **Non-goals / Boundaries**:
  - MVP **neposkytuje** autonomní diagnostiku ani terapeutická doporučení (jsme asistent, ne náhrada lékaře)
  - MVP **není** určen pro pacienty, pouze pro healthcare professionals
  - MVP **nezahrnuje** DeepConsult, VZP Navigator, "Generovat jinak", mobile app, nebo full MDR certifikaci (to je Fáze 2-3)
  - MVP **neřeší** celou epikrízu podle vyhlášky 98/2012 Sb. (11 sekcí) — pouze zjednodušená Epikríza 0.1 se 3 datovými zdroji

---

## 3) Users & Stories

### Primary Persona: Dr. Jana Nováková - Praktická Lékařka

**Kontext**: 45 let, 18 let praxe, malé město, 25-30 pacientů denně, středně pokročilá IT uživatelka, používá ICZ IKIS.

- **Story A**: Jako praktická lékařka chci dostat rychlou odpověď na klinický dotaz během vyšetření pacienta, abych nemusela trávit 10+ minut hledáním na více webech a mohla věnovat více času pacientovi.

- **Story B**: Jako praktická lékařka chci vidět, zda je lék hrazený pojišťovnou přímo v odpovědi AI, abych nemusela zvlášť kontrolovat SÚKL a VZP a mohla hned předepsat správnou medikaci.

- **Story C**: Jako praktická lékařka chci mít k dispozici české i mezinárodní guidelines v češtině, abych nemusela překládat anglické zdroje a přesto měla přístup k nejnovějším poznatkům.

- **Story D**: Jako praktická lékařka chci automaticky vygenerovat epikrízu po hospitalizaci pacienta kliknutím na jedno tlačítko, abych ušetřila 20 minut manuálního vyplňování a zkrácení z formulářů.

- **Story E**: Jako praktická lékařka chci mít audit trail všech AI asistovaných rozhodnutí, abych měla právní ochranu při případných kontrolách nebo sporech s pojišťovnou.

### Secondary Persona: MUDr. Petr Svoboda - Kardiolog

**Kontext**: 38 let, 12 let praxe, městská nemocnice, 15-20 pacientů denně, pokročilý IT uživatel, používá PubMed pravidelně.

- **Story F**: Jako kardiolog chci rychle srovnat české kardiologické guidelines (ČKS) s mezinárodními doporučeními (ESC/AHA), abych viděl, kde jsou rozdíly a mohl informovaně rozhodovat.

- **Story G**: Jako kardiolog chci dostat stručné shrnutí nové studie z ESC kongresu během 5 sekund, abych nemusel číst celý 12-stránkový full-text a přesto věděl, jak to ovlivní mou praxi.

- **Story H**: Jako kardiolog chci kontrolovat interakce léků při komplexní medikaci (12+ léků), abych předešel závažným komplikacím a měl okamžité varování při rizikových kombinacích.

### Secondary Persona: Dr. Martin Kučera - Lékař na Urgentním Příjmu

**Kontext**: 32 let, 5 let praxe, fakultní nemocnice, 12-24h směny, velmi pokročilý uživatel, zvyklý na rychlá digitální řešení.

- **Story I**: Jako lékař na urgentním příjmu chci během resuscitace nebo kritické situace dostat okamžitou odpověď na neobvyklou kombinaci symptomů, abych snížil riziko chyby při únavě (noční služby).

- **Story J**: Jako lékař na urgentním příjmu chci mít "safety net" pro diferenciální diagnostiku vzácných případů ve 3 ráno, abych nemusel spoléhat pouze na vlastní unavený úsudek.

---

## 4) Key Features

### Feature A: Conversational AI Asistent (Chat Interface)

**Co uživatel může dělat:**
Lékař otevře Benjamin modální okno (kliknutím na plovoucí FAB widget v FONS Enterprise) nebo Chrome Extension a komunikuje s AI asistentem v přirozeném českém jazyce prostřednictvím chat interface. Zadá klinický dotaz (např. "Jaké jsou guidelines pro léčbu diabetu 2. typu u pacienta s KV rizikem?") a během 5 sekund obdrží stručnou odpověď (3-5 vět) s 2-5 inline citacemi [1], [2], [3] na ověřené zdroje získané prostřednictvím MCP (Model Context Protocol) nástrojů (PubMed, SÚKL, Semantic Scholar, ČLS JEP). Každá citace má rozbalovací panel zdrojů s detaily (název, autor, rok, PMID/DOI/URL). Může pokračovat v konverzaci s follow-up otázkami. Prázdný stav (empty state) zobrazuje 6 Quick Start Cards s návrhy dotazů (Diagnostika, Farmakologie, Guidelines, Lab, Klinický případ, Novinky).

**Primární benefit:**
Úspora 80% času na hledání informací (z 10+ minut na 30 sekund), eliminace jazykové bariéry (vše v češtině), a zvýšená jistota v rozhodování díky evidence-based odpovědím s transparentními zdroji. Conversational interface umožňuje iterativní upřesňování dotazů bez nutnosti začínat znovu.

**Technická implementace (Supabase):**
- MCP (Model Context Protocol) tools pro připojení k medicínským zdrojům (PubMed, SÚKL, Semantic Scholar, MEDLINE, ČLS JEP)
- LLM: Claude Sonnet 4.5 via Supabase Edge Function (benjamin-chat)
- Datové zdroje MVP: PubMed API, SÚKL databáze, Semantic Scholar API, české guidelines (ČLS JEP)
- Automatické logování do ai_queries tabulky s RLS včetně conversation_id pro tracking konverzace
- Response time target: <5 sekund (p95)
- Active Connections Indicator: "✅ Připojeno: PubMed • SÚKL • Semantic Scholar"

### Feature B: Epikríza 0.1 - Automatické Generování Dokumentace (Tab)

**Co uživatel může dělat:**
Lékař v Benjamin modálním okně přepne na záložku "Epikríza" (tab navigation v horní části modalu). Systém automaticky načte kontext aktuálního pacienta z FONS Enterprise (jméno, datum narození, oddělení, hospitalizace) a zobrazí Patient Context Banner. Lékař zkontroluje automaticky zaškrtnuté datové zdroje (☑️ Dekurzy, ☑️ Laboratorní výsledky, ☑️ Medikace, ☑️ Vyšetření) a klikne na tlačítko "🤖 Generovat Epikrízu". Během 15-30 sekund (progress bar) systém vygeneruje strukturovanou epikrízu podle vyhlášky č. 98/2012 Sb. §21. Lékař může použít tlačítko "Generovat jinak" pro alternativní formulaci. Výstup je zobrazen v rich text editoru, který umožňuje úpravy před exportem do FONS Enterprise.

**Primární benefit:**
Zkrácení času na vytvoření epikrízy z 20 minut na 2 minuty (90% úspora), zajištění konzistentní struktury dokumentace, a snížení rizika opomenutí důležitých informací. Lékař se může více soustředit na klinické zhodnocení místo manuálního přepisování. Tab-based interface zajišťuje, že epikríza je součástí jednotného workflow Benjamina.

**Technická implementace (Supabase):**
- Input: JSON payload z FONS Enterprise s patient context, medicalReports, labResults, medications, examinations
- Processing: Supabase Edge Function (epicrisis-generate) → Claude API s prompt template podle vyhlášky §21
- Output: Strukturovaný text v epicrisis_generations tabulce s patient_id, version, is_final flags
- Lékař vždy kontroluje finální text (rich text editor s možností úprav)
- Možnost regenerace (version tracking via parent_id) - tlačítko "Generovat jinak"
- Export do FONS Enterprise přes API integration

### Feature C: Translator - Jazykový Překladač (MVP Základní, Tab)

**Co uživatel může dělat:**
Lékař v Benjamin modálním okně přepne na záložku "Translator". Uvidí dvousloupcový layout (Input Panel 48% | Output Panel 48%) s centrálním tlačítkem "🌍 Přeložit". V horní části je Translation Settings Bar s výběrem jazykového směru (🇨🇿 ⇄ 🇬🇧), režimu překladu (Odborný / Zjednodušený) a swap tlačítkem ⇄. Lékař vloží nebo napíše text do Input Panel (max 5000 znaků), klikne na "🌍 Přeložit" a během 2-5 sekund se v Output Panel zobrazí přeložený text. Má možnost zobrazit terminologický slovník (expandable) s definicemi klíčových pojmů nebo uložit překlad do historie.

**Primární benefit:**
Rychlý překlad odborných textů (SPC léků, studie) bez ztráty medicínské přesnosti, eliminace potřeby externích překladačů (Google Translate často chybí kontext). Dvousloupcový layout umožňuje rychlé srovnání originálního a přeloženého textu. Tab-based interface zajišťuje integraci do jednotného workflow Benjamina.

**Technická implementace (Supabase):**
- Supabase Edge Function (translator) → Claude API s medical translation prompt
- Parametry: text, source_language, target_language, mode (expert/simplified)
- MVP: Pouze základní režimy (Odborný / Zjednodušený) pro jazykový pár CZ ↔ EN
- Translation history: Uložení do translations tabulky s RLS
- Fáze 2: Odborný ↔ Laický, více jazyků (SK/PL/DE), terminologická databáze (SNOMED CT, MeSH)

### Feature D: Integrace - Modální Okno + Chrome Extension

**Co uživatel může dělat:**
Benjamin je dostupný dvojím způsobem:

**(1) Modální okno v FONS Enterprise (1200×800px overlay):** Lékař pracuje v FONS Enterprise a vidí plovoucí FAB widget (56×56px) v pravém dolním rohu. Kliknutím se otevře Benjamin modální okno přes aktuální obsah (overlay). Modální okno má tab-based navigation v horní části (Chat | Epikríza | Translator | Settings) s Chat jako výchozí záložkou. Systém automaticky načte kontext aktuálního pacienta z FONS Enterprise (pokud relevantní pro Epikrízu). Modální okno lze přetahovat (draggable), minimizovat nebo zavřít — nepřerušuje práci v FONS Enterprise.

**(2) Chrome Extension (popup 400×600px + side panel 400×full height):** Lékař klikne na ikonu Benjamin rozšíření v Chrome toolbar. Otevře se popup (400×600px) s kompaktní verzí interface (icon-only tabs) nebo side panel (400×full height) docked to browser edge s plnou konverzační historií. Extension funguje na libovolné stránce, nejen v FONS systému. Content script detekuje FONS stránky a poskytuje context-aware funkce.

**Primární benefit:**
Zero friction workflow — lékař nemusí opouštět známé prostředí FONS Enterprise nebo aktuální browser tab, nepřepíná mezi aplikacemi, a má vše na jednom místě. Context-aware funkce (např. automatické načtení ID pacienta pro epikrízu při použití v FONS) šetří další kliknutí. Chrome Extension umožňuje používat Benjamin kdekoli v browseru (např. při čtení PubMed článků).

**Technická implementace (Supabase):**
- Frontend: Next.js 14 + Supabase JS client (modal), React + Chrome Extension API Manifest V3 (extension)
- Content Script: Injected do FONS Enterprise pro detekci patient context a floating FAB widget
- Auth: Supabase Auth s Azure AD provider, single sign-on across modal + extension
- API: REST calls na Supabase Edge Functions
- Session management: JWT tokens, 1 hodina timeout, sync across devices
- RLS policies zajišťují, že user vidí pouze své data
- Modal draggable/minimizable: Z-index 9999, Escape key close

### Feature E: Audit Trail & Bezpečnost (GDPR by Design)

**Co uživatel může dělat:**
Lékař přepne na záložku "Settings" v Benjamin modálním okně a klikne na "Historie konverzací". Uvidí chronologický seznam všech svých interakcí s Benjaminem (chat dotazy, generování epikríz, překlady) včetně času, typu interakce, vstupu, výstupu a použitých MCP zdrojů. Každý záznam lze rozkliknout pro zobrazení detailu včetně citací s PMID/DOI odkazy. Administrátor nemocnice má přístup k agregovaným metrikám používání (bez osobních dat pacientů) prostřednictvím Supabase Dashboard. Všechna data jsou automaticky logována do audit_logs tabulky s Row Level Security.

**Primární benefit:**
Právní ochrana lékaře ("Řídil jsem se guidelines XYZ z roku 2024, které jsem získal prostřednictvím Benjamin AI asistenta"), compliance s GDPR a vyhláškou 98/2012 Sb., možnost zpětně dohledat rozhodování pro případné kontroly nebo soudní spory. V případě pochybností může kdykoli ověřit, jaké zdroje byly použity pro konkrétní odpověď (včetně PMID/DOI odkazů).

**Technická implementace (Supabase):**
- audit_logs tabulka s RLS (user vidí své, admin vidí všechny)
- Timestamp, user_id, action (chat/epicrisis/translation), resource_id, input, output, mcp_sources JSONB, conversation_id
- Provenance metadata u každé citace (zdroj, datum publikace, PMID/DOI)
- Encryption: TLS 1.3 in transit, AES-256 at rest
- EU hosting: Supabase Frankfurt datacenter
- Export function: CSV export historie pro právní účely

---

## 5) Key Flows

### Example 1: Rychlý Klinický Dotaz (Chat - Happy Path)

- **Trigger**: Dr. Nováková má během vyšetření pacienta s diabetem 2. typu a kardiovaskulárním rizikem pochybnost, jaké léky předepsat.
- **Path**: Klikne na plovoucí FAB widget (56×56px) v pravém dolním rohu FONS Enterprise. Otevře se Benjamin modální okno (1200×800px) s výchozí záložkou "Chat". V prázdném stavu vidí 6 Quick Start Cards — klikne na "Farmakologie" nebo rovnou zadá otázku do chat input: "Jaké jsou guidelines pro léčbu diabetu 2. typu u pacienta s KV rizikem?", stiskne Enter. Během 3 sekund se zobrazí AI odpověď v levém chat bubble s inline citacemi [1], [2], [3] a rozbalovacím panelem zdrojů (Sources Panel). Systém prostřednictvím MCP nástrojů získal data z PubMed, SÚKL a ČLS JEP. Dr. Nováková vidí odpověď s 3 citacemi: [1] ČLS JEP 2024 (české diabetologické guidelines), [2] ESC 2023 guidelines (kardiovaskulární prevence), [3] SÚKL - hrazené SGLT2 inhibitory (empagliflozin, dapagliflozin).
- **Result**: Dr. Nováková má evidence-based odpověď s odkazy na zdroje, ví, že SGLT2 inhibitory jsou preferovány a jsou hrazené VZP, může okamžitě předepsat a věnovat zbývající čas vysvětlení pacientovi. Celá interakce trvala 30 sekund místo 10 minut. Může pokračovat s follow-up otázkou: "Jaké jsou kontraindikace empagliflozinu?" bez nutnosti začínat znovu.

### Example 2: Generování Epikrízy (Epikríza Tab - Happy Path)

- **Trigger**: Dr. Svoboda propouští pacienta po 5 dnech hospitalizace pro akutní infarkt myokardu, musí vytvořit epikrízu.
- **Path**: Otevře Benjamin modální okno v FONS Enterprise (kliknutím na FAB widget), přepne na záložku "Epikríza" v horní tab navigation. Systém automaticky načte kontext aktuálního pacienta z FONS Enterprise a zobrazí Patient Context Banner: "Jan Novák, *1965 (58 let) | Oddělení: Kardiologie | Hospitalizace: 15.1.2026 - 20.1.2026 (5 dní) | Status: ✅ Data dostupná". Lékař zkontroluje automaticky zaškrtnuté datové zdroje (☑️ Dekurzy (8), ☑️ Laboratorní výsledky (23), ☑️ Medikace (15), ☑️ Vyšetření (5)) a klikne na tlačítko "🤖 Generovat Epikrízu". Zobrazí se progress bar (15-30s), systém načte data (lékařské zprávy: anamnéza, průběh; laboratorní výsledky: troponin, lipidogram, KO; medikace: ASA, statiny, betablokátor). Edge Function zavolá Claude API s promptem podle vyhlášky §21. Za 18 sekund se v rich text editoru zobrazí předvyplněný text s 5 sekcemi: identifikace pacienta, diagnózy (I21.0 STEMI přední stěny), průběh hospitalizace, laboratorní výsledky, medikace, doporučení pro ambulantní péči.
- **Result**: Dr. Svoboda zkontroluje vygenerovaný text (nalezne 2 drobné formulační úpravy, opraví je přímo v editoru), klikne na "📤 Exportovat do FONS" a uzavře epikrízu. Celý proces trval 2 minuty místo 20 minut manuálního vyplňování. Epikríza je uložena v epicrisis_generations tabulce s is_final=true a exportována do FONS Enterprise.

### Example 3: Překlad SPC Léku (Translator Tab - Happy Path)

- **Trigger**: Dr. Nováková potřebuje vysvětlit pacientovi vedlejší účinky nového léku z anglického SPC (Summary of Product Characteristics).
- **Path**: Zkopíruje relevantní sekci SPC (např. "Adverse reactions: Headache (common), dizziness (common), nausea (uncommon)...") z PubMed. Otevře Benjamin modální okno, přepne na záložku "Translator". Uvidí dvousloupcový layout (Input Panel | Output Panel). V Translation Settings Bar vybere jazykový směr "🇬🇧 → 🇨🇿" a režim "Zjednodušený" (aby text byl srozumitelný pro pacienta). Vloží zkopírovaný text do Input Panel (levý sloupec), klikne na centrální tlačítko "🌍 Přeložit". Za 3 sekundy se v Output Panel (pravý sloupec) zobrazí překlad: "Vedlejší účinky: Bolest hlavy (časté), závratě (časté), nevolnost (méně časté)...". Může rozkliknout terminologický slovník pro zobrazení definice "časté" = >1/100 až <1/10.
- **Result**: Dr. Nováková má český překlad v pacientsky srozumitelné formě, který může ukázat pacientovi nebo použít pro informovaný souhlas. Ušetřila 5 minut hledání českého SPC nebo používání Google Translate (který často chybí lékařský kontext a pacientsky přívětivou formulaci).

### Example 4: Noční Urgentní Situace (Chat - Critical Use Case)

- **Trigger**: Dr. Kučera má ve 3 ráno na urgentním příjmu pacienta s neobvyklou kombinací symptomů (bolest břicha + neurologické příznaky + leukocytóza). Je unavený po 18 hodinách služby.
- **Path**: Během stabilizace pacienta otevře Benjamin Chrome Extension na tabletu (kliknutím na ikonu rozšíření → side panel 400×full height docked to edge). V chat interface zadá "Diferenciální diagnostika: bolest břicha + neurologické příznaky + leukocytóza". Systém prostřednictvím MCP nástrojů získá data z PubMed a MEDLINE, za 4 sekundy vrátí možné diagnózy s prioritizací podle pravděpodobnosti: "Možné diagnózy: [1] **Porfyrie** (vzácná, ale závažná - bolest břicha + neurologické příznaky patří do klasické triády) [PMID: 12345], [2] Lead poisoning (olověná intoxikace) [PMID: 67890], [3] SLE s neurologickým postižením [PMID: 24680]. Doporučení: U porfyrie kontrolovat delta-aminolevulovou kyselinu (ALA) a porfobilinogen (PBG) v moči." Sources Panel zobrazuje 3 rozkliknutelné zdroje.
- **Result**: Dr. Kučera díky AI "safety net" nezapomněl na vzácnou diagnózu (porfyrie), kterou by při únavě mohl přehlédnout. Nařídil správné vyšetření (delta-aminolevulová kyselina v moči), diagnóza potvrzena. AI asistent **potenciálně zachránil život** tím, že pomohl vyloučit běžnější, ale méně závažné diagnózy. Extension side panel umožnil rychlý přístup bez narušení práce v EHR systému.

### Example 5: Kontrola Lékových Interakcí (Chat - Preventivní Use Case)

- **Trigger**: Dr. Nováková má pacientku (78 let) s 12 léky, psychiatr přidal sertralin (SSRI). Pacientka má nově závratě.
- **Path**: Dr. Nováková otevře Benjamin modální okno, v chat interface zadá: "Interakce sertralin + warfarin + bisoprolol + amlodipine + metformin?". Systém prostřednictvím MCP nástrojů získá data z SÚKL databáze a PubMed, za 3 sekundy vrátí: "**🔴 ZÁVAŽNÁ INTERAKCE**: Sertralin + Warfarin → ↑ riziko krvácení (inhibice CYP2C9), INR může ↑ o 10-50% [1]. **Doporučení**: Častější kontroly INR (za 3-5 dnů, pak týdně). **🟡 MÍRNÁ INTERAKCE**: Sertralin + Bisoprolol → možná bradykardie [2]." Sources Panel zobrazuje [1] PMID 12345 (farmakologická studie), [2] SÚKL - SPC sertralin.
- **Result**: Dr. Nováková okamžitě nařídí kontrolu INR a monitorování srdeční frekvence, předešla potenciálně závažnému krvácení. Bez AI by možná na interakci zapomněla (12 léků = velká kognitivní zátěž). Může pokračovat s follow-up otázkou: "Jak často by měly být kontroly INR?"

### Example 6: Historie Dotazů pro Audit (Settings Tab - Legal Protection)

- **Trigger**: Dr. Svoboda předepsal off-label lék (dronedaron místo amiodaronu) na základě nové studie ESC 2024. Pojišťovna zpochybňuje rozhodnutí při kontrole.
- **Path**: Dr. Svoboda otevře Benjamin modální okno, přepne na záložku "Settings" a klikne na "Historie konverzací". Uvidí chronologický seznam všech svých interakcí s Benjaminem. Vyhledá dotaz z daného data (15.3.2026): "Dronedaron vs amiodaron ESC 2024 - kdy preferovat?". Rozklikne záznam a systém zobrazí původní dotaz, kompletní odpověď AI ("Dronedaron je non-inferior k amiodaronu pro fibrilaci síní, s nižším rizikem thyreoidálních komplikací...") a použité MCP zdroje: [1] PMID 67890: PRAGMATIC-AF study - dronedaron non-inferior, nižší thyreoidální komplikace [2] ESC guidelines 2024. Může exportovat tento záznam jako PDF pro dokumentaci.
- **Result**: Dr. Svoboda exportuje audit trail jako PDF a předloží pojišťovně jako obhajobu rozhodnutí. Pojišťovna akceptuje, že lékař se řídil aktuální studií publikovanou v mezinárodním kardiologickém časopise. **Právní ochrana funguje** - lékař má dokumentované, evidence-based rozhodování s přesnými citacemi zdrojů.

---

## 6) Competitive Analysis

### Landscape - Kdo řeší tento problém

**Mezinárodní konkurenti:**
- **OpenEvidence** - AI asistent pro lékaře, rychlé odpovědi s citacemi, zdarma
- **UpToDate Expert AI** - Premium clinical decision support, $500+/rok, Wolters Kluwer
- **DynaMed + Dyna AI** - RAG-based AI, EBSCO databáze, předplatné
- **ChatGPT/Claude (generic)** - Obecné AI chatboty, široce dostupné

**České alternativy:**
- **ICZ AV(D) Asistent** - AI pro kódování diagnóz, administrativa
- **Manuální workflow** - Lékaři hledají sami na PubMed + SÚKL + guidelines (většina lékařů dnes)

**Cílové publikum:**
- OpenEvidence/UpToDate → Anglicky mluvící lékaři (US/UK/globálně)
- ChatGPT → Široká veřejnost včetně lékařů (experimentálně)
- ICZ → České nemocnice s Enterprise systémy
- Manuální → Všichni čeští lékaři (default)

### Value Thesis - Proposice každého hráče

**OpenEvidence**: "Bezplatný AI asistent s citacemi pro evidence-based medicine" → Trade-off: Jen angličtina, žádná integrace do českých EHR, nepokrývá SÚKL/VZP.

**UpToDate AI**: "Autoritativní klinická znalostní báze s AI asistencí" → Trade-off: Drahé, US-centric guidelines, žádná lokalizace pro ČR.

**ChatGPT/Claude**: "Univerzální AI s medicínskými znalostmi" → Trade-off: Halucinace, žádné citace, není medical-grade, GDPR nejasný.

**ICZ AV(D)**: "Automatizace administrativy pro české nemocnice" → Trade-off: Pouze kódování diagnóz, žádná klinická podpora.

**Manuální workflow**: "Plná kontrola, žádné riziko AI" → Trade-off: Extrémně časově náročné (10+ min/dotaz), fragmentace zdrojů, únava vede k chybám.

**Benjamin**: "První český AI asistent s lokalizací, SÚKL/VZP integrací, MCP tools připojením k medicínským zdrojům, GDPR by design a EHR native integrací (modální okno + Chrome Extension)" → Trade-off: Menší databáze než UpToDate (budeme růst), vyžaduje důvěru v AI (educace potřebná).

### Strengths / Weaknesses - Zkušenostní pro/proti

**OpenEvidence:**
- ✅ **Síla**: Rychlé, kvalitní odpovědi, zdarma, dobře navržené UI
- ❌ **Slabina**: Jazyková bariéra (EN only), chybí české zdroje (SÚKL, VZP), žádná EHR integrace v ČR

**UpToDate AI:**
- ✅ **Síla**: Autoritativní obsah, uzavřený peer-reviewed, EHR integrace (US systémy)
- ❌ **Slabina**: Velmi drahé ($500+/rok), US-centric (české guidelines chybí), složité na adopci pro běžné lékaře

**ChatGPT/Claude:**
- ✅ **Síla**: Flexibilní, dostupné všude, rychlé
- ❌ **Slabina**: Halucinace (bez RAG), žádné citace, není medical-specific, GDPR compliance nejasná, nemocnice to zakážou

**ICZ AV(D):**
- ✅ **Síla**: Česky, integrace do FONS Enterprise, administrativa
- ❌ **Slabina**: Pouze kódování diagnóz, žádná klinická podpora (neodpovídá na Q&A)

**Manuální workflow:**
- ✅ **Síla**: Plná kontrola lékaře, žádné riziko AI chyby
- ❌ **Slabina**: Extrémně pomalé, fragmentace (3-4 weby), únava → chyby, frustrující

### Our Differentiators - Naše jedinečné body

**1. Lokalizace (Brand Keyword: "Lokalizovaný")**
Jsme první a jediný AI asistent plně lokalizovaný pro české zdravotnictví — odpovědi v češtině, české guidelines (ČLS JEP), SÚKL databáze (registrace léků), VZP hrazení, ÚZIS statistiky. Eliminujeme jazykovou bariéru (lékaři nemusí překládat studie) a poskytujeme kontext relevantní pro ČR (co je hrazeno pojišťovnou, jaké jsou české postupy).

**2. Důvěryhodnost (Brand Keyword: "Důvěryhodný")**
Každá odpověď má povinné inline citace (2-5 zdrojů) s přesnými DOI/PMID/URL a paragraph excerpts. RAG architektura eliminuje halucinace (odpovídáme POUZE z dokumentů v databázi). Audit trail každé interakce pro právní ochranu lékaře. Transparentnost zdrojů → lékaři vidí, odkud informace pochází.

**3. Rychlost (Brand Keyword: "Rychlý")**
Odpovědi do 5 sekund (vs. 10+ minut manuální hledání). Supabase Edge Functions (serverless, auto-scaling) + pgvector (native PostgreSQL) zajišťují nízkou latenci. Lékaři šetří 312 hodin ročně = 39 pracovních dní, což je měřitelný ROI 2,526%.

**4. Bezpečnost (Brand Keyword: "Bezpečný")**
GDPR by design s Supabase Row Level Security (RLS) — každý user vidí pouze své data. EU hosting (Frankfurt datacenter), encryption at rest (AES-256) a in transit (TLS 1.3). Audit logs pro compliance s vyhláškou 98/2012 Sb. a připravenost na MDR Class IIa (Fáze 3).

**5. EHR Integrace (Brand Keyword: "Seamless integration")**
Nativní integrace do FONS Enterprise (side-panel), single sign-on (Azure AD), context-aware (automatické načtení pacienta). Lékaři nepřepínají mezi aplikacemi → zero friction workflow. Konkurenti (OpenEvidence, UpToDate) nemají české EHR pluginy.

**Trade-offs, které přijímáme:**
- **Menší databáze než UpToDate**: Máme "pouze" PubMed + SÚKL + české guidelines v MVP (Fáze 2 přidá Cochrane, NICE, BMČ). Ale pokrýváme 80% use cases českých lékařů.
- **Vyžaduje důvěru v AI**: Lékaři musí přestat spoléhat pouze na vlastní paměť a začít používat AI asistenta. Řešíme: Transparentnost (citace), educace (pilotní program), KOL zapojení.
- **Závislost na kvalitě zdrojů**: Pokud české guidelines zaostávají za mezinárodními, AI to odráží. Řešíme: Vždy zobrazujeme i mezinárodní zdroje (PubMed, ESC) pro srovnání.

### Switching Costs & Risks - Migrační náklady a rizika

**Z manuálního workflow na Benjamin:**
- **Switching cost**: Nízký — lékaři pouze přidají nový nástroj (modální okno v FONS Enterprise nebo Chrome Extension), nemusí měnit stávající EHR nebo workflow.
- **Riziko**: Lékaři se musí naučit psát dobré dotazy (prompt engineering). Řešíme: Quick Start Cards s návrhy dotazů, příklady use cases v prázdném stavu, onboarding tutoriál.
- **Rezistence**: Starší lékaři mohou mít nedůvěru k AI ("Nechci, aby mi robot říkal, co dělat"). Řešíme: Framing "asistent, ne náhrada", KOL ambasadoři, transparentnost citací s MCP tools indikátorem.

**Z konkurenčních AI nástrojů (ChatGPT) na Benjamin:**
- **Switching cost**: Téměř nulový — Benjamin je specifický pro medicínu, integrovaný do EHR a dostupný jako modální okno + Chrome Extension (ChatGPT ne).
- **Riziko**: Lékaři si zvykli na flexibility ChatGPT (může odpovídat na cokoliv). Benjamin je úzce zaměřený na klinické dotazy s MCP připojením k medicínským zdrojům. Řešíme: Ukazujeme výhody (citace, GDPR, medical-grade kvalita, zero friction workflow).

**Z UpToDate na Benjamin:**
- **Switching cost**: Nízký — Benjamin je levnější (990 Kč vs. $500+) a má české zdroje (SÚKL, VZP, ČLS JEP guidelines).
- **Riziko**: UpToDate má větší databázi autoritativního obsahu (peer-reviewed articles). Řešíme: Jasně komunikujeme, že pokrýváme 80% běžných use cases + postupně rozšiřujeme databázi prostřednictvím MCP tools (Fáze 2-3: Cochrane, NICE, BMČ).

**Risks při misuse:**
- **Over-reliance na AI**: Lékař může slepo důvěřovat AI bez kritického myšlení. Řešíme: Disclaimer "Asistent, ne náhrada lékaře", vždy vyžadujeme kontrolu lékaře (zejména u epikríz).
- **Halucinace (edge cases)**: I přes RAG může AI v 1-2% případů generovat nesprávné odpovědi. Řešíme: User reporting "Report incorrect", human-in-the-loop review vzorkově, continuous improvement.

### Notes - Referenční odkazy

**Konkurenční dokumentace:**
- OpenEvidence: https://www.openevidence.com/ (trial testován, screenshots archived)
- UpToDate AI: https://www.uptodate.com/home/ai (pricing $545/rok individual)
- DynaMed: https://www.dynamed.com/ (EBSCO product)
- Isabel DDx: https://www.isabelhealthcare.com/ (diferenciální diagnostika)

**České zdroje:**
- ICZ AV(D): Interní dokumentace FONS Enterprise
- SÚKL databáze: https://www.sukl.cz/
- České guidelines: https://www.cls.cz/
- ÚZIS: https://www.uzis.cz/

**AI Benchmarks:**
- Med-PaLM 2 (Google): 85.4% accuracy on USMLE
- Claude 3.5 Sonnet: 88% on medical Q&A (internal testing)
- RAG vs non-RAG: 95% vs 70% citation accuracy (internal study)

**User research:**
- 10 user interviews s praktickými lékaři (prosinec 2025)
- Pain points: Čas (80%), Fragmentace (65%), Jazyková bariéra (45%)
- Willingness to pay: 73% ano za 990 Kč/měsíc, 15% ne, 12% depends

---

**Konec PRD MVP - Verze 1.0**
