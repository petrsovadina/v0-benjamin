# Product Charter — MediAI

## 1) Product Positioning

MediAI je modulární AI platforma, která funguje jako inteligentní dokumentační vrstva vedle existujících ambulantních systémů. Automaticky transformuje audio záznamy lékařských rozhovorů do kompletních strukturovaných lékařských zpráv — od přepisu přes extrakci klinických dat až po generování finálních dekursů, ambulantních zpráv a epikríz. Řešíme kritický problém českého zdravotnictví — administrativní přetížení lékařů, které zabírá 40–60% jejich pracovní doby a odvádí je od péče o pacienty.

V Phase 1 cílíme na lázeňská zařízení v České republice, kde vysoká frekvence rutinních vyšetření (vstupní, kontrolní, výstupní) vytváří enormní dokumentační zátěž. Naše řešení nabízí úsporu až 70% času stráveného dokumentací při zachování vysoké přesnosti, souladu s GDPR a kompatibility se stávajícími ambulantními systémy (SmartMEDIX, Medicus, CGM) prostřednictvím exportu a copy-paste workflow.

Dlouhodobá vize zahrnuje expanzi do ambulantní medicíny, fyzioterapie a nemocničního prostředí, s postupnou integrací do stávajících IS prostřednictvím API, lékařského mailu a dalších kanálů.

## 2) Brand Keywords

- **Důvěryhodnost** — Zpracováváme nejcitlivější zdravotní data s maximálním zabezpečením, šifrováním a plným soulasem s GDPR, viditelně komunikujeme bezpečnostní opatření
- **Efektivita** — Každý krok je optimalizován pro minimalizaci času — od nahrání audio po export finální zprávy zabere průměrně 2–3 minuty místo 10–15 minut ruční práce
- **Přesnost** — AI model je trénován na českou lékařskou terminologii a spolehlivě rozpoznává specifickou lázeňskou dokumentaci (vstupní zprávy, kontroly, výstupky)
- **Jednoduchost** — Intuitivní rozhraní navržené pro lékaře bez nutnosti technického školení — nahraji, zkontroluju, exportuju
- **Transparentnost** — Uživatel vždy vidí, co se děje s jeho daty, jak probíhá zpracování a může kdykoliv zasáhnout do extrakce informací

## 3) Core Problem / JTBD

Když lázeňský lékař přijme nového pacienta nebo provádí kontrolní vyšetření, potřebuje vytvořit strukturovanou lékařskou zprávu obsahující anamnézu, indikaci, kontraindikace, léčebný plán a doporučení. Při běžném provozu to znamená 15–20 vstupních vyšetření týdně, průběžné kontroly a výstupní zprávy pro každého pacienta. Ruční psaní nebo diktování do diktafonu s následným přepisováním zabírá 40–60% pracovní doby lékaře — čas, který by mohl věnovat péči o pacienty.

Bez automatizace čelí lékař chronickému časovému tlaku, chybám při přepisování, nekonzistentnímu formátování zpráv a frustraci z administrativní zátěže, která ho odvádí od skutečného poslání — léčit lidi. Navíc hrozí riziko nekompletní dokumentace, což může vést k problémům při kontrolách pojišťoven nebo revizních lékařů.

## 4) Goals & Mission

- **Mission:** Osvobodit lékaře od administrativní zátěže a vrátit jim čas na péči o pacienty pomocí AI technologií, které spolehlivě a bezpečně transformují mluvené slovo do strukturované lékařské dokumentace.

- **Desired Outcomes (descriptive):**
  - Lékaři tráví o 60–70% méně času administrativou a mají více prostoru pro kvalitní péči o pacienty
  - Lékařská dokumentace je konzistentní, kompletní, přesná a splňuje požadavky pojišťoven bez dodatečných úprav
  - Zdravotnická zařízení dosahují vyšší efektivity provozu a spokojenosti lékařů, což snižuje fluktuaci a vyhoření personálu
  - Bezpečnost a soukromí zdravotních dat je absolutní priorita — žádné kompromisy v oblasti GDPR a šifrování
  - Systém je tak jednoduchý, že lékař nepotřebuje žádné školení a může začít používat okamžitě
  - Extrakce klinických dat je přizpůsobitelná potřebám konkrétního lékaře nebo zařízení (custom entity schema)

## 5) Solutions We Own

### Rychlé nahrání a přepis audio
- **What it solves:** Eliminace ručního psaní nebo diktování s následným přepisováním při každém pacientovi
- **Typical path:** Lékař během rozhovoru s pacientem zapne nahrávání (mikrofon nebo upload souboru), po dokončení systém automaticky spustí AI přepis pomocí Gemini 3 Pro, během 30–90 sekund je dostupný textový přepis
- **Outcome for the user:** Lékař má k dispozici přesný textový záznam rozhovoru bez jakékoliv manuální práce, může okamžitě pokračovat dalším pacientem
- **Boundaries:** Nepodporujeme real-time přepis během hovoru (zatím), fokus je na post-procesing kvalitu
- **Guiding principles:** Rychlost / Přesnost terminologie / Zero friction

### Automatická extrakce a strukturování klinických dat
- **What it solves:** Transformace nestrukturovaného přepisu rozhovoru do strukturované lékařské zprávy s automatickou identifikací klíčových entit (PII, diagnózy, medikace, symptomy, alergies)
- **Typical path:** Po dokončení přepisu systém automaticky spustí LangChain Extract pro identifikaci entit dle konfigurace (default: PII + základní klinická data), uživatel vidí zvýrazněné entity v textu a strukturovaný přehled, může upravit extrakční parametry a znovu spustit proces
- **Outcome for the user:** Strukturovaná data připravená k exportu nebo vložení do nemocničního IS, minimální manuální úpravy potřeba
- **Boundaries:** Komplexní klinické reasoning (např. diferenciální diagnostika) není v MVP scope
- **Guiding principles:** Konfigurovatelnost / Transparentnost / Bezpečnost dat

### Editace a synchronizovaná kontrola přepisu
- **What it solves:** Potřeba ověřit přesnost přepisu a opravit případné chyby před finalizací zprávy
- **Typical path:** Lékař otevře detail přepisu, vidí WYSIWYG textový editor vedle audio přehrávače, může přehrát audio a současně číst text, provádět úpravy v reálném čase
- **Outcome for the user:** 100% kontrola nad finální podobou zprávy, rychlá identifikace a korekce chyb, jistota správnosti dokumentace
- **Boundaries:** Neposkytujeme pokročilé formátování (tabulky, grafy) v MVP
- **Guiding principles:** Snadná kontrola / Rychlé úpravy / Audio-text sync

### Konfigurace extrakce pro různé typy vyšetření
- **What it solves:** Různé typy lékařských rozhovorů vyžadují extrakci různých dat (vstupní vyšetření vs. kontrola vs. výstupní zpráva)
- **Typical path:** Uživatel si vytvoří custom konfiguraci extrakce buď pomocí přirozeného jazyka ("chci extrahovat fyzioterapeutické procedury a jejich toleranci") nebo definováním konkrétních entit, konfigurace se uloží a lze ji použít opakovaně
- **Outcome for the user:** Přizpůsobený systém extrakce pro konkrétní workflow lázeňského lékaře, konzistentní strukturování různých typů zpráv
- **Boundaries:** Pokročilé AI reasoning pro komplexní medicínské inferencing není v MVP
- **Guiding principles:** Flexibilita / Opakovatelnost / User control

### AI generování kompletních lékařských zpráv
- **What it solves:** Automatická transformace přepisu a extrahovaných entit do finální lékařské zprávy (vstupní vyšetření, kontrolní zpráva, výstupní zpráva, dekurs, epikríza) s profesionální strukturou a formulacemi
- **Typical path:** Po dokončení přepisu a extrakce lékař vybere typ zprávy a šablonu, systém pomocí AI vygeneruje kompletní strukturovanou zprávu rozdělěnou do sekcí (anamnéza, nynější onemocnění, objektivní nález, závěr, doporučení), lékař může zprávu zkontrolovat a upravit v editoru
- **Outcome for the user:** Kompletní lékařská zpráva připravená k použití během 2–3 minut místo 15–20 minut ručního psaní, konzistentní struktura a profesionální formulace, splňuje požadavky pojišťoven
- **Boundaries:** Neprovádíme klinické reasoning nebo diagnostické závěry — pouze strukturujeme a formulujeme informace z rozhovoru a extrahovaných dat
- **Guiding principles:** Automatizace / Kvalita / User control / Template flexibility

### Správa šablon pro různé typy zpráv
- **What it solves:** Různé typy lékařských zpráv vyžadují různou strukturu sekcí, formulace a povinné údaje (vstupní vyšetření má jinou strukturu než dekurs nebo výstupní zpráva)
- **Typical path:** Lékař může použít defaultní šablony (vstupní vyšetření - lázně, kontrolní vyšetření, výstupní zpráva, dekurs) nebo vytvořit vlastní custom šablony definováním sekcí, pořadí, povinných polí a preferovaných formulací pro AI generování
- **Outcome for the user:** Personalizované šablony odpovídající workflow konkrétního lékaře nebo zařízení, konzistentní výstupy napříč všemi zprávami, jednoduchá správa a opakované použití šablon
- **Boundaries:** Template engine je zaměřený na strukturu dokumentu, ne na klinické guidelines nebo protokoly léčby
- **Guiding principles:** Standardizace / Flexibilita / Reusability

### Export a integrace do zdravotnických systémů
- **What it solves:** Přenos hotové zprávy do ambulantního IS nebo předání pacientovi/pojišťovně/praktickému lékaři
- **Typical path:** Po finalizaci úprav lékař klikne na Export, vybere formát (.txt, .docx) nebo použije one-click copy formátovaného textu pro vložení do svého ambulantního systému (SmartMEDIX, Medicus, CGM, PC Doktor)
- **Outcome for the user:** Hotová lékařská zpráva ve standardním formátu připravená k okamžitému použití, copy-paste workflow funguje paralelně vedle existujícího IS bez nutnosti integrace
- **Boundaries:** Přímá API integrace do konkrétních IS je Phase 2 feature (SmartMEDIX API priorita), v Phase 1 focus na export souborů a copy-paste
- **Guiding principles:** Standardizace / Kompatibilita / Zero friction / Paralelní workflow
