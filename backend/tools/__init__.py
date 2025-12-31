"""
Tool Registry System - Public API

This module provides a centralized registry for managing and invoking tools
across the application. It offers a unified interface for tool registration,
validation, and invocation with comprehensive logging and type safety.

Public API:
    - ToolDefinition: Interface defining a tool's metadata and handler
    - ToolResult: Standardized response structure for tool invocations
    - ToolRegistry: Central registry for registering and invoking tools
    - get_registry: Get the default singleton registry instance
    - init_default_registry: Initialize and populate the default registry

Usage:
    from backend.tools import ToolRegistry, ToolDefinition, ToolResult
    from pydantic import BaseModel

    # Create registry instance
    registry = ToolRegistry()

    # Define input schema
    class MyToolInput(BaseModel):
        message: str

    # Create and register a tool
    def my_handler(message: str) -> dict:
        return {"result": message}

    tool = ToolDefinition(
        name="my_tool",
        description="A sample tool",
        parameters=MyToolInput,
        handler=my_handler
    )
    registry.register(tool)

    # Invoke the tool
    result = registry.invoke("my_tool", message="Hello!")
    # result.success == True, result.data == {"result": "Hello!"}

Singleton Usage:
    from backend.tools import get_registry, init_default_registry

    # Initialize once at startup with all MCP tools
    init_default_registry()

    # Get the singleton registry anywhere in the app
    registry = get_registry()
    result = await registry.invoke_async("sukl_search_drugs", query="aspirin")
"""

from typing import Optional

from backend.tools.base import ToolDefinition, ToolResult
from backend.tools.registry import ToolRegistry

# Module-level singleton registry instance (lazy initialized)
_default_registry: Optional[ToolRegistry] = None


def get_registry() -> ToolRegistry:
    """
    Get the default singleton registry instance.

    Uses lazy initialization to avoid import-time side effects.
    If the registry hasn't been created yet, creates an empty one.
    Use init_default_registry() to populate it with MCP tools.

    Returns:
        ToolRegistry: The singleton registry instance.

    Example:
        >>> from backend.tools import get_registry
        >>> registry = get_registry()
        >>> registry.list_tools()
        []  # Empty until init_default_registry() is called
    """
    global _default_registry
    if _default_registry is None:
        _default_registry = ToolRegistry()
    return _default_registry


def init_default_registry() -> ToolRegistry:
    """
    Initialize the default registry with all available MCP tools.

    Creates the singleton registry if it doesn't exist, then registers
    all MCP tools (SUKL and PubMed). Safe to call multiple times -
    subsequent calls are no-ops if tools are already registered.

    Returns:
        ToolRegistry: The initialized singleton registry.

    Example:
        >>> from backend.tools import init_default_registry
        >>> registry = init_default_registry()
        >>> registry.list_tools()
        ['pubmed_search_literature', 'sukl_get_drug_details', 'sukl_search_drugs']
    """
    registry = get_registry()

    # Import MCP tool registration functions (lazy import pattern)
    from backend.tools.mcp.pubmed import register_pubmed_tools
    from backend.tools.mcp.sukl import register_sukl_tools

    # Register SUKL tools if not already registered
    if not registry.has_tool("sukl_search_drugs"):
        register_sukl_tools(registry)

    # Register PubMed tools if not already registered
    if not registry.has_tool("pubmed_search_literature"):
        register_pubmed_tools(registry)

    return registry


__all__ = [
    # Core classes
    "ToolDefinition",
    "ToolResult",
    "ToolRegistry",
    # Singleton access
    "get_registry",
    "init_default_registry",
]

__version__ = "0.1.0"
