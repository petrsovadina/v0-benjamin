"""
Tool Registry Base Classes

This module defines the core interfaces and data structures for the tool registry:
- ToolDefinition: Defines a tool's metadata and handler
- ToolResult: Standardized response structure for tool invocations

These classes are implemented in subtasks 1.2 and 1.3.
"""

from dataclasses import dataclass, field
from typing import Any, Callable, Optional, Type, Union
from pydantic import BaseModel


@dataclass
class ToolDefinition:
    """
    Defines a tool's metadata and execution handler.

    Attributes:
        name: Unique identifier for the tool
        description: Human-readable description of what the tool does
        parameters: Pydantic model class for input validation
        handler: Callable that executes the tool logic (sync or async)

    Note:
        Full implementation in subtask 1.2.
    """

    name: str
    description: str
    parameters: Type[BaseModel]
    handler: Callable[..., Any]


class ToolResult(BaseModel):
    """
    Standardized response structure for tool invocations.

    Attributes:
        success: Whether the tool executed successfully
        data: Result data if successful
        error: Error message if failed
        duration_ms: Execution time in milliseconds

    Note:
        Full implementation with factory methods in subtask 1.3.
    """

    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    duration_ms: Optional[float] = None

    @classmethod
    def ok(cls, data: Any, duration_ms: Optional[float] = None) -> "ToolResult":
        """Create a successful result."""
        return cls(success=True, data=data, duration_ms=duration_ms)

    @classmethod
    def fail(cls, error: str, duration_ms: Optional[float] = None) -> "ToolResult":
        """Create a failure result."""
        return cls(success=False, error=error, duration_ms=duration_ms)
