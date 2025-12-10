# Editor Přepisu
Stránka s WYSIWYG editorem pro úpravu přepisu se synchronizovaným audio přehrávačem pro snadnou kontrolu přesnosti textu.

Layout Hierarchy:
- Header (Full-width):
  - Horní navigace s editor toolbar
- Content Container (Positioned below the header):
  - Dvousloupcový layout:
    - Levý sloupec: Audio přehrávač (25% šířky, fixed)
    - Pravý sloupec: Textový editor (75% šířky)

## Horní Navigace s Editor Toolbar
- Logo MediAI s linkem na Dashboard
- Breadcrumb: Dashboard > Detail Přepisu > Editor
- Editor toolbar (centrální):
  - Bold, Italic, Underline
  - Heading 1, Heading 2, Heading 3
  - Bullet list, Numbered list
  - Undo, Redo
  - Find & Replace
- Akční tlačítka (pravá strana):
  - Status indicator: "Uloženo" / "Ukládám..." / "Neuložené změny"
  - Tlačítko "Uložit" (primární)
  - Tlačítko "Uložit a Exportovat"
  - Tlačítko "Zrušit Změny"
- Uživatelský avatar

## Levý Sloupec: Audio Přehrávač (Fixed/Sticky)

### Audio Controls
- Waveform vizualizace (kompaktní)
- Play/Pause tlačítko
- Timeline s časem (current / total)
- Previous 5s / Next 5s tlačítka
- Playback speed: 0.5x, 0.75x, 1x, 1.25x, 1.5x, 2x
- Volume control

### Synchronizace Info
- Nadpis: "Synchronizace Audio ↔ Text"
- Info text: "Klikněte na časovou značku v textu pro skok v audio"
- Toggle: "Automatické přehrávání při kliknutí" (ON/OFF)

### Entity Highlight Controls
- Nadpis: "Zvýraznění Entit"
- Toggle switches:
  - PII entity (modrá) - ON
  - Diagnózy (červená) - ON
  - Medikace (zelená) - ON
  - Alergies (oranžová) - ON
  - Symptomy (fialová) - ON
- Tlačítko "Upravit Entity Manuálně"

### Quick Actions
- Tlačítko "Přidat Časovou Značku"
- Tlačítko "Vložit Template"
- Tlačítko "Formátovat Jako Lékařská Zpráva"

## Pravý Sloupec: Textový Editor

### Editor Header
- Název dokumentu (editovatelný)
- Word count: např. "1,247 slov"
- Character count: např. "8,456 znaků"
- Reading time: např. "~6 min čtení"

### WYSIWYG Editor Oblast
- Bohatý textový editor (shadcn UI based):
  - Plně formátovatelný text
  - Časové značky integrované jako kliknutelné badges (např. [00:30], [01:15])
  - Extrahované entity zvýrazněny barevně podle typu
  - Hover na entity zobrazí tooltip s editační možností
  - Inline editace entit (double-click otevře editor)
  - Drag & drop pro přeskupení textových bloků
  - Comment/note funkce pro interní poznámky
- Editor obsahuje reálný lékařský text s kompletní strukturou:

  "# VSTUPNÍ LÉKAŘSKÁ ZPRÁVA

  [00:05] Datum vyšetření: 5. prosince 2025
  [00:08] Vyšetřující lékař: MUDr. Martin Novák

  ## IDENTIFIKAČNÍ ÚDAJE PACIENTA
  [00:15] Jméno: Jan Novotný
  [00:18] Datum narození: 15.3.1965 (věk 60 let)
  [00:22] Pojišťovna: VZP

  ## ANAMNÉZA
  [00:35] **Rodinná anamnéza:** Matka - diabetes mellitus 2. typu, otec - ischemická choroba srdeční

  [01:05] **Osobní anamnéza:**
  - Artróza kolen (diagnostikována 2018)
  - Hypertenze (léčena od roku 2015)
  - Stav po operaci pravého kolena (2020)

  [01:45] **Farmakologická anamnéza:**
  - Amlodipine 10 mg - 1x denně ráno
  - Ibuprofen 400 mg - dle potřeby při bolesti

  [02:15] **Alergická anamnéza:**
  - Alergie na penicilin (vyrážka)
  - Potravinová alergie na ořechy

  ## NYNĚJŠÍ ONEMOCNĚNÍ
  [02:45] Pacient udává dlouhodobé potíže s bolestí kolen, zejména při chůzi do schodů a po delší zátěži. Bolest hodnotí na škále 6-7/10. Omezená pohyblivost pravého kolene, ranní ztuhlost trvající cca 30 minut. Praktický lékař doporučil lázeňskou léčbu zaměřenou na pohybový aparát.

  [03:30] V posledních 3 měsících zhoršení stavu, nutnost užívání analgetik téměř denně. Pacient má zájem o nefarmakologické metody léčby.

  ## FYZIKÁLNÍ VYŠETŘENÍ
  [04:15] **Celkový stav:** Dobrý, pacient plně orientován, spolupracuje
  [04:22] **TK:** 135/85 mmHg
  [04:25] **Puls:** 76/min, pravidelný
  [04:28] **Výška:** 178 cm
  [04:30] **Hmotnost:** 92 kg
  [04:32] **BMI:** 29.0 (nadváha)

  [04:50] **Pohybový aparát:**
  - Omezená flexe pravého kolene (90°)
  - Bolestivost při palpaci mediální strany obou kolen
  - Lehké otoky periartikulární oblasti
  - Chůze bez hole, mírně antalgická

  ## INDIKACE K LÁZEŇSKÉ LÉČBĚ
  [05:30] Gonartróza oboustranná s převahou vpravo, hypertenze kompenzovaná medikací

  ## KONTRAINDIKACE
  [05:45] Žádné absolutní kontraindikace. Relativní kontraindikace: nadváha (nutnost kontroly BMI), hypertenze (pravidelná kontrola TK).

  ## DOPORUČENÝ LÉČEBNÝ PLÁN
  [06:15] **Fyzioterapie:**
  - Léčebná tělesná výchova - zaměření na posílení quadricepsu - 5x týdně
  - Cvičení v bazénu - 3x týdně

  [06:45] **Fyzikální terapie:**
  - Elektroterapie (TENS) na kolenní klouby - denně
  - Magnetoterapie - 5x týdně
  - Parafínové zábaly - 3x týdně

  [07:20] **Balneoterapie:**
  - Koupele s přísadami minerálů - obden
  - Perličková koupel - 2x týdně

  [07:50] **Doporučení:**
  - Redukce hmotnosti (cílová 85 kg)
  - Pravidelná kontrola TK
  - Pokračování v užívání antihypertenziv
  - Omezení NSAID, pouze při silné bolesti

  ## ZÁVĚR
  [08:30] Pacient přijat k 3týdenní lázeňské léčbě. Plánované kontrolní vyšetření za 10 dní. Doporučena spolupráce s fyzioterapeuty a pravidelné sledování vitálních funkcí.

  ___
  MUDr. Martin Novák
  Lázeňský lékař
  Licence: XXXX"

- Editor features:
  - Auto-save každých 30 sekund
  - Version history tracking
  - Spell checker pro češtinu s lékařskou terminologií
  - Find & Replace modal (Ctrl+F)
  - Dark mode toggle

## Floating Helper Panel (pravý dolní roh, collapsible)
- Nadpis: "AI Asistent"
- Quick suggestions:
  - "Formátovat jako standardní zprávu"
  - "Přidat chybějící sekce"
  - "Kontrola terminologie"
  - "Sugesce pro zlepšení struktury"
- Použití AI: tlačítko "Vylepšit Text AI"

## Modální Okno: Manuální Editace Entity (při kliknutí na "Upravit Entity")
- Výběr typu entity: Dropdown (PII, Diagnóza, Medikace, Alergie, Symptom)
- Text entity: Input field
- Confidence score: Slider
- Pozice v textu: Auto-detected
- Tlačítka: "Uložit", "Smazat Entitu", "Zrušit"
