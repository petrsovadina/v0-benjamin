"""
Tool Registry Implementation

This module implements the central ToolRegistry class for managing
tool registration, invocation, and logging.

Note:
    Full implementation in subtask 1.4.
"""

from typing import Any, Dict, List

from backend.tools.base import ToolDefinition, ToolResult


class ToolRegistry:
    """
    Central registry for managing and invoking tools.

    The registry provides:
    - Tool registration with unique name validation
    - Unified invocation API with input validation
    - Tool discovery (list all registered tools)
    - Tool metadata retrieval

    Attributes:
        _tools: Internal dictionary mapping tool names to definitions

    Note:
        Full implementation with async support and logging in subtask 1.4.
    """

    def __init__(self) -> None:
        """Initialize an empty tool registry."""
        self._tools: Dict[str, ToolDefinition] = {}

    def register(self, tool: ToolDefinition) -> None:
        """
        Register a tool with the registry.

        Args:
            tool: The tool definition to register

        Raises:
            ValueError: If a tool with the same name is already registered
        """
        if tool.name in self._tools:
            raise ValueError(f"Tool '{tool.name}' already registered")
        self._tools[tool.name] = tool

    def invoke(self, name: str, **kwargs: Any) -> ToolResult:
        """
        Invoke a registered tool by name.

        Args:
            name: The name of the tool to invoke
            **kwargs: Arguments to pass to the tool handler

        Returns:
            ToolResult with success/failure status and data or error

        Raises:
            KeyError: If the tool is not registered

        Note:
            Full implementation with validation and logging in subtask 1.4.
        """
        if name not in self._tools:
            raise KeyError(f"Tool '{name}' not registered")

        tool = self._tools[name]
        try:
            result = tool.handler(**kwargs)
            return ToolResult.ok(data=result)
        except Exception as e:
            return ToolResult.fail(error=str(e))

    def list_tools(self) -> List[str]:
        """
        List all registered tool names.

        Returns:
            List of tool names
        """
        return list(self._tools.keys())

    def get_tool(self, name: str) -> ToolDefinition:
        """
        Get a tool definition by name.

        Args:
            name: The name of the tool

        Returns:
            The tool definition

        Raises:
            KeyError: If the tool is not registered
        """
        if name not in self._tools:
            raise KeyError(f"Tool '{name}' not registered")
        return self._tools[name]
