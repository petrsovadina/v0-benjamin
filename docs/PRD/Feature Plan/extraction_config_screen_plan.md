# Konfigurace Extrakce
Stránka pro správu a vytváření konfigurací automatické extrakce dat z přepisů s možností definovat custom entity schémata.

Layout Hierarchy:
- Header (Full-width):
  - Horní navigace
- Content Container (Positioned below the header):
  - Hlavní obsahová oblast

## Horní Navigace
- Logo MediAI s linkem na Dashboard
- Breadcrumb: Dashboard > Konfigurace Extrakce
- Tlačítko "Vytvořit Novou Konfiguraci" (primární CTA)
- Uživatelský avatar s dropdown menu

## Hlavní Obsahová Oblast

### Úvodní Sekce
- Nadpis stránky: "Konfigurace Extrakce Dat"
- Popisný text: "Vytvořte vlastní šablony pro automatickou extrakci klinických dat z přepisů rozhovorů. Můžete definovat entity přirozeným jazykem nebo specifikovat konkrétní schéma."
- Info box s tipy:
  - "Defaultní konfigurace je vhodná pro většinu případů"
  - "Custom konfigurace umožňují přizpůsobit extrakci pro specifické typy zpráv (vstupní, kontrolní, výstupní)"
  - "Každá konfigurace může být použita opakovaně pro různé nahrávky"

### Seznam Konfigurací (Cards)

#### Defaultní Konfigurace (Nelze Smazat)
- Badge: "Defaultní"
- Název: "Výchozí (PII + Základní Klinická Data)"
- Popis: "Automatická extrakce osobních údajů pacienta a základních klinických informací"
- Počet entit: 8 typů
  - PII entity (Jméno, Datum narození, Kontakt)
  - Diagnózy
  - Medikace
  - Alergies
  - Symptomy
  - Vitální funkce
- Použito v: 47 přepisů
- Akce:
  - Tlačítko "Zobrazit Detail"
  - Tlačítko "Duplikovat a Upravit"
  - Badge "Aktivní" (používá se při nových nahrávkách)

#### Custom Konfigurace 1
- Badge: "Custom"
- Název: "Výstupní Zpráva - Fyzioterapie"
- Popis: "Extrakce specifická pro výstupní zprávy zaměřené na fyzioterapeutické procedury"
- Počet entit: 12 typů
  - Vše z defaultní konfigurace
  - + Typy fyzioterapeutických procedur
  - + Frekvence aplikace
  - + Subjektivní hodnocení pacienta
  - + Doporučení pro další péči
- Vytvořeno: 15.11.2025
- Použito v: 23 přepisů
- Akce:
  - Tlačítko "Upravit"
  - Tlačítko "Duplikovat"
  - Tlačítko "Smazat"
  - Toggle: Nastavit jako výchozí

#### Custom Konfigurace 2
- Badge: "Custom"
- Název: "Kontrolní Vyšetření - Krátká Forma"
- Popis: "Zjednodušená extrakce pro rychlé kontrolní vyšetření během lázeňského pobytu"
- Počet entit: 6 typů
  - Jméno pacienta
  - Subjektivní stav pacienta
  - Změny v symptomech
  - Nové stížnosti
  - Úpravy v léčbě
  - Doporučení
- Vytvořeno: 28.11.2025
- Použito v: 12 přepisů
- Akce:
  - Tlačítko "Upravit"
  - Tlačítko "Duplikovat"
  - Tlačítko "Smazat"
  - Toggle: Nastavit jako výchozí

#### Custom Konfigurace 3
- Badge: "Custom"
- Název: "Vstupní Vyšetření - Komplexní"
- Popis: "Rozšířená extrakce pro detailní vstupní vyšetření včetně rodinné anamnézy"
- Počet entit: 15 typů
  - Vše z defaultní konfigurace
  - + Rodinná anamnéza
  - + Osobní anamnéza
  - + Sociální anamnéza
  - + Pracovní anamnéza
  - + Předchozí hospitalizace
  - + Fyzikální vyšetření data
  - + Indikace k lázeňské léčbě
- Vytvořeno: 02.12.2025
- Použito v: 8 přepisů
- Akce:
  - Tlačítko "Upravit"
  - Tlačítko "Duplikovat"
  - Tlačítko "Smazat"
  - Toggle: Nastavit jako výchozí

### Prázdný Stav (pokud nejsou custom konfigurace)
- Ilustrace
- Nadpis: "Zatím nemáte vlastní konfigurace"
- Popis: "Vytvořte custom konfiguraci pro specifické typy lékařských zpráv"
- Velké CTA tlačítko: "Vytvořit První Konfiguraci"

## Statistiky a Přehledy (pravý sidebar nebo horní cards)
- Card: Celkový počet konfigurací
- Card: Nejpoužívanější konfigurace
- Card: Průměrná přesnost extrakce (%)
- Card: Celkový počet použití všech konfigurací
