## [1.0.0] - 31. 12. 2025

### ✨ Přidáno
- 🎉 **Pokročilá podpora agentického workflow**: Rozšířená struktura `ClinicalState` umožňuje vícestupňové uvažování, sledování volání nástrojů a správu kontextu pacienta prostřednictvím integrace LangGraph Checkpointer
- Funkce uchovávání a obnovy stavu pro správu stavových relací bez narušení stávající funkčnosti workflow
- Abstraktní vrstva registru nástrojů poskytuje jednotné rozhraní pro volání serverů MCP (SÚKL, PubMed) s typově bezpečnou validací
- Komplexní protokolování nástrojů a pozorovatelnost napříč celou platformou
- Podpora funkcí Deep Agents ve stávajícím pracovním postupu RAG (Retrieval-Augmented Generation)

### 🔄 Změny
- 🚀 **Vylepšený ekosystém LangChain**: Migrace z verze 0.1.x na 0.3.x+ v backendu Pythonu (7 základních balíčků)
- Přepracovaný systém vyvolávání nástrojů pro použití centralizovaného registru nástrojů se standardizovaným rozhraním
- Vylepšené řízení kontextu pacientů s vylepšenými schopnostmi sledování stavu
- Implementovány konzistentní vzorce správy nástrojů napříč všemi komponentami platformy

### 🐛 Opraveno
- Zachována úplná zpětná kompatibilita během aktualizace LangChain bez jediného selhání testu
- Odstraněna všechna varování o zastaralosti v řetězci závislostí
- Zajištěna hladká integrace nového registru nástrojů bez narušení stávajících pracovních postupů
```