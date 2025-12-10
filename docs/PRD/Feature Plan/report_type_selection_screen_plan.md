# Výběr Typu Zprávy
Stránka pro výběr typu lékařské zprávy, kterou má AI vygenerovat z přepisu rozhovoru. Umožňuje výběr z předpřipravených šablon nebo vytvoření custom šablony.

Layout Hierarchy:
- Header (Full-width):
  - Horní navigace
- Content Container (Positioned below the header):
  - Hlavní obsahová oblast s výběrem šablon

## Horní Navigace
- Logo MediAI s linkem na Dashboard
- Breadcrumb: Dashboard > Detail Přepisu > Generovat Zprávu
- Uživatelský avatar s dropdown menu

## Hlavní Obsahová Oblast

### Page Header
- Nadpis: "Vygenerovat Lékařskou Zprávu"
- Popis: "Vyberte typ zprávy, kterou chcete vygenerovat z tohoto přepisu. AI automaticky vytvoří strukturovaný dokument připravený k použití."
- Informační badge: "Přepis: Vstupní vyšetření - Pavel Novotný" (název aktuálního přepisu)

### Přehled Přepisu (Collapsed Card)
- Collapsible sekce s náhledem přepisu
- Header: "Náhled Přepisu" s tlačítkem pro expand/collapse
- Při rozbalení zobrazí:
  - Datum a čas nahrávky
  - Délka audio: 8:34
  - Zkrácený text přepisu (prvních 200 znaků)
  - Link "Zobrazit Kompletní Přepis" → vede na Transcript Detail

### Výběr Šablony Zprávy

#### Sekce: Doporučené Šablony
Popis: "Nejčastěji používané šablony pro lázeňskou medicínu"

**Card 1: Vstupní Vyšetření - Lázně**
- Ikona: Document + Medical Bag
- Název: "Vstupní Vyšetření - Lázně"
- Popis: "Komplexní vstupní zpráva obsahující anamnézu, indikaci, kontraindikace, objektivní nález a léčebný plán"
- Badge: "Nejvíce používaná"
- Sections preview (malý font):
  - Anamnéza
  - Nynější onemocnění
  - Indikace k lázeňské léčbě
  - Kontraindikace
  - Objektivní nález
  - Léčebný plán
  - Doporučení
- Časová náročnost: "⏱ Cca 45 sekund"
- Tlačítko: "Vygenerovat Zprávu" (primární)

**Card 2: Kontrolní Vyšetření**
- Ikona: Clipboard Check
- Název: "Kontrolní Vyšetření"
- Popis: "Stručný záznam průběhu léčby, reakce pacienta na terapii a případné úpravy procedur"
- Sections preview:
  - Subjektivní stav pacienta
  - Objektivní nález
  - Průběh léčby
  - Úpravy procedur
  - Plán dalšího postupu
- Časová náročnost: "⏱ Cca 30 sekund"
- Tlačítko: "Vygenerovat Zprávu" (primární)

**Card 3: Výstupní Zpráva - Lázně**
- Ikona: Document + Check Circle
- Název: "Výstupní Zpráva - Lázně"
- Popis: "Komprehenzivní výstupní zpráva shrnující celý lázeňský pobyt, dosažené výsledky a doporučení"
- Sections preview:
  - Shrnutí pobytu
  - Průběh léčby
  - Aplikované procedury
  - Dosažené výsledky
  - Subjektivní hodnocení pacienta
  - Doporučení pro domácí péči
  - Doporučení pro praktického lékaře
- Časová náročnost: "⏱ Cca 60 sekund"
- Tlačítko: "Vygenerovat Zprávu" (primární)

**Card 4: Dekurs**
- Ikona: Notes
- Název: "Dekurs (Denní Záznam)"
- Popis: "Stručný denní lékařský záznam o stavu pacienta a aplikovaných postupech"
- Sections preview:
  - Subjektivní stav
  - Objektivní nález
  - Aplikované procedury
  - Reakce na léčbu
  - Plán na další den
- Časová náročnost: "⏱ Cca 25 sekund"
- Tlačítko: "Vygenerovat Zprávu" (primární)

#### Sekce: Další Šablony
Popis: "Méně používané nebo custom šablony"

**Card 5: Epikríza**
- Ikona: Document Medical
- Název: "Epikríza"
- Popis: "Závěrečná lékařská zpráva o hospitalizaci nebo lázeňském pobytu"
- Badge: "Komplexní"
- Sections preview:
  - Diagnóza
  - Anamnéza
  - Průběh hospitalizace/pobytu
  - Provedená vyšetření a postupy
  - Stav při propuštění
  - Doporučená terapie
  - Další doporučení
- Časová náročnost: "⏱ Cca 90 sekund"
- Tlačítko: "Vygenerovat Zprávu" (primární)

**Card 6: Rychlá Poznámka**
- Ikona: Note Quick
- Název: "Rychlá Poznámka"
- Popis: "Jednoduchý strukturovaný záznam bez předdefinovaných sekcí"
- Badge: "Flexibilní"
- Sections preview:
  - Volná struktura dle obsahu přepisu
- Časová náročnost: "⏱ Cca 20 sekund"
- Tlačítko: "Vygenerovat Zprávu" (primární)

### Custom Šablony (pokud existují)
- Zobrazí se pouze pokud uživatel má vytvořené vlastní custom šablony
- Seznam custom šablon s názvem, popisem a tlačítkem "Vygenerovat Zprávu"
- Ikona pro editaci šablony (vede na Report Templates)

### Správa Šablon
- Tlačítko: "Spravovat Šablony" (sekundární, outlined)
- Vede na stránku Report Templates Management

### Informační Panel (Pravý Sidebar - volitelně)
**Tipy pro Generování**
- "💡 AI analyzuje celý přepis a automaticky extrahuje relevantní informace"
- "✏️ Po vygenerování můžete zprávu upravit před exportem"
- "📋 Custom šablony můžete vytvořit v sekci Správa Šablon"
- "⚡ Generování probíhá během 30-90 sekund v závislosti na typu zprávy"

**Bezpečnost**
- Badge: "🔒 Šifrováno end-to-end"
- Badge: "🇪🇺 GDPR Compliant"
