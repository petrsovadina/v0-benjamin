# Phase 01: Foundation & Working Prototype

Tato fáze validuje základní hypotézu "Czech Medical Google" — AI asistent, který odpovídá na klinické dotazy s citacemi. Na konci fáze bude fungovat end-to-end flow: uživatel položí dotaz → backend zpracuje s Claude → odpověď s citacemi se zobrazí ve frontendu.

## Tasks

- [x] Verify and fix existing backend startup:
  - Run `uvicorn backend.main:app --reload --port 8000` and verify it starts
  - Check for import errors and fix any broken dependencies
  - Ensure `/docs` endpoint returns Swagger UI
  - Test basic health endpoint returns 200 OK

- [x] Create ClinicalState schema for LangGraph workflow:
  - Create `backend/app/core/schemas/clinical_state.py`
  - Define TypedDict `ClinicalState` with fields:
    - `messages: Annotated[list, add_messages]` for conversation history
    - `classification: Optional[QueryClassification]` for intent detection
    - `drug_results: Optional[RetrievalResult]` for SÚKL data
    - `pubmed_results: Optional[RetrievalResult]` for literature
    - `all_citations: list[Citation]` for aggregated citations
    - `overall_confidence: float` for quality scoring
    - `response_complete: bool` for workflow state
  - Define `Citation` Pydantic model with: source_type, identifier, title, url, relevance_score, snippet
  - Define `RetrievalResult` Pydantic model with: content, citations, confidence, agent_source
  - Define `QueryClassification` Pydantic model with 8 intent types

- [ ] Implement basic Query Classifier node:
  - Create `backend/app/core/nodes/query_classifier.py`
  - Use Claude with structured output to classify into 8 intents:
    - drug_info, drug_interaction, guideline_lookup, clinical_question
    - pricing_coverage, urgent_diagnostic, compound_query, general
  - Extract entities (drugs, conditions, ATC codes) from query
  - Determine urgency level (routine, priority, urgent)
  - Return classification with primary_intent and secondary_intents

- [ ] Implement PubMed retrieval tool for smoke test:
  - Create `backend/tools/pubmed_tool.py`
  - Implement `search_pubmed(query, max_results=5)` function
  - Use NCBI E-utilities API (esearch + efetch)
  - Parse XML response to extract: PMID, title, authors, journal, year, abstract
  - Return list of `PubMedArticle` results with proper Citation objects

- [ ] Create simple single-agent LangGraph workflow:
  - Update `backend/agent_graph.py` to use new ClinicalState schema
  - Define nodes: `classify_query` → `retrieve_pubmed` → `generate_response`
  - Implement `generate_response` node that:
    - Takes PubMed results and original query
    - Calls Claude to synthesize answer in Czech
    - Generates inline citations [1], [2], [3] format
    - Appends reference list at the end
  - Compile graph with MemorySaver checkpointer

- [ ] Create FastAPI endpoint for clinical queries:
  - Create or update `backend/app/api/v1/endpoints/query.py`
  - Implement `POST /api/v1/query` endpoint
  - Request body: `{"query": str, "thread_id": Optional[str]}`
  - Response: `{"response": str, "citations": list[dict], "confidence": float}`
  - Add proper error handling and timeout (30s max)
  - Enable streaming response for real-time output

- [ ] Update frontend chat interface to use new endpoint:
  - Verify `components/dashboard/chat-interface.tsx` sends to correct endpoint
  - Ensure citations are parsed and displayed via `chat-citations.tsx`
  - Add loading state during API call
  - Display confidence score in UI (optional badge)
  - Test full flow: type query → see answer with citations

- [ ] Write smoke test script for validation:
  - Create `backend/scripts/smoke_test.py`
  - Test 5 representative clinical queries:
    - Drug info: "Jaké jsou kontraindikace metforminu?"
    - Clinical question: "Diferenciální diagnostika bolesti na hrudi"
    - Guidelines: "Guidelines pro léčbu hypertenze"
    - Pricing: "Je Xarelto hrazen pojišťovnou?"
    - Urgent: "Pacient s ST elevací"
  - Assert response contains at least 1 citation
  - Assert response latency < 10 seconds
  - Assert response is in Czech
  - Print pass/fail summary

- [ ] Run full integration test and document results:
  - Start backend: `uvicorn backend.main:app --reload`
  - Start frontend: `pnpm dev`
  - Login to dashboard and navigate to chat
  - Test each of the 5 smoke test queries manually
  - Verify citations are clickable and lead to PubMed
  - Document any issues in `Auto Run Docs/Initiation/Working/phase-01-results.md`
  - Capture response times and quality observations
