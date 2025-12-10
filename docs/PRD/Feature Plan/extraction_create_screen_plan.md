# Vytvořit Konfiguraci Extrakce
Stránka pro vytvoření nové konfigurace automatické extrakce dat s možností definovat entity přirozeným jazykem nebo pomocí strukturovaného schématu.

Layout Hierarchy:
- Header (Full-width):
  - Horní navigace
- Content Container (Positioned below the header):
  - Centrální formulářová oblast s krokovým průvodcem

## Horní Navigace
- Logo MediAI s linkem na Dashboard
- Breadcrumb: Dashboard > Konfigurace Extrakce > Vytvořit Novou
- Tlačítko "Uložit Koncept" (sekundární)
- Tlačítko "Uložit a Použít" (primární, disabled dokud není vyplněno minimum)
- Uživatelský avatar

## Krokový Průvodce (Steps Indicator)
- Krok 1: Základní Informace (aktivní)
- Krok 2: Definice Entit
- Krok 3: Testování
- Krok 4: Shrnutí

## Krok 1: Základní Informace

### Formulář
- Pole: Název Konfigurace
  - Placeholder: "např. Výstupní zpráva - Rehabilitace"
  - Help text: "Použijte popisný název, který vám pomůže rychle identifikovat účel"
- Pole: Popis (volitelné)
  - Textarea
  - Placeholder: "Popište, pro jaký typ zpráv je tato konfigurace určena..."
  - Character count: 0/500
- Pole: Vycházet z existující konfigurace
  - Dropdown: "Žádná" / "Výchozí" / Seznam custom konfigurací
  - Help text: "Můžete vycházet z existující konfigurace a pouze ji upravit"

### Typ Konfigurace (Radio Buttons)
- Volba 1: Výchozí šablona (doporučeno pro začátečníky)
  - Popis: "Použije základní extrakci PII a klinických dat, kterou můžete rozšířit"
- Volba 2: Prázdná šablona (pro pokročilé uživatele)
  - Popis: "Začnete s prázdnou šablonou a definujete všechny entity od začátku"

### Akční Tlačítka
- Tlačítko "Pokračovat na Definici Entit" (primární)
- Tlačítko "Zrušit"

## Krok 2: Definice Entit

### Metoda Definice (Tab Selector)
- Tab 1: Přirozený Jazyk (doporučeno) - aktivní
- Tab 2: Strukturované Schéma (pokročilé)

### Tab 1: Přirozený Jazyk

#### Promptové Pole
- Nadpis: "Popište, jaká data chcete extrahovat"
- Velký textarea:
  - Placeholder: "Například: 'Chci extrahovat typy fyzioterapeutických procedur, frekvenci jejich aplikace, subjektivní hodnocení pacienta na jejich účinek a doporučení pro další péči po ukončení lázeňského pobytu.'"
  - Character count
  - Help text: "Popište svými slovy, jaké informace chcete z přepisu vytáhnout. AI automaticky vytvoří vhodné entity."
- Příklady (collapsible):
  - Příklad 1: "Chci extrahovat podrobnou rodinnou anamnézu včetně onemocnění rodičů a sourozenců..."
  - Příklad 2: "Potřebuji identifikovat všechny fyzioterapeutické procedury a jejich frekvenci..."
  - Příklad 3: "Chci zaznamenat změny v medikaci během pobytu..."

#### AI Generování
- Tlačítko "Vygenerovat Entity z Popisu" (velké, primární)
- Loading state při generování
- Preview vygenerovaných entit:
  - Seznam entit s typy a popisem
  - Možnost upravit nebo odstranit každou entitu
  - Možnost přidat další entity manuálně

### Tab 2: Strukturované Schéma

#### Entity Builder
- Nadpis: "Definujte Entity Manuálně"
- Seznam již definovaných entit (pokud vycházíme z existující):
  - Entity Card 1: Jméno Pacienta (PII)
    - Typ: Text
    - Povinná: Ano
    - Příklady hodnot: "Jan Novák", "Marie Svobodová"
    - Akce: Upravit, Smazat
  - Entity Card 2: Datum Narození (PII)
    - Typ: Datum
    - Povinná: Ano
    - Formát: DD.MM.RRRR
    - Akce: Upravit, Smazat
  - Entity Card 3: Diagnózy
    - Typ: Seznam
    - Povinná: Ne
    - Sub-pole: Název diagnózy, ICD-10 kód
    - Příklady: "Artróza kolen (M17)", "Hypertenze (I10)"
    - Akce: Upravit, Smazat

#### Přidání Nové Entity
- Tlačítko "Přidat Entitu" (+ ikona)
- Modal/Form pro novou entitu:
  - Název entity: Input field
  - Typ entity: Dropdown (Text, Číslo, Datum, Seznam, Boolean, Strukturovaný objekt)
  - Kategorie: Dropdown (PII, Diagnóza, Medikace, Alergie, Symptom, Procedura, Jiné)
  - Popis entity: Textarea
  - Je povinná: Checkbox
  - Příklady hodnot: Multi-input field
  - Validační pravidla (volitelné): Regex pattern
  - Tlačítka: "Přidat Entitu", "Zrušit"

### Akční Tlačítka (na konci kroku)
- Tlačítko "Zpět na Základní Informace"
- Tlačítko "Pokračovat na Testování" (primární)

## Krok 3: Testování

### Test na Vzorových Datech
- Nadpis: "Otestujte Konfiguraci na Vzorových Přepisech"
- Popis: "Nahrajte vzorek přepisu nebo použijte ukázkový text pro ověření, že extrakce funguje správně"

#### Test Input
- Tab 1: Nahrát Testovací Soubor
  - Upload area pro audio soubor
  - Nebo upload TXT souboru s přepisem
- Tab 2: Vložit Ukázkový Text
  - Velký textarea s placeholder textem lékařského rozhovoru
  - Tlačítko "Načíst Ukázkový Text" (pre-fill s demo daty)

#### Test Execution
- Tlačítko "Spustit Test Extrakce" (primární)
- Loading state

#### Test Results
- Úspěšnost extrakce: 92% (velký, zelený badge)
- Počet nalezených entit: 15

##### Nalezené Entity (strukturovaný seznam)
- PII Entity:
  - Jméno pacienta: "Jan Novotný" ✓ (confidence 98%)
  - Datum narození: "15.3.1965" ✓ (confidence 95%)
- Diagnózy:
  - "Artróza kolen" ✓ (confidence 92%)
  - "Hypertenze" ✓ (confidence 90%)
- Medikace:
  - "Amlodipine 10 mg" ✓ (confidence 88%)
- Alergies:
  - "Penicilin" ✓ (confidence 94%)
- Custom Entity 1 (Fyzioterapeutické Procedury):
  - "Léčebná tělesná výchova" ✓ (confidence 85%)
  - "Koupele s minerály" ✓ (confidence 82%)
- Custom Entity 2 (Subjektivní Hodnocení):
  - "Bolest kloubů 6-7/10" ✓ (confidence 79%)

##### Chybějící Entity (pokud něco nebylo nalezeno)
- Vitální funkce: Nebylo detekováno v testovacím textu
- Doporučení pro další péči: Částečně detekováno (confidence nízké)

##### Akce na Základě Výsledků
- Info box: "Některé entity mají nízké confidence score. Zvažte úpravu definice nebo přidání více příkladů."
- Tlačítko "Upravit Definici Entit" (vrátí na Krok 2)
- Tlačítko "Test Je OK, Pokračovat"

### Akční Tlačítka
- Tlačítko "Zpět na Definici Entit"
- Tlačítko "Pokračovat na Shrnutí" (primární)

## Krok 4: Shrnutí

### Přehled Konfigurace
- Karta s detaily:
  - Název: [Název konfigurace]
  - Popis: [Popis]
  - Počet definovaných entit: [Číslo]
  - Test úspěšnost: [Procento]
  - Vytvoří se jako: Aktivní / Neaktivní (toggle)

### Seznam Všech Entit (collapsible groups)
- PII Entity (3)
- Klinické Informace (5)
- Custom Entity (4)

### Možnosti Použití
- Checkbox: "Nastavit jako výchozí konfiguraci"
- Checkbox: "Použít pro nové nahrávky automaticky"
- Info: "Můžete kdykoli změnit tuto konfiguraci nebo vytvořit další"

### Finální Akce
- Tlačítko "Zpět na Testování"
- Tlačítko "Uložit Konfiguraci" (velké, primární CTA)
- Po uložení: Přesměrování na seznam konfigurací se success notifikací
