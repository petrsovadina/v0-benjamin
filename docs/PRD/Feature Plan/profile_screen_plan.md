# Profil Uživatele
Veřejný profil uživatele s přehledem aktivity, statistik a profesionálních informací.

Layout Hierarchy:
- Header (Full-width):
  - Horní navigace
- Content Container (Positioned below the header):
  - Hlavní obsahová oblast

## Horní Navigace
- Logo MediAI s linkem na Dashboard
- Breadcrumb: Dashboard > Profil
- Tlačítko "Upravit Profil" (primární CTA)
- Uživatelský avatar s dropdown menu

## Hlavní Obsahová Oblast

### Profilová Sekce (Header)
- Velký avatar uživatele
- Jméno a titul: "MUDr. Martin Novák"
- Specializace: "Lázeňská medicína, Rehabilitace"
- Zdravotnické zařízení: "Lázně Karlovy Vary"
- Status badge: "Professional" (typ účtu)
- Datum registrace: "Člen od listopadu 2025"
- Quick actions:
  - Tlačítko "Upravit Profil"
  - Tlačítko "Nastavení"

### Statistiky (Cards Row)
- Card 1: Celkový Počet Nahrávek
  - Číslo: 234
  - Trend: +12 tento týden (zelená šipka)
- Card 2: Ušetřený Čas
  - Číslo: 94 hodin
  - Popis: "Díky automatickému přepisu"
- Card 3: Přesnost Přepisů
  - Číslo: 96.5%
  - Popis: "Průměrná přesnost"
- Card 4: Aktivita Tento Měsíc
  - Číslo: 47 nahrávek
  - Graf: Mini sparkline

### Aktivita a Historie (Tabs)

#### Tab: Nedávná Aktivita (aktivní)
- Timeline posledních akcí:
  - Dnes 14:30: Exportován přepis "Kontrolní vyšetření - P. Novotný"
  - Dnes 09:15: Vytvořena nová nahrávka "Vstupní vyšetření - P. Svoboda"
  - Včera 16:45: Upravena konfigurace "Výstupní Zpráva - Fyzioterapie"
  - Včera 11:20: Exportován přepis "Výstupní zpráva - P. Černá"
  - 03.12.2025: Vytvořena nová konfigurace extrakce
  - 02.12.2025: Vytvořeno 5 nových nahrávek
  - 01.12.2025: Aktualizován profil
- Tlačítko "Načíst Více"

#### Tab: Statistiky Měsíce
- Graf počtu nahrávek za posledních 6 měsíců (Line chart)
- Graf ušetřeného času (Bar chart)
- Rozložení typů zpráv (Pie chart):
  - Vstupní vyšetření: 45%
  - Kontrolní vyšetření: 35%
  - Výstupní zprávy: 20%

#### Tab: Konfigurace Extrakce
- Seznam všech vytvořených konfigurací s jejich využitím:
  - Výchozí (PII + Základní): 156 použití
  - Výstupní Zpráva - Fyzioterapie: 45 použití
  - Kontrolní Vyšetření - Krátká Forma: 23 použití
  - Vstupní Vyšetření - Komplexní: 10 použití

### Profesionální Informace

#### Kvalifikace
- Titul: MUDr.
- Specializace: Lázeňská medicína, Rehabilitace a fyzikální medicína
- Lékařská licence: XXXX
- Zdravotnické zařízení: Lázně Karlovy Vary

#### Kontaktní Informace (Privátní)
- Email: martin.novak@email.cz
- Telefon: +420 XXX XXX XXX
- Pozn: Kontaktní údaje viditelné pouze pro vlastníka profilu

### Nastavení Soukromí

#### Viditelnost Profilu
- Radio buttons:
  - Soukromý (pouze já)
  - Viditelný pro kolegy ve stejném zařízení
  - Veřejný (volitelné - pro případné budoucí社交 features)
- Aktuálně vybraná: Soukromý

#### Sdílení Dat
- Checkbox: "Povolte anonymizované sdílení statistik pro zlepšování AI modelů"
- Checkbox: "Zobrazit moji aktivitu kolegům" (OFF)
