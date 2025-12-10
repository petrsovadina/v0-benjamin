# Dashboard
Hlavní přehledová stránka zobrazující seznam všech audio nahrávek s jejich stavy zpracování a rychlým přístupem k hlavním funkcím.

Layout Hierarchy:
- Header (Full-width):
  - Horní navigace
- Content Container (Positioned below the header):
  - Hlavní obsahová oblast

## Horní Navigace
- Logo MediAI
- Vyhledávací pole pro přepisy a zprávy
- Tlačítko "Nová Nahrávka" (primární CTA)
- **[NOVÉ]** Tlačítko "Správa Šablon" (sekundární) → vede na Report Templates
- Ikona notifikací
- Ikona nastavení
- Uživatelský avatar s dropdown menu

## Hlavní Obsahová Oblast
- Nadpis stránky: "Moje Nahrávky"
- Filtr a řazení:
  - Filtr podle stavu (Všechny, Čeká, Přepisuje se, Hotovo, Chyba)
  - Řazení podle data (nejnovější, nejstarší)
  - Řazení podle názvu (A-Z, Z-A)
- Seznam nahrávek (cards):
  - Karta nahrávky 1 (Hotovo):
    - Název nahrávky nebo auto-generovaný název (např. "Vstupní vyšetření - 5.12.2025 09:30")
    - Datum a čas nahrávky
    - Status badge "Hotovo" (zelený)
    - **[NOVÉ]** Badge: "Zpráva Vygenerována" (fialový, pokud existuje AI vygenerovaná zpráva)
    - Délka audio nahrávky (např. "8:45")
    - Extrahované entity preview (3 hlavní PII/klinická data)
    - **[NOVÉ]** Preview vygenerované zprávy (pokud existuje): "Vstupní vyšetření - Lázně" s mini ikonou dokumentu
    - Akční tlačítka:
      - Zobrazit
      - **[NOVÉ]** Generovat Zprávu (primární, pokud zpráva ještě neexistuje) → vede na Report Type Selection
      - **[NOVÉ]** Zobrazit Zprávu (primární, pokud zpráva existuje) → vede na Report Preview
      - Upravit
      - Exportovat (dropdown s možností exportu přepisu nebo zprávy)
      - Smazat
  - Karta nahrávky 2 (Přepisuje se):
    - Název nahrávky
    - Datum a čas nahrávky
    - Status badge "Přepisuje se" (modrý) s progress bar
    - Délka audio nahrávky
    - Odhadovaný čas dokončení (např. "~45 sekund")
  - Karta nahrávky 3 (Hotovo):
    - Název nahrávky
    - Datum a čas nahrávky
    - Status badge "Hotovo" (zelený)
    - Délka audio nahrávky
    - Extrahované entity preview
    - Akční tlačítka: Zobrazit, Upravit, Exportovat, Smazat
  - Karta nahrávky 4 (Čeká):
    - Název nahrávky
    - Datum a čas nahrávky
    - Status badge "Čeká" (šedý)
    - Délka audio nahrávky
    - Informace o pozici ve frontě
  - Karta nahrávky 5 (Chyba):
    - Název nahrávky
    - Datum a čas nahrávky
    - Status badge "Chyba" (červený)
    - Délka audio nahrávky
    - Chybová zpráva: "Přepis se nezdařil - Nízká kvalita audio"
    - Tlačítko "Zkusit znovu"
  - Karta nahrávky 6 (Hotovo):
    - Název nahrávky
    - Datum a čas nahrávky
    - Status badge "Hotovo" (zelený)
    - Délka audio nahrávky
    - Extrahované entity preview
    - Akční tlačítka: Zobrazit, Upravit, Exportovat, Smazat
- Statistiky a přehledy:
  - Celkový počet nahrávek
  - Počet nahrávek tento týden
  - **[NOVÉ]** Počet vygenerovaných zpráv (celkově a tento týden)
  - Ušetřený čas (odhad na základě počtu přepisů **+ vygenerovaných zpráv**)
  - Quick stats cards:
    - **[NOVÉ]** "Vygenerované zprávy: 45" s trendem (např. +12 tento týden)
    - **[NOVÉ]** "Nejpoužívanější šablona: Vstupní vyšetření - Lázně (23×)"

## Prázdný Stav (pro nové uživatele)
- Ilustrace/ikona
- Nadpis: "Začněte s vaší první nahrávkou"
- Popis: "Nahrajte audio rozhovor s pacientem a během 90 sekund získejte strukturovaný přepis"
- Velké CTA tlačítko: "Nahrát První Audio"
- Seznam benefitů (3 body):
  - Úspora až 70% času s dokumentací
  - Automatická extrakce klinických dat
  - 100% GDPR compliant
