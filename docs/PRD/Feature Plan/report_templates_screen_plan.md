# Správa Šablon Zpráv
Stránka pro správu předpřipravených a custom šablon lékařských zpráv. Umožňuje prohlížení, editaci, duplikaci a mazání šablon.

Layout Hierarchy:
- Header (Full-width):
  - Horní navigace
- Content Container (Positioned below the header):
  - Hlavní obsahová oblast se seznamem šablon

## Horní Navigace
- Logo MediAI s linkem na Dashboard
- Breadcrumb: Dashboard > Správa Šablon
- Uživatelský avatar s dropdown menu

## Hlavní Obsahová Oblast

### Page Header
- Nadpis: "Správa Šablon Zpráv"
- Popis: "Spravujte předpřipravené šablony nebo vytvořte vlastní custom šablony přizpůsobené workflow vašeho zařízení."
- Tlačítko: "Vytvořit Novou Šablonu" (primární, large) → vede na Create Template

### Filtr a Vyhledávání
- Search bar: "Hledat šablonu..."
- Filtry (dropdown buttons):
  - "Typ Šablony": Všechny / Defaultní / Custom
  - "Kategorie": Všechny / Vstupní / Kontrolní / Výstupní / Dekurs / Epikríza / Ostatní
  - "Seřadit podle": Název (A-Z) / Nejpoužívanější / Nedávno upravené / Datum vytvoření
- Badge s počtem šablon: "Celkem 12 šablon"

## Seznam Šablon

### Sekce: Defaultní Šablony (Systémové)
Popis: "Předpřipravené šablony pro běžné typy zpráv v lázeňské medicíně"

**Card 1: Vstupní Vyšetření - Lázně**
- Ikona: Document + Medical Bag
- Název: "Vstupní Vyšetření - Lázně"
- Badge: "Defaultní" (modrý)
- Badge: "Nejpoužívanější" (zlatý)
- Krátký popis: "Komplexní vstupní zpráva obsahující anamnézu, indikaci, kontraindikace, objektivní nález a léčebný plán"
- Statistiky:
  - Počet sekcí: 7
  - Průměrná délka: 850 slov
  - Použito: 156× (za poslední měsíc)
- Sections preview (collapsible):
  - Anamnéza
  - Nynější onemocnění
  - Indikace k lázeňské léčbě
  - Kontraindikace
  - Objektivní nález
  - Léčebný plán
  - Doporučení
- Akce:
  - "Zobrazit Detail" (ghost button)
  - "Duplikovat" (ghost button) → vytvoří custom kopii pro editaci
  - "Použít" (primární button) → jde na Report Type Selection s touto šablonou předvybranou

**Card 2: Kontrolní Vyšetření**
- Ikona: Clipboard Check
- Název: "Kontrolní Vyšetření"
- Badge: "Defaultní"
- Krátký popis: "Stručný záznam průběhu léčby a reakce pacienta na terapii"
- Statistiky:
  - Počet sekcí: 5
  - Průměrná délka: 420 slov
  - Použito: 89×
- Sections preview:
  - Subjektivní stav pacienta
  - Objektivní nález
  - Průběh léčby
  - Úpravy procedur
  - Plán dalšího postupu
- Akce: Zobrazit Detail / Duplikovat / Použít

**Card 3: Výstupní Zpráva - Lázně**
- Ikona: Document + Check Circle
- Název: "Výstupní Zpráva - Lázně"
- Badge: "Defaultní"
- Krátký popis: "Komprehenzivní výstupní zpráva shrnující celý lázeňský pobyt"
- Statistiky:
  - Počet sekcí: 7
  - Průměrná délka: 1200 slov
  - Použito: 45×
- Sections preview:
  - Shrnutí pobytu
  - Průběh léčby
  - Aplikované procedury
  - Dosažené výsledky
  - Subjektivní hodnocení pacienta
  - Doporučení pro domácí péči
  - Doporučení pro praktického lékaře
- Akce: Zobrazit Detail / Duplikovat / Použít

**Card 4: Dekurs**
- Ikona: Notes
- Název: "Dekurs (Denní Záznam)"
- Badge: "Defaultní"
- Statistiky:
  - Počet sekcí: 5
  - Použito: 67×
- Akce: Zobrazit Detail / Duplikovat / Použít

**Card 5: Epikríza**
- Ikona: Document Medical
- Název: "Epikríza"
- Badge: "Defaultní"
- Statistiky:
  - Počet sekcí: 7
  - Použito: 12×
- Akce: Zobrazit Detail / Duplikovat / Použít

**Card 6: Rychlá Poznámka**
- Ikona: Note Quick
- Název: "Rychlá Poznámka"
- Badge: "Defaultní"
- Statistiky:
  - Počet sekcí: 1 (flexibilní)
  - Použito: 34×
- Akce: Zobrazit Detail / Duplikovat / Použít

### Sekce: Moje Custom Šablony
Popis: "Šablony, které jste vytvořili nebo upravili"

**Card: Výstupní Zpráva - Fyzioterapie (Custom)**
- Ikona: Document + Custom Tag
- Název: "Výstupní Zpráva - Fyzioterapie"
- Badge: "Custom" (fialový)
- Badge: "Nedávno upraveno" (oranžový, pokud upraveno v posledních 7 dnech)
- Krátký popis: "Výstupní zpráva zaměřená na fyzioterapeutické procedury a jejich toleranci"
- Vytvořeno: 15.11.2025
- Poslední úprava: 3.12.2025
- Statistiky:
  - Počet sekcí: 6 (custom)
  - Průměrná délka: 980 slov
  - Použito: 23×
- Sections preview (collapsible):
  - Shrnutí pobytu
  - Aplikované fyzioterapeutické procedury
  - Frekvence a intenzita aplikací
  - Subjektivní tolerance procedur
  - Objektivní hodnocení účinnosti
  - Doporučení pro další péči
- Akce:
  - "Zobrazit Detail" (ghost)
  - "Upravit" (ghost) → vede na Edit Template
  - "Duplikovat" (ghost)
  - "Smazat" (ghost, red) → zobrazí potvrzovací modal
  - "Použít" (primární)

**Card: Dekurs - Rehabilitační Oddělení (Custom)**
- Ikona: Notes + Custom Tag
- Název: "Dekurs - Rehabilitační Oddělení"
- Badge: "Custom"
- Vytvořeno: 1.12.2025
- Statistiky:
  - Počet sekcí: 5
  - Použito: 8×
- Akce: Zobrazit Detail / Upravit / Duplikovat / Smazat / Použít

### Empty State (pokud nemá custom šablony)
- Ilustrace prázdného stavu
- Text: "Zatím nemáte žádné custom šablony"
- Popis: "Vytvořte vlastní šablonu přizpůsobenou workflow vašeho zařízení nebo duplikujte existující defaultní šablonu a upravte ji."
- Tlačítko: "Vytvořit První Šablonu" (primární)

## Detail Šablony (Modal nebo Slide-in Panel)
Když uživatel klikne "Zobrazit Detail":
- Název šablony
- Typ (Defaultní / Custom)
- Popis
- Kompletní seznam sekcí s popisem každé sekce:
  - Název sekce
  - Instrukce pro AI (co má extrahovat)
  - Příklad výstupu
- Statistiky použití (graf za poslední 3 měsíce)
- Tlačítka:
  - "Zavřít"
  - "Duplikovat" (pro defaultní šablony)
  - "Upravit" (pro custom šablony)
  - "Použít"

## Potvrzení Smazání (Modal)
Když uživatel klikne "Smazat" na custom šabloně:
- Varování: "⚠️ Opravdu chcete smazat tuto šablonu?"
- Text: "Tato akce je nevratná. Šablona bude trvale odstraněna a nebude dostupná pro generování zpráv."
- Název šablony: "Výstupní Zpráva - Fyzioterapie"
- Checkbox: "Rozumím, že tato akce je nevratná"
- Tlačítka: "Zrušit" / "Smazat Šablonu" (červené, disabled dokud není zaškrtnut checkbox)

## Informační Panel (Pravý Sidebar - volitelně)
**Tipy pro Šablony**
- "💡 Custom šablony můžete vytvořit duplikací existujících šablon"
- "📋 Každá sekce může mít vlastní instrukce pro AI"
- "🔄 Šablony můžete kdykoliv upravit nebo smazat"
- "⚡ Defaultní šablony nelze upravit, ale můžete je duplikovat"

**Statistiky Využití**
- Graf s počtem použití všech šablon za poslední měsíc
- Top 3 nejpoužívanější šablony
