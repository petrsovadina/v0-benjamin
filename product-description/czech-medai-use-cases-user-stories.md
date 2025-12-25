# Czech MedAI — Use Cases & User Stories

---

## 📋 Use Cases

### UC-01: Rychlý klinický dotaz (QuickConsult)

**Název:** Rychlé vyhledání klinické informace

**Aktér:** Lékař (praktický lékař, specialista, nemocniční lékař)

**Předpoklady:**
- Lékař je přihlášen do systému
- Má ověřenou lékařskou licenci (IČP/ČLK)

**Hlavní scénář:**
1. Lékař zadá klinický dotaz v češtině
2. Systém klasifikuje typ dotazu (léky, guidelines, obecný)
3. Systém vyhledá relevantní informace v příslušných zdrojích
4. Systém vygeneruje odpověď s inline citacemi
5. Lékař obdrží odpověď do 5 sekund
6. Lékař může kliknout na citaci pro zobrazení původního zdroje

**Alternativní scénáře:**
- 2a. Dotaz je nejasný → Systém požádá o upřesnění
- 4a. Nedostatek zdrojů → Systém informuje o omezené evidenci
- 5a. Timeout → Systém zobrazí částečnou odpověď s upozorněním

**Výsledek:** Lékař získá ověřenou odpověď s citacemi

---

### UC-02: Vyhledání informací o léku

**Název:** Získání informací o léčivém přípravku

**Aktér:** Lékař

**Předpoklady:**
- Lékař je přihlášen
- SÚKL databáze je dostupná

**Hlavní scénář:**
1. Lékař zadá název léku nebo účinné látky
2. Systém vyhledá lék v SÚKL databázi
3. Systém zobrazí:
   - Indikace a kontraindikace
   - Dávkování
   - Lékové interakce
   - Nežádoucí účinky
   - Úhradové podmínky VZP
4. Lékař může zobrazit plné SPC (Souhrn údajů o přípravku)

**Alternativní scénáře:**
- 2a. Lék není v ČR registrován → Systém nabídne alternativy
- 3a. Více přípravků stejného názvu → Systém zobrazí seznam k výběru

**Výsledek:** Lékař má kompletní informace o léku včetně úhrad

---

### UC-03: Vyhledání guidelines

**Název:** Nalezení doporučeného postupu

**Aktér:** Lékař

**Předpoklady:**
- Lékař je přihlášen
- Guidelines databáze je aktuální

**Hlavní scénář:**
1. Lékař zadá diagnózu nebo klinickou situaci
2. Systém identifikuje relevantní guidelines (české i mezinárodní)
3. Systém zobrazí:
   - Shrnutí doporučeného postupu
   - Klíčové body
   - Odkaz na plný text guidelines
4. Lékař může požádat o porovnání českých a mezinárodních guidelines

**Alternativní scénáře:**
- 2a. České guidelines neexistují → Systém nabídne mezinárodní (ESC, ADA...)
- 3a. Guidelines jsou zastaralé → Systém upozorní na datum vydání

**Výsledek:** Lékař zná aktuální doporučený postup

---

### UC-04: Ověření úhrady

**Název:** Zjištění úhradových podmínek

**Aktér:** Lékař

**Předpoklady:**
- Lékař je přihlášen
- VZP data jsou aktuální

**Hlavní scénář:**
1. Lékař zadá dotaz na úhradu léku nebo výkonu
2. Systém vyhledá informace v databázi VZP
3. Systém zobrazí:
   - Výši úhrady
   - Podmínky úhrady (preskripční omezení)
   - Doplatek pacienta
   - Alternativní plně hrazené přípravky
4. Lékař může zobrazit detail úhradových podmínek

**Výsledek:** Lékař ví, zda je lék/výkon hrazen a za jakých podmínek

---

### UC-05: Historie dotazů

**Název:** Zobrazení historie klinických dotazů

**Aktér:** Lékař

**Hlavní scénář:**
1. Lékař otevře sekci „Historie"
2. Systém zobrazí seznam předchozích dotazů
3. Lékař může:
   - Filtrovat podle data, typu dotazu
   - Vyhledávat v historii
   - Znovu otevřít předchozí dotaz
   - Exportovat historii

**Výsledek:** Lékař má přístup k předchozím dotazům a odpovědím

---

## 👤 User Stories

### Epic 1: Klinické dotazy

| ID | User Story | Priorita | Akceptační kritéria |
|----|------------|----------|---------------------|
| US-001 | Jako **praktický lékař** chci zadat klinický dotaz v češtině, abych rychle získal odpověď bez nutnosti prohledávat více zdrojů. | P0 | - Odpověď do 5 sekund<br>- Minimálně 2 citace<br>- Česká terminologie |
| US-002 | Jako **specialista** chci kliknout na citaci a zobrazit původní zdroj, abych mohl ověřit informace. | P0 | - Klikatelné PMID/DOI odkazy<br>- Otevření v novém okně<br>- Zobrazení abstraktu |
| US-003 | Jako **lékař** chci dostávat odpovědi s korektní českou lékařskou terminologií, abych je mohl přímo použít. | P0 | - Správné české názvy diagnóz<br>- Zkratky vysvětleny<br>- Konzistentní terminologie |
| US-004 | Jako **lékař na urgentním příjmu** chci mít možnost hlasového zadání dotazu, abych nemusel psát během ošetření. | P2 | - Speech-to-text v češtině<br>- Přesnost > 95%<br>- Funguje i v hlučném prostředí |

---

### Epic 2: Informace o lécích

| ID | User Story | Priorita | Akceptační kritéria |
|----|------------|----------|---------------------|
| US-005 | Jako **praktický lékař** chci zjistit informace o konkrétním léku, abych věděl indikace, kontraindikace a dávkování. | P1 | - Data ze SÚKL<br>- Aktuální SPC<br>- Kompletní informace |
| US-006 | Jako **lékař** chci vidět, zda je lék hrazen VZP, abych pacientovi předepsal dostupný lék. | P1 | - Aktuální úhradová data<br>- Zobrazení doplatku<br>- Alternativní přípravky |
| US-007 | Jako **lékař** chci být upozorněn na lékové interakce, abych předešel nežádoucím kombinacím. | P2 | - Kontrola zadaných léků<br>- Klasifikace závažnosti<br>- Doporučení alternativ |
| US-008 | Jako **lékař** chci vyhledat lék podle účinné látky, abych našel všechny dostupné přípravky. | P1 | - Vyhledávání podle ATC<br>- Seznam generik<br>- Porovnání cen |

---

### Epic 3: Guidelines a doporučené postupy

| ID | User Story | Priorita | Akceptační kritéria |
|----|------------|----------|---------------------|
| US-009 | Jako **kardiolog** chci najít aktuální české guidelines pro specifickou diagnózu, abych postupoval podle národních standardů. | P0 | - České guidelines prioritně<br>- Datum vydání<br>- Odkaz na plný text |
| US-010 | Jako **specialista** chci porovnat české a mezinárodní guidelines, abych pochopil rozdíly v doporučeních. | P2 | - Paralelní zobrazení<br>- Zvýraznění rozdílů<br>- Vysvětlení odlišností |
| US-011 | Jako **lékař** chci být informován o nových guidelines v mém oboru, abych měl vždy aktuální informace. | P2 | - Notifikace o novinkách<br>- Personalizace podle oboru<br>- Shrnutí změn |

---

### Epic 4: Uživatelský účet a nastavení

| ID | User Story | Priorita | Akceptační kritéria |
|----|------------|----------|---------------------|
| US-012 | Jako **lékař** chci se přihlásit pomocí své profesní identity, aby byl můj přístup ověřen. | P0 | - OAuth přihlášení<br>- Ověření licence ČLK/IČP<br>- 2FA povinné |
| US-013 | Jako **lékař** chci zobrazit historii svých dotazů, abych se mohl vrátit k předchozím odpovědím. | P1 | - Seznam dotazů<br>- Filtrování a vyhledávání<br>- Export do PDF |
| US-014 | Jako **lékař** chci si uložit často používané dotazy, abych je nemusel zadávat opakovaně. | P2 | - Oblíbené dotazy<br>- Organizace do složek<br>- Rychlý přístup |
| US-015 | Jako **lékař** chci nastavit preferovaný jazyk odpovědí, abych mohl volit mezi češtinou a angličtinou. | P2 | - Volba jazyka<br>- Zapamatování preference<br>- Přepínání v rozhraní |

---

### Epic 5: Integrace a rozšíření

| ID | User Story | Priorita | Akceptační kritéria |
|----|------------|----------|---------------------|
| US-016 | Jako **lékař** chci používat Czech MedAI přímo v mém EHR systému, abych nemusel přepínat aplikace. | P2 | - Browser extension<br>- Podpora STAPRO, ICZ<br>- Kontextový dotaz |
| US-017 | Jako **lékař** chci sdílet odpověď s kolegou, abychom mohli konzultovat složitý případ. | P2 | - Generování odkazu<br>- Export do PDF<br>- Anonymizace dat |
| US-018 | Jako **vedoucí oddělení** chci vidět statistiky používání, abych mohl vyhodnotit přínos nástroje. | P2 | - Dashboard statistik<br>- Export reportů<br>- Anonymizovaná data |

---

## 🎯 Prioritizace (MoSCoW)

### Must Have (P0) — MVP
- US-001: Zadání klinického dotazu
- US-002: Zobrazení citací
- US-003: Česká terminologie
- US-009: Vyhledání guidelines
- US-012: Přihlášení a ověření

### Should Have (P1) — Beta
- US-005: Informace o lécích
- US-006: Úhrady VZP
- US-008: Vyhledávání podle účinné látky
- US-013: Historie dotazů

### Could Have (P2) — Future
- US-004: Hlasové zadání
- US-007: Lékové interakce
- US-010: Porovnání guidelines
- US-011: Notifikace o novinkách
- US-014: Uložené dotazy
- US-015: Volba jazyka
- US-016: EHR integrace
- US-017: Sdílení odpovědí
- US-018: Statistiky používání

---

## 📊 User Journey Map

### Praktický lékař — Typický den

```
8:00  Příchod do ordinace
      │
8:15  První pacient — diabetes + hypertenze
      │
      ├──→ Czech MedAI: "První linie léčby hypertenze u diabetika?"
      │    ← Odpověď za 4s: ACE inhibitory/sartany [citace]
      │
9:30  Pacient s neznámým lékem ze zahraničí
      │
      ├──→ Czech MedAI: "Informace o léku Entresto"
      │    ← SÚKL data + úhrady VZP + alternativy
      │
11:00 Složitý případ — potřeba konzultace
      │
      ├──→ Czech MedAI: "Guidelines fibrilace síní 2024"
      │    ← České i ESC guidelines + porovnání
      │
12:30 Přestávka
      │
14:00 Odpolední ordinace
      │
      ├──→ Czech MedAI: Historie dotazů → návrat k rannímu případu
      │
17:00 Konec ordinace
```

---

*Dokument vytvořen: 13.12.2025*
