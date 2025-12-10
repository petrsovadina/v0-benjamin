# Náhled Vygenerované Zprávy
Stránka zobrazující AI vygenerovanou lékařskou zprávu s možností kontroly, editace a exportu. Lékař může zkontrolovat strukturovaný dokument před finálním exportem do ambulantního IS.

Layout Hierarchy:
- Header (Full-width):
  - Horní navigace
- Content Container (Positioned below the header):
  - Dvousloupcový layout:
    - Levý sloupec (70% šířky): AI vygenerovaná zpráva s editorem
    - Pravý sloupec (30% šířky): Metadata, akce, náhled přepisu

## Horní Navigace
- Logo MediAI s linkem na Dashboard
- Breadcrumb: Dashboard > Detail Přepisu > Vygenerovaná Zpráva
- Uživatelský avatar s dropdown menu

## Levý Sloupec: Vygenerovaná Zpráva

### Action Bar (Sticky Top)
- Název typu zprávy: "Vstupní Vyšetření - Lázně"
- Status badge: "✓ Vygenerováno" (zelený)
- Tlačítka:
  - "Uložit Změny" (primární, pokud byly provedeny úpravy)
  - "Exportovat" (dropdown):
    - Exportovat jako .TXT
    - Exportovat jako .DOCX
    - Zkopírovat do Schránky (formátovaný text)
    - Zkopírovat do Schránky (plain text)
  - "Regenerovat Zprávu" (sekundární, outlined) - zobrazí modal s potvrzením
  - "Zpět na Výběr Šablony" (sekundární, ghost)

### Zpráva Editor (WYSIWYG)

**Metadata Sekce (Top of Document)**
- Datum vyšetření: 5.12.2025
- Jméno pacienta: Pavel Novotný
- Rodné číslo: XXXXXX/XXXX
- Lékař: MUDr. Martin Novák
- Zařízení: Lázně Karlovy Vary

**Generované Sekce Zprávy:**

#### Sekce 1: Anamnéza
- Nadpis sekce s ikonou pro regeneraci této sekce
- Editovatelný text (WYSIWYG):
  - Rodinná anamnéza
  - Osobní anamnéza
  - Alergologická anamnéza
  - Farmakologická anamnéza
- Tlačítko "🔄 Regenerovat Tuto Sekci" (small, ghost) - při hoveru zobrazí tooltip

#### Sekce 2: Nynější Onemocnění
- Nadpis sekce s ikonou pro regeneraci
- Editovatelný text popisující aktuální zdravotní stav a důvod lázeňské léčby

#### Sekce 3: Indikace k Lázeňské Léčbě
- Nadpis sekce
- Editovatelný seznam diagnóz a indikací

#### Sekce 4: Kontraindikace
- Nadpis sekce
- Editovatelný seznam kontraindikací (pokud žádné, zobrazí "Bez kontraindikací")

#### Sekce 5: Objektivní Nález
- Nadpis sekce
- Editovatelný text s fyzikálním vyšetřením:
  - Celkový stav
  - Vitální funkce
  - Lokální nález
  - Neurologický status (pokud relevantní)

#### Sekce 6: Léčebný Plán
- Nadpis sekce
- Editovatelný strukturovaný seznam:
  - Navrhované procedury
  - Frekvence aplikace
  - Doporučená medikace
  - Režimová opatření

#### Sekce 7: Závěr a Doporučení
- Nadpis sekce
- Editovatelný text se závěrečným shrnutím a doporučeními

**Editor Features:**
- Inline editace každé sekce
- Formátovací toolbar (tučné, kurzíva, seznamy, nadpisy)
- Automatické ukládání změn (každých 30 sekund)
- Indikátor posledního uložení: "Uloženo před 2 minutami"
- Word count pro celý dokument

### Regenerace Sekce Modal
- Když uživatel klikne "Regenerovat Tuto Sekci":
  - Modal s potvrzením: "Opravdu chcete regenerovat tuto sekci? Stávající obsah bude přepsán."
  - Možnost zadat dodatečné instrukce: "Zaměřte se více na kardiovaskulární problematiku"
  - Tlačítka: "Zrušit" / "Regenerovat"

## Pravý Sloupec: Metadata a Akce

### Informace o Generování
- Card s metadaty:
  - Čas generování: "45 sekund"
  - Datum a čas: "5.12.2025, 14:32"
  - Použitá šablona: "Vstupní Vyšetření - Lázně"
  - Zdroj: "Přepis z 5.12.2025, 14:25"

### Statistiky Zprávy
- Card se statistikami:
  - Počet slov: 847
  - Počet sekcí: 7
  - Úplnost: 95% (progress bar) - indikuje, kolik sekcí obsahuje kompletní informace
  - Confidence score: 92% - AI confidence v extrahovaných informacích

### Náhled Přepisu (Collapsible)
- Card s náhledem původního přepisu
- Header: "Zdrojový Přepis" s tlačítkem pro expand/collapse
- Při rozbalení:
  - Zkrácený text přepisu (prvních 300 znaků)
  - Link "Zobrazit Kompletní Přepis" → otevře Transcript Detail v novém tabu

### Extrahované Entity (Collapsible)
- Card se seznamem extrahovaných entit
- Header: "Extrahované Informace" s tlačítkem pro expand/collapse
- Při rozbalení:
  - Strukturovaný přehled:
    - **PII**: Jméno, Rodné číslo, Adresa
    - **Diagnózy**: M54.5 (Bolesti bederní páteře), I10 (Esenciální hypertenze)
    - **Medikace**: Prenessa 5mg, Ibalgin při bolesti
    - **Alergies**: Penicilin
    - **Vitální funkce**: TK 140/85, Puls 72

### Quick Actions
- Tlačítko "📧 Odeslat Emailem" (sekundární)
- Tlačítko "🖨️ Tisk" (sekundární)
- Tlačítko "📁 Uložit do Šablony" (sekundární) - umožní vytvořit custom šablonu na základě této zprávy

### Bezpečnost a Compliance
- Badge: "🔒 Šifrováno end-to-end"
- Badge: "🇪🇺 GDPR Compliant"
- Audit log link: "Zobrazit Historii Změn"

## Export Modal
Když uživatel klikne "Exportovat":
- Modal s náhledem:
  - Preview finálního formátování
  - Volba formátu: .TXT / .DOCX / Copy to Clipboard
  - Checkbox: "Zahrnout metadata (pacient, lékař, datum)"
  - Checkbox: "Připojit originální přepis jako přílohu"
- Tlačítka: "Zrušit" / "Exportovat"

Po exportu:
- Success notifikace: "✓ Zpráva úspěšně exportována"
- Automatické přesměrování zpět na Dashboard po 2 sekundách (s možností "Zůstat na stránce")
