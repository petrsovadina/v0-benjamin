# Detail Přepisu
Stránka zobrazující kompletní přepis audio nahrávky s extrahovanými entitami, audio přehrávačem a možností exportu nebo editace.

Layout Hierarchy:
- Header (Full-width):
  - Horní navigace
- Content Container (Positioned below the header):
  - Dvousloupcový layout:
    - Levý sloupec: Audio přehrávač a metadata (30% šířky)
    - Pravý sloupec: Přepis a extrahované entity (70% šířky)

## Horní Navigace
- Logo MediAI s linkem na Dashboard
- Breadcrumb: Dashboard > Detail Přepisu
- Akční tlačítka:
  - **[NOVÉ]** Tlačítko "Generovat Zprávu" (primární, pokud zpráva ještě neexistuje)
  - Tlačítko "Upravit" (otevře editor)
  - Tlačítko "Exportovat" s dropdown (.txt, .docx, **[NOVÉ]** Export zprávy - pokud existuje)
  - Tlačítko "Smazat"
  - Share button (volitelné)
- Uživatelský avatar s dropdown menu

## Levý Sloupec: Audio a Metadata

### Audio Přehrávač
- Waveform vizualizace audio nahrávky
- Play/Pause tlačítko (velké, centrální)
- Timeline s časovými značkami
- Volume control
- Playback speed control (0.5x, 0.75x, 1x, 1.25x, 1.5x, 2x)
- Celková délka audio (např. "8:45")

### Metadata Nahrávky
- Název nahrávky (editovatelný inline)
- Datum a čas vytvoření
- Velikost souboru
- Formát souboru (MP3/WAV/M4A)
- Status badge: "Hotovo" (zelený)
- Použitá konfigurace extrakce: "Výchozí"

### Quick Actions
- Tlačítko "Zkopírovat Text" (ikona + text)
- Tlačítko "Stáhnout Audio"
- Tlačítko "Znovu Přepsat" (pokud byla chyba)

### GDPR a Bezpečnost
- Security badge: "End-to-end šifrováno"
- GDPR compliance indikátor
- Informace o uchování dat

## Pravý Sloupec: Přepis a Entity

### Záložky (Tabs)
- Tab 1: Přepis (aktivní)
- Tab 2: Extrahované Entity
- **[NOVÉ]** Tab 3: Vygenerovaná Zpráva (pouze pokud zpráva existuje)
- Tab 4: Historie Změn

### Tab 1: Přepis
- Nadpis: "Přepis Rozhovoru"
- Toolbar s akcemi:
  - Tlačítko "Přejít do Editoru"
  - Tlačítko "Zkopírovat Vše"
  - Search funkce pro vyhledávání v textu
  - Zvýraznit entity (toggle)
- Textová oblast s přepisem:
  - Formátovaný text rozhovoru
  - Extrahované entity zvýrazněny barevně podle typu:
    - PII entity (jméno, datum narození) - modrá
    - Diagnózy - červená
    - Medikace - zelená
    - Alergies - oranžová
    - Symptomy - fialová
  - Časové značky každých 30 sekund (kliknutelné - skočí v audio)
  - Hover na entity zobrazí tooltip s typem a confidence score
- Příklad textu:
  "Lékař: Dobrý den, pane [Jméno Pacienta]. Jaký je důvod vaší návštěvy v lázních?

  Pacient: Dobrý den, doktore. Mám dlouhodobé problémy s klouby, zejména s koleny. Můj praktický lékař mi doporučil lázeňskou léčbu.

  Lékař: Rozumím. Máte nějaké další diagnózy nebo chronická onemocnění?

  Pacient: Ano, mám vysoký krevní tlak a užívám na to [Název léku] 10 mg denně. Také mám alergii na [Název alergenu].

  Lékař: Dobře, to si poznamenáme. Jaké procedury jste dostal doporučené od praktického lékaře?..."

### Tab 2: Extrahované Entity
- Strukturovaný přehled všech identifikovaných entit:

#### PII Entity (Osobní Údaje)
- Jméno pacienta: [Jméno Příjmení]
- Datum narození: [DD.MM.RRRR]
- Pohlaví: [Muž/Žena]
- Kontakt: [Telefon/Email - pokud zmíněno]

#### Klinické Informace
- Primární diagnózy:
  - Artróza kolen (ICD-10: M17)
  - Hypertenze (ICD-10: I10)
- Medikace:
  - [Název léku] 10 mg - 1x denně
  - [Další lék] - dle potřeby
- Alergies:
  - [Název alergenu] - závažnost: střední
- Symptomy:
  - Bolest kloubů - intenzita 6/10
  - Omezená pohyblivost
- Kontraindikace:
  - Vysoký krevní tlak - pozor na některé fyzioterapeutické procedury
- Doporučené procedury:
  - Vodoléčba
  - Léčebná tělesná výchova
  - Elektroterapie

#### Metadata
- Confidence score celkové extrakce: 92%
- Počet identifikovaných entit: 15
- Použitá konfigurace: "Výchozí (PII + Základní klinická data)"
- Tlačítko "Re-run Extrakce" s možností změnit konfiguraci

### Tab 3: Vygenerovaná Zpráva **[NOVÉ]**
*Tento tab se zobrazí pouze pokud již byla pro tento přepis vygenerována AI zpráva*

- Nadpis: "Vygenerovaná Lékařská Zpráva"
- Informační badge: Typ šablony (např. "Vstupní vyšetření - Lázně")
- Metadata zprávy:
  - Datum vygenerování
  - Čas generování (např. "45 sekund")
  - Počet slov
  - Úplnost: 95% (progress bar)
- Náhled zprávy (read-only, strukturovaný):
  - Metadata sekce (Pacient, Lékař, Datum)
  - Všechny sekce zprávy (Anamnéza, Nynější onemocnění, atd.)
  - Formátování zachováno
- Akce:
  - Tlačítko "Upravit Zprávu" (primární) → vede na Report Preview v edit módu
  - Tlačítko "Zobrazit Detail" → vede na plnou stránku Report Preview
  - Tlačítko "Exportovat Zprávu" (dropdown: .txt, .docx, kopírovat)
  - Tlačítko "Regenerovat Zprávu" (sekundární, outlined) - potvrzovací modal
- Pokud zpráva neexistuje:
  - Empty state s ikonou
  - Text: "Pro tento přepis zatím nebyla vygenerována žádná zpráva"
  - Popis: "Vygenerujte strukturovanou lékařskou zprávu během 30-60 sekund"
  - Tlačítko "Vygenerovat Zprávu" (primární) → vede na Report Type Selection

### Tab 4: Historie Změn
- Timeline všech úprav:
  - Vytvoření přepisu - [Datum Čas] - Systém
  - Extrakce dat dokončena - [Datum Čas] - Systém
  - **[NOVÉ]** Vygenerování zprávy - [Datum Čas] - Systém (s informací o použité šabloně)
  - Úprava textu - [Datum Čas] - [Jméno Uživatele]
  - **[NOVÉ]** Úprava zprávy - [Datum Čas] - [Jméno Uživatele]
  - Export do .docx - [Datum Čas] - [Jméno Uživatele]
  - **[NOVÉ]** Export zprávy do .docx - [Datum Čas] - [Jméno Uživatele]
- Každá položka obsahuje:
  - Typ akce
  - Datum a čas
  - Uživatel/systém
  - Detail změny (pokud relevantní)

## Floating Action Buttons (pravý dolní roh)
- **[NOVÉ]** Primární FAB tlačítko "Generovat Zprávu" (pokud zpráva neexistuje) / "Zobrazit Zprávu" (pokud zpráva existuje)
- Sekundární FAB "Přejít do Editoru"
- Terciární FAB "Exportovat"
