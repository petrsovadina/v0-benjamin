Níže máš **kompletní, detailní a profesionální popis klinického AI asistenta**, tak jak by vypadal v návrhu produktu, dokumentaci pro vedení, odborné společnosti nebo investiční pitch.
Je to **maximálně konkrétní**, **technicky přesné**, **strategické** a **plně reflektuje české zdravotnictví**.

---

# 🧠 **Czech MedAI – Klinický AI Asistent**

### *Komplexní, bezpečný a auditovatelný systém pro podporu klinického rozhodování v ČR*

---

# 1) 🔭 **Hlavní mise asistenta**

Vytvořit **důvěryhodného digitálního kolegu** pro české lékaře, který:

* poskytuje rychlé, přesné a ověřené odpovědi na klinické dotazy,
* funguje v češtině a rozumí českému zdravotnickému prostředí,
* čerpá z lokálních, regulovaných zdrojů (SÚKL, guidelines, registrů),
* je transparentní a každou odpověď umí citovat,
* snižuje administrativu, urychluje rozhodování a zvyšuje bezpečnost péče.

Asistent není chatbot.
Je to **klinický nástroj**, srovnatelný s UpToDate, Micromedex, Lexicomp – ale lokalizovaný pro ČR a inteligentnější díky AI.

---

# 2) 🩺 **Co klinický AI asistent umí**

## **A) Odpovídat na klinické dotazy v češtině**

Příklady dotazů, které lékaři běžně potřebují:

* *„Jaké je doporučené dávkování Eliquisu u fibrilace síní u pacienta s GFR 28?“*
* *„Jaké jsou kontraindikace u Jardiance u diabetu 2. typu?“*
* *„Jaký antibiotický režim doporučuje ESC u komunitní pneumonie?“*
* *„Můžu podat ibuprofen pacientce ve 3. trimestru?“*

Asistent odpovídá **stručně, přesně, strukturovaně a s citacemi**.

---

## **B) Detailní léková podpora**

Postavená na databázi léčiv, kterou právě připravujeme.

Asistent umí:

* vyhledat léčivo podle názvu, ATC, účinné látky
* zobrazit stručné indikace
* dávkovací režimy
* interakce
* úhrady, doplatky
* registrační status
* alternativy (generika, podobné ATC skupiny)
* porovnání dvou léků

A hlavně: **vše zdrojuje z SPC / SÚKL.**

---

## **C) Práce s klinickými guidelines**

Asistent má přístup k:

* ESC (kardiologie)
* EASD (diabetes)
* ERS (respirace)
* EULAR (revmatologie)
* NICE (UK evidence-based)
* WHO
* české odborné společnosti, pokud mají veřejné materiály

Umí shrnout doporučené postupy a propojit je s lékovými daty.

---

## **D) Analýza lékařských dokumentů**

Asistent umí:

* shrnout klinický nález
* extrahovat klíčové informace (diagnóza, léčba, rizika)
* detekovat nejasnosti v dokumentaci
* doporučit doplnění
* klasifikovat dokumenty (propouštěcí zpráva, nález, zpráva pro praktika…)

To podporuje jak nemocnice, tak ambulantní praxi.

---

## **E) Práce s multimodálními vstupy**

Nativně:

* text
* audio (přepis konzultací)
* dokumenty PDF
* obrázky (rentgeny, grafy, laboratorní výsledky)

Asistent je „vstřebá“, extrahuje informace a navrhne závěry.

---

## **F) Tvorba textů pro klinickou praxi**

Např.:

* lékařské zprávy
* propouštěcí zprávy
* doporučení pro pacienta
* zprávy pro praktického lékaře
* žádanky
* krátké shrnutí pro sestru

Se zachováním struktury, terminologie a compliance.

---

## **G) Propojení s EHR systémy**

Asistent je navržen tak, aby šel integrovat do:

* nemocničních IS (IKIS, Medea, NIS FONS…)
* ambulantních systémů (CGM, Medicus, SmartMEDIX…)
* LIS systémy
* PACS/RIS

Tj. lékař nemusí nikam jinam chodit – AI pracuje tam, kde pracuje on.

---

# 3) ⚙️ **Technická architektura asistenta**

## **A) Knowledge Base (Klinická datová vrstva)**

Skládá se z:

* lékové databáze (SÚKL – SPC, PIL, úhrady, obaly)
* guidelines
* PubMed / PMC open access
* odborných článků
* klasifikací (ATC, INN, SNOMED, LOINC…)
* lokálních číselníků

Tato vrstva je **strukturovaná, verzovaná, auditovatelná**.

---

## **B) RAG (Retrieval-Augmented Generation)**

Každá odpověď AI se generuje takto:

1. dotaz → vektorová mapa
2. retriever hledá v klinických zdrojích
3. RAG sestaví přesné citace
4. LLM vytvoří odpověď *pouze* z toho, co našlo
5. generuje se citace, zdroj, odkaz, verze SPC

Tím eliminujeme halucinace a získáme **důvěryhodnost**.

---

## **C) LLM (jazykový model)**

Model (např. Gemini 3 Pro, GPT-5, Llama 3) je řízen:

* řízenými prompt-režimy
* bezpečnostními pravidly
* specializovanými klinickými agenty
* strukturálními odpověďmi (obsahové šablony)

LLM není zdroj pravdy — jen generátor nad ověřenými daty.

---

## **D) Orchestrace a aktualizace**

Systém běží na:

* denních aktualizacích léčiv
* pravidelných synchronizacích guidelines
* verzování každého datasetu
* auditu (kdo/čím/odkud je informace)
* monitoringu kvality dat

---

# 4) 🔐 **Bezpečnost, regulace a compliance**

Asistent respektuje:

* **GDPR** (pracuje lokálně, žádná data pacientů se neukládají)
* **MDR** (systém je připraven na certifikaci jako Medical Device Class IIa)
* **NIS2** (infrastruktura, logování, bezpečnost)
* **auditovatelnost** (každá odpověď má svůj zdroj)

Bezpečnostní filozofie:
**AI nesmí nikdy odpovědět něco, co nemá podloženo v datech.**

---

# 5) 🤝 **Pro koho je asistent určen**

### Primárně pro:

* lékaře (nemocniční i ambulantní)
* sestry
* farmaceuty
* klinické výzkumníky
* fyzioterapeuty
* pracovníky LSPP / urgentu

### Sekundárně:

* zdravotnická zařízení
* pojišťovny (pro kontrolu úhrad)
* dodavatele EHR systémů
* legislativní orgány (komentace návrhů)

---

# 6) 💡 **Jaký problém řeší**

Klinická praxe je zahlcená:

* množstvím informací
* chaotickými zdroji
* zastaralými databázemi
* enormní administrativou
* chybovostí
* přetížením zdravotníků

Asistent:

* šetří čas
* zvyšuje kvalitu rozhodování
* sjednocuje informace
* snižuje rizika
* odstraňuje zbytečnou administrativu
* modernizuje praxi

---

# 7) 🧩 **Shrnutí v jedné větě**

**Klinický AI asistent je inteligentní, bezpečný a plně auditovatelný digitální partner lékaře, který propojuje česká léková data, klinické guidelines a vědeckou literaturu do okamžitých, přesných a citovaných odpovědí.**

---
Tady máš **hotový, přehledný a přímo použitelný výstup** se *všemi relevantními zdroji*, rozdělený podle kategorií (ČR + mezinárodní), včetně **konkrétních URL**, **účelu**, a **doporučení pro použití v klinickém AI asistentovi**.

Je to připravené tak, aby se to dalo vložit do dokumentace, do RAG pipeline, nebo do architektury knowledge layer.

---

# 📚 **RELEVANTNÍ ZDROJE PRO KLINICKÉHO AI ASISTENTA (CZ + EU + GLOBAL)**

*(kompletní kurátorovaný seznam)*

---

# 🇨🇿 **1) Česká oficiální data – léčiva, úhrady, regulace**

## **SÚKL — Otevřená data a registry**

**Primární zdroj pro léčiva v ČR**

* Databáze léčivých přípravků (DLP)
  [https://opendata.sukl.cz/?q=databaze-lecivych-pripravku](https://opendata.sukl.cz/?q=databaze-lecivych-pripravku)

* SPC – Souhrny údajů o léčivém přípravku
  [https://opendata.sukl.cz/?q=spc](https://opendata.sukl.cz/?q=spc)

* PIL – příbalové letáky
  [https://opendata.sukl.cz/?q=pil](https://opendata.sukl.cz/?q=pil)

* Obaly
  [https://opendata.sukl.cz/?q=obaly](https://opendata.sukl.cz/?q=obaly)

* Ceny a úhrady
  [https://prehledy.sukl.cz/prs/](https://prehledy.sukl.cz/prs/)

* Přehledová databáze RLP
  [https://www.sukl.cz/leciva/prehledova-databaze-rlp](https://www.sukl.cz/leciva/prehledova-databaze-rlp)

* eRecept (informace + API)
  [https://www.epreskripce.cz](https://www.epreskripce.cz)

**Použití:**
→ léčiva, složení, indikace, kontraindikace, interakce, úhrady, preskripční omezení
→ core dataset pro klinické odpovědi v ČR

---

# 📊 **2) ÚZIS ČR – národní zdravotnické registry**

* ÚZIS – hlavní portál
  [https://www.uzis.cz](https://www.uzis.cz)

* Národní zdravotní registry (kompletní seznam)
  [https://www.uzis.cz/resortni-registr](https://www.uzis.cz/resortni-registr)

* Registr hospitalizací (NRHOSP)
  [https://www.uzis.cz/resortni-registr/nrhosp/](https://www.uzis.cz/resortni-registr/nrhosp/)

* Národní onkologický registr (NOR)
  [https://www.uzis.cz/resortni-registr/nor/](https://www.uzis.cz/resortni-registr/nor/)

* Registr reprodukčního zdraví
  [https://www.uzis.cz/resortni-registr/nrrz/](https://www.uzis.cz/resortni-registr/nrrz/)

* Zdravotnické ročenky a statistiky
  [https://www.uzis.cz/category/publikace/zdravotnicka-rocenka/](https://www.uzis.cz/category/publikace/zdravotnicka-rocenka/)

**Použití:**
→ incidence, prevalence, epidemiologie, demografie, hospitalizace
→ evidence pro kontextové odpovědi pro české lékaře

---

# 🏛 **3) Ministerstvo zdravotnictví – standardy, doporučení, legislativa**

* Klinické doporučené postupy MZ
  [https://www.mzcr.cz/odbor-koncepci-a-legislativy/doporucene-postupy/](https://www.mzcr.cz/odbor-koncepci-a-legislativy/doporucene-postupy/)

* Metodiky, standardy péče
  [https://www.mzcr.cz/category/odbor-koncepci-a-legislativy/](https://www.mzcr.cz/category/odbor-koncepci-a-legislativy/)

* Zdravotnická legislativa
  [https://www.mzcr.cz/dokumenty/legislativa_1757_1.html](https://www.mzcr.cz/dokumenty/legislativa_1757_1.html)

**Použití:**
→ závazné předpisy, doporučené postupy, právní rámec, lokální specifika

---

# 🩺 **4) České odborné společnosti – lokální guidelines**

**ČLS JEP (umbrella)**
[https://www.cls.cz](https://www.cls.cz)

## Nejvýznamnější obory:

* Česká kardiologická společnost
  [https://www.kardio-cz.cz/doporucene-postupy-1](https://www.kardio-cz.cz/doporucene-postupy-1)

* Česká diabetologická společnost
  [https://www.diab.cz/doporucene-postupy](https://www.diab.cz/doporucene-postupy)

* Česká neurologická společnost
  [https://www.czech-neuro.cz/doporucene-postupy/](https://www.czech-neuro.cz/doporucene-postupy/)

* Česká pneumologická a ftizeologická společnost
  [https://www.pneumologie.cz/doporucene-postupy/](https://www.pneumologie.cz/doporucene-postupy/)

* Česká onkologická společnost (Linkos)
  [https://www.linkos.cz/odborne-informace/doporucene-postupy/](https://www.linkos.cz/odborne-informace/doporucene-postupy/)

**Použití:**
→ klinické doporučené postupy **specifické pro ČR** (klíčová vrstva RAG)

---

# 🌍 **5) Mezinárodní klinické guidelines**

* ESC – European Society of Cardiology
  [https://www.escardio.org/Guidelines](https://www.escardio.org/Guidelines)

* ADA – American Diabetes Association
  [https://diabetes.org/diabetes/ada-standards-care](https://diabetes.org/diabetes/ada-standards-care)

* EASD – European Association for the Study of Diabetes
  [https://easd.org/guidelines/](https://easd.org/guidelines/)

* AHA – American Heart Association
  [https://professional.heart.org/en/guidelines-and-statements](https://professional.heart.org/en/guidelines-and-statements)

* ERS – European Respiratory Society
  [https://www.ersnet.org/guidelines/top-issues/](https://www.ersnet.org/guidelines/top-issues/)

* IDSA – Infectious Diseases Society of America
  [https://www.idsociety.org/practice-guideline/](https://www.idsociety.org/practice-guideline/)

* WHO – zdravotnické guidelines
  [https://www.who.int/publications/guidelines](https://www.who.int/publications/guidelines)

**Použití:**
→ komparace českých vs. mezinárodních postupů
→ klinická rozhodovací podpora při absenci lokálních doporučení

---

# 📚 **6) Evidence-based literatura – studie, meta-analýzy**

* PubMed
  [https://pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov)

* Europe PMC (open-access plné texty)
  [https://europepmc.org](https://europepmc.org)

* Cochrane Library
  [https://www.cochranelibrary.com](https://www.cochranelibrary.com)

* ClinicalTrials.gov
  [https://clinicaltrials.gov](https://clinicaltrials.gov)

* NIH / NCBI
  [https://www.ncbi.nlm.nih.gov](https://www.ncbi.nlm.nih.gov)

**Použití:**
→ citace, studie, důkazy, plné texty, meta-analýzy
→ nejdůležitější vrstva pro evidence-based AI

---

# 💊 **7) Farmakologie, interakce, dávkování, klasifikace**

* WHO ATC/DDD toolkit
  [https://www.who.int/tools/atc-ddd-toolkit](https://www.who.int/tools/atc-ddd-toolkit)

* RxNorm
  [https://www.nlm.nih.gov/research/umls/rxnorm/index.html](https://www.nlm.nih.gov/research/umls/rxnorm/index.html)

* DrugBank
  [https://go.drugbank.com](https://go.drugbank.com)

* WHO Drug Dictionary
  [https://www.who-umc.org/whodrug/](https://www.who-umc.org/whodrug/)

**Použití:**
→ klasifikace léčiv, dávky, interakce
→ cross-walk mezi mezinárodními a českými názvy

---

# 🏥 **8) České EHR systémy – integrace**

* ICZ IKIS
  [https://www.iczgroup.com/produkty/ikis/](https://www.iczgroup.com/produkty/ikis/)

* CGM / Medicus
  [https://www.cgm.com/cz](https://www.cgm.com/cz)

* Medisoft
  [https://www.medisoft.cz](https://www.medisoft.cz)

* ISIN – infekční nemoci
  [https://www.uzis.cz/isin](https://www.uzis.cz/isin)

**Použití:**
→ EHR kontext, audit, integrace API

---

# 📘 **9) Vzdělávací / výukové / alternativní zdroje (doplňkové)**

* WikiSkripta (doplňkově)
  [https://www.wikiskripta.eu](https://www.wikiskripta.eu)

* LibreTexts – biologie / medicína
  [https://med.libretexts.org](https://med.libretexts.org)

* OpenStax – biologie, anatomie
  [https://openstax.org/subjects/science](https://openstax.org/subjects/science)

* GPnotebook
  [https://gpnotebook.com](https://gpnotebook.com)