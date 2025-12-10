# Nahrát Audio
Stránka pro nahrání audio souboru nebo přímé nahrávání přes mikrofon s následným automatickým spuštěním AI přepisu.

Layout Hierarchy:
- Header (Full-width):
  - Horní navigace
- Content Container (Positioned below the header):
  - Centrální upload oblast (vertikální zarovnání na střed)

## Horní Navigace
- Logo MediAI s linkem na Dashboard
- Breadcrumb: Dashboard > Nahrát Audio
- Uživatelský avatar s dropdown menu

## Centrální Upload Oblast
- Nadpis stránky: "Nahrát Audio Nahrávku"
- Popisný text: "Vyberte soubor nebo nahrajte přímo přes mikrofon"

## Upload Možnosti (Tab/Toggle Switch)
- Tab 1: Nahrát Soubor (aktivní)
  - Drag-and-drop zóna:
    - Velká ikona upload
    - Text: "Přetáhněte audio soubor sem"
    - Text: "nebo"
    - Tlačítko "Vybrat Soubor"
    - Podporované formáty: MP3, WAV, M4A (max 100 MB)
  - Informace o zpracování:
    - Ikona zámku: "Šifrováno end-to-end"
    - Ikona hodiny: "Přepis trvá 30-90 sekund"
    - GDPR badge
- Tab 2: Nahrát Mikrofonem
  - Velká ikona mikrofonu (neaktivní/aktivní stav)
  - Tlačítko "Spustit Nahrávání" (velké, centrální)
  - Timer zobrazující aktuální délku nahrávky (00:00)
  - Tlačítko "Zastavit Nahrávání" (zobrazí se po startu)
  - Audio waveform vizualizace (při nahrávání)
  - Informační text: "Klikněte pro spuštění nahrávání rozhovoru"

## Předchozí Nahrávky (Sidebar nebo spodní sekce)
- Nadpis: "Poslední Nahrávky"
- Mini seznam posledních 3 nahrávek:
  - Název + datum
  - Status badge
  - Quick action: Zobrazit detail

## Konfigurace Přepisu (Volitelné - Rozbalovací Sekce)
- Nadpis: "Nastavení Přepisu"
- Výběr konfigurace extrakce:
  - Dropdown: "Výchozí (PII + Základní klinická data)"
  - Možnost vybrat custom konfiguraci
  - Link na "Vytvořit novou konfiguraci"
- Jazyk přepisu: Čeština (defaultní, zatím není možnost změny)

## Akční Tlačítka (Po výběru souboru nebo dokončení nahrávky)
- Náhled zvoleného souboru/nahrávky:
  - Název souboru
  - Velikost souboru
  - Délka audio
  - Mini audio přehrávač pro kontrolu
- Tlačítko "Spustit Přepis" (primární CTA, velké)
- Tlačítko "Zrušit" nebo "Nahrát Jiný Soubor"

## Processing Stav (Po spuštění přepisu)
- Progress bar s procentem dokončení
- Status text: "Přepisuji audio pomocí AI..."
- Odhadovaný zbývající čas
- Animace/indikátor zpracování
- Tlačítko "Zrušit Přepis"
