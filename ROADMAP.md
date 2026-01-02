# Roadmap - Czech MedAI 🗺️

> Plán vývoje AI asistenta pro české lékaře

Tento dokument obsahuje přehled dokončených funkcí a plánovaný vývoj projektu Czech MedAI. Roadmap je pravidelně aktualizován na základě zpětné vazby uživatelů a technologického vývoje.

---

## ✅ Dokončené funkce

### Základní infrastruktura
- [x] Next.js 16 frontend s App Router
- [x] FastAPI backend s LangGraph orchestrací
- [x] Supabase integrace (auth, databáze, RLS)
- [x] Dark/Light mode s next-themes
- [x] Responzivní design (mobile-first)

### AI Chat
- [x] Konverzační rozhraní v češtině
- [x] Evidence-based odpovědi s citacemi
- [x] PubMed integrace (29M+ článků)
- [x] Streaming odpovědí (backend) - ⚠️ Frontend zatím nevyužívá
- [x] Historie konverzací

### Lékařské nástroje
- [x] VZP Navigator - vyhledávání úhrad
- [x] SÚKL databáze léčiv s embeddings
- [x] Generátor epikrizy
- [x] Překladač lékařských textů
- [x] Audio transkripce

### Data Pipeline
- [x] ETL pipeline pro SÚKL data
- [x] Sémantické vyhledávání (OpenAI embeddings)
- [x] Automatická aktualizace cen léčiv

### Autentizace & Bezpečnost
- [x] Email autentizace přes Supabase
- [x] Row Level Security (RLS) - ⚠️ **14 tabulek bez RLS** - viz BACKLOG.md
- [x] Session management
- [ ] Ochrana API endpointů - ⚠️ **Některé endpointy bez auth** - viz BACKLOG.md

---

## 📝 Detailní backlog

Pro detailní rozepsání úkolů a priorit viz **[BACKLOG.md](BACKLOG.md)**.

---

## 🎯 Krátkodobé cíle (1-3 měsíce)

### Vylepšení AI chatu
- [ ] Kontextové pamatování napříč sezeními
- [ ] Vylepšení přesnosti odpovědí pro české guidelines
- [ ] Podpora přílohy obrázků (RTG, CT snímky)
- [ ] Rychlejší odezva při komplexních dotazech

### Rozšíření datových zdrojů
- [ ] Integrace českých klinických guidelines
- [ ] Propojení s databází lékových interakcí
- [ ] Aktualizace SPC/PIL dokumentů v reálném čase

### UX vylepšení
- [ ] Oblíbené dotazy a šablony
- [ ] Klávesové zkratky pro power users
- [ ] Vylepšené zobrazení citací
- [ ] Export konverzací do PDF

### Kvalita & Stabilita
- [ ] Rozšíření test coverage (frontend + backend)
- [ ] Performance monitoring a alerting
- [ ] Error tracking s Sentry
- [ ] Dokumentace API (OpenAPI 3.1)

---

## 🚀 Střednědobé cíle (3-6 měsíců)

### DeepConsult 2.0
- [ ] Pokročilá analýza komplexních případů
- [ ] Generování diferenciální diagnostiky
- [ ] Literární rešerše s citacemi
- [ ] Porovnání léčebných postupů

### SÚKL Alerts
- [ ] Real-time notifikace o změnách v SPC
- [ ] Upozornění na stažení šarží
- [ ] Personalizované alerty podle specializace
- [ ] Push notifikace (web + mobile)

### EHR Integrace
- [ ] REST API pro české EHR systémy
- [ ] Integrace s ICZ AMIS
- [ ] Podpora pro CGM systémy
- [ ] Medisoft konektory
- [ ] HL7 FHIR kompatibilita

### Premium funkce
- [ ] Týmové účty s rolemi
- [ ] Admin dashboard pro správce
- [ ] Audit log aktivit
- [ ] Pokročilá analytika použití

### Mobilní aplikace
- [ ] React Native PWA wrapper
- [ ] Offline režim pro základní funkce
- [ ] Biometrické přihlášení

---

## 🔮 Dlouhodobá vize (6+ měsíců)

### AI & Machine Learning
- [ ] Fine-tuned model pro českou medicínu
- [ ] Vlastní embeddings pro české lékařské texty
- [ ] Prediktivní analýzy na základě dat
- [ ] Voice-first rozhraní

### Rozšíření ekosystému
- [ ] Marketplace pro extensions
- [ ] Plugin systém pro třetí strany
- [ ] White-label řešení pro nemocnice
- [ ] Integrace s pojišťovnami (VZP, ČPZP, OZP)

### Certifikace & Compliance
- [ ] MDR certifikace zdravotnického prostředku
- [ ] ISO 27001 certifikace
- [ ] HIPAA compliance (pro mezinárodní expanzi)
- [ ] CE marking

### Mezinárodní expanze
- [ ] Slovenská lokalizace
- [ ] Podpora pro ŠÚKL (SK)
- [ ] Další středoevropské trhy

---

## 💡 Jak přispět nebo navrhnout funkci

### Hlášení chyb
Pokud narazíte na chybu, vytvořte Issue v GitHub repozitáři s:
- Popisem problému
- Kroky k reprodukci
- Očekávaným vs. skutečným chováním
- Screenshots (pokud relevantní)

### Návrhy nových funkcí
Pro návrh nové funkce:
1. Zkontrolujte, zda podobný návrh již neexistuje v Issues
2. Vytvořte nový Issue s labelem `feature-request`
3. Popište use case a očekávané chování
4. Uveďte prioritu z vašeho pohledu

### Přispění kódem
1. Forkněte repozitář
2. Vytvořte feature branch (`git checkout -b feature/nova-funkce`)
3. Commitněte změny (`git commit -m 'Přidání nové funkce'`)
4. Pushněte branch (`git push origin feature/nova-funkce`)
5. Otevřete Pull Request

### Kontakt
- **GitHub Issues**: Pro technické dotazy a návrhy
- **Email**: podpora@czechmedai.cz *(připravujeme)*

---

## 📊 Prioritizace

Funkce jsou prioritizovány na základě:
1. **Dopad na uživatele** - Kolik lékařů bude mít z funkce prospěch?
2. **Klinická hodnota** - Zlepší to péči o pacienty?
3. **Technická proveditelnost** - Jak složité je implementovat?
4. **Regulatorní požadavky** - Je nutné pro certifikaci?

---

## 📅 Historie aktualizací

| Datum | Verze | Změny |
|-------|-------|-------|
| Leden 2025 | 1.0 | První verze roadmap |

---

*Poslední aktualizace: leden 2025*

**Poznámka**: Tento roadmap je orientační a může se měnit na základě priorit, dostupných zdrojů a zpětné vazby uživatelů.
