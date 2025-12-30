# Gotchas & Pitfalls

Things to watch out for in this codebase.

## [2025-12-30 17:51]
In Pydantic v2, classmethod names cannot match field names due to __getattr__ conflicts. Factory methods for ToolResult are named create_success()/create_failure() instead of success()/failure() to avoid conflict with the 'success' field. Aliases ok()/fail() are also provided.

_Context: backend/tools/base.py - ToolResult class factory methods_

## [2025-12-30 20:17]
When creating ToolDefinition instances with lazy import handlers, the handler parameter must reference the wrapper function (e.g., _get_drug_details_handler) NOT the imported function name (e.g., get_drug_details) which would be undefined at module load time.

_Context: backend/tools/mcp/sukl.py - Fixed handler reference bug that caused 470 failed session attempts_
