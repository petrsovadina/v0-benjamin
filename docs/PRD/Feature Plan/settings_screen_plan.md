# Nastavení
Stránka pro správu uživatelského účtu, aplikačních preferencí, bezpečnostních nastavení a GDPR compliance.

Layout Hierarchy:
- Header (Full-width):
  - Horní navigace
- Content Container (Positioned below the header):
  - Dvousloupcový layout:
    - Levý sloupec: Navigační menu nastavení (25% šířky)
    - Pravý sloupec: Obsahová oblast nastavení (75% šířky)

## Horní Navigace
- Logo MediAI s linkem na Dashboard
- Breadcrumb: Dashboard > Nastavení
- Uživatelský avatar s dropdown menu

## Levý Sloupec: Navigační Menu Nastavení

### Sekce: Účet
- Profil (aktivní)
- Bezpečnost
- Fakturace a Předplatné

### Sekce: Aplikace
- Obecné Nastavení
- Audio a Přepis
- Notifikace

### Sekce: Soukromí a Data
- GDPR a Ochrana Dat
- Export a Smazání Dat

### Sekce: Podpora
- Nápověda a Dokumentace
- Kontakt na Podporu

## Pravý Sloupec: Obsahová Oblast

### Tab: Profil (aktivní)

#### Základní Informace
- Avatar uživatele (kliknutelný pro změnu)
  - Tlačítko "Změnit Profilový Obrázek"
  - Tlačítko "Odstranit"
- Pole: Jméno a Příjmení
  - Hodnota: "MUDr. Martin Novák"
- Pole: Email
  - Hodnota: "martin.novak@email.cz"
  - Badge: "Ověřeno"
- Pole: Telefon (volitelné)
  - Hodnota: "+420 XXX XXX XXX"
- Pole: Specializace
  - Hodnota: "Lázeňská medicína, Rehabilitace"
- Pole: Zdravotnické Zařízení
  - Hodnota: "Lázně Karlovy Vary"
- Pole: Lékařská Licence
  - Hodnota: "XXXX"
- Tlačítko "Uložit Změny" (primární)

#### Propojené Účty
- Google účet:
  - Ikona Google
  - Email: "martin.novak@gmail.com"
  - Status: "Připojeno"
  - Tlačítko "Odpojit"

### Tab: Bezpečnost

#### Přihlášení a Autentizace
- Aktuální metoda přihlášení: Google OAuth
- Tlačítko "Změnit Metodu Přihlášení"

#### Dvoufaktorová Autentizace (2FA)
- Status: Vypnuto / Zapnuto
- Popis: "Přidejte extra vrstvu zabezpečení pro váš účet"
- Tlačítko "Zapnout 2FA" / "Nastavit 2FA"

#### Aktivní Relace
- Seznam aktivních přihlášení:
  - Session 1:
    - Zařízení: Chrome on Windows
    - Lokace: Karlovy Vary, CZ
    - Poslední aktivita: Právě teď
    - Tlačítko "Odhlásit"
  - Session 2:
    - Zařízení: Safari on iPhone
    - Lokace: Praha, CZ
    - Poslední aktivita: Před 2 hodinami
    - Tlačítko "Odhlásit"
- Tlačítko "Odhlásit Všechna Ostatní Zařízení"

#### Historie Přihlášení
- Timeline posledních přihlášení (10 záznamů)
- Každý záznam obsahuje: Datum, Čas, Zařízení, Lokace, IP adresa

### Tab: Fakturace a Předplatné

#### Aktuální Plán
- Název plánu: "Professional" (nebo "Trial")
- Cena: 1,499 Kč/měsíc
- Další fakturace: 5. ledna 2026
- Počet nahrávek: 234 / ∞ (unlimited)
- Počet uživatelů: 1 / 3
- Tlačítko "Změnit Plán"
- Tlačítko "Zrušit Předplatné"

#### Platební Metoda
- Kreditní karta: **** **** **** 1234 (Visa)
- Expirace: 12/2027
- Tlačítko "Změnit Platební Metodu"
- Tlačítko "Přidat Novou Kartu"

#### Fakturační Historie
- Seznam faktur (tabulka):
  - Datum | Částka | Status | Akce
  - 05.12.2025 | 1,499 Kč | Zaplaceno | Stáhnout PDF
  - 05.11.2025 | 1,499 Kč | Zaplaceno | Stáhnout PDF
  - 05.10.2025 | 1,499 Kč | Zaplaceno | Stáhnout PDF

### Tab: Obecné Nastavení

#### Jazyk a Lokalizace
- Jazyk aplikace: Čeština
- Časové pásmo: (GMT+1) Praha
- Formát data: DD.MM.RRRR
- Formát času: 24-hodinový

#### Zobrazení
- Motiv: Světlý / Tmavý / Automaticky (podle systému)
- Velikost písma: Malé / Střední / Velké
- Hustota obsahu: Kompaktní / Pohodlná / Prostorná

#### Výchozí Nastavení
- Výchozí konfigurace extrakce: Dropdown s výběrem
- Automaticky spustit přepis po nahrání: Toggle ON/OFF
- Automatické ukládání v editoru: Toggle ON (každých 30 s)

### Tab: Audio a Přepis

#### Nastavení Audio
- Kvalita nahrávání: Nízká / Střední / Vysoká (doporučeno)
- Automatické odstranění šumu: Toggle ON
- Maximální délka nahrávky: 60 minut (dropdown: 30/60/120 minut)

#### Nastavení Přepisu
- Model přepisu: Gemini 3 Pro (fixed)
- Jazyk přepisu: Čeština (fixed pro MVP)
- Přesnost vs. Rychlost: Slider (Rychlejší ← → Přesnější)
- Automatické časové značky: Toggle ON (každých 30 sekund)
- Formátování výstupu:
  - Checkbox: Strukturovat podle replik (Lékař:/Pacient:)
  - Checkbox: Přidat interpunkci automaticky
  - Checkbox: Kapitalizovat začátky vět

#### Nastavení Extrakce
- Automatická extrakce po přepisu: Toggle ON
- Zvýraznit entity v textu: Toggle ON
- Zobrazit confidence score: Toggle ON
- Minimální confidence threshold: Slider (50% - 95%)

### Tab: Notifikace

#### Email Notifikace
- Přepis dokončen: Toggle ON
- Chyba při přepisu: Toggle ON
- Exportován přepis: Toggle OFF
- Týdenní souhrn aktivity: Toggle ON
- Marketingové zprávy: Toggle OFF

#### Push Notifikace (Webové)
- Přepis dokončen: Toggle ON
- Chyba při přepisu: Toggle ON
- Připomínky a úkoly: Toggle OFF

#### Notifikace v Aplikaci
- Zobrazit notifikační badge: Toggle ON
- Zvukové upozornění: Toggle OFF

### Tab: GDPR a Ochrana Dat

#### Přehled Zpracování Dat
- Info box s vysvětlením:
  - Jaká data sbíráme
  - Jak data používáme
  - Kde data uchováváme (EU data center - Google Cloud)
  - Jak dlouho data uchováváme

#### Vaše Práva (GDPR)
- Právo na přístup k datům
  - Popis: "Stáhněte kopii všech vašich dat"
  - Tlačítko "Stáhnout Moje Data"
- Právo na opravu
  - Popis: "Opravte nepřesné osobní údaje"
  - Link na "Upravit Profil"
- Právo na výmaz (Právo být zapomenut)
  - Popis: "Trvale smažte svůj účet a všechna data"
  - Tlačítko "Požádat o Smazání Účtu" (červené)
- Právo na přenositelnost
  - Popis: "Exportujte data v strojově čitelném formátu"
  - Tlačítko "Exportovat Data (JSON)"

#### Souhlas a Zpracování
- Checkbox: "Souhlasím se zpracováním citlivých zdravotních dat" (CHECKED, povinné)
- Checkbox: "Souhlasím se zpracováním mých dat za účelem zlepšování AI modelů" (volitelné)
- Datum posledního souhlasu: 1.12.2025
- Link na "Kompletní Zásady Ochrany Osobních Údajů"

#### Bezpečnost Dat
- Šifrování: End-to-end šifrování všech audio nahrávek a přepisů
- Uchovávání: Data uložená v EU data centerech (Frankfurt, Německo)
- Audit trail: Kompletní historie přístupu k datům
- Tlačítko "Zobrazit Audit Log"

### Tab: Export a Smazání Dat

#### Export Všech Dat
- Popis: "Stáhněte kompletní archiv všech vašich nahrávek, přepisů a nastavení"
- Formát: ZIP archiv obsahující:
  - Všechny audio soubory
  - Všechny přepisy (TXT + JSON)
  - Konfigurační soubory
  - Metadata a historie
- Tlačítko "Vytvořit Export" (primární)
- Info: "Export může trvat několik minut. Zašleme vám email, když bude připraven."

#### Předchozí Exporty
- Seznam vytvořených exportů:
  - Export 1:
    - Datum vytvoření: 15.11.2025
    - Velikost: 2.3 GB
    - Status: Připraveno
    - Tlačítko "Stáhnout"
    - Tlačítko "Smazat"
  - Export 2:
    - Datum vytvoření: 01.10.2025
    - Velikost: 1.8 GB
    - Status: Připraveno
    - Tlačítko "Stáhnout"
    - Tlačítko "Smazat"

#### Smazání Účtu
- Warning box (červený):
  - "⚠️ Trvale smazat účet"
  - Popis: "Tato akce je nevratná. Všechna vaše data budou trvale smazána do 30 dnů."
- Checklist před smazáním:
  - Checkbox: "Rozumím, že tato akce je nevratná"
  - Checkbox: "Exportoval jsem všechna důležitá data"
  - Checkbox: "Zrušil jsem své předplatné"
- Tlačítko "Smazat Můj Účet" (červené, disabled dokud nejsou checked všechny checkboxy)

### Tab: Nápověda a Dokumentace

#### Rychlá Nápověda
- Sekce s často kladenými otázkami (FAQ):
  - Jak nahrát první audio?
  - Jak upravit přepis?
  - Jak vytvořit custom konfiguraci extrakce?
  - Jak exportovat přepis?
  - Jak změnit předplatné?
- Každá FAQ je collapsible s odpovědí

#### Dokumentace a Tutoriály
- Link: "Kompletní Uživatelská Příručka"
- Link: "Video Tutoriály"
- Link: "Tipy a Triky"
- Link: "Co je nového? (Changelog)"

#### Kontakt na Podporu
- Email: podpora@mediai.cz
- Telefon: +420 XXX XXX XXX
- Pracovní doba: Po-Pá 8:00-17:00
- Tlačítko "Odeslat Zprávu Podpoře"

#### Systémové Informace
- Verze aplikace: 1.0.2
- Poslední aktualizace: 1.12.2025
- Browser: Chrome 120.0
- Platforma: Windows 11
