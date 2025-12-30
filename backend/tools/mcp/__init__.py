"""
MCP Server Wrappers for Tool Registry

This package provides utilities for wrapping MCP (Model Context Protocol)
server functions as ToolDefinition instances compatible with the Tool Registry.

The wrappers enable:
- Seamless integration of existing MCP servers (SUKL, PubMed) into the registry
- Automatic Pydantic schema generation from function signatures
- Preservation of async behavior and function metadata

Public API:
    Base utilities:
    - create_mcp_tool: Factory function to create ToolDefinition from MCP functions
    - create_mcp_tools_batch: Create multiple tools from a list of functions
    - extract_function_metadata: Extract metadata from function signatures
    - create_pydantic_model_from_params: Generate Pydantic model from parameters

    SUKL tools:
    - SuklSearchInput: Pydantic model for drug search input
    - SuklDrugDetailInput: Pydantic model for drug detail input
    - sukl_search_drugs: ToolDefinition for searching drugs
    - sukl_get_drug_details: ToolDefinition for getting drug details
    - register_sukl_tools: Function to register all SUKL tools

    PubMed tools:
    - PubMedSearchInput: Pydantic model for literature search input
    - pubmed_search_literature: ToolDefinition for searching medical literature
    - register_pubmed_tools: Function to register all PubMed tools

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

    # Or use pre-built SUKL tools
    from backend.tools.mcp import register_sukl_tools
    register_sukl_tools(registry)

    # Or use pre-built PubMed tools
    from backend.tools.mcp import register_pubmed_tools
    register_pubmed_tools(registry)
"""

from backend.tools.mcp.base import (
    create_mcp_tool,
    create_mcp_tools_batch,
    create_pydantic_model_from_params,
    extract_function_metadata,
)
from backend.tools.mcp.pubmed import (
    PUBMED_TOOLS,
    PubMedSearchInput,
    pubmed_search_literature,
    register_pubmed_tools,
)
from backend.tools.mcp.sukl import (
    SUKL_TOOLS,
    SuklDrugDetailInput,
    SuklSearchInput,
    register_sukl_tools,
    sukl_get_drug_details,
    sukl_search_drugs,
)

__all__ = [
    # Base utilities
    "create_mcp_tool",
    "create_mcp_tools_batch",
    "create_pydantic_model_from_params",
    "extract_function_metadata",
    # SUKL tools
    "SuklSearchInput",
    "SuklDrugDetailInput",
    "sukl_search_drugs",
    "sukl_get_drug_details",
    "register_sukl_tools",
    "SUKL_TOOLS",
    # PubMed tools
    "PubMedSearchInput",
    "pubmed_search_literature",
    "register_pubmed_tools",
    "PUBMED_TOOLS",
]
