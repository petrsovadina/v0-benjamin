## [1.1.0] - 2025-12-25

### ✨ Added
- 🎉 **PDF Import Pipeline**: Kompletní implementace importu PDF souborů českých medicínských guidelines včetně parsování dokumentů, chunking obsahu a generování embeddings
- Automatické zpracování a uložení guideline obsahu do vektorové databáze
- 🔍 **Semantic Search**: Vylepšená retrieval funkčnost pro extrakci relevantního obsahu guidelines z AI odpovědí
- Support pro metadata handling a kategorizaci medicínských dokumentů

### 🔧 Changed
- Optimalizované chunking strategie pro medicínský obsah s lepší zachováním kontextu
- Vylepšená integrace s Graphiti memory systémem pro cross-session retrieval

### 🐛 Fixed
- 🔒 **Git Merge Conflict**: Vyřešeny nevyřešené merge konflikty v hlavním README.md souboru (značky <<<<<<< HEAD)
- Opraveno zobrazení dokumentace na GitHubu a ujasnění vstupního bodu projektu pro nové vývojáře

## [1.0.0] - 2025-12-25

### ✨ Nové funkce
- 🎉 **Pokyny PDF**: Kompletní systém pro nahrávání a vyhledávání českých lékařských pokynů s podporou embedding a citací
- 🎤 **AI transkripce API**: Nový koncový bod pro transkripci zvuku s umělou inteligencí
- 💬 **Perzistence historie chatu**: Trvalé ukládání a zobrazení historie konverzací s dedikovanými stránkami sezení
- Aktualizované specifikace API pro nástroje AI a léky
- Nový SUKL retriever pro vyhledávání léčiv

### 🔧 Vylepšení
- Vylepšená zpracování chyb s strukturovaným kontextem v logování
- Přidáno logiku opakování pro selhání generování embedding
- Validace velikosti souboru pro uploadový koncový bod
- Strukturované chybové odpovědi s podrobnostmi
- Refaktorování backendu imports a konfigurací
- Nová struktura dokumentace a aktualizace závislostí
- Optimalizace workflow grafu s integrací pokynů uzlu

### 🐛 Opravy
- Opraveny limitace frekvence chatu
- Opraveny deep linky SUKL
- Opraveny chybějící importy

### 📚 Dokumentace
- Implementace nové struktury dokumentace
- Konsolidace dokumentačních souborů do nového hlavního PRD
- Odebrání starých plánů funkcí a průvodců stylem

### 🧪 Testování
- Jednotkové testy pro GuidelinesLoader
- Integrační testy pro uploadový koncový bod
- Komplexní E2E testy pro kompletní pipeline
- Jednotkové testy pro search_guidelines()
- Testy SUKL retrieveru

### 🔄 Ostatní
- Odebrání zastaralého souboru
- Aktualizace konfigurace projektu a závislostí
- Přidání CI workflow