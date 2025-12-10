# PRD — MediAI MVP: AI-Powered Lékařská Dokumentace pro Lázně

## 1) Background

Lázeňští lékaři čelí extrémní administrativní zátěži při zpracování desítek vstupních, kontrolních a výstupních vyšetření týdně. Ruční psaní nebo diktování s následným přepisováním zabírá až 60% jejich pracovní doby, což vede k chronickému vyhoření a odvedení pozornosti od péče o pacienty. Tato iterace MediAI MVP (Phase 1) adresuje klíčový problém z Product Charter — transformaci audio záznamů lékařských rozhovorů do kompletních strukturovaných lékařských zpráv pomocí AI. Nejde jen o přepis, ale o automatické generování finálních dokumentů (vstupní vyšetření, kontroly, výstupky, dekursy, epikrízy) připravených k okamžitému použití. Cílíme přímo na Dr. Martina Nováka, lázeňského lékaře, který potřebuje rychlé a přesné nástroje pro dokumentaci bez technické složitosti. Tento problém řešíme právě nyní, protože kombinace Gemini 3 Pro, LangChain Extract a moderních LLM konečně umožňuje dosáhnout potřebné přesnosti v české lékařské terminologii při zachování GDPR compliance a bezpečnosti.

## 2) Objectives & Desired Outcomes

- **Dramatické snížení administrativní zátěže:** Lékaři tráví o 60–70% méně času psaním dokumentace, vstupní zpráva trvá 2–3 minuty místo 10–15 minut, výstupní zpráva 5 minut místo 20 minut, díky AI generování kompletních strukturovaných dokumentů připravených k okamžitému použití
- **Vysoká přesnost a konzistence:** Všechny lékařské zprávy mají jednotnou strukturu, obsahují kompletní informace a splňují požadavky pojišťoven bez dodatečných úprav, chybovost při přepisu české lékařské terminologie je pod 5%, AI generované zprávy používají profesionální lékařské formulace a správnou strukturu sekcí
- **Bezproblémové přijetí lékařem:** Systém je tak intuitivní, že lékař začne produktivně pracovat během první hodiny bez školení, nahrání audio a získání přepisu trvá méně než 90 sekund, AI generování kompletní lékařské zprávy zabere 30-60 sekund, finální kontrola a úpravy zabere méně než 2 minuty
- **Absolutní bezpečnost a důvěra:** Zdravotní data jsou šifrována end-to-end, systém je plně GDPR compliant, lékař má jasný přehled o zpracování dat a viditelné indikátory zabezpečení v každém kroku
- **Flexibilita a přizpůsobení:** Lékaři mohou používat defaultní šablony zpráv nebo vytvářet vlastní custom šablony odpovídající workflow jejich zařízení, systém se přizpůsobí individuálním potřebám bez ztráty jednoduchosti
- **Non-goals / Boundaries (Phase 1):** Neposkytujeme real-time přepis během rozhovoru (batch processing only), neprovádíme pokročilé klinické reasoning nebo diferenciální diagnostiku, neintegrujeme přímo do konkrétních nemocničních IS přes API (pouze export souborů a copy-paste workflow), nepodporujeme složité formátování (tabulky, grafy) v textovém editoru

## 3) Users & Stories

- **Primary Persona:** Dr. Martin Novák (Lázeňský lékař)
  - Story A: Jako lázeňský lékař chci nahrát audio rozhovor se vstupním vyšetřením pacienta a do 90 sekund získat strukturovaný textový přepis, abych nemusel trávit 10 minut ručním psaním anamnézy.
  - Story B: Jako lázeňský lékař chci, aby systém automaticky identifikoval klíčové klinické informace (diagnózy, medikace, alergies, kontraindikace) z přepisu, abych mohl rychle vytvořit kompletní vstupní zprávu.
  - Story C: Jako lázeňský lékař chci mít možnost přehrát audio synchronizovaně s textem a opravit případné chyby v přepisu, abych měl jistotu 100% přesnosti finální zprávy.
  - Story D: Jako lázeňský lékař chci nakonfigurovat vlastní extrakční šablonu pro různé typy zpráv (vstup, kontrola, výstup), abych měl konzistentní strukturu dokumentace pro celý pobyt pacienta.
  - Story E: **[NOVÉ]** Jako lázeňský lékař chci automaticky vygenerovat kompletní vstupní zprávu z přepisu rozhovoru (včetně anamnézy, nynějšího onemocnění, objektivního nálezu, závěru a doporučení) během 30-60 sekund, abych nemusel zprávu psát ručně a mohl se věnovat dalšímu pacientovi.
  - Story F: **[NOVÉ]** Jako lázeňský lékař chci vybrat z předpřipravených šablon zpráv (vstupní vyšetření, kontrola, výstupka, dekurs) nebo vytvořit vlastní šablonu s custom strukturou sekcí, abych měl konzistentní formátování odpovídající požadavkům mého zařízení a pojišťoven.
  - Story G: **[NOVÉ]** Jako lázeňský lékař chci mít možnost zkontrolovat a upravit AI vygenerovanou zprávu před exportem, abych měl plnou kontrolu nad finálním dokumentem a mohl opravit případné nepřesnosti.
  - Story H: Jako lázeňský lékař chci exportovat finální zprávu ve formátech .txt nebo .docx s jednotným formátováním, abych ji mohl okamžitě vložit do nemocničního IS (SmartMEDIX, Medicus, CGM) nebo zaslat praktickému lékaři.
  - Story I: Jako lázeňský lékař chci vidět jasné indikátory zabezpečení a GDPR compliance, abych měl důvěru, že citlivá zdravotní data jsou v bezpečí.
  - Story J: Jako lázeňský lékař chci mít možnost diktovat poznámky během obchůzky mimo ordinaci (tablet/mobil), abych mohl efektivně dokumentovat kontroly přímo u fyzioterapeutických provozů.

## 4) Key Feature

- **Rychlé nahrání audio (soubor + mikrofon):** Drag-and-drop upload audio souborů (MP3, WAV, M4A) nebo přímé nahrávání přes mikrofon jedním kliknutím, okamžité spuštění AI přepisu bez dalších kroků
- **AI přepis s Gemini 3 Pro:** Automatický přepis audio do textu během 30–90 sekund s podporou české lékařské terminologie, viditelný progress bar a indikace stavu (Čeká, Přepisuje se, Hotovo, Chyba)
- **Automatická extrakce klinických dat (LangChain Extract):** Defaultní identifikace PII entit a základních klinických dat (diagnózy, medikace, symptomy, alergies, vitální funkce), zvýraznění extrahovaných entit v textu, strukturovaný přehled nalezených informací
- **Konfigurovatelná extrakce:** Možnost vytvořit custom konfiguraci extrakce buď přirozeným jazykem ("chci extrahovat fyzioterapeutické procedury") nebo definováním konkrétních entit, uložení a opakované použití konfigurací pro různé typy zpráv
- **[NOVÉ] AI generování kompletních lékařských zpráv:** Automatická transformace přepisu a extrahovaných entit do finální lékařské zprávy (vstupní vyšetření, kontrolní zpráva, výstupní zpráva, dekurs, epikríza) s profesionální strukturou, správnou terminologií a formulacemi během 30-60 sekund, kompletní zpráva rozdělená do standardních sekcí (anamnéza, nynější onemocnění, objektivní nález, závěr, doporučení)
- **[NOVÉ] Správa šablon zpráv:** Předpřipravené defaultní šablony pro běžné typy zpráv (vstupní vyšetření - lázně, kontrolní vyšetření, výstupní zpráva, dekurs, epikríza) s možností vytvoření vlastních custom šablon, definování struktury sekcí, pořadí, povinných polí a preferovaných formulací, uložení a opakované použití šablon
- **[NOVÉ] Editor AI vygenerovaných zpráv:** WYSIWYG editor pro kontrolu a úpravu AI vygenerované zprávy před exportem, možnost upravit libovolnou sekci nebo formulaci, tlačítko pro regeneraci konkrétní sekce, preview finálního formátování
- **WYSIWYG textový editor se synchronizovaným audio:** Přehledný editor s možností formátování, audio přehrávač vedle textu pro snadnou kontrolu přepisu, tlačítko pro zkopírování textu do schránky
- **Export a správa přepisů:** Přehledný dashboard všech nahrávek s jejich stavy, možnost filtrování a vyhledávání, export finálního přepisu i vygenerovaných zpráv ve formátech .txt a .docx s konzistentním formátováním, copy-paste workflow pro okamžité vložení do ambulantních systémů (SmartMEDIX, Medicus, CGM, PC Doktor)
- **Google OAuth autentizace:** Jednoduché přihlášení přes Google účet pomocí Firebase, bezpečná správa session, jasné indikátory zabezpečení a GDPR compliance
- **Bezpečnost a GDPR compliance:** End-to-end šifrování dat (at rest i in transit), viditelné security badges, transparentní komunikace zpracování dat, audit trail a historie změn

## 5) Key Flow

- **Example:** **[AKTUALIZOVÁNO]** Vstupní vyšetření nového pacienta v lázních s AI generováním zprávy
  - **Trigger:** Lékař provádí ranní vstupní vyšetření nového pacienta, vede rozhovor o anamnéze, indikaci, kontraindikacích a léčebném plánu
  - **Path:** Lékař klikne na "Nová nahrávka" → zapne mikrofon → vede běžný rozhovor s pacientem → ukončí nahrávání → systém automaticky spustí AI přepis (30–90 s) → zobrazí se textový přepis se zvýrazněnými extrahovanými entitami (PII, diagnózy, medikace, alergies) → **[NOVÉ]** lékař klikne "Generovat Zprávu" → vybere šablonu "Vstupní vyšetření - Lázně" → AI vygeneruje kompletní strukturovanou zprávu během 30-60 s (anamnéza, nynější onemocnění, objektivní nález, závěr, doporučení) → lékař zkontroluje zprávu a provede případné úpravy → klikne "Exportovat" nebo "Zkopírovat" pro vložení do SmartMEDIX
  - **Result:** Lékař má kompletní finální vstupní zprávu připravenou k okamžitému použití během 2–3 minut místo 10–15 minut ručního psaní, zpráva má profesionální formulace a konzistentní strukturu

- **Example:** **[NOVÉ]** Generování výstupní zprávy z kumulovaných záznamů
  - **Trigger:** Pacient je před ukončením lázeňského pobytu, lékař potřebuje vytvořit výstupní zprávu shrnující celý pobyt, reakci na léčbu a doporučení pro domácí péči
  - **Path:** Lékař otevře záznam pacienta na dashboardu → vidí všechny přepisy z celého pobytu (vstupní vyšetření, 3 kontroly, komunikace s fyzioterapeuty) → klikne "Generovat Výstupní Zprávu" → vybere šablonu "Výstupní zpráva - Lázně" → systém analyzuje všechny dostupné záznamy → AI vygeneruje komprehenzivní výstupní zprávu během 60-90 s (sumarizace pobytu, průběh léčby, dosažené výsledky, doporučení) → lékař zkontroluje a doplní osobní komentář → exportuje .docx pro zaslání praktickému lékaři a pojišťovně
  - **Result:** Výstupní zpráva, která by běžně zabírá 20-30 minut ručního psaní a agregace informací, je připravena během 5 minut s kompletním přehledem celého pobytu

- **Example:** Kontrolní vyšetření během lázeňského pobytu
  - **Trigger:** Pacient přichází na kontrolu, lékař potřebuje zaznamenat průběh léčby, reakci na terapii a případné úpravy procedur
  - **Path:** Lékař otevře existující záznam pacienta → klikne "Přidat kontrolní poznámku" → diktuje krátký záznam o průběhu → systém přepíše během 20–30 s → lékař zkontroluje a potvrdí → poznámka se připojí k historii pacienta
  - **Result:** Rychlý záznam kontroly bez nutnosti ručního psaní, historie průběhu pobytu je kompletní a strukturovaná

- **Example:** Konfigurace custom extrakce pro výstupní zprávy
  - **Trigger:** Lékař chce vytvořit vlastní šablonu pro výstupní zprávy, která extrahuje specifické informace o fyzioterapeutických procedurách a jejich toleranci
  - **Path:** Lékař otevře "Nastavení extrakce" → klikne "Nová konfigurace" → zadá popisem: "Chci extrahovat typy fyzioterapeutických procedur, frekvenci aplikace, subjektivní hodnocení pacienta a doporučení pro další péči" → systém vytvoří custom extraction schema → lékař ji pojmenuje "Výstupní zpráva - Fyzioterapie" → uloží → při dalším přepisu vybere tuto konfiguraci
  - **Result:** Lékař má personalizovanou šablonu extrakce, která přesně odpovídá struktuře výstupních zpráv v jeho zařízení

- **Example:** Diktování poznámek během obchůzky mimo ordinaci
  - **Trigger:** Lékař je na kontrole u fyzioterapeutických provozů, potřebuje zaznamenat doporučení pro úpravu procedur
  - **Path:** Lékař otevře MediAI na tabletu → klikne "Rychlý diktát" → nadiktuje poznámku během chůze → systém přepíše během 15–20 s → lékař zkontroluje na displeji → klikne "Uložit a sdílet" → text je dostupný pro fyzioterapeuty
  - **Result:** Rychlá komunikace s personálem, eliminace ústního předávání informací, které se mohou ztratit nebo nepřesně interpretovat

- **Example:** **[NOVÉ]** Vytvoření custom šablony pro specifický typ zprávy
  - **Trigger:** Lékař potřebuje vytvořit vlastní šablonu pro dekurs (denní lékařský záznam), která má specifickou strukturu požadovanou jeho zařízením
  - **Path:** Lékař otevře "Správa Šablon" → klikne "Vytvořit Novou Šablonu" → zadá název "Dekurs - Rehabilitační oddělení" → definuje strukturu sekcí: "Subjektivní stav pacienta", "Objektivní nález", "Aplikované procedury", "Reakce na léčbu", "Plán na další den" → pro každou sekci definuje klíčové informace, které má AI extrahovat → uloží šablonu → při příštím generování zprávy vybere tuto custom šablonu
  - **Result:** Lékař má personalizovanou šablonu, která přesně odpovídá workflow a požadavkům jeho oddělení, generované zprávy jsou okamžitě použitelné bez nutnosti úprav struktury

## 6) Competitive Analysis

- **Landscape (kdo tento problém řeší):**
  - Ruční psaní/diktování: Tradiční metoda, většina lékařů v ČR
  - Google Speech-to-Text / Amazon Transcribe: Generické STT API, využívají technicky zdatní lékaři
  - Specialized medical STT (Nuance Dragon Medical, 3M M*Modal): Globální hráči pro zdravotnictví, primárně US/EU trh
  - AI scribing startups (Suki.ai, Nabla Copilot): Moderní AI asistenti pro lékaře, focus na US trh
  - Manual transcription services: Externí služby s lidským přepisováním, velmi drahé

- **Value Thesis (value proposition každého hráče):**
  - Ruční psaní: 100% kontrola, žádná závislost na technologiích, ale extrémně časově náročné (trade-off: čas za autonomii)
  - Generické STT API: Nízké náklady, flexibilita, ale vyžaduje technické znalosti a nemá lékařský kontext (trade-off: cena za kvalitu)
  - Specialized medical STT: Vysoká přesnost lékařské terminologie, ale vysoké náklady, složitá implementace, primárně angličtina (trade-off: přesnost za dostupnost)
  - AI scribing startups: Moderní UX, ambient listening, ale drahé, zaměřené na US trh, anglický jazyk, complex workflows (trade-off: feature richness za jednoduchost)
  - Manual transcription: Vysoká přesnost, ale extrémně drahé, pomalé (24–48h turnaround), GDPR risk (trade-off: přesnost za rychlost/bezpečnost)

- **Strengths / Weaknesses (experience pros/cons):**
  - Generické STT: Rychlé onboardingu (+), ale nízká přesnost lékařské terminologie (-), chybí extrakce dat (-), pouze přepis bez strukturování (-)
  - Specialized medical STT: Vysoká přesnost (+), ale složité nastavení a integrace (-), vysoké náklady $500+/měsíc (-), primárně angličtina (-)
  - AI scribing startups: Ambient listening (+), pokročilá extrakce (+), ale extrémně složité UX (-), vyžaduje dlouhé školení (-), cena $200-400/měsíc (-), není česká lokalizace (-)

- **Our Differentiators (naše unikátní body):**
  - **Zaměření na český trh a lázeňské workflow:** Jediné řešení optimalizované pro českou lékařskou terminologii a specifické potřeby lázeňských lékařů (vstupní/kontrolní/výstupní zprávy), přímá integrace s lokálním kontextem
  - **Jednoduchost nad feature richness:** Zero learning curve — nahraji, zkontroluju, vygeneruji zprávu, exportuju — žádné složité ambient workflows nebo konfigurace, produktivita od první minuty (trade-off: obětujeme pokročilé funkce jako real-time přepis za extrémní jednoduchost)
  - **Kompletní workflow od audio po finální dokument:** Na rozdíl od konkurence, která poskytuje pouze přepis, MediAI generuje kompletní strukturované lékařské zprávy připravené k okamžitému použití — úspora času není 50%, ale 70%+ (trade-off: specifičtější use case než generické STT)
  - **Konfigurovatelná extrakce i šablony zpráv:** Flexibilní custom extraction schemas i report templates, které se přizpůsobí workflow konkrétního lékaře/zařízení, defaultní konfigurace "funguje out-of-the-box", ale lze přizpůsobit (trade-off: strukturovanost bez rigidity)
  - **Paralelní workflow s existujícími IS:** Funguje vedle SmartMEDIX, Medicus, CGM bez nutnosti integrace — copy-paste workflow znamená nulovou implementační složitost a okamžitý start (trade-off: manuální přenos místo přímé integrace v Phase 1)
  - **Transparentní bezpečnost a GDPR:** Viditelné security indikátory, jasná komunikace zpracování dat, data hostovaná v EU (Google Cloud), end-to-end šifrování jako standard (trust jako core value)

- **Switching Costs & Risks (migrační náklady a rizika):**
  - Z ručního psaní: Minimální resistance — lékaři už teď chtějí změnu, hlavní risk je nedůvěra v AI přesnost → adresujeme transparentním editorem s audio sync, kde má lékař plnou kontrolu
  - Z generických STT API: Střední resistance — tech-savvy uživatelé ztratí "full control", ale získají strukturovanou extrakci a lékařský kontext → value add musí být okamžitě viditelný
  - Risk z nesprávné extrakce: Pokud AI špatně identifikuje klinická data, může to vést k chybám v dokumentaci → mitigace: extrahované entity jsou vždy zvýrazněné a kontrolovatelné, lékař má final say
  - Change management v lázeňských zařízeních: Implementace nového nástroje vyžaduje buy-in od vedení → důraz na ROI (úspora času = úspora nákladů), pilot programy s 1–2 lékaři před rollout

- **Notes (reference odkazy):**
  - LangChain Extract dokumentace: https://github.com/langchain-ai/langchain-extract
  - Gemini 3 Pro capabilities: https://ai.google.dev/gemini-api/docs
  - Firebase Authentication: https://firebase.google.com/docs/auth
  - GDPR compliance checklist: https://gdpr.eu/checklist/
