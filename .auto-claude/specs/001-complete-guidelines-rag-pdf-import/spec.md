# Complete Guidelines RAG PDF Import

## Overview
# Complete Guidelines RAG PDF Import

Implement the full PDF import pipeline for Czech medical guidelines, including document parsing, chunking, embedding generation, and storage in the vector database. Enable reliable retrieval of guideline content for AI responses.

## Rationale
Czech doctors need access to local clinical guidelines - this is a critical gap that general AI tools (ChatGPT, Claude) cannot address. Evidence-based recommendations require proper guideline citations.

## User Stories
- As an admin, I want to upload Czech medical guideline PDFs so that doctors can search this content
- As a doctor, I want to see which guideline a recommendation comes from so that I can verify the source

## Acceptance Criteria
- [ ] PDF documents can be uploaded via admin endpoint
- [ ] Documents are parsed, chunked, and embedded in vector database
- [ ] Chunks maintain source metadata (document name, page number)
- [ ] At least 3 different guideline formats are supported
- [ ] Import progress and errors are properly logged


## Workflow Type

**Type**: feature

**Rationale**: This is a new feature implementation that adds complete RAG (Retrieval-Augmented Generation) capabilities for medical guidelines. While a basic upload endpoint exists, this task requires building out the full pipeline, fixing schema mismatches, implementing retrieval logic, and ensuring production-grade reliability with multi-format support and comprehensive error handling.

## Task Scope

### Services Involved
- **Backend (FastAPI)** (primary) - PDF upload endpoint, processing pipeline, vector storage, retrieval API
- **Supabase** (integration) - Vector database storage with pgvector extension, metadata persistence

### This Task Will:
- [x] Verify and enhance the existing PDF upload endpoint at `/api/v1/admin/upload/guideline`
- [x] Fix schema mismatch between chunk storage and guidelines table structure
- [x] Implement proper metadata tracking (document name, page number) throughout the pipeline
- [x] Test and validate support for at least 3 different Czech guideline PDF formats
- [x] Add comprehensive logging for import progress and error handling
- [x] Implement guideline retrieval in the RAG graph (currently TODO at line 74 of `backend/app/core/graph.py`)
- [x] Add endpoint to query guidelines with proper source citations
- [x] Create unit and integration tests for the pipeline

### Out of Scope:
- Frontend UI for admin PDF upload (will be implemented in future task)
- User authentication and authorization (already exists)
- Real-time processing status updates (background tasks are sufficient)
- OCR for scanned PDFs (only text-based PDFs in scope)
- Automatic guideline discovery/scraping from external sources

## Service Context

### Backend Service (FastAPI)

**Tech Stack:**
- Language: Python 3.13
- Framework: FastAPI
- Key libraries: langchain-community, langchain-text-splitters, langchain-openai, supabase, openai
- Key directories:
  - `backend/app/api/v1/endpoints/` - API endpoints
  - `backend/data_processing/loaders/` - Document loaders
  - `backend/services/` - Shared services (logger, search)
  - `backend/data/guidelines_pdfs/` - PDF upload storage

**Entry Point:** `backend/app/main.py`

**How to Run:**
```bash
# From project root
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn app.main:app --reload --port 8000
```

**Port:** 8000

**Environment Variables Required:**
```
SUPABASE_URL=https://higziqzcjmtmkzxbbzik.supabase.co
SUPABASE_KEY=<your-key>
OPENAI_API_KEY=<your-key>
ANTHROPIC_API_KEY=<your-key>
PUBMED_EMAIL=<your-email>
```

### Database Service (Supabase/PostgreSQL)

**Tech Stack:**
- Database: PostgreSQL with pgvector extension
- Vector dimensions: 1536 (OpenAI text-embedding-3-small)
- Index type: HNSW with cosine similarity

**Key Tables:**
- `guidelines` - Stores guideline chunks with embeddings (see migration 008_guidelines.sql)
- `app_errors` - Error logging table

**Migration File:** `supabase/migrations/008_guidelines.sql`

## Files to Modify

| File | Service | What to Change |
|------|---------|---------------|
| `backend/data_processing/loaders/guidelines_loader.py` | Backend | Fix schema mismatch - align chunk storage with guidelines table columns; improve metadata extraction |
| `backend/app/api/v1/endpoints/admin.py` | Backend | Add validation, improve error handling, add status endpoint for tracking uploads |
| `backend/app/core/graph.py` | Backend | Implement guideline retrieval node (replace TODO at line 74) |
| `backend/app/services/search_service.py` | Backend | Add `search_guidelines()` method for vector similarity search |
| `supabase/migrations/008_guidelines.sql` | Database | **CRITICAL CHANGES**: (1) Add `content TEXT NOT NULL` column for chunk text, (2) Add `metadata JSONB DEFAULT '{}'` column for page/source tracking, (3) Add `match_guidelines()` RPC function for vector search (current schema has only `full_content` - see migration 006 documents table for column patterns) |

## Files to Reference

These files show patterns to follow:

| File | Pattern to Copy |
|------|----------------|
| `backend/data_processing/loaders/guidelines_loader.py` | PDF loading with PyPDFLoader, chunking with RecursiveCharacterTextSplitter, embedding generation |
| `backend/app/api/v1/endpoints/admin.py` | FastAPI file upload with BackgroundTasks, validation patterns |
| `backend/services/logger.py` | StructuredLogger usage for JSON logging with metadata |
| `backend/app/core/graph.py` | LangGraph state management, node implementation patterns |
| `backend/app/api/v1/endpoints/query.py` | Citation formatting, source metadata handling |

## Patterns to Follow

### Pattern 1: Background Task Processing

From `backend/app/api/v1/endpoints/admin.py`:

```python
async def run_ingestion_task():
    """Background task to run the ingestion pipeline."""
    logger.info("Starting background ingestion task...")
    loader = GuidelinesLoader(pdf_dir=UPLOAD_DIR)
    await loader.ingest_pdfs()
    logger.info("Background ingestion task finished.")

@router.post("/upload/guideline")
async def upload_guideline(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    # Save file first
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Then trigger background processing
    background_tasks.add_task(run_ingestion_task)
```

**Key Points:**
- Always save the uploaded file to disk BEFORE triggering background task (file stream closes)
- Use FastAPI's BackgroundTasks for long-running operations
- Return immediately with status "uploaded" and "indexing started in background"

### Pattern 2: Chunking with Metadata Preservation

From `backend/data_processing/loaders/guidelines_loader.py`:

```python
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Load PDF (creates one Document per page)
loader = PyPDFLoader(file_path)
docs = loader.load()

# Split with context preservation
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,  # 20% overlap for context
    separators=["\n\n", "\n", " ", ""]
)
chunks = text_splitter.split_documents(docs)

# Preserve metadata
for chunk in chunks:
    metadata = {
        "source": filename,
        "page": chunk.metadata.get("page", 0),  # 0-indexed
        **chunk.metadata  # Preserve all original metadata
    }
```

**Key Points:**
- PyPDFLoader creates one Document per page with 0-indexed page numbers
- RecursiveCharacterTextSplitter preserves Document metadata through splits
- 20% chunk overlap (200 chars for 1000 char chunks) maintains context at boundaries
- Always include source filename and page number in metadata

### Pattern 3: Structured Logging

From `backend/services/logger.py`:

```python
from backend.services.logger import get_logger

logger = get_logger(__name__)

# Info logging with metadata
logger.info(f"Processing {filename}...",
    file_size=os.path.getsize(file_path),
    total_chunks=len(chunks)
)

# Error logging with exception
try:
    # ... processing
except Exception as e:
    logger.error(f"Failed to process {filename}",
        error=e,
        filename=filename,
        step="embedding_generation"
    )
```

**Key Points:**
- Use `get_logger(__name__)` for module-scoped logging
- Pass structured metadata as kwargs for JSON output
- Error logs are automatically sent to Supabase `app_errors` table
- Always include context (filename, step, etc.) in error logs

### Pattern 4: Vector Similarity Search

Expected pattern for `search_service.py`:

```python
from langchain_openai import OpenAIEmbeddings
from backend.app.core.config import settings

async def search_guidelines(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
    """Search guidelines using vector similarity."""
    # 1. Generate query embedding
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        api_key=settings.OPENAI_API_KEY
    )
    embedding = embeddings.embed_query(query)

    # 2. Search with RPC function (cosine similarity)
    response = self.supabase.rpc('match_guidelines', {
        'query_embedding': embedding,
        'match_threshold': 0.7,
        'match_count': limit
    }).execute()

    # 3. Format results with metadata
    return [{
        "id": item["id"],
        "content": item["content"],
        "title": item["title"],
        "page": item["metadata"].get("page"),
        "similarity": item["similarity"]
    } for item in response.data]
```

**Key Points:**
- Use RPC function for vector search (Supabase pattern)
- Include similarity threshold (0.7-0.8 typical for medical content)
- Return structured data with source metadata for citations

**IMPORTANT - RPC Function Required:**
The `match_guidelines` RPC function must be created in the database migration. Add this SQL to `008_guidelines.sql`:

```sql
-- RPC function for vector similarity search on guidelines
CREATE OR REPLACE FUNCTION match_guidelines(
    query_embedding vector(1536),
    match_threshold float,
    match_count int
)
RETURNS TABLE (
    id uuid,
    title text,
    content text,
    metadata jsonb,
    similarity float
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        guidelines.id,
        guidelines.title,
        guidelines.content,
        guidelines.metadata,
        1 - (guidelines.embedding <=> query_embedding) AS similarity
    FROM guidelines
    WHERE 1 - (guidelines.embedding <=> query_embedding) > match_threshold
    ORDER BY guidelines.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;
```

## Requirements

### Functional Requirements

1. **PDF Upload via Admin Endpoint**
   - Description: Admin users can upload Czech medical guideline PDFs through POST `/api/v1/admin/upload/guideline`
   - Acceptance:
     - Endpoint accepts PDF files only (rejects other formats with 400 error)
     - File is saved to `backend/data/guidelines_pdfs/` directory
     - Returns immediately with status "uploaded" and background processing initiated
     - Logs upload event with filename and file size

2. **Document Parsing and Chunking**
   - Description: PDFs are parsed into pages, then chunked into searchable segments
   - Acceptance:
     - Uses PyPDFLoader to extract text per page
     - Chunks text with RecursiveCharacterTextSplitter (1000 chars, 200 overlap)
     - Each chunk preserves source metadata (filename, page number)
     - Logs chunk count per document

3. **Embedding Generation**
   - Description: Text chunks are converted to 1536-dimensional vectors using OpenAI's text-embedding-3-small model
   - Acceptance:
     - Embeddings generated in batches of 50 to avoid rate limits
     - Each chunk has corresponding embedding vector
     - Errors during embedding generation are logged and don't crash the pipeline
     - Retry logic for transient API failures

4. **Vector Database Storage**
   - Description: Chunks with embeddings are stored in Supabase `guidelines` table
   - Acceptance:
     - Each chunk stored as separate row with vector embedding
     - Database columns populated: `title` (filename), `organization`, `publication_year`, `content` (chunk text), `embedding` (1536-dim vector)
     - Metadata JSONB column contains: `{"source": filename, "page": page_number, ...}` for citation tracking
     - Duplicate prevention: delete existing chunks for filename before inserting new ones (idempotency via metadata->>source filter)
     - HNSW index automatically used for similarity search

5. **Guideline Retrieval in RAG Pipeline**
   - Description: When query type is "guidelines", retrieve relevant chunks from vector database
   - Acceptance:
     - Graph classifier routes guideline queries to `retrieve_guidelines_node`
     - Vector similarity search returns top 5 most relevant chunks
     - Results include source metadata (title, page number) for citations
     - Citations displayed to user in format: "Source: [title], page [X]"

6. **Multi-Format PDF Support**
   - Description: System handles at least 3 different Czech guideline PDF formats
   - Acceptance:
     - Test with standard text PDFs (e.g., MS Word → PDF exports)
     - Test with PDFs containing tables (e.g., dosage tables in guidelines)
     - Test with multi-column layouts (e.g., journal-style guidelines)
     - Document any format-specific handling or limitations

7. **Comprehensive Error Handling and Logging**
   - Description: All pipeline stages log progress and handle errors gracefully
   - Acceptance:
     - Upload errors logged with file details
     - Parsing errors logged with page number
     - Embedding errors logged with retry count
     - Database errors logged with SQL details
     - All errors written to both stdout (JSON) and Supabase `app_errors` table
     - Pipeline continues processing other files even if one fails

### Edge Cases

1. **Duplicate Uploads** - If same PDF uploaded twice, delete old chunks and replace with new ones (idempotency)
2. **Empty PDFs** - If PDF has no text (scanned images), log warning and skip (return 0 chunks)
3. **Very Large PDFs** - If PDF >500 pages, process in smaller batches to avoid memory issues
4. **Malformed PDFs** - If PyPDFLoader fails, try fallback parser (e.g., pdfplumber) before failing
5. **Non-Czech Content** - Mark `is_czech` flag based on language detection (currently defaults to True)
6. **Missing Metadata** - If PDF lacks metadata (title, author), use filename as title and "Unknown" for organization

## Implementation Notes

### DO
- Follow the existing GuidelinesLoader pattern in `backend/data_processing/loaders/guidelines_loader.py`
- Use StructuredLogger from `backend/services/logger.py` for all logging
- Reuse OpenAI embeddings configuration from `backend/app/core/config.py`
- Process embeddings in batches of 50 to respect OpenAI rate limits
- Include source filename and page number in every chunk's metadata JSONB field: `{"source": "filename.pdf", "page": 0}`
- Delete existing chunks for a file before inserting new ones (idempotency via `metadata->>source` filter)
- Use FastAPI's BackgroundTasks for long-running PDF processing
- Add `content` and `metadata` columns to guidelines table (follow documents table pattern from migration 006)
- Create `match_guidelines()` RPC function in migration for vector similarity search (SQL provided in Pattern 4)
- Store chunks in the `guidelines` table with proper schema alignment
- Implement retry logic for transient API failures (embeddings, database)

### DON'T
- Create new embedding models - use existing `OpenAIEmbeddings(model="text-embedding-3-small")`
- Block the upload endpoint waiting for processing to complete
- Store the entire PDF in the database - only store chunks
- Skip metadata tracking - citations depend on source attribution
- Use generic error messages - include context (filename, step, error details)
- Create a new logger implementation - use `get_logger(__name__)`
- Modify the `guidelines` table schema without a migration file
- Process all chunks in a single database transaction - use batches

## Development Environment

### Start Services

```bash
# Terminal 1: Start Frontend (Next.js)
npm run dev
# Runs on http://localhost:3000

# Terminal 2: Start Backend (FastAPI)
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
# Runs on http://localhost:8000

# Terminal 3: Supabase Local (optional for local testing)
npx supabase start
# Vector DB available on local PostgreSQL
```

### Service URLs
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs (Swagger UI)
- Supabase Studio: http://localhost:54323 (if running local)

### Required Environment Variables

Create `backend/.env`:
```bash
SUPABASE_URL=https://higziqzcjmtmkzxbbzik.supabase.co
SUPABASE_KEY=<your-service-role-key>
OPENAI_API_KEY=<your-openai-key>
ANTHROPIC_API_KEY=<your-anthropic-key>
PUBMED_EMAIL=<your-email>
```

### Test Data Preparation

Place test Czech guideline PDFs in:
- `backend/data/guidelines_pdfs/` (upload destination)
- `backend/tests/fixtures/` (test fixtures with at least 3 different formats)

## Success Criteria

The task is complete when:

1. [x] Admin can upload PDF via POST `/api/v1/admin/upload/guideline` with proper validation
2. [x] PDF is parsed, chunked, embedded, and stored in `guidelines` table
3. [x] Source metadata (filename, page number) preserved throughout pipeline
4. [x] At least 3 different Czech guideline formats successfully processed
5. [x] Guideline retrieval implemented in graph.py (TODO at line 74 resolved)
6. [x] Queries classified as "guidelines" retrieve relevant chunks with citations
7. [x] All processing stages logged with structured JSON output
8. [x] Errors handled gracefully without crashing the pipeline
9. [x] No console errors when uploading and querying guidelines
10. [x] Existing tests still pass
11. [x] New unit tests added for GuidelinesLoader and search_guidelines()
12. [x] Integration test validates end-to-end flow: upload → process → retrieve

## QA Acceptance Criteria

**CRITICAL**: These criteria must be verified by the QA Agent before sign-off.

### Unit Tests

| Test | File | What to Verify |
|------|------|----------------|
| `test_guidelines_loader_chunk_creation` | `backend/tests/test_guidelines_loader.py` | Verify chunks created with correct metadata (source, page) |
| `test_guidelines_loader_embedding_generation` | `backend/tests/test_guidelines_loader.py` | Verify embeddings are 1536-dimensional vectors |
| `test_guidelines_loader_batch_processing` | `backend/tests/test_guidelines_loader.py` | Verify batch processing (50 chunks per batch) |
| `test_search_guidelines_vector_similarity` | `backend/tests/test_search_service.py` | Verify search returns relevant results with similarity scores |
| `test_upload_endpoint_pdf_validation` | `backend/tests/test_admin_endpoints.py` | Verify only PDFs accepted, other formats rejected with 400 |

### Integration Tests

| Test | Services | What to Verify |
|------|----------|----------------|
| `test_end_to_end_guideline_upload` | Backend ↔ Supabase | Upload PDF → verify chunks in database with embeddings |
| `test_guideline_retrieval_in_graph` | Backend ↔ Supabase | Query with "guidelines" type → verify relevant chunks retrieved |
| `test_citation_metadata_preservation` | Backend ↔ Supabase | Upload → query → verify citations include source + page number |

### End-to-End Tests

| Flow | Steps | Expected Outcome |
|------|-------|------------------|
| Admin Upload & Doctor Query | 1. POST PDF to `/api/v1/admin/upload/guideline` 2. Wait for background processing (check logs) 3. POST query to `/api/v1/query/` with guideline question 4. Verify response includes citations | Citations format: "Source: [filename], page [X]"; Response includes relevant guideline content |
| Multi-Format Support | 1. Upload 3 different PDF formats 2. Verify all processed successfully 3. Query content from each format | All 3 formats stored in database; Queries return content from all formats |
| Error Recovery | 1. Upload invalid/corrupted PDF 2. Verify error logged 3. Verify pipeline continues 4. Upload valid PDF 5. Verify success | Error logged to `app_errors` table; Valid upload processes correctly |

### Database Verification

| Check | Query/Command | Expected |
|-------|---------------|----------|
| Guidelines table populated | `SELECT COUNT(*) FROM guidelines WHERE title = '[test-filename]'` | Count > 0 (chunks exist) |
| Embeddings generated | `SELECT COUNT(*) FROM guidelines WHERE embedding IS NOT NULL` | Count matches total chunks |
| HNSW index exists | `SELECT indexname FROM pg_indexes WHERE tablename = 'guidelines' AND indexname = 'idx_guidelines_embedding'` | Index exists |
| Metadata preserved | `SELECT metadata FROM guidelines WHERE title = '[test-filename]' LIMIT 1` | metadata JSONB contains "source" and "page" keys |

### API Verification

| Endpoint | Method | Test Case | Expected Response |
|----------|--------|-----------|-------------------|
| `/api/v1/admin/upload/guideline` | POST | Upload valid PDF | 200, {"status": "uploaded", "message": "...background..."} |
| `/api/v1/admin/upload/guideline` | POST | Upload .docx file | 400, {"detail": "Only PDF files are supported."} |
| `/api/v1/query/` | POST | Query: "Jaké jsou doporučení pro léčbu hypertenze?" | 200, includes citations with "guidelines" source_type |

### Logging Verification

| Log Event | Expected Log Entry | Where to Check |
|-----------|-------------------|----------------|
| Upload started | `{"level": "INFO", "message": "File saved to ...", "filename": "..."}` | stdout (JSON) |
| Processing started | `{"level": "INFO", "message": "Processing ...", "total_chunks": N}` | stdout (JSON) |
| Error handling | `{"level": "ERROR", "message": "Failed to process ...", "error_details": "..."}` | stdout + `app_errors` table |
| Processing complete | `{"level": "INFO", "message": "Ingestion complete. Total chunks stored: N"}` | stdout (JSON) |

### QA Sign-off Requirements

- [x] All unit tests pass (`pytest backend/tests/test_guidelines_loader.py -v`)
- [x] All integration tests pass
- [x] All E2E tests pass (upload → process → query → citations verified)
- [x] Database verification complete (chunks stored, embeddings exist, metadata correct)
- [x] API verification complete (upload endpoint validated, query endpoint returns citations)
- [x] Logging verification complete (all events logged with proper structure)
- [x] No regressions in existing functionality (all existing tests pass)
- [x] Code follows established patterns (LangChain, StructuredLogger, FastAPI BackgroundTasks)
- [x] No security vulnerabilities introduced (file validation, path traversal prevention)
- [x] Multi-format support validated (3+ different PDF formats tested)
- [x] Performance acceptable (embedding generation <5 min for 100-page PDF)
- [x] Error handling tested (corrupt PDF, network failures, database errors)
