# Specification: Upgrade LangChain Dependencies to 0.3.x+ for Deep Agents Support

## Overview

This task upgrades the entire LangChain ecosystem from version 0.1.x to 0.3.x+ across the Python backend to enable Deep Agents functionality in the existing RAG (Retrieval-Augmented Generation) workflow. The upgrade spans 7 core packages and requires maintaining complete backward compatibility with zero test failures and no deprecation warnings.

## Workflow Type

**Type**: Feature

**Rationale**: This is a dependency upgrade that enables new capabilities (Deep Agents) rather than fixing bugs or refactoring existing code. The upgrade adds new functionality while preserving existing behavior, which classifies it as a feature enhancement.

## Task Scope

### Services Involved
- **backend** (primary) - Python/FastAPI service containing all LangChain integrations for RAG workflow, agent graphs, and LLM interactions

### This Task Will:
- [ ] Upgrade all 7 LangChain-related packages from 0.1.x/0.0.x to 0.3.x+
- [ ] Verify compatibility of `@tool` decorator, message classes, and structured output APIs
- [ ] Validate StateGraph, workflow compilation, and checkpointing patterns
- [ ] Test RAG pipeline (PyPDFLoader → text splitting → embeddings)
- [ ] Ensure Deep Agents functionality is accessible in LangGraph 0.3.x
- [ ] Eliminate all deprecation warnings from upgraded packages
- [ ] Verify all existing tests pass without modification

### Out of Scope:
- Refactoring existing agent graph implementations
- Adding new Deep Agents features (only enabling capability)
- Modifying RAG workflow logic or retrieval strategies
- Updating frontend Next.js dependencies
- Database schema changes

## Service Context

### Backend Service

**Tech Stack:**
- Language: Python 3.13
- Framework: FastAPI
- LLM Integration: LangChain 0.1.x → 0.3.x
- Agent Framework: LangGraph 0.2.0 → 0.3.0
- Key directories: `backend/`, `backend/app/`, `backend/data_processing/`

**Entry Point:** `backend/main.py` and `backend/app/main.py`

**How to Run:**
```bash
# From project root
cd backend
source venv/bin/activate  # or equivalent for your OS
uvicorn main:app --reload --port 8000
```

**Port:** 8000 (FastAPI backend)

**Critical Environment Variables:**
- `ANTHROPIC_API_KEY` - Required for Claude model integration (langchain-anthropic)
- `OPENAI_API_KEY` - Required for embeddings in RAG pipeline (langchain-openai)

## Files to Modify

| File | Service | What to Change |
|------|---------|---------------|
| `backend/requirements.txt` | backend | Update all LangChain package versions to ≥0.3.0 |
| `backend/pyproject.toml` (if exists) | backend | Sync LangChain version constraints to ≥0.3.0 |
| `backend/agent_graph.py` | backend | Verify `@tool` decorator and StateGraph API compatibility |
| `backend/epicrisis_graph.py` | backend | Verify graph compilation and message handling |
| `backend/translator_graph.py` | backend | Verify tool binding and async invocation patterns |
| `backend/app/core/graph.py` | backend | Validate conditional edges and interrupts (LangGraph 0.3 changes) |
| `backend/app/core/llm.py` | backend | Verify `ChatAnthropic` initialization and `with_structured_output()` |
| `backend/app/core/state.py` | backend | Validate `AgentState` definition and message classes |
| `backend/data_processing/loaders/guidelines_loader.py` | backend | Verify PyPDFLoader API (0.0.10→0.3.0 major jump) |

## Files to Reference

These files show patterns to follow:

| File | Pattern to Copy |
|------|----------------|
| `backend/agent_graph.py` | StateGraph workflow pattern, node/edge definitions |
| `backend/app/core/llm.py` | ChatAnthropic model initialization with environment variables |
| `backend/app/core/state.py` | Message class usage (HumanMessage, AIMessage, SystemMessage) |
| `backend/data_processing/loaders/guidelines_loader.py` | RAG pipeline: PyPDFLoader → RecursiveCharacterTextSplitter → embeddings |

## Patterns to Follow

### LangChain-Core Tool Definition

From research context - used in `agent_graph.py`:

```python
from langchain_core.tools import tool

@tool
def my_tool_function(arg: str) -> str:
    """Tool description for the LLM"""
    return result
```

**Key Points:**
- Verify `@tool` decorator signature unchanged in 0.3.x
- Tool descriptions must remain compatible with LLM tool binding

### LangChain-Anthropic Model Initialization

From research context - pattern in `app/core/llm.py`:

```python
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(
    model='claude-3-haiku-20240307',
    # environment: ANTHROPIC_API_KEY is auto-detected
)

# Tool binding pattern
llm_with_tools = llm.bind_tools([tool1, tool2])

# Structured output pattern
structured_llm = llm.with_structured_output(OutputSchema)
```

**Key Points:**
- Verify `bind_tools()` method signature in 0.3.x
- Validate `with_structured_output()` compatibility with schema definitions
- Ensure async methods (`ainvoke`) remain functional

### LangGraph StateGraph Pattern

From research context - pattern in graph files:

```python
from langgraph.graph import StateGraph
from langgraph.checkpoint.memory import MemorySaver

# Define workflow
workflow = StateGraph(AgentState)
workflow.add_node("node_name", node_function)
workflow.add_edge("node_a", "node_b")
workflow.add_conditional_edges("router", routing_function)

# Compile with checkpointing
checkpointer = MemorySaver()
graph = workflow.compile(checkpointer=checkpointer)
```

**Key Points:**
- LangGraph 0.2→0.3 may have breaking changes in StateGraph API
- Conditional edges and interrupts need verification
- Checkpointing with MemorySaver must remain functional

### RAG Pipeline Pattern

From `backend/data_processing/loaders/guidelines_loader.py`:

```python
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings

# Load PDF documents
loader = PyPDFLoader(file_path)
documents = loader.load()

# Split text into chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
chunks = splitter.split_documents(documents)

# Generate embeddings
embeddings = OpenAIEmbeddings()
```

**Key Points:**
- PyPDFLoader API changes (0.0.10→0.3.0 major version jump) are critical
- Text splitter parameters must remain compatible
- Embedding generation for vector store must be unchanged

## Requirements

### Functional Requirements

1. **Package Version Upgrades**
   - Description: All 7 LangChain packages upgraded to ≥0.3.0 with coordinated versions
   - Acceptance: `pip list | grep langchain` shows all packages at 0.3.x or higher

2. **Backward Compatibility**
   - Description: Existing RAG workflow, agent graphs, and LLM interactions function identically
   - Acceptance: All API endpoints return same responses for identical inputs pre/post upgrade

3. **Test Suite Pass Rate**
   - Description: 100% of existing tests pass without modification
   - Acceptance: `pytest backend/` exits with 0 failures

4. **Deep Agents Enablement**
   - Description: LangGraph 0.3.x features are accessible (not necessarily implemented)
   - Acceptance: `import langgraph` shows version ≥0.3.0, Deep Agents features importable

5. **Zero Deprecation Warnings**
   - Description: No deprecation warnings appear in logs or test output
   - Acceptance: Run full test suite with warnings enabled, grep output for "Deprecation"

### Edge Cases

1. **Transitive Dependency Conflicts** - Use `pip install --upgrade` with all packages listed together to ensure dependency resolver finds compatible versions
2. **Environment Variable Detection** - Verify ANTHROPIC_API_KEY and OPENAI_API_KEY are detected post-upgrade
3. **Async/Await Compatibility** - Test async invocation methods (`ainvoke`, `astream`) in FastAPI routes
4. **Message Serialization** - Verify message history serialization in checkpointing hasn't changed format

## Implementation Notes

### DO
- **Upgrade all packages together**: Run single `pip install` command with all 7 packages to avoid version conflicts
- **Read migration guides**: Check LangChain 0.3.x migration documentation before testing
- **Test in isolation**: Create separate venv to test upgrade before modifying main environment
- **Verify imports first**: Test all imports succeed before running full application
- **Check RAG pipeline first**: PyPDFLoader is critical path - verify immediately after upgrade
- **Run existing test suite**: Execute `test_multiformat_pdf_support.py` and all graph-related tests

### DON'T
- **Don't upgrade packages one-by-one**: This will cause dependency conflicts
- **Don't skip testing tool binding**: `bind_tools()` signature may have changed
- **Don't ignore warnings**: Even if tests pass, deprecation warnings indicate future breakage
- **Don't modify code preemptively**: Only change code if upgrade causes actual failures
- **Don't skip async testing**: FastAPI routes use async patterns extensively

## Development Environment

### Start Services

```bash
# Backend (FastAPI + LangChain)
cd backend
source venv/bin/activate
pip install --upgrade langchain>=0.3.0 langchain-core>=0.3.0 langchain-community>=0.3.0 \
  langchain-anthropic>=0.3.0 langchain-openai>=0.3.0 langchain-text-splitters>=0.3.0 \
  langgraph>=0.3.0
uvicorn main:app --reload --port 8000

# Frontend (Next.js) - not modified but needed for E2E testing
npm run dev  # Runs on port 3000
```

### Service URLs
- Backend API: http://localhost:8000
- API Health Check: http://localhost:8000/health
- Frontend: http://localhost:3000
- Frontend Backend Proxy: http://localhost:3000 → http://localhost:8000 (via NEXT_PUBLIC_API_URL)

### Required Environment Variables
- `ANTHROPIC_API_KEY`: API key for Claude models (langchain-anthropic)
- `OPENAI_API_KEY`: API key for embeddings and OpenAI models (langchain-openai)
- `NEXT_PUBLIC_API_URL`: Frontend → Backend connection (default: http://localhost:8000)

## Success Criteria

The task is complete when:

1. [ ] All 7 LangChain packages at version ≥0.3.0 (`langchain`, `langchain-core`, `langchain-community`, `langchain-anthropic`, `langchain-openai`, `langchain-text-splitters`, `langgraph`)
2. [ ] `pytest backend/` passes with 0 failures
3. [ ] No deprecation warnings in test output or application logs
4. [ ] Backend starts successfully with `uvicorn main:app --reload`
5. [ ] RAG workflow endpoints (`/query`, `/stream`) return valid responses
6. [ ] Agent endpoints (`/epicrisis`, `/translate`) function correctly
7. [ ] Deep Agents features importable from `langgraph` package
8. [ ] All graph nodes, edges, and checkpointing functional
9. [ ] Tool definitions and binding work as expected
10. [ ] Message classes (HumanMessage, AIMessage, etc.) serialize correctly

## QA Acceptance Criteria

**CRITICAL**: These criteria must be verified by the QA Agent before sign-off.

### Unit Tests
| Test | File | What to Verify |
|------|------|----------------|
| PDF Loading | `test_multiformat_pdf_support.py` | PyPDFLoader correctly loads and parses PDF documents |
| Tool Definitions | Graph files (`agent_graph.py`, etc.) | `@tool` decorator creates valid tool instances |
| Message Handling | `backend/app/core/state.py` | Message classes instantiate and serialize correctly |
| LLM Initialization | `backend/app/core/llm.py` | ChatAnthropic initializes with correct parameters |

### Integration Tests
| Test | Services | What to Verify |
|------|----------|----------------|
| RAG Query Flow | backend ↔ OpenAI Embeddings | PDF → chunks → embeddings → vector search works end-to-end |
| Agent Graph Execution | backend (LangGraph) | StateGraph compiles, executes nodes, manages state correctly |
| Tool Binding | backend ↔ Anthropic | Tools bind to LLM, Claude can invoke them correctly |
| Async Invocation | FastAPI ↔ LangChain | `ainvoke()` and `astream()` methods work in async routes |

### End-to-End Tests
| Flow | Steps | Expected Outcome |
|------|-------|------------------|
| RAG Query | 1. POST to `/query` with question 2. Backend retrieves context 3. Claude generates answer | Valid JSON response with answer and sources |
| Epicrisis Generation | 1. POST to `/epicrisis` with patient data 2. Graph executes epicrisis workflow | Structured medical report returned |
| Translation | 1. POST to `/translate` with text 2. Translation graph executes | Translated text in target language |
| Streaming Response | 1. POST to `/stream` endpoint 2. Receive SSE stream | Progressive token-by-token response |

### API Verification
| Endpoint | URL | Checks |
|----------|-----|--------|
| Health Check | `http://localhost:8000/health` | Returns 200, JSON with status |
| RAG Query | `http://localhost:8000/query` | POST returns answer with retrieved context |
| Epicrisis | `http://localhost:8000/epicrisis` | POST returns structured medical report |
| Translate | `http://localhost:8000/translate` | POST returns translated text |
| Upload Guideline | `http://localhost:8000/upload/guideline` | POST processes PDF, updates vector store |

### Dependency Verification
| Check | Command | Expected |
|-------|---------|----------|
| LangChain Version | `pip show langchain \| grep Version` | Version: 0.3.x or higher |
| LangGraph Version | `pip show langgraph \| grep Version` | Version: 0.3.x or higher |
| No Conflicts | `pip check` | No broken dependencies |
| Deep Agents Import | `python -c "from langgraph.prebuilt import ToolNode"` | No import errors |

### QA Sign-off Requirements
- [ ] All unit tests pass (`pytest backend/ -v`)
- [ ] All integration tests pass (RAG pipeline, agent graphs)
- [ ] All E2E tests pass (API endpoints respond correctly)
- [ ] API verification complete (all endpoints functional)
- [ ] Dependency versions verified (all ≥0.3.0)
- [ ] No regressions in existing functionality
- [ ] Code follows established patterns (no API changes needed)
- [ ] No security vulnerabilities introduced (dependency audit clean)
- [ ] Zero deprecation warnings in logs
- [ ] Deep Agents features confirmed accessible
