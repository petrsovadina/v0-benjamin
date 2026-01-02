# Czech MedAI Backend

> FastAPI backend pro Czech MedAI — AI orchestrace, SÚKL pipeline, REST API.

---

## 📁 Struktura

```
backend/
├── app/                          # FastAPI aplikace
│   ├── api/v1/                   # REST API v1
│   │   ├── endpoints/
│   │   │   ├── query.py          # Chat endpointy (auth ✅)
│   │   │   ├── ai.py             # AI tools (auth ⚠️ CHYBÍ!)
│   │   │   ├── drugs.py          # SÚKL léčiva
│   │   │   └── admin.py          # Admin operace
│   │   └── deps.py               # Auth dependencies
│   ├── core/
│   │   ├── config.py             # Settings (env vars)
│   │   ├── graph.py              # LangGraph RAG workflow
│   │   └── state.py              # ClinicalState TypedDict
│   ├── schemas/                  # Pydantic modely
│   └── services/                 # Business logic
├── agent_graph.py                # Streaming agent (tools)
├── epicrisis_graph.py            # Epikríza LangGraph
├── translator_graph.py           # Překladač LangGraph
├── pipeline/                     # SÚKL ETL pipeline
├── data_processing/              # Data transformace
├── mcp_servers/                  # MCP servery (PubMed, SÚKL)
├── tests/                        # Pytest testy
├── main.py                       # FastAPI entry point
└── requirements.txt              # Python dependencies
```

---

## 🚀 Spuštění

> ⚠️ **Důležité:** Spouštět z **kořenového adresáře** projektu (`v0-benjamin/`), ne z `backend/`.

```bash
# 1. Virtual environment
python -m venv backend/venv
source backend/venv/bin/activate  # macOS/Linux

# 2. Dependencies
pip install -r backend/requirements.txt

# 3. Environment variables
cp backend/.env.example backend/.env
# Upravit: ANTHROPIC_API_KEY, OPENAI_API_KEY, SUPABASE_URL, SUPABASE_KEY

# 4. Spustit server
uvicorn backend.main:app --reload --port 8000
```

- **API:** http://localhost:8000
- **Swagger UI:** http://localhost:8000/docs
- **Health:** http://localhost:8000/health

---

## 🔐 Autentizace

Bearer token z Supabase Auth:

```http
Authorization: Bearer <jwt_token>
```

**Auth dependency** (`app/api/v1/deps.py`):
```python
async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    # Validuje token proti Supabase
```

---

## 🔌 API Endpointy

### Chat & Query (`/api/v1/query`)

| Method | Endpoint | Auth | Popis |
|--------|----------|------|-------|
| POST | `/api/v1/query/` | ✅ | Chat (non-streaming) |
| POST | `/api/v1/query/stream` | ⚠️ | Streaming chat (NDJSON) |
| GET | `/api/v1/query/history` | ✅ | Historie dotazů |

**Request body:**
```json
{
  "message": "Jaké je dávkování aspirinu?",
  "history": [],
  "session_id": "optional-uuid"
}
```

### AI Tools (`/api/v1/ai`)

> ⚠️ **Bezpečnostní varování:** Tyto endpointy NEMAJÍ autentizaci! Viz [BACKLOG.md](../BACKLOG.md#us-12).

| Method | Endpoint | Auth | Popis |
|--------|----------|------|-------|
| POST | `/api/v1/ai/epicrisis` | ❌ | Generování epikrizy |
| POST | `/api/v1/ai/translate` | ❌ | Překlad textu |
| POST | `/api/v1/ai/transcribe` | ❌ | Audio transkripce |

### Drugs (`/api/v1/drugs`)

| Method | Endpoint | Auth | Popis |
|--------|----------|------|-------|
| GET | `/search?q=aspirin&limit=20` | ❌ | Sémantické vyhledávání |
| GET | `/vzp-search?q=...` | ❌ | VZP vyhledávání |
| GET | `/{sukl_code}` | ❌ | Detail léku |

### Admin (`/api/v1/admin`)

| Method | Endpoint | Auth | Popis |
|--------|----------|------|-------|
| POST | `/upload-guideline` | ✅ | Upload guidelines PDF |

---

## 🧠 AI Grafy (LangGraph)

Backend obsahuje **dva různé AI systémy**:

### 1. RAG Workflow (`app/core/graph.py`)
- **Použití:** `/api/v1/query/` (non-streaming)
- **Nodes:** classifier → retriever → synthesizer
- **State:** `ClinicalState` TypedDict

```python
class ClinicalState(TypedDict):
    messages: List[BaseMessage]
    query: str
    classification: str
    retrieved_docs: List[Dict]
    citations: List[Dict]
    answer: str
    reasoning_steps: List[str]
    tool_calls: List[Dict]
    error: Optional[str]
```

### 2. Streaming Agent (`agent_graph.py`)
- **Použití:** `/api/v1/query/stream`
- **Typ:** Tool-based agent s Claude 3
- **Tools:** SÚKL search, PubMed, Guidelines retrieval

### 3. Specialized Graphs
- `epicrisis_graph.py` — Generování epikrízy
- `translator_graph.py` — Lékařský překlad

---

## 💉 SÚKL Data Pipeline

ETL pro data ze Státního ústavu pro kontrolu léčiv.

```bash
# Full pipeline (z kořenového adresáře)
python -m backend.pipeline.run_pipeline --drugs --pricing --documents --with-embeddings
```

### Jednotlivé kroky

```bash
# Stáhnout raw data
python -m backend.pipeline.run_pipeline --download

# Léčiva + embeddings
python -m backend.pipeline.run_pipeline --drugs --with-embeddings

# Ceny (current + historical)
python -m backend.pipeline.run_pipeline --pricing

# SPC/PIL dokumenty
python -m backend.pipeline.run_pipeline --documents
```

### Parametry

| Flag | Popis |
|------|-------|
| `--limit N` | Zpracovat pouze N položek |
| `--with-embeddings` | Generovat OpenAI vektory (~$5-10 za 20k léků) |
| `--dry-run` | Bez zápisu do DB |

---

## 🗄️ Databáze

Supabase PostgreSQL s pgvector. Klíčové tabulky:

| Tabulka | Popis |
|---------|-------|
| `users` | Uživatelé (sync s auth.users) |
| `queries` | AI dotazy s citacemi |
| `citations` | Strukturované citace |
| `drugs` | SÚKL léčiva + embeddings |
| `guidelines` | České guidelines + embeddings |
| `chat_sessions` | Chat sessions |
| `chat_messages` | Chat historie |

> ⚠️ **14 tabulek nemá RLS!** Viz [BACKLOG.md](../BACKLOG.md#us-11).

---

## 🧪 Testování

```bash
# Z backend/ adresáře
pytest                     # Všechny testy
pytest -v                  # Verbose
pytest --cov              # Coverage report
pytest tests/test_api.py  # Specifický soubor
```

### Verifikační skripty

```bash
# Ověření kompilace grafů
python verify_graph_compilation.py

# Ověření RAG flow
python verify_complete_rag_flow.py

# Ověření agenta
python verify_agent.py
```

---

## 🔧 Konfigurace

### Environment Variables (`backend/.env`)

```env
# AI Providers (povinné)
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=...

# Database (povinné)
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=eyJ...  # Service role key

# Optional
ENVIRONMENT=development
LOG_LEVEL=INFO
```

### Settings class (`app/core/config.py`)

```python
class Settings(BaseSettings):
    SUPABASE_URL: str
    SUPABASE_KEY: str
    ANTHROPIC_API_KEY: str
    OPENAI_API_KEY: str
    # ...
```

---

## 📦 Docker

```bash
# Build
docker build -t czech-medai-backend .

# Run
docker run -p 8000:8000 --env-file .env czech-medai-backend
```

---

## ⚠️ Známé problémy

1. **Auth chybí na AI endpointech** — `ai.py` nemá `Depends(get_current_user)`
2. **Streaming nekonzistentní** — Backend ready, frontend nepoužívá
3. **14 DB tabulek bez RLS** — Bezpečnostní riziko

Viz [BACKLOG.md](../BACKLOG.md) pro řešení.

---

## 📚 Další dokumentace

- [../README.md](../README.md) — Hlavní README
- [../docs/architecture/](../docs/architecture/README.md) — Architektura
- [../docs/data_pipeline.md](../docs/data_pipeline.md) — SÚKL pipeline detaily
- [../BACKLOG.md](../BACKLOG.md) — Product backlog

---

*Poslední aktualizace: Leden 2026*
