# Specification: Upgrade LangChain Dependencies to 0.3.x with Deep Agents Support

## Overview

Upgrade all LangChain-related dependencies from 0.1.x to 0.3.x+ versions to enable Deep Agents support while maintaining full backward compatibility with existing RAG workflow. This is a major version upgrade requiring careful validation of breaking changes in graph construction, message handling, tool execution, and checkpoint system. The upgrade affects two critical graph implementations (`graph.py` and `agent_graph.py`) and must ensure zero test failures and no deprecation warnings.

## Workflow Type

**Type**: feature

**Rationale**: This is a dependency upgrade that introduces new capabilities (Deep Agents support) while maintaining existing functionality. It requires structured implementation with multiple validation checkpoints, making it a feature workflow rather than a simple refactor or migration.

## Task Scope

### Services Involved
- **backend** (primary) - Python FastAPI service with LangChain-based RAG workflow

### This Task Will:
- [ ] Update `requirements.txt` with new dependency versions (langchain 0.3.x, langchain-core 0.3.x, langgraph 0.2.x, langgraph-checkpoint 2.0.x)
- [ ] Add new `langgraph-checkpoint` dependency for graph persistence
- [ ] Verify compatibility of `graph.py` with new LangGraph APIs
- [ ] Verify compatibility of `agent_graph.py` with new LangGraph APIs
- [ ] Fix all breaking changes from 0.1.x → 0.3.x migration
- [ ] Update graph compilation to support new checkpoint system
- [ ] Ensure all existing tests pass without modification
- [ ] Eliminate all deprecation warnings

### Out of Scope:
- Adding new Deep Agents features beyond basic support
- Modifying existing RAG workflow behavior or logic
- Upgrading other unrelated dependencies
- Database schema changes or migrations
- Frontend changes

## Service Context

### Backend

**Tech Stack:**
- Language: Python 3.13
- Framework: FastAPI
- Key directories: `backend/app/`, `backend/tests/`, `backend/pipeline/`
- LangChain Framework: StateGraph-based workflow orchestration

**Entry Point:** `backend/main.py`

**How to Run:**
```bash
cd backend
python -m uvicorn main:app --reload --port 8000
```

**Port:** 8000

**Key Dependencies:**
- FastAPI for REST API
- LangChain for LLM orchestration
- LangGraph for workflow state management
- Supabase for vector storage
- Pytest for testing

## Files to Modify

| File | Service | What to Change |
|------|---------|---------------|
| `backend/requirements.txt` | backend | Update langchain (0.1→0.3), langchain-core (0.1→0.3), langgraph (0.1→0.2), add langgraph-checkpoint (2.0+) |
| `backend/app/core/graph.py` | backend | Update imports (START/END constants), add checkpoint to compile(), fix message handling if needed |
| `backend/agent_graph.py` | backend | Update imports, add checkpoint to compile(), verify ToolNode/tools_condition APIs |

## Files to Reference

These files show patterns to follow:

| File | Pattern to Copy |
|------|----------------|
| `backend/app/core/graph.py` | Current StateGraph usage, message handling patterns, async node implementations |
| `backend/agent_graph.py` | Tool decorator usage, ToolNode pattern, tools_condition routing |
| `backend/tests/test_rag_flow_verification.py` | RAG workflow validation patterns |
| `backend/requirements.txt` | Current dependency version format and structure |

## Patterns to Follow

### StateGraph Construction Pattern

From `backend/app/core/graph.py`:

```python
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

class ClinicalState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    # ... other fields

workflow = StateGraph(ClinicalState)
workflow.add_node("classifier", classifier_node)
# ... add more nodes
app = workflow.compile()  # May need checkpointer parameter in 0.3.x
```

**Key Points:**
- TypedDict state with `add_messages` annotation for message accumulation
- Async node functions that return partial state updates
- Graph compiled without explicit checkpointer (needs update)

### Tool-Based Agent Pattern

From `backend/agent_graph.py`:

```python
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import tool

@tool
async def search_pubmed(query: str):
    """Search PubMed for medical articles."""
    # implementation

tools = [search_pubmed, search_sukl_drugs]
workflow.add_node("tools", ToolNode(tools))
workflow.add_conditional_edges("agent", tools_condition)
```

**Key Points:**
- `@tool` decorator for tool definitions with async support
- `ToolNode` wraps tools for graph execution
- `tools_condition` provides conditional routing logic

### Structured Output Classification

From `backend/app/core/graph.py`:

```python
structured_llm = llm.with_structured_output(QueryClassification)
result = await structured_llm.ainvoke(classification_prompt.format(query=last_msg))
```

**Key Points:**
- `with_structured_output()` API may have signature changes in 0.3.x
- Async invocation with `ainvoke()`

## Requirements

### Functional Requirements

1. **Dependency Version Upgrade**
   - Description: Update all LangChain dependencies to target versions
   - Acceptance:
     - `langchain >= 0.3.0` in requirements.txt
     - `langchain-core >= 0.3.0` in requirements.txt
     - `langgraph >= 0.2.0` in requirements.txt
     - `langgraph-checkpoint >= 2.0.0` in requirements.txt
     - `pip install -r requirements.txt` succeeds without conflicts

2. **Graph.py Compatibility**
   - Description: Ensure graph.py works with new LangGraph 0.2.x APIs
   - Acceptance:
     - All imports resolve successfully
     - Graph compiles without errors
     - StateGraph construction works with new API
     - START/END constants accessible
     - `add_messages` annotation works
     - Async nodes execute correctly

3. **Agent_graph.py Compatibility**
   - Description: Ensure agent_graph.py works with new LangGraph 0.2.x APIs
   - Acceptance:
     - ToolNode API compatible
     - tools_condition routing works
     - @tool decorator functions correctly
     - Graph compilation succeeds
     - Tool execution flows correctly

4. **Checkpoint System Integration**
   - Description: Add new checkpoint system required by LangGraph 0.2.x
   - Acceptance:
     - `langgraph-checkpoint` package installed
     - Both graphs compile with checkpoint configuration (MemorySaver or explicit None)
     - No checkpoint-related errors during graph execution

5. **Test Suite Validation**
   - Description: All existing tests must pass without modification
   - Acceptance:
     - `pytest backend/tests/` returns 0 failures
     - All RAG workflow tests pass
     - No test code modifications required
     - Test execution time similar to before

6. **Zero Deprecation Warnings**
   - Description: No deprecation warnings during execution
   - Acceptance:
     - `pytest backend/tests/ -W error::DeprecationWarning` passes
     - Manual test queries show no warnings in logs
     - No FutureWarning messages

### Edge Cases

1. **Version Conflicts** - If dependency resolver fails, pin compatible sub-dependencies explicitly
2. **Import Path Changes** - If START/END move to different module, update all import statements
3. **Checkpoint Requirement** - If compile() fails without checkpointer, add MemorySaver() as default
4. **Message API Changes** - If BaseMessage constructors change, update message creation patterns
5. **Tool Execution Breaking** - If ToolNode signature changes, update tool binding pattern
6. **Structured Output Changes** - If with_structured_output() API changes, update classification logic

## Implementation Notes

### DO
- Update all four dependencies together in a single commit
- Run tests immediately after dependency update to identify breaks
- Use `MemorySaver()` from `langgraph.checkpoint.memory` if compile() requires checkpointer
- Check LangChain 0.3.x migration guide for official breaking change list
- Verify both graph implementations independently
- Test with actual LLM calls, not just mocks
- Use `pip install --upgrade` to ensure clean dependency resolution

### DON'T
- Update dependencies one at a time (version compatibility issues)
- Skip test execution after each fix
- Ignore deprecation warnings (address them proactively)
- Modify test expectations to make tests pass (tests validate behavior)
- Add unnecessary abstractions or refactoring (scope is upgrade only)
- Change RAG workflow logic or add new features

## Development Environment

### Start Services

```bash
# Backend (FastAPI + LangChain)
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Run tests
pytest backend/tests/ -v
pytest backend/tests/ -W error::DeprecationWarning  # Check for warnings
```

### Service URLs
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

### Required Environment Variables
```bash
# Backend (.env)
ANTHROPIC_API_KEY=<your-key>  # For LLM calls
OPENAI_API_KEY=<your-key>     # Alternative LLM provider
SUPABASE_URL=<url>            # Vector store
SUPABASE_KEY=<key>            # Vector store auth
```

## Success Criteria

The task is complete when:

1. [ ] `requirements.txt` contains all four upgraded dependencies with correct versions
2. [ ] `pip install -r backend/requirements.txt` completes successfully
3. [ ] `backend/app/core/graph.py` imports and compiles without errors
4. [ ] `backend/agent_graph.py` imports and compiles without errors
5. [ ] `pytest backend/tests/` passes with 0 failures
6. [ ] No DeprecationWarning or FutureWarning messages appear during test execution
7. [ ] Manual RAG workflow test succeeds (send query → get response with citations)
8. [ ] Graph execution shows expected flow through classifier → retrieval → synthesizer nodes
9. [ ] Tool-based agent executes tools correctly when needed
10. [ ] No breaking changes introduced to API contracts or response formats

## QA Acceptance Criteria

**CRITICAL**: These criteria must be verified by the QA Agent before sign-off.

### Unit Tests
| Test | File | What to Verify |
|------|------|----------------|
| Test LLM Configuration | `backend/tests/test_api_integration.py` | LLM initialization with new packages |
| Test Message Handling | `backend/tests/test_rag_flow_verification.py` | Message state accumulation works |
| Test Tool Execution | `backend/tests/test_sukl_retriever.py` | Tool decorator and ToolNode compatibility |
| Test Classification | `backend/tests/test_rag_flow_verification.py` | Structured output classification works |

### Integration Tests
| Test | Services | What to Verify |
|------|----------|----------------|
| RAG Workflow E2E | backend | Full query → classification → retrieval → synthesis flow |
| Graph Compilation | backend | Both graph.py and agent_graph.py compile successfully |
| Checkpoint System | backend | Graphs compile with checkpoint configuration |
| Tool Routing | backend | tools_condition correctly routes to ToolNode |

### End-to-End Tests
| Flow | Steps | Expected Outcome |
|------|-------|------------------|
| Drug Query | 1. POST /query with drug question 2. Graph executes 3. Response returned | Classification → SÚKL retrieval → synthesis with citations |
| Guideline Query | 1. POST /query with guideline question 2. Graph executes 3. Response returned | Classification → guideline retrieval → synthesis with page citations |
| Tool-Based Query | 1. POST to agent endpoint 2. Agent decides tool use 3. Tool executes 4. Response synthesized | Agent → ToolNode → Agent → Response loop works |

### Dependency Verification
| Check | Command | Expected |
|-------|---------|----------|
| Langchain version | `pip show langchain \| grep Version` | Version: 0.3.x |
| Langchain-core version | `pip show langchain-core \| grep Version` | Version: 0.3.x |
| Langgraph version | `pip show langgraph \| grep Version` | Version: 0.2.x |
| Langgraph-checkpoint | `pip show langgraph-checkpoint \| grep Version` | Version: 2.0.x |
| No conflicts | `pip check` | No broken requirements |

### Code Verification
| Check | File | Expected |
|-------|------|----------|
| Imports resolve | `backend/app/core/graph.py` | No ImportError when loading |
| Graph compiles | `backend/app/core/graph.py` | `app = workflow.compile()` succeeds |
| Checkpoint added | `backend/app/core/graph.py` | Compile has checkpointer or explicit None |
| Imports resolve | `backend/agent_graph.py` | No ImportError when loading |
| Graph compiles | `backend/agent_graph.py` | `app = workflow.compile()` succeeds |

### Warning Check
| Check | Command | Expected |
|-------|---------|----------|
| No deprecations | `pytest backend/tests/ -W error::DeprecationWarning` | All tests pass, no warnings raised |
| Clean logs | Manual query execution | No warning messages in uvicorn logs |

### QA Sign-off Requirements
- [ ] All unit tests pass (test_api_integration.py, test_rag_flow_verification.py, test_sukl_retriever.py)
- [ ] All integration tests pass (RAG workflow E2E, graph compilation, checkpoint system)
- [ ] All E2E tests pass (drug query flow, guideline query flow, tool-based query flow)
- [ ] All dependencies verified at correct versions
- [ ] All code verification checks pass (imports, compilation, checkpoint)
- [ ] Zero deprecation/future warnings detected
- [ ] No regressions in existing functionality
- [ ] Code follows existing patterns (no unnecessary refactoring)
- [ ] No security vulnerabilities introduced (pip-audit passes)
- [ ] Manual smoke test confirms RAG workflow functional

## Breaking Changes Reference

### Expected Breaking Changes from 0.1.x → 0.3.x

Based on research phase findings, these breaking changes are anticipated:

1. **Graph Compilation**
   - 0.1.x: `workflow.compile()`
   - 0.3.x: `workflow.compile(checkpointer=checkpointer)` or explicit None
   - Fix: Import `MemorySaver` from `langgraph.checkpoint.memory` and pass to compile()

2. **Import Paths**
   - 0.1.x: `from langgraph.graph import START, END`
   - 0.3.x: May be relocated or renamed
   - Fix: Check langgraph.graph.constants or langgraph.constants

3. **Tool Node API**
   - 0.1.x: `ToolNode(tools)`
   - 0.3.x: Constructor signature may have changed
   - Fix: Check for additional required parameters (config, etc.)

4. **Message State Handling**
   - 0.1.x: `add_messages` from `langgraph.graph.message`
   - 0.3.x: May be in `langgraph.graph` or require different import
   - Fix: Update import path if relocated

5. **Structured Output**
   - 0.1.x: `llm.with_structured_output(Schema)`
   - 0.3.x: API signature may require additional parameters
   - Fix: Check for schema parameter format changes

## Rollback Plan

If upgrade causes critical issues:

1. **Immediate Rollback**
   ```bash
   git checkout backend/requirements.txt
   pip install -r backend/requirements.txt --force-reinstall
   pytest backend/tests/
   ```

2. **Gradual Rollback** (if partial upgrade possible)
   - Try keeping langchain-core 0.3.x but rolling back langgraph to 0.1.x
   - Check compatibility matrix in LangChain docs

3. **Issue Escalation**
   - If specific API is broken, check LangChain GitHub issues for known problems
   - Consider pinning to specific 0.3.x minor version (e.g., 0.3.1 instead of 0.3.0)

---

**Implementation Priority**: HIGH
**Estimated Complexity**: MEDIUM (dependency upgrade with known breaking changes)
**Risk Level**: MEDIUM (breaking changes expected but well-documented)
**Testing Requirement**: EXTENSIVE (full test suite must pass)
