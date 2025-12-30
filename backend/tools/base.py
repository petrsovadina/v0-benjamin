"""
Tool Registry Base Classes

This module defines the core interfaces and data structures for the tool registry:
- ToolDefinition: Defines a tool's metadata and handler
- ToolResult: Standardized response structure for tool invocations
"""

import asyncio
import inspect
from dataclasses import dataclass, field
from typing import Any, Callable, Optional, Type, Union
from pydantic import BaseModel


@dataclass
class ToolDefinition:
    """
    Defines a tool's metadata and execution handler.

    A ToolDefinition encapsulates everything needed to register and invoke
    a tool through the ToolRegistry. It supports both synchronous and
    asynchronous handler functions.

    Attributes:
        name: Unique identifier for the tool. Must be unique within a registry.
        description: Human-readable description of what the tool does.
        parameters: Pydantic model class for input validation. The model's
            fields define the expected parameters for the tool.
        handler: Callable that executes the tool logic. Can be either
            a sync function (def) or async function (async def).

    Example:
        >>> from pydantic import BaseModel
        >>> class EchoInput(BaseModel):
        ...     message: str
        >>> def echo_handler(message: str) -> dict:
        ...     return {"echoed": message}
        >>> tool = ToolDefinition(
        ...     name="echo",
        ...     description="Echoes back the input message",
        ...     parameters=EchoInput,
        ...     handler=echo_handler
        ... )

    Raises:
        TypeError: If handler is not callable.
        TypeError: If parameters is not a Pydantic BaseModel subclass.
    """

    name: str
    description: str
    parameters: Type[BaseModel]
    handler: Callable[..., Any]

    def __post_init__(self) -> None:
        """Validate fields after dataclass initialization."""
        # Validate handler is callable
        if not callable(self.handler):
            raise TypeError(
                f"Handler must be callable, got {type(self.handler).__name__}"
            )

        # Validate parameters is a Pydantic BaseModel subclass
        if not (
            isinstance(self.parameters, type) and issubclass(self.parameters, BaseModel)
        ):
            raise TypeError(
                f"Parameters must be a Pydantic BaseModel subclass, "
                f"got {type(self.parameters).__name__}"
            )

        # Validate name is non-empty string
        if not self.name or not isinstance(self.name, str):
            raise ValueError("Tool name must be a non-empty string")

        # Validate description is non-empty string
        if not self.description or not isinstance(self.description, str):
            raise ValueError("Tool description must be a non-empty string")

    @property
    def is_async(self) -> bool:
        """Check if the handler is an async function."""
        return asyncio.iscoroutinefunction(self.handler)


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
