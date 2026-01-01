# Czech MedAI Backend

Python backend powering the Czech MedAI Assistant. Handles AI orchestration, data processing, and integration with SÚKL.

## 🛠️ Setup

**Important**: Run all commands from the **project root folder** (`v0-benjamin`) to ensure correct module resolution.

1.  **Create Virtual Environment**:
    ```bash
    python -m venv backend/venv
    source backend/venv/bin/activate  # macOS/Linux
    # .\backend\venv\Scripts\activate  # Windows
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r backend/requirements.txt
    ```

3.  **Environment Variables**:
    Create `.env` file in the `backend` directory (copy from `backend/.env.example`).
    Required variables:
    - `OPENAI_API_KEY`: Required for generating SÚKL embeddings (Sémantické vyhledávání)
    - `ANTHROPIC_API_KEY`: For Claude 3 (Required)
    - `GOOGLE_API_KEY`: For Audio Transcription (Required)
    - `SUPABASE_URL`: Database URL
    - `SUPABASE_KEY`: Service Role Key (Required for pipeline writes)
    - `ENVIRONMENT`: Set to `development`, `staging`, or `production` (default: `development`)
    - `CORS_ORIGINS`: **Required in production** - JSON array of allowed origins
      - Example: `CORS_ORIGINS='["https://app.benjamin.cz","https://benjamin.cz"]'`
      - Development example: `CORS_ORIGINS='["http://localhost:3000","http://localhost:5173"]'`
      - **Important**: The application will fail to start if `CORS_ORIGINS` is empty when `ENVIRONMENT=production`

## 🚀 Running the API

Start the FastAPI server (from the **project root** directory):

```bash
uvicorn backend.main:app --reload --port 8000
```

- **API URL**: `http://localhost:8000`
- **Documentation**: `http://localhost:8000/docs`

## 🔐 Authentication

All API endpoints (except `/docs`, `/health`) require a valid Bearer Token from Supabase Auth.

```http
Authorization: Bearer <your_jwt_token>
```

## 🔌 API Endpoints

### 1. Chat & Query (`/api/v1/query`)

#### `POST /api/v1/query`
Standard chat endpoint (non-streaming).

**Body:**
```json
{
  "message": "Jaké je dávkování aspirinu?",
  "history": [],
  "session_id": "optional-uuid"
}
```

#### `POST /api/v1/query/stream`
Streaming chat endpoint (NDJSON). Returns chunks of tokens and metadata.

### 2. Drugs (`/api/v1/drugs`)

#### `GET /api/v1/drugs/search`
Semantic and full-text search for drugs.

**Parameters:**
- `q`: Search query (e.g., "aspirine", "lék na bolest hlavy")
- `limit`: Max results (default 20)

**Response:**
```json
[
  {
    "sukl_code": "0046214",
    "name": "ASPIRIN C",
    "atc_name": "KYSELINA ACETYLSALICYLOVÁ...",
    "price": 120.50,
    "similarity": 0.85
  }
]
```

#### `GET /api/v1/drugs/{sukl_code}`
Get detailed information about a specific drug.

### 3. AI Tools (`/api/v1/ai`)

#### `POST /api/v1/ai/epicrisis`
Generate medical report from notes.

#### `POST /api/v1/ai/translate`
Translate medical text (default target: Czech).

#### `POST /api/v1/ai/transcribe`
Transcribe audio file (e.g., patient visit recording).


## 💉 SÚKL Data Pipeline

The project includes a robust ETL pipeline for processing data from SÚKL (Státní ústav pro kontrolu léčiv).
It handles:
1. **DLP (Léčiva)**: Monthly & eRecept updates.
2. **Pricing (Ceny)**: Current prices & Historical archives (LEK-13).
3. **Documents**: SPC/PIL links.
4. **Vectors**: Semantic embeddings for search.

**Important**: Run the pipeline from the **project root folder** (one level up from `backend`) to ensure correct module resolution.

```bash
# From v0-benjamin root
python -m backend.pipeline.run_pipeline [flags]
```

### Available Commands

- **Full Pipeline** (Download, Parse, Import, Embed):
  ```bash
  python -m backend.pipeline.run_pipeline --drugs --pricing --documents --with-embeddings
  ```

- **Individual Steps**:
  ```bash
  # 1. Download raw CSVs from SÚKL
  python -m backend.pipeline.run_pipeline --download

  # 2. Process Drugs (DLP) + Embeddings
  python -m backend.pipeline.run_pipeline --drugs --with-embeddings

  # 3. Process Pricing (Current & History)
  python -m backend.pipeline.run_pipeline --pricing

  # 4. Process SPC/PIL Documents
  python -m backend.pipeline.run_pipeline --documents
  ```

- **Options**:
  - `--limit <number>`: Process only N items (useful for testing)
  - `--with-embeddings`: Generate OpenAI vectors for drugs (Costs money!)
  - `--dry-run`: Run without writing to database

## 🧪 Testing

Run tests using `pytest`:

```bash
# From backend directory
pytest
```
