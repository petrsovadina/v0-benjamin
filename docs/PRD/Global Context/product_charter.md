# Product Charter — Benjamin (AI Klinický Asistent)

## 1) Product Positioning

Benjamin je AI asistent pro české lékaře, který poskytuje inteligentní podporu při klinickém rozhodování a zdravotnické dokumentaci prostřednictvím conversational interface s přímým přístupem k medicínským zdrojům (MCP tools). Je dostupný jako modální okno integrované do systému FONS Enterprise a jako Chrome Extension, čímž lékaře osvobozuje od rutinní administrativy a poskytuje rychlý přístup k ověřeným medicínským poznatkům v jejich rodném jazyce.

Na rozdíl od zahraničních AI nástrojů, které nejsou přizpůsobeny českému zdravotnictví, Benjamin kombinuje mezinárodní vědecké poznatky (PubMed, Semantic Scholar) s českými legislativními požadavky, národními guidelines a databázemi (SÚKL, ÚZIS, ČLS JEP). Jsme první AI asistent, který rozumí specifickým potřebám českých lékařů a mluví jejich jazykem — jak doslova, tak přeneseně.

## 2) Brand Keywords

- **Důvěryhodný** — Vždy uvádíme přesné zdroje s citacemi (PMID/DOI), transparentnost je základem každé naší odpovědi
- **Rychlý** — Odpovídáme do 5 sekund, protože čas lékaře je drahocenný a pacienti čekají
- **Lokalizovaný** — Plná podpora češtiny včetně lékařské terminologie, české legislativy a národních guidelines
- **Bezpečný** — GDPR by design, hosting v EU, audit trail každé interakce pro právní ochranu lékaře
- **Spolehlivý** — Evidence-based přístup, RAG architektura eliminující halucinace, pouze recenzované zdroje

## 3) Core Problem / JTBD

Když lékař potřebuje během vyšetření rychle ověřit správný postup, zkontrolovat interakce léků nebo vytvořit epikrízu po hospitalizaci, čelí fragmentaci informací roztříštěných po různých systémech, jazykové bariéře (většina zdrojů pouze v angličtině) a nedostatku času. Bez našeho řešení musí otevřít 3-4 různé weby (PubMed, SÚKL, doporučené postupy ČLS JEP), strávit 10+ minut hledáním, přeložit anglické zdroje a syntézovat informace — mezitím čekají další pacienti. Výsledkem je frustrace, potenciální chyby v rozhodování a 30% pracovní doby věnované administrativě místo péče o pacienty.

## 4) Goals & Mission

- **Mission:** Demokratizovat přístup českých lékařů k aktuálním medicínským poznatkům a osvobodit je od časově náročné administrativy, aby mohli věnovat více času péči o pacienty, přičemž zajistíme nejvyšší standardy bezpečnosti a důvěryhodnosti informací.

- **Desired Outcomes (descriptive):**
  - Lékaři ušetří minimálně 80% času věnovaného hledání informací a manuálnímu vyplňování dokumentace
  - Každé klinické rozhodnutí je podloženo aktuálními guidelines s přesnými citacemi zdrojů
  - Zdravotnická dokumentace splňuje legislativní požadavky (vyhláška č. 98/2012 Sb.) při minimálním úsilí lékaře
  - Pacienti dostávají kvalitnější péči díky tomu, že lékaři mají více času a lepší přístup k poznatkům
  - Ochrana práv lékaře prostřednictvím auditovatelnosti všech AI asistovaných rozhodnutí
  - Snížení administrativní zátěže lékařů z 30% na méně než 10% jejich pracovní doby

## 5) Solutions We Own

### Klinická Podpora (Conversational AI Asistent)
- **What it solves:** Lékaři potřebují rychlé, spolehlivé odpovědi na klinické otázky během vyšetření nebo urgentních situací, ale nemají čas procházet desítky studií nebo hledat v různých databázích.
- **Typical path:** Lékař otevře Benjamin modální okno nebo Chrome Extension a komunikuje s AI asistentem v přirozeném českém jazyce (např. "Jaké jsou guidelines pro léčbu diabetu 2. typu u pacienta s kardiovaskulárním rizikem?"). Systém prostřednictvím MCP (Model Context Protocol) nástrojů získává data z připojených medicínských zdrojů (PubMed, SÚKL, Semantic Scholar, MEDLINE, ČLS JEP), Claude AI syntetizuje odpověď a vrátí ji do 5 sekund s inline citacemi [1], [2], [3] a rozbalovacím panelem zdrojů.
- **Outcome for the user:** Lékař obdrží stručnou, evidence-based odpověď přímo v chat rozhraní s přesnými citacemi na ověřené zdroje, včetně možnosti zobrazit detail každého zdroje (název, autor, rok, link). Může pokračovat v konverzaci s follow-up otázkami. Celá interakce je automaticky zalogována do audit_logs tabulky s RLS ochranou. Chat interface je dostupný jak v modálním okně (1200×800px) integrovaném do FONS Enterprise, tak jako Chrome Extension (popup 400×600px nebo side panel 400×full height).
- **Boundaries:** Neposkytujeme autonomní diagnostiku ani terapeutická doporučení — jsme asistent, ne náhrada lékaře. Neodpovídáme na dotazy pacientů, pouze healthcare professionals. MVP využívá MCP připojení k základním datovým zdrojům (PubMed, SÚKL, Semantic Scholar, ČLS JEP).
- **Guiding principles:** Conversational UX / Evidence-based / Transparentnost zdrojů / MCP tools integration / Rychlost
- **References:** MCP (Model Context Protocol), Supabase Edge Functions, Claude Sonnet 4.5, PubMed, SÚKL, Semantic Scholar, MEDLINE, ČLS JEP guidelines

### Dokumentační Asistence (Epikríza Tab)
- **What it solves:** Vytváření epikríz je časově náročný proces vyžadující procházení všech relevantních záznamů o pacientovi, jejich syntézu a strukturování podle legislativních požadavků — lékař tím často stráví 15-30 minut na hospitalizaci.
- **Typical path:** Lékař v Benjamin modálním okně přepne na záložku "Epikríza", systém automaticky načte kontext aktuálního pacienta z FONS Enterprise (jméno, datum narození, oddělení, hospitalizace). Lékař zkontroluje automaticky zaškrtnuté datové zdroje (☑️ Dekurzy, ☑️ Laboratorní výsledky, ☑️ Medikace, ☑️ Vyšetření) a klikne na "🤖 Generovat Epikrízu". Během 15-30 sekund systém vygeneruje strukturovanou epikrízu podle vyhlášky č. 98/2012 Sb. §21 s možností "Generovat jinak" pro alternativní formulaci.
- **Outcome for the user:** Lékař obdrží předvyplněnou epikrízu v rich text editoru obsahující všechny povinné náležitosti (identifikace, diagnózy, průběh hospitalizace, vyšetření, léčba, doporučení), kterou pouze zkontroluje, případně upraví a exportuje do FONS Enterprise — proces se zkrátí z 20 minut na 2 minuty.
- **Boundaries:** MVP (Epikríza 0.1) pracuje s dekurzy, laboratorními výsledky, medikací a základními diagnózami. Plná verze (Epikríza 1.0) zahrnuje všech 11 sekcí požadovaných legislativou včetně konzilií, zákroků a ošetřovatelského plánu. Lékař musí vždy finální text zkontrolovat a schválit. Epikríza je dostupná jako záložka v modálním okně, ne jako samostatná stránka.
- **Guiding principles:** Legislativní compliance / Úspora času / Kontrola lékaře / Tab-based UX
- **References:** Vyhláška č. 98/2012 Sb. §21, FONS Enterprise data model, Supabase Edge Functions

### Komunikační Nástroje (Translator Tab)
- **What it solves:** Lékaři potřebují překládat mezi odbornou terminologií a pacientsky srozumitelným jazykem, překonávat jazykové bariéry u cizinců a standardizovat používanou terminologii v dokumentaci.
- **Typical path:** Lékař v Benjamin modálním okně přepne na záložku "Translator", vloží nebo vepíše text do levého panelu (Input Panel), vybere jazykový směr (🇨🇿 ⇄ 🇬🇧) a režim překladu (Odborný / Zjednodušený), poté klikne na "🌍 Přeložit". Během 2-5 sekund se v pravém panelu (Output Panel) zobrazí přeložený text s respektováním medicínského kontextu.
- **Outcome for the user:** Lékař obdrží přeložený text v požadované formě — pacientsky srozumitelné vysvětlení pro informovaný souhlas, překlad do angličtiny pro mezinárodní komunikaci, nebo zjednodušenou verzi odborného textu. Má možnost prohodit jazyky tlačítkem ⇄, zobrazit terminologický slovník s definicemi klíčových pojmů nebo uložit překlad do historie. Dvousloupcový layout (vstup | výstup) umožňuje rychlé srovnání originálního a přeloženého textu.
- **Boundaries:** MVP zahrnuje základní režimy překladu (Odborný / Zjednodušený) pro jazykový pár 🇨🇿 ⇄ 🇬🇧. Plná verze (Fáze 3) obsahuje všechny 4 režimy, více jazyků (slovenština, polština, němčina) a terminologickou databázi (SNOMED CT, MeSH, MKN-10). Translator je dostupný jako záložka v modálním okně.
- **Guiding principles:** Medicínská přesnost / Kontextové porozumění / Rychlost / Tab-based UX
- **References:** Claude Sonnet 4.5, SNOMED CT, MeSH, MKN-10, SÚKL databáze léků, Supabase Edge Functions

### Integrace s FONS Enterprise a Chrome Extension
- **What it solves:** AI nástroje jsou často izolované od zdravotnických systémů, což vytváří friction v workflow lékaře — musí přepínat mezi aplikacemi, kopírovat data a narušovat svou koncentraci.
- **Typical path:** Benjamin je dostupný dvojím způsobem: (1) Jako **modální okno** (1200×800px overlay) integrované do FONS Enterprise — lékař klikne na plovoucí widget (FAB 56×56px) v pravém dolním rohu stránky a Benjamin se otevře přes aktuální obsah. (2) Jako **Chrome Extension** — lékař klikne na ikonu rozšíření v Chrome toolbar a otevře se popup (400×600px) nebo side panel (400×full height). V obou případech má okamžitý přístup ke všem funkcím (Chat, Epikríza, Translator, Settings) prostřednictvím záložkové navigace. Autentizace probíhá přes Supabase Auth s Azure AD SSO, kontext aktuálního pacienta je automaticky načten z FONS Enterprise (pokud je dostupný).
- **Outcome for the user:** Bezešvá AI asistence bez nutnosti opouštět známé prostředí FONS Enterprise nebo aktuální browser tab, automatické načítání kontextu pacienta prostřednictvím Supabase Row Level Security, single sign-on autentizace s session managementem. Modální okno lze přetahovat, minimalizovat nebo zavřít — nepřerušuje práci v FONS Enterprise. Chrome Extension funguje na libovolné stránce, nejen v FONS systému.
- **Boundaries:** MVP zahrnuje modální okno pro FONS Enterprise (content script injected) a Chrome Extension (popup + side panel). Fáze 2 přidává real-time notifications (Supabase Realtime) a offline režim pro Extension. Fáze 3 zahrnuje public REST API pro externí EHR systémy (ICZ IKIS, CGM) a standalone web aplikaci s PWA podporou.
- **Guiding principles:** Seamless integration / Modal overlay UX / Chrome Extension accessibility / Context-aware / Single workspace / Serverless scalability
- **References:** FONS Enterprise UIX design system, Chrome Extension API (Manifest V3), Supabase Auth (Azure AD), Supabase Edge Functions, Content Scripts

### Auditovatelnost a Bezpečnost
- **What it solves:** Lékaři potřebují právní ochranu svých rozhodnutí a systémy musí splňovat přísné požadavky GDPR a zdravotnických regulací, přičemž AI systémy často působí jako "černá skříňka" bez možnosti ověření.
- **Typical path:** Každá interakce s Benjaminem (chat dotaz, generování epikrízy, překlad) je automaticky zaznamenávána do Supabase PostgreSQL databáze s Row Level Security včetně času, typu interakce, vstupu, výstupu, použitých MCP zdrojů a identifikace uživatele. Lékař má možnost kdykoli zobrazit historii svých dotazů a citované zdroje prostřednictvím záložky "Settings" → "Historie konverzací". Všechna data jsou šifrována (TLS 1.3 in transit, AES-256 at rest) a uložena v EU datacentrech Supabase (Frankfurt). RLS policies zajišťují, že každý lékař vidí pouze své vlastní interakce a data svých pacientů podle oprávnění v FONS Enterprise.
- **Outcome for the user:** Lékař má kompletní audit trail všech AI asistovaných rozhodnutí pro případné právní spory nebo revize, s garantovanou ochranou dat prostřednictvím Supabase Row Level Security. Splnění GDPR, ISO 27001 a MDR požadavků zajišťuje legislativní compliance nemocnice. V případě pochybností může kdykoli ověřit, jaké zdroje byly použity pro konkrétní odpověď (včetně PMID/DOI odkazů).
- **Boundaries:** MVP zahrnuje základní audit logging v PostgreSQL s RLS policies pro chat, epikrízu a translator funkce. Fáze 2 přidává Supabase Dashboard + Langfuse observability pro analýzu používání a detekci anomálií. Fáze 3 zahrnuje full MDR Class IIa certifikaci a compliance reporting pro zdravotní pojišťovny.
- **Guiding principles:** Transparence / GDPR by design / Legal protection / Row Level Security / Audit trail
- **References:** GDPR, vyhláška č. 98/2012 Sb., MDR Class IIa, ISO 27001, Supabase Security, Supabase Row Level Security Policies
