# Specification: Tool Registry System

## Overview

This task creates a centralized **Tool Registry** system that provides a unified interface for invoking all tools across the application. The registry wraps existing MCP servers (SÚKL, PubMed) into a standardized tool interface with type-safe validation and comprehensive logging. This abstraction layer enables consistent tool management, validation, and observability across the entire platform.

## Workflow Type

**Type**: feature

**Rationale**: This is a new capability being added to the codebase. We're creating a foundational infrastructure component that doesn't exist yet - a central registry pattern for tool management. This is not refactoring existing code, but rather building new abstractions to standardize how tools are registered, validated, and invoked.

## Task Scope

### Services Involved
- **Backend** (primary) - Python/FastAPI service where the tool registry will be implemented

### This Task Will:
- [x] Create `backend/tools/__init__.py` with public API exports
- [x] Define `ToolDefinition` interface in `backend/tools/base.py` (name, description, parameters, handler)
- [x] Define `ToolResult` class in `backend/tools/base.py` for standardized responses
- [x] Implement `ToolRegistry` class in `backend/tools/registry.py` with registration and invocation logic
- [x] Add Pydantic-based input/output validation for type safety
- [x] Implement logging infrastructure for all tool calls (audit trail)
- [x] Create MCP server wrappers for SÚKL and PubMed servers conforming to `ToolDefinition` interface

### Out of Scope:
- Modifying existing MCP server implementations (wrapper approach only)
- Creating new tools beyond MCP server wrappers
- Frontend integration (registry is backend-only for now)
- Authentication/authorization for tool invocation
- Rate limiting or quota management
- Distributed tool registry (single-instance only)

## Service Context

### Backend Service

**Tech Stack:**
- Language: Python 3.13
- Framework: FastAPI
- ORM: SQLAlchemy
- Validation: Pydantic
- Key directories: `backend/app/`, `backend/tools/`

**Entry Point:** `backend/app/main.py`

**How to Run:**
```bash
# Navigate to backend directory
cd backend

# Install dependencies (if needed)
pip install -r requirements.txt

# Run development server
uvicorn app.main:app --reload --port 8000
```

**Port:** 8000

**Health Check:** `GET http://localhost:8000/health`

## Files to Modify

| File | Service | What to Change |
|------|---------|---------------|
| N/A | N/A | This is a greenfield implementation - no existing files to modify |

## Files to Reference

These files show patterns to follow:

| File | Pattern to Copy |
|------|----------------|
| `backend/app/api/v1/endpoints/*.py` | FastAPI route structure and Pydantic model usage |
| `backend/app/main.py` | Application initialization and configuration patterns |
| Existing MCP server implementations | Understanding MCP server interface for wrapper design |

## Patterns to Follow

### Pydantic Model Pattern

From FastAPI endpoints in `backend/app/api/v1/endpoints/`:

```python
from pydantic import BaseModel, Field

class ToolInput(BaseModel):
    """Type-safe input validation"""
    param_name: str = Field(..., description="Parameter description")
    optional_param: int = Field(default=10, ge=1, le=100)

    class Config:
        json_schema_extra = {
            "example": {
                "param_name": "example_value",
                "optional_param": 42
            }
        }
```

**Key Points:**
- Use Pydantic `BaseModel` for all data structures
- Add `Field()` descriptors with validation constraints
- Include schema examples for API documentation
- Enable strict type checking with Config class

### Registry Pattern

```python
from typing import Dict, Callable, Any

class Registry:
    """Central registry for managing registered items"""
    def __init__(self):
        self._items: Dict[str, Any] = {}

    def register(self, name: str, item: Any) -> None:
        """Register an item by name"""
        if name in self._items:
            raise ValueError(f"Item '{name}' already registered")
        self._items[name] = item

    def get(self, name: str) -> Any:
        """Retrieve registered item by name"""
        if name not in self._items:
            raise KeyError(f"Item '{name}' not found")
        return self._items[name]

    def list_all(self) -> list[str]:
        """List all registered item names"""
        return list(self._items.keys())
```

**Key Points:**
- Use dictionary for O(1) lookup performance
- Validate uniqueness during registration
- Provide clear error messages for missing items
- Support introspection (list all registered items)

### Logging Pattern

```python
import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)

def log_tool_call(tool_name: str, inputs: Dict[str, Any], result: Any):
    """Log tool invocation for audit trail"""
    logger.info(
        "Tool invoked",
        extra={
            "tool_name": tool_name,
            "inputs": inputs,
            "success": result.success,
            "duration_ms": result.duration
        }
    )
```

**Key Points:**
- Use structured logging with `extra` parameter
- Include tool name, inputs, success status, and timing
- Use appropriate log levels (INFO for success, ERROR for failures)
- Ensure sensitive data is not logged

## Requirements

### Functional Requirements

1. **Tool Registration**
   - Description: Registry must allow tools to be registered with unique names
   - Acceptance: Can register a tool with name, description, parameters schema, and handler function
   - Validation: Attempting to register duplicate names raises clear error

2. **Tool Invocation**
   - Description: Registry provides unified API to invoke any registered tool
   - Acceptance: Can call `registry.invoke(tool_name, **kwargs)` and receive standardized result
   - Validation: Input validation occurs before handler execution

3. **Type Safety**
   - Description: All tool inputs and outputs are validated using Pydantic schemas
   - Acceptance: Invalid inputs raise `ValidationError` with clear messages
   - Validation: Tool results conform to `ToolResult` structure

4. **MCP Server Integration**
   - Description: Existing MCP servers (SÚKL, PubMed) callable through registry
   - Acceptance: MCP servers wrapped as tools with standardized interface
   - Validation: MCP wrapper maintains original functionality while providing uniform API

5. **Audit Logging**
   - Description: All tool invocations logged with inputs, outputs, and timing
   - Acceptance: Every tool call generates structured log entry
   - Validation: Logs include tool_name, inputs, success status, duration

### Edge Cases

1. **Duplicate Registration** - Raise `ValueError` with message "Tool '{name}' already registered"
2. **Tool Not Found** - Raise `KeyError` with message "Tool '{name}' not registered"
3. **Invalid Input Schema** - Raise `ValidationError` from Pydantic with field-level errors
4. **Handler Exception** - Catch exceptions, log error, return `ToolResult` with `success=False` and error message
5. **Missing Required Parameters** - Pydantic validation catches and raises clear error before handler execution
6. **Async vs Sync Handlers** - Registry supports both synchronous and asynchronous handler functions

## Implementation Notes

### DO
- **Follow interface-based design**: Define `ToolDefinition` as abstract interface that all tools implement
- **Use Pydantic everywhere**: Validate all inputs with `BaseModel`, all outputs with `ToolResult`
- **Implement wrapper pattern for MCP**: Create adapter layer that doesn't modify original MCP servers
- **Log all invocations**: Use structured logging with consistent format (tool_name, inputs, result, duration)
- **Make registry singleton**: Ensure single global registry instance using module-level instance
- **Support both sync and async**: Handle both `def` and `async def` handler functions
- **Include rich metadata**: Store tool description, parameter schemas, examples in `ToolDefinition`
- **Use type hints everywhere**: Full type coverage for IDE support and runtime validation

### DON'T
- **Don't modify MCP servers directly**: Use wrapper/adapter pattern to maintain backward compatibility
- **Don't swallow exceptions**: Catch, log, and re-raise or return error in `ToolResult`
- **Don't skip validation**: Always validate inputs before invoking handler
- **Don't use print statements**: Use proper logging infrastructure
- **Don't hardcode tool registrations**: Keep registration flexible and dynamic
- **Don't leak sensitive data**: Sanitize inputs/outputs in logs (e.g., API keys, passwords)

## Development Environment

### Start Services

```bash
# Backend only (registry is backend component)
cd backend
uvicorn app.main:app --reload --port 8000
```

### Service URLs
- Backend API: http://localhost:8000
- API Docs (Swagger): http://localhost:8000/docs
- Health Check: http://localhost:8000/health

### Required Environment Variables
- `NEXT_PUBLIC_API_URL`: http://localhost:8000 (backend API URL)
- No additional environment variables required for tool registry itself
- MCP servers may require their own configuration (SÚKL, PubMed API keys, etc.)

### Testing the Registry

```python
# Example manual test in Python REPL
from backend.tools import ToolRegistry, ToolDefinition, ToolResult
from pydantic import BaseModel

# Create registry instance
registry = ToolRegistry()

# Define a simple tool
class EchoInput(BaseModel):
    message: str

def echo_handler(message: str) -> dict:
    return {"echoed": message}

tool = ToolDefinition(
    name="echo",
    description="Echoes back the input message",
    parameters=EchoInput,
    handler=echo_handler
)

# Register and invoke
registry.register(tool)
result = registry.invoke("echo", message="Hello, Registry!")
print(result)  # ToolResult(success=True, data={"echoed": "Hello, Registry!"})
```

## Success Criteria

The task is complete when:

1. [x] **ToolDefinition interface created** - `backend/tools/base.py` defines the tool contract (name, description, parameters, handler)
2. [x] **ToolResult class created** - `backend/tools/base.py` defines standardized result structure (success, data, error, duration)
3. [x] **ToolRegistry implemented** - `backend/tools/registry.py` provides registration and invocation methods
4. [x] **Pydantic validation integrated** - All inputs validated through Pydantic schemas defined in `ToolDefinition.parameters`
5. [x] **Logging infrastructure added** - All tool calls logged with structured format (tool_name, inputs, success, duration)
6. [x] **MCP server wrappers created** - SÚKL and PubMed MCP servers wrapped as tools conforming to `ToolDefinition`
7. [x] **Uniform API verified** - All tools invokable via `registry.invoke(tool_name, **kwargs)`
8. [x] **Type safety confirmed** - Invalid inputs raise `ValidationError`, outputs conform to `ToolResult`
9. [x] **No console errors** - Clean execution without warnings or errors
10. [x] **Backward compatibility maintained** - Existing MCP server functionality preserved through wrappers

## QA Acceptance Criteria

**CRITICAL**: These criteria must be verified by the QA Agent before sign-off.

### Unit Tests

| Test | File | What to Verify |
|------|------|----------------|
| `test_tool_definition_validation` | `backend/tests/test_tools_base.py` | ToolDefinition requires name, description, parameters, handler |
| `test_tool_result_structure` | `backend/tests/test_tools_base.py` | ToolResult has success, data, error, duration fields |
| `test_registry_registration` | `backend/tests/test_tools_registry.py` | Tools can be registered with unique names |
| `test_duplicate_registration_error` | `backend/tests/test_tools_registry.py` | Duplicate tool names raise ValueError |
| `test_tool_invocation` | `backend/tests/test_tools_registry.py` | Registered tools can be invoked via registry.invoke() |
| `test_tool_not_found_error` | `backend/tests/test_tools_registry.py` | Invoking non-existent tool raises KeyError |
| `test_input_validation` | `backend/tests/test_tools_registry.py` | Invalid inputs raise Pydantic ValidationError |
| `test_handler_exception_handling` | `backend/tests/test_tools_registry.py` | Handler exceptions caught and returned as ToolResult with success=False |
| `test_logging_tool_calls` | `backend/tests/test_tools_registry.py` | All invocations generate structured log entries |
| `test_async_handler_support` | `backend/tests/test_tools_registry.py` | Both sync and async handlers work correctly |

### Integration Tests

| Test | Services | What to Verify |
|------|----------|----------------|
| `test_mcp_sukl_wrapper` | backend (MCP SÚKL) | SÚKL MCP server callable through registry with same results as direct call |
| `test_mcp_pubmed_wrapper` | backend (MCP PubMed) | PubMed MCP server callable through registry with same results as direct call |
| `test_registry_list_tools` | backend | Can retrieve list of all registered tools |
| `test_tool_metadata_retrieval` | backend | Can get tool description and parameter schema from registry |

### End-to-End Tests

| Flow | Steps | Expected Outcome |
|------|-------|------------------|
| Register and Invoke Tool | 1. Create ToolDefinition 2. Register to registry 3. Invoke with valid inputs | Returns ToolResult with success=True and expected data |
| Invalid Input Handling | 1. Register tool with Pydantic schema 2. Invoke with invalid inputs | Raises ValidationError before handler execution |
| MCP Server Compatibility | 1. Wrap MCP server as tool 2. Invoke through registry 3. Compare with direct MCP call | Results match, wrapper adds no breaking changes |
| Audit Trail Verification | 1. Invoke multiple tools 2. Check log output | Each invocation logged with tool_name, inputs, success, duration |

### Python REPL Verification

| Test | Command | Expected |
|------|---------|----------|
| Import registry | `from backend.tools import ToolRegistry` | No import errors |
| Import base classes | `from backend.tools import ToolDefinition, ToolResult` | No import errors |
| Create registry instance | `registry = ToolRegistry()` | Instance created successfully |
| Register sample tool | `registry.register(sample_tool)` | Tool registered without errors |
| List registered tools | `registry.list_tools()` | Returns list with sample tool name |
| Invoke tool | `registry.invoke("sample", param="value")` | Returns ToolResult instance |

### Code Quality Checks

| Check | Command | Expected |
|-------|---------|----------|
| Type checking | `mypy backend/tools/` | No type errors |
| Linting | `flake8 backend/tools/` | No linting errors |
| Import structure | `python -c "from backend.tools import ToolRegistry, ToolDefinition, ToolResult"` | Successful import |

### QA Sign-off Requirements
- [ ] All unit tests pass (10/10)
- [ ] All integration tests pass (4/4)
- [ ] All E2E tests pass (4/4)
- [ ] Python REPL verification complete (6/6)
- [ ] Code quality checks pass (type checking, linting, imports)
- [ ] No regressions in existing MCP server functionality
- [ ] Code follows established FastAPI/Pydantic patterns
- [ ] No security vulnerabilities introduced (sensitive data sanitized in logs)
- [ ] Documentation complete (docstrings for all classes and methods)
- [ ] Logging infrastructure operational (structured logs visible)
