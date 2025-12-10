# Vytvořit Šablonu Zprávy
Stránka pro vytvoření nové custom šablony lékařské zprávy. Průvodce (wizard) umožňuje definovat název, typ, strukturu sekcí a instrukce pro AI generování.

Layout Hierarchy:
- Header (Full-width):
  - Horní navigace
- Content Container (Positioned below the header):
  - Multi-step wizard s progress barem
  - Hlavní obsahová oblast (mění se podle kroku)
  - Pravý sidebar s náhledem (volitelný)

## Horní Navigace
- Logo MediAI s linkem na Dashboard
- Breadcrumb: Dashboard > Správa Šablon > Vytvořit Šablonu
- Uživatelský avatar s dropdown menu

## Progress Bar (Sticky Top)
- 4 kroky vizualizované jako progress stepper:
  1. Základní Informace (aktivní)
  2. Definice Sekcí
  3. Instrukce pro AI
  4. Kontrola a Uložení
- Tlačítka navigace:
  - "Zpět" (sekundární, ghost)
  - "Další" (primární) / "Dokončit" (v posledním kroku)
  - "Zrušit" (sekundární, outlined) → zobrazí potvrzovací modal

---

## Krok 1: Základní Informace

### Formulář
**Název Šablony** (povinné)
- Input field
- Placeholder: "např. Vstupní vyšetření - Kardiologie"
- Validace: Maximálně 80 znaků
- Helper text: "Pojmenujte šablonu tak, aby bylo zřejmé, k čemu slouží"

**Kategorie** (povinné)
- Dropdown select:
  - Vstupní vyšetření
  - Kontrolní vyšetření
  - Výstupní zpráva
  - Dekurs (denní záznam)
  - Epikríza
  - Konziliární nález
  - Rychlá poznámka
  - Jiné (custom kategorie)
- Pokud zvolí "Jiné", zobrazí se input pro zadání vlastní kategorie

**Popis** (volitelné)
- Textarea
- Placeholder: "Stručný popis účelu této šablony..."
- Validace: Maximálně 300 znaků
- Helper text: "Popis pomůže vám i kolegům pochopit, kdy šablonu použít"

**Založit na existující šabloně** (volitelné)
- Dropdown select s možností "Vytvořit od začátku" nebo vybrat existující šablonu
- Pokud vybere existující, předvyplní se sekce a struktura z té šablony
- Seznam šablon:
  - Žádná (vytvořit od začátku)
  - Vstupní vyšetření - Lázně
  - Kontrolní vyšetření
  - Výstupní zpráva - Lázně
  - Dekurs
  - ... (všechny dostupné šablony)

**Ikona šablony** (volitelné)
- Grid s ikonami na výběr (Document, Clipboard, Notes, Medical Bag, atd.)
- Preview vybrané ikony

---

## Krok 2: Definice Sekcí

### Popis kroku
"Definujte strukturu zprávy vytvořením sekcí. Každá sekce bude obsahovat specifickou část lékařské zprávy."

### Seznam Sekcí (Drag & Drop)
Zobrazuje seznam sekcí s možností změny pořadí (drag handles):

**Sekce 1** (Card s drag handle)
- Drag handle ikona (:::)
- Nadpis: "Sekce 1"
- Input: Název sekce (např. "Anamnéza")
- Textarea: Popis sekce (volitelné)
- Checkbox: "Povinná sekce" (pokud zaškrtnuto, AI musí vygenerovat tuto sekci)
- Checkbox: "Povolit prázdnou sekci" (pokud není relevantní obsah)
- Tlačítko: "Odstranit Sekci" (ikona, ghost, červené)
- Collapsible: "Pokročilé Nastavení"
  - Očekávaná délka: Krátká (< 100 slov) / Střední (100-300 slov) / Dlouhá (> 300 slov)
  - Priorita: Nízká / Střední / Vysoká (ovlivňuje, jak moc se AI zaměří na detail)

**Sekce 2** (Card)
- Stejná struktura jako Sekce 1
- Název: "Nynější onemocnění"

**Sekce 3** (Card)
- Název: "Objektivní nález"

*... další sekce podle potřeby*

### Akce se Sekcemi
- Tlačítko: "+ Přidat Sekci" (primární, outlined)
- Tlačítko: "Přidat Standardní Sadu Sekcí" (dropdown):
  - Vstupní vyšetření (7 sekcí)
  - Kontrolní vyšetření (5 sekcí)
  - Výstupní zpráva (7 sekcí)
  - Dekurs (5 sekcí)

### Náhled Struktury (Pravý Sidebar)
- Live preview struktury zprávy
- Zobrazuje názvy sekcí v pořadí
- Indikuje povinné sekce (*)

---

## Krok 3: Instrukce pro AI

### Popis kroku
"Nastavte, jak má AI generovat obsah pro každou sekci. Můžete použít přirozený jazyk."

### Globální Instrukce
**Obecné instrukce pro celou zprávu** (volitelné)
- Textarea
- Placeholder: "např. Používejte formální lékařský jazyk, zaměřte se na kardiovaskulární problematiku, vynechte informace o dermatologických nálezech..."
- Helper text: "Tyto instrukce platí pro všechny sekce zprávy"

### Instrukce pro Jednotlivé Sekce
Pro každou sekci z Kroku 2:

**Sekce: Anamnéza**
- Accordion / Collapsible card
- Název sekce (read-only, z Kroku 2)
- Textarea: "Instrukce pro tuto sekci"
  - Placeholder: "Co má AI extrahovat a jak formulovat obsah této sekce?"
  - Příklad předvyplněného textu (pokud existuje):
    "Extrahujte rodinnou, osobní, alergologickou a farmakologickou anamnézu. Strukturujte do odstavců. Zdůrazněte chronická onemocnění a relevantní rodinnou zátěž."

**Entity a Data k Extrakci** (volitelné, advanced)
- Collapsible: "Specifické informace k extrakci"
- Checklist s běžnými entitami:
  - ☑ Diagnózy (ICD-10 kódy)
  - ☑ Medikace
  - ☑ Alergies
  - ☑ Vitální funkce
  - ☑ Rodinná anamnéza
  - ☐ Laboratorní hodnoty
  - ☐ Zobrazovací vyšetření
  - ☐ Procedury
- Input: "Vlastní entity" (free text)

### Náhled Příkladu (Pravý Sidebar)
- Zobrazí mockup vygenerované zprávy na základě instrukcí
- "⚠️ Toto je pouze ilustrativní náhled"

---

## Krok 4: Kontrola a Uložení

### Shrnutí Šablony
Přehledná karta shrnující všechny nastavení:

**Základní Informace**
- Název: "Vstupní vyšetření - Kardiologie"
- Kategorie: Vstupní vyšetření
- Popis: "Komplexní vstupní zpráva zaměřená na kardiologické pacienty"
- Ikona: [preview ikony]

**Struktura Zprávy**
- Seznam sekcí s jejich názvy (7 sekcí):
  1. Anamnéza (povinná)
  2. Nynější onemocnění (povinná)
  3. Kardiovaskulární anamnéza (povinná)
  4. Objektivní nález (povinná)
  5. EKG a zobrazovací vyšetření
  6. Závěr
  7. Doporučení (povinná)

**AI Instrukce**
- Globální instrukce (zkrácený preview)
- Počet sekcí s custom instrukcemi: 5/7

### Akce
- Tlačítko: "Uložit Šablonu" (primární, large)
- Checkbox: "Nastavit jako výchozí šablonu pro kategorii 'Vstupní vyšetření'" (volitelné)
- Link: "Upravit Základní Informace" → vrátí na Krok 1
- Link: "Upravit Sekce" → vrátí na Krok 2
- Link: "Upravit Instrukce" → vrátí na Krok 3

### Success State
Po kliknutí na "Uložit Šablonu":
- Success notifikace: "✓ Šablona úspěšně vytvořena"
- Modal s možnostmi:
  - "Použít Šablonu Nyní" → přesměruje na Report Type Selection s touto šablonou
  - "Vytvořit Další Šablonu" → reset formuláře, znovu na Krok 1
  - "Zpět na Správu Šablon" → přesměruje na Report Templates

---

## Potvrzení Zrušení (Modal)
Když uživatel klikne "Zrušit" během vytváření:
- "⚠️ Opravdu chcete zrušit vytváření šablony?"
- "Všechny dosud zadané informace budou ztraceny."
- Tlačítka: "Pokračovat v Úpravách" / "Zrušit Vytváření" (červené)

---

## Pravý Sidebar (Volitelný, Sticky)

### Tips & Tricks
**💡 Tipy pro Vytváření Šablon**
- "Definujte pouze sekce, které jsou pro váš use case relevantní"
- "Používejte jasné a stručné názvy sekcí"
- "AI instrukce mohou být napsány běžným jazykem"
- "Můžete začít duplikací existující šablony a upravit ji"

### Náhled v Reálném Čase
- Live preview struktury zprávy s názvy sekcí
- Počítadlo sekcí
- Počítadlo slov v instrukcích

### Příklady Šablon
- Link: "Prohlédnout příklady šablon"
- Link: "Dokumentace - Jak vytvořit efektivní šablonu"
