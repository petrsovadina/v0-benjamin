# Benjamin - Návrh Dalších Features (Post-MVP)

**Kontext:** Benjamin MVP (Fáze 1) poskytuje conversational AI asistent, automatické generování epikríz a medicínský překladač. Tento dokument navrhuje další relevantní features pro Fázi 2-3, které adresují pokročilé potřeby lékařů a rozšiřují competitive advantage.

**Metodologie:** Features navrženy na základě:
- Analýzy 3 person (Dr. Nováková, Dr. Svoboda, Dr. Kučera)
- Competitive analysis (gaps vs OpenEvidence, UpToDate, ChatGPT)
- User research pain points (Čas 80%, Fragmentace 65%, Jazyková bariéra 45%)
- PRD MVP non-goals (DeepConsult, VZP Navigator, "Generovat jinak", MDR certifikace)

---

## Prioritizační Framework

### MoSCoW Prioritizace

**Must Have (Fáze 2)** - Kritické pro škálování na 500+ lékařů
- Features, které adresují top 3 pain pointy z user research
- Competitive parity s OpenEvidence/UpToDate
- GDPR/MDR compliance requirements

**Should Have (Fáze 2-3)** - Vysoká hodnota, ale ne blokery
- Features, které vytvářejí differentiation vs konkurence
- Pokročilé use cases pro power users (Dr. Svoboda - kardiolog)
- Monetization enablers

**Could Have (Fáze 3+)** - Nice-to-have, lower ROI
- Experimentální features (voice, multimodal)
- Niche use cases (<20% uživatelů)
- Future-forward tech (AGI preparedness)

**Won't Have (Out of Scope)** - Explicitly rejected
- Features pro pacienty (B2C pivot)
- Autonomní diagnostika (regulatorní risk)
- Features nevyžadující AI (generic EHR funkcionalita)

---

## 🚀 FÁZE 2: Škálování & Differentiation (Q3-Q4 2026)

### **Feature 1: DeepConsult - Hloubková Rešerše s Full-Text Studiemi** 🔥 MUST HAVE

#### **User Problem (z Person)**
**Dr. Svoboda (Kardiolog):**
> "Chci dostat stručné shrnutí nové studie z ESC kongresu během 5 sekund, abych nemusel číst celý 12-stránkový full-text."

**Current MVP Gap:**
- Benjamin MVP zobrazuje pouze abstrakty z PubMed (ne full-text)
- Lékaři musí ručně otevřít PDF studie a číst celých 10-15 stránek
- Chybí AI summarization pro dlouhé dokumenty (systematic reviews, meta-analyses)

#### **Proposed Solution**

**Co uživatel může dělat:**
Lékař v Chat interface zadá dotaz: **"Shrň mi studiu PRAGMATIC-AF 2024 o dronedaron vs amiodaron"**. Benjamin detekuje, že jde o specifickou studii, spustí **DeepConsult mód** a:

1. **Najde full-text PDF** (z PubMed Central, ScienceDirect, nebo institutional access)
2. **Extrahuje klíčové sekce:**
   - **Abstract** (executive summary)
   - **Methods** (study design, n=?, duration, endpoints)
   - **Results** (primary/secondary outcomes, statistical significance)
   - **Conclusions** (clinical implications)
   - **Limitations** (bias, confounding, generalizability)
3. **Vygeneruje AI summary** (500-700 slov):
   ```
   📄 PRAGMATIC-AF Study (ESC 2024) - Dronedaron vs Amiodaron

   🔬 Design: Randomized controlled trial, n=1,200, multicentrická studie (EU),
              follow-up 24 měsíců.

   🎯 Primary Endpoint: Kardiovaskulární mortalita + rehospitalizace
      → Dronedaron: 18.5% vs Amiodaron: 19.2% (p=0.64, non-inferior)

   ✅ Key Findings:
      - Dronedaron non-inferior k amiodaronu pro fibrilaci síní
      - ⬇️ Thyreoidální komplikace: 3.2% vs 12.1% (p<0.001) - VÝZNAMNÉ
      - ⬇️ Plicní toxicita: 1.1% vs 4.5% (p=0.002)
      - Žádný rozdíl v arytmické kontrole (AF recurrence)

   ⚠️ Limitations:
      - Pouze evropská populace (low generalizability pro Asii)
      - Průměrný věk 68 let (mladší pacienti underrepresented)
      - Vyloučeni pacienti s NYHA III-IV srdeční insuficiencí

   💊 Clinical Implication:
      U pacientů s fibrilací síní BEZ závažné SI preferovat dronedaron
      kvůli lepšímu safety profile (thyreoidea, plíce).

   📚 Citation: [PMID: 67890] PRAGMATIC-AF Investigators, Eur Heart J 2024
   ```

4. **Umožní follow-up otázky:**
   - "Jaké byly inclusion/exclusion criteria?"
   - "Kolik pacientů mělo diabetes?"
   - "Jaký byl dosing protocol?"

#### **Technická Implementace**

**Backend:**
- **MCP Tool: PDF Fetcher**
  - Integrace s PubMed Central API (open access articles)
  - ScienceDirect API (institutional subscription)
  - arXiv, bioRxiv (pre-prints)
  - Fallback: Manual upload (lékař nahraje PDF)

- **PDF Processing:**
  - OCR + structure extraction (Anthropic Claude PDF API)
  - Section detection (Abstract, Methods, Results, Discussion)
  - Table/Figure extraction (multimodal Claude)

- **Long Context Summarization:**
  - Claude Sonnet 4.5 (200K context window)
  - Prompt template pro structured summary
  - Extractive + abstractive summarization

**UX:**
- **Trigger:** Lékař zadá "Shrň studii [název]" nebo "DeepConsult: [PMID]"
- **Loading State:** "📄 Stahuji full-text a analyzuji... (15-30s)"
- **Output:** Strukturovaný summary s 5 sekcemi + option pro "Zobrazit full-text PDF"
- **Follow-up:** Conversational Q&A o specifických částech studie

**Pricing Impact:**
- DeepConsult mode = premium feature (limit 10 queries/month na basic plan)
- Pro plan: Unlimited DeepConsult + priority PDF fetching

#### **Success Metrics**
- **Adoption:** 40% lékařů používá DeepConsult ≥1x týdně
- **Time Savings:** 12 min (čtení full-text) → 2 min (AI summary) = 83% úspora
- **Satisfaction:** NPS >60 pro DeepConsult feature

#### **Competitive Advantage**
- **vs OpenEvidence:** Nemají full-text summarization, pouze abstrakty
- **vs UpToDate:** Mají peer-reviewed summaries, ale ne real-time (delay 3-6 měsíců)
- **vs ChatGPT:** Nemůže fetchovat paywalled articles (PDF access)

---

### **Feature 2: VZP Navigator - Automatická Kontrola Úhrad Pojišťovny** 🔥 MUST HAVE

#### **User Problem (z Person)**
**Dr. Nováková (Praktická lékařka):**
> "Chci vidět, zda je lék hrazený pojišťovnou přímo v odpovědi AI, abych nemusela zvlášť kontrolovat SÚKL a VZP."

**Current MVP Gap:**
- Benjamin zobrazuje SÚKL registraci (ano/ne), ale **ne VZP hrazení**
- Lékař musí otevřít VZP web nebo zavolat na VZP helpdesk
- Nejasnost ohledně žádostí o individuální úhradu (IU) vs standardní hrazení

#### **Proposed Solution**

**Co uživatel může dělat:**
Lékař v Chat interface zadá: **"Je empagliflozin hrazený pro diabetes 2. typu?"**. Benjamin prostřednictvím MCP tool **VZP Navigator** vrátí:

```
💊 Empagliflozin (Jardiance)

✅ HRAZENÍ VZP:
- Indikace: Diabetes mellitus 2. typu (T2DM)
- Podmínky: HbA1c ≥ 53 mmol/mol (7.0%) po selhání metforminu
- Úhrada: ✅ Ano, standardní hrazení (Seznam kategorizovaných LP)
- Doplatek pacienta: 30 Kč (na recept)

📋 KÓDY PRO PŘEDPIS:
- Kód omezení: H013 (Endokrinologie - diabetolog, internista)
- Diagnóza (ICD-10): E11 (Diabetes mellitus 2. typu)

⚠️ POZNÁMKA:
- Pokud HbA1c < 53 mmol/mol → Individuální úhrada (IU) nutná
  → Žádost o IU: Formulář VZP 12345, odůvodnění kardiorenal benefit

🔗 Zdroje:
- VZP Seznam LP: Empagliflozin (aktualizace 15.12.2025)
- SÚKL SPC: Jardiance 10mg/25mg
```

**Rozšířené Use Cases:**
1. **Off-label použití:**
   - "Je empagliflozin hrazený pro srdeční selhání?"
   - → "⚠️ Off-label: Srdeční selhání není v indikaci. Žádost o IU nutná."

2. **Cenové srovnání:**
   - "Jaké SGLT2 inhibitory jsou nejlevnější pro pacienta?"
   - → Tabulka: Empagliflozin 30 Kč, Dapagliflozin 50 Kč, Canagliflozin 45 Kč

3. **Interakce s žádostí o IU:**
   - "Jak napsat žádost o IU pro empagliflozin u NYHA II?"
   - → Template žádosti + doporučená literatura (kardiorenal benefit)

#### **Technická Implementace**

**MCP Tool: VZP Navigator**
- **Data Source:** VZP Seznam kategorizovaných LP (aktualizace měsíčně)
- **Scraping/API:**
  - Option 1: VZP public API (pokud existuje)
  - Option 2: Web scraping VZP databáze (https://www.vzp.cz/)
  - Option 3: Partnership s VZP (official data feed)

- **Database Schema (Supabase):**
  ```sql
  CREATE TABLE vzp_reimbursement (
    id UUID PRIMARY KEY,
    drug_name TEXT, -- empagliflozin
    brand_names TEXT[], -- Jardiance, Forxiga
    atc_code TEXT, -- A10BK03
    indication TEXT, -- Diabetes mellitus 2. typu
    reimbursement_status TEXT, -- full / partial / off-label
    conditions TEXT, -- HbA1c ≥ 53 mmol/mol
    patient_copay NUMERIC, -- 30 Kč
    restriction_code TEXT, -- H013
    last_updated TIMESTAMP
  );
  ```

**AI Prompt Engineering:**
- Kontext injection: "Vždy kontroluj VZP hrazení pro všechny léky v odpovědi"
- Structured output: Tabulka s sloupci (Drug, VZP Status, Conditions, Copay)

**UX:**
- **Inline v Chat odpovědi:** Automaticky zobrazuje VZP status při zmínce léku
- **Expandable Panel:** "Zobrazit detaily úhrady VZP" (dropdown)
- **Badge v Odpovědi:** ✅ Hrazeno | ⚠️ IU nutná | ❌ Nehrazeno

#### **Success Metrics**
- **Adoption:** 70% lékařů používá VZP Navigator ≥5x týdně
- **Time Savings:** 5 min (VZP web) → 0 min (inline info) = 100% úspora
- **Accuracy:** 95%+ přesnost VZP dat (měsíční sync check)

#### **Competitive Advantage**
- **Unique to Czech Market:** Žádný konkurent (OpenEvidence, UpToDate) nemá VZP data
- **Sticky Feature:** Lékaři nemohou žít bez toho po zkušení
- **Monetization:** Premium feature (Pro plan required)

---

### **Feature 3: Smart Epikríza 1.0 - Kompletní Epikríza dle Vyhlášky 98/2012 Sb.** 🟡 SHOULD HAVE

#### **User Problem (z MVP Boundary)**
**MVP Epikríza 0.1:**
- Pouze 3 datové zdroje (dekurzy, lab, medikace)
- Chybí 8 dalších sekcí podle vyhlášky § 21:
  - Vyšetření (RTG, CT, EKG)
  - Konzilia
  - Zákroky a operace
  - Ošetřovatelský plán
  - Sociální anamnéza
  - Atd.

**Dr. Svoboda (Kardiolog):**
> "Potřebuji kompletní epikrízu s konzilii a zákroky (PCI, coronarografie), ne jen základní info."

#### **Proposed Solution**

**Smart Epikríza 1.0:**
- **Všech 11 sekcí** podle vyhlášky č. 98/2012 Sb. § 21
- **Inteligentní parsing** FONS Enterprise dat:
  - Dekurzy (text mining pro klinický průběh)
  - Laboratorní výsledky (trend analysis: troponin ↑ → ↓)
  - Medikace (včetně změn dávkování a discontinuation)
  - Vyšetření (RTG, CT, MRI reports → structured findings)
  - Konzilia (kardiolog, neurolog → recommendations extraction)
  - Zákroky (PCI, operace → procedural details)
  - Ošetřovatelský plán (mobility, pain management)
  - Sociální anamnéza (home care, follow-up planning)

**Nové Funkce:**
1. **"Generovat jinak" Button:**
   - MVP: Lékař musí ručně editovat → časově náročné
   - 1.0: Klikne "Generovat jinak" → AI vytvoří alternativní formulaci
   - Use case: "Verze pro VZP kontrolu" vs "Verze pro pacienta"

2. **Sekce Selectability:**
   - Lékař může vybrat: "Chci pouze anamnézu + průběh + doporučení"
   - Nebo: "Chci kompletní 11 sekcí"

3. **Template Library:**
   - Pre-made templates pro běžné diagnózy:
     - "Akutní infarkt myokardu (STEMI) s PCI"
     - "Pneumonie s hospitalizací"
     - "Diabetes s akutní dekompenzací"

#### **Technická Implementace**

**Enhanced FONS Enterprise Integration:**
- Rozšířené API calls pro více datových zdrojů (6 → 11)
- Structured data extraction (NLP pro konzilia, zákroky)

**AI Prompt Template:**
```
Vytvoř kompletní propouštěcí zprávu podle vyhlášky č. 98/2012 Sb. § 21:

1. Identifikační údaje pacienta
2. Diagnózy (vstupní + výstupní)
3. Osobní + rodinná anamnéza
4. Nynější onemocnění (anamnéza přijetí)
5. Průběh hospitalizace
6. Fyzikální vyšetření
7. Laboratorní výsledky (včetně trendů)
8. Zobrazovací vyšetření (RTG, CT, MRI)
9. Konziliární vyšetření
10. Zákroky a operace
11. Doporučení pro další péči

Data: {fons_data_json}
```

**Version Control:**
- User může mít 3-5 verzí epikrízy (drafts)
- Track changes mezi verzemi (diff view)

#### **Success Metrics**
- **Completeness:** 95% epikríz obsahuje všech 11 sekcí
- **Regeneration Rate:** 40% lékařů používá "Generovat jinak" ≥1x
- **Time Savings:** 20 min → 3 min (s úpravami) = 85% úspora

---

### **Feature 4: Real-Time Collaboration - Sdílení Konverzací s Kolegy** 🟡 SHOULD HAVE

#### **User Problem**
**Dr. Kučera (Urgentní příjem):**
> "Ve 3 ráno nemám k dispozici specialisty (kardiolog, neurolog) pro okamžitou konzultaci."

**Current Workflow:**
- Lékař má složitý případ → konzultuje Benjamin
- Chce se poradit s kolegou → musí zkopírovat celý thread
- Kolega nemá kontext → musí číst dlouhý text

#### **Proposed Solution**

**Real-Time Collaboration:**
1. **Share Conversation Button:**
   - V Chat interface: Tlačítko "🔗 Sdílet s kolegou"
   - Vygeneruje secure link: `benjamin.ai/shared/abc123` (expire za 24h)
   - Kolega otevře link → vidí celou konverzaci včetně citací

2. **Live Annotation:**
   - Kolega může přidat komentář: "💬 Souhlasím s diagnózou, ale doporuču..."
   - Original lékař vidí komentář v real-time (Supabase Realtime)

3. **Multi-Doctor Consultation Mode:**
   - Lékař může "pozvat" 2-3 kolegy do conversation threadu
   - Všichni vidí otázky + AI odpovědi + navzájem komentáře
   - Use case: Multidisciplinary team meetings (MDT)

#### **Technická Implementace**

**Supabase Realtime:**
- Websocket connection pro live updates
- `shared_conversations` tabulka s RLS policies
- Permission management (viewer / editor / owner)

**GDPR Compliance:**
- **Anonymization:** Před sdílením odstranit PII (jméno pacienta, RC)
- **Consent:** Lékař musí potvrdit: "Odesouhlasit sdílení (bez PII)"
- **Audit:** Log všech sdílení (kdo, komu, kdy, access count)

**UX:**
- **Share Modal:**
  - Checkbox: ☑️ Anonymizovat data pacienta
  - Expires in: [24 hours ▾]
  - Generate Link button

#### **Success Metrics**
- **Adoption:** 25% lékařů sdílí ≥1 konverzaci měsíčně
- **Collaboration:** Průměrně 1.5 komentářů na sdílenou konverzaci
- **Reduced Consultation Time:** 15 min (telefon + vysvětlování) → 5 min (sdílený link)

---

### **Feature 5: Voice Input - "Hey Benjamin" Voice Activation** 🟢 COULD HAVE

#### **User Problem**
**Dr. Nováková (Praktická lékařka):**
> "Během vyšetření pacienta nemám ruce volné na psaní - třímám stetoskop, kontroluji puls."

**Current Workflow:**
- Lékař musí psát dotaz → přerušuje vyšetření pacienta
- Alternativa: Diktovat asistentce → ta píše do Benjamina

#### **Proposed Solution**

**Voice Input:**
1. **Voice Button v Chat Interface:**
   - Mikrofon ikona vedle text input
   - Klikne → začne nahrávat: "Jaké jsou guidelines pro léčbu diabetu 2. typu..."
   - Speech-to-text (OpenAI Whisper) → text se objeví v inputu
   - Lékař může editovat před odesláním

2. **"Hey Benjamin" Wake Word (Chrome Extension):**
   - Always-listening mód (opt-in)
   - Lékař řekne: **"Hey Benjamin, jaké jsou interakce warfarinu?"**
   - Extension otevře side panel → voice input → AI odpověď
   - Hands-free workflow

3. **Voice Response (Optional):**
   - AI odpověď může být přečtena nahlas (TTS)
   - Use case: Urgentní příjem, lékař má ruce zaneprázdněny

#### **Technická Implementace**

**Speech-to-Text:**
- OpenAI Whisper API (best accuracy pro český jazyk)
- Real-time streaming transcription (low latency)

**Wake Word Detection:**
- On-device ML model (Porcupine wake word engine)
- Privacy: Audio se neukládá, pouze local processing

**Text-to-Speech (Optional):**
- Czech TTS engine (Google Cloud TTS nebo Azure)

**UX:**
- **Permissions:** User musí povolit microphone access
- **Privacy Controls:**
  - Toggle: "Always listen for Hey Benjamin" (off by default)
  - Visual indicator: 🎤 červená tečka při recording
  - Instant cancel button (X)

#### **Success Metrics**
- **Adoption:** 15% lékařů používá voice input ≥1x týdně
- **Accuracy:** 90%+ přesnost Czech transcription
- **Use Cases:** 60% voice queries jsou z urgentního příjmu (hands-free scenarios)

---

## 🔮 FÁZE 3: AI-Native Healthcare Platform (2027+)

### **Feature 6: Predictive Alerts - Proaktivní Doporučení** 🔥 HIGH VALUE

#### **Vision**
Benjamin se mění z **reactive** (odpovídá na dotazy) na **proactive** (navrhuje akce).

**Example Scenarios:**
1. **Patient Risk Stratification:**
   - Benjamin analyzuje FONS Enterprise data pacienta
   - Detekuje: "⚠️ Pacient má HbA1c 65 mmol/mol + BMI 32 + kouří"
   - Alert: "Vysoké riziko kardiovaskulární události. Doporučuji: SGLT2i + statiny."

2. **Drug Interaction Prevention:**
   - Lékař předepisuje nový lék v FONS Enterprise
   - Benjamin detekuje interakci s existing medikací
   - Popup: "🔴 VAROVÁNÍ: Sertralin + Warfarin → riziko krvácení. Zvážit alternativu?"

3. **Follow-up Reminders:**
   - Benjamin sleduje pacientovu historii
   - Pacient měl laboratorní výsledky s hraničním TSH
   - Alert: "📅 Připomínka: Kontrola TSH za 3 měsíce (pacient XY)"

#### **Technická Implementace**
- **Background Jobs:** Supabase Cron (scheduled tasks)
- **Rule Engine:** If-then rules + ML model (risk scoring)
- **Push Notifications:** Chrome Extension notifications + Email

---

### **Feature 7: Multimodal AI - Image Analysis (RTG, CT, EKG)** 🔮 FUTURE

#### **Vision**
Benjamin může analyzovat medicínské snímky (RTG, CT, EKG) a poskytovat AI insights.

**Example Use Cases:**
1. **RTG Chest:**
   - Lékař nahraje RTG snímek do Benjamina
   - AI: "🫁 Nálezy: Pravostranný pleurální výpotek (small), žádné infiltráty. Doporučuji: Ultrazvuk hrudníku."

2. **EKG Interpretation:**
   - Lékař nahraje 12-svodové EKG
   - AI: "⚡ Nález: ST elevace ve svodech V1-V4 → STEMI přední stěny. Urgentní PCI!"

3. **CT Brain:**
   - AI detekuje: "🧠 Hypodenzní ložisko v levé MCA oblasti → ischemická CMP"

#### **Technická Implementace**
- **Multimodal LLM:** Claude 3.5 Sonnet (podporuje image input)
- **Medical Image Models:** Pre-trained models (X-ray classification, CT segmentation)
- **DICOM Support:** Integration s PACS systémy

#### **Regulatory:**
- **MDR Class IIb/III:** Vyžaduje CE certifikaci pro AI diagnostiku
- **Clinical Validation:** Prospektivní studie (1000+ pacientů)
- **Liability:** Jasný disclaimer ("asistent, ne diagnostický nástroj")

---

### **Feature 8: Mobile App (iOS/Android) - Offline Režim** 🟢 COULD HAVE

#### **Vision**
Benjamin jako nativní mobilní app pro lékaře na vizitách, domácích návštěvách, nebo offline (horské oblasti).

**Key Features:**
- **Offline Mode:** Cached guidelines + basic Q&A (on-device LLM)
- **Camera Integration:** Fotit recepty, laboratorní výsledky → OCR → parse
- **QR Code Patient Linking:** Scan QR code na kartičce pacienta → instant FONS data load

#### **Technická Implementace**
- **React Native** nebo **Flutter** (cross-platform)
- **On-device LLM:** Llama 3 8B (quantized) pro offline inference
- **Sync:** Background sync při online připojení

---

## 📊 Prioritizační Matice (ROI vs Effort)

| Feature | User Impact | Competitive Advantage | Effort (Months) | Priority |
|---------|-------------|----------------------|----------------|----------|
| **DeepConsult (Full-Text)** | 🔥🔥🔥 | 🔥🔥🔥 | 3 | **MUST** |
| **VZP Navigator** | 🔥🔥🔥 | 🔥🔥🔥 | 2 | **MUST** |
| **Smart Epikríza 1.0** | 🔥🔥 | 🔥 | 2 | **SHOULD** |
| **Real-Time Collaboration** | 🔥🔥 | 🔥🔥 | 1.5 | **SHOULD** |
| **Voice Input** | 🔥 | 🔥 | 1 | **COULD** |
| **Predictive Alerts** | 🔥🔥🔥 | 🔥🔥🔥 | 4 | **Fáze 3** |
| **Multimodal AI (Images)** | 🔥🔥🔥 | 🔥🔥🔥 | 6 | **Fáze 3** |
| **Mobile App** | 🔥🔥 | 🔥 | 3 | **Fáze 3** |

---

## 🎯 Recommended Roadmap

### **Q3-Q4 2026 (Fáze 2):**
**Theme:** Škálování z 50 → 500 lékařů + Competitive Parity

1. ✅ **VZP Navigator** (2 měsíce) - Unique to Czech market, sticky feature
2. ✅ **DeepConsult** (3 měsíce) - Match UpToDate depth, differentiate vs OpenEvidence
3. ✅ **Smart Epikríza 1.0** (2 měsíce) - Complete legislative compliance
4. ✅ **Real-Time Collaboration** (1.5 měsíce) - Network effects, viral growth

**Expected Outcomes:**
- Retention: 60% → 75%
- NPS: 50 → 65
- DAU/WAU: 40% → 55%
- Upsell to Pro: 20% users

### **2027 (Fáze 3):**
**Theme:** AI-Native Healthcare Platform

1. ✅ **Predictive Alerts** (4 měsíce) - Proactive AI, preventive care
2. ✅ **Multimodal AI** (6 měsíců) - Image analysis, EKG interpretation
3. ✅ **Mobile App** (3 měsíce) - Expand TAM (visiting doctors, rural areas)
4. ✅ **MDR Class IIa Certification** (6-12 měsíců) - Regulatory compliance, trust

**Expected Outcomes:**
- Market Leadership: #1 AI clinical assistant v ČR
- Enterprise Contracts: 10+ nemocnic (site licenses)
- International Expansion: Slovakia, Poland pilots

---

## 💰 Monetization Strategy

### **Pricing Tiers (Post-MVP):**

**Basic (Zdarma):**
- Chat Q&A (10 queries/day)
- Epikríza 0.1 (3 datové zdroje)
- Translator (basic)
- Historie 30 dní

**Pro (990 Kč/měsíc):**
- Unlimited Chat Q&A
- DeepConsult (unlimited full-text)
- VZP Navigator
- Smart Epikríza 1.0 (11 sekcí)
- Real-Time Collaboration
- Historie 12 měsíců
- Priority support

**Enterprise (Custom Pricing):**
- All Pro features
- Multi-user licenses (site-wide)
- SSO (SAML)
- Dedicated Supabase instance
- Custom MCP tools (hospital-specific guidelines)
- SLA (99.9% uptime)
- On-premise deployment option

---

## 🚨 Risk Mitigation

### **Technical Risks:**
1. **PDF Fetching Failure (DeepConsult):**
   - **Mitigation:** Fallback na manual upload, partnership s publishers

2. **VZP Data Staleness:**
   - **Mitigation:** Monthly sync checks, user reporting "Data is outdated"

3. **Voice Recognition Accuracy:**
   - **Mitigation:** User can edit transcription before sending

### **Regulatory Risks:**
1. **MDR Compliance (Multimodal AI):**
   - **Mitigation:** Start clinical validation early (1-2 years lead time)

2. **GDPR (Real-Time Collaboration):**
   - **Mitigation:** Anonymization by default, consent workflows

---

## ✅ Success Criteria (Fáze 2 Completion)

**Adoption:**
- 500+ active lékařů (10x growth from MVP)
- 60% use ≥1 advanced feature (DeepConsult, VZP Navigator)

**Engagement:**
- DAU/WAU: 55% (up from 40%)
- Queries/user/day: 8 (up from 5)

**Revenue:**
- 20% conversion to Pro plan
- ARPU: 200 Kč/user/month (mix of Free + Pro)

**Retention:**
- 75% retention po 6 měsících (up from 60%)
- Churn rate: <5% měsíčně

**NPS:**
- NPS >65 (up from 50)
- "Would recommend": 85%+

---

**Konec Feature Proposals - Připraveno k prioritizaci s Product Team**
