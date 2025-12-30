"""
MCP Server Wrappers for Tool Registry

This package provides utilities for wrapping MCP (Model Context Protocol)
server functions as ToolDefinition instances compatible with the Tool Registry.

The wrappers enable:
- Seamless integration of existing MCP servers (SUKL, PubMed) into the registry
- Automatic Pydantic schema generation from function signatures
- Preservation of async behavior and function metadata

Public API:
    - create_mcp_tool: Factory function to create ToolDefinition from MCP functions
    - create_mcp_tools_batch: Create multiple tools from a list of functions
    - extract_function_metadata: Extract metadata from function signatures
    - create_pydantic_model_from_params: Generate Pydantic model from parameters

Usage:
    from backend.tools.mcp import create_mcp_tool
    from backend.mcp_servers.sukl_server import search_drugs

    # Wrap MCP function as a tool
    tool = create_mcp_tool(search_drugs)

    # Register with the tool registry
    from backend.tools import ToolRegistry
    registry = ToolRegistry()
    registry.register(tool)

    # Invoke through the registry
    result = await registry.invoke_async("search_drugs", query="aspirin")
"""

from backend.tools.mcp.base import (
    create_mcp_tool,
    create_mcp_tools_batch,
    create_pydantic_model_from_params,
    extract_function_metadata,
)

__all__ = [
    "create_mcp_tool",
    "create_mcp_tools_batch",
    "create_pydantic_model_from_params",
    "extract_function_metadata",
]
