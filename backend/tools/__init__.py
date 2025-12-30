"""
Tool Registry System - Public API

This module provides a centralized registry for managing and invoking tools
across the application. It offers a unified interface for tool registration,
validation, and invocation with comprehensive logging and type safety.

Public API:
    - ToolDefinition: Interface defining a tool's metadata and handler
    - ToolResult: Standardized response structure for tool invocations
    - ToolRegistry: Central registry for registering and invoking tools

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
"""

from backend.tools.base import ToolDefinition, ToolResult
from backend.tools.registry import ToolRegistry

__all__ = [
    "ToolDefinition",
    "ToolResult",
    "ToolRegistry",
]

__version__ = "0.1.0"
