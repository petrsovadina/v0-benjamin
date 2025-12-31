"""
Tool Registry Base Classes

This module defines the core interfaces and data structures for the tool registry:
- ToolDefinition: Defines a tool's metadata and handler
- ToolResult: Standardized response structure for tool invocations
"""

import asyncio
from dataclasses import dataclass
from typing import Any, Callable, Optional, Type
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
        """
        Validate fields after dataclass initialization.

        Performs validation on all ToolDefinition fields to ensure:
        - name is a non-empty string
        - description is a non-empty string
        - parameters is a Pydantic BaseModel subclass
        - handler is a callable (function, method, or callable class)

        Raises:
            TypeError: If handler is not callable or parameters is not a BaseModel subclass.
            ValueError: If name or description is empty or not a string.
        """
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
        """
        Check if the handler is an async function.

        This property is used by the ToolRegistry to determine whether to
        await the handler or call it synchronously. It uses asyncio's
        iscoroutinefunction() to detect async def functions.

        Returns:
            bool: True if the handler is an async function, False otherwise.

        Example:
            >>> async def async_handler(x: int) -> int:
            ...     return x * 2
            >>> def sync_handler(x: int) -> int:
            ...     return x * 2
            >>> tool_async = ToolDefinition(..., handler=async_handler)
            >>> tool_async.is_async
            True
            >>> tool_sync = ToolDefinition(..., handler=sync_handler)
            >>> tool_sync.is_async
            False
        """
        return asyncio.iscoroutinefunction(self.handler)


class ToolResult(BaseModel):
    """
    Standardized response structure for tool invocations.

    ToolResult provides a consistent format for all tool execution outcomes,
    whether successful or failed. It includes timing information for performance
    monitoring and debugging.

    Attributes:
        success: Whether the tool executed successfully. True if the handler
            completed without errors, False otherwise.
        data: Result data from the tool handler if successful. Can be any
            JSON-serializable value. None if the execution failed.
        error: Human-readable error message if the execution failed. None if
            successful. Should provide enough context for debugging.
        duration_ms: Execution time in milliseconds. Measured from before
            input validation to after handler completion. Useful for
            performance monitoring and identifying slow tools.

    Example:
        >>> # Creating results directly
        >>> result = ToolResult(success=True, data={"items": [1, 2, 3]}, duration_ms=42.5)
        >>> result.success
        True

        >>> # Using factory methods (recommended)
        >>> success_result = ToolResult.create_success(data={"user": "john"}, duration_ms=10.0)
        >>> failure_result = ToolResult.create_failure(error="Connection timeout", duration_ms=5000.0)

        >>> # Checking result status
        >>> if result.success:
        ...     process_data(result.data)
        ... else:
        ...     log_error(result.error)

    Note:
        Factory methods are named `create_success()` and `create_failure()` to avoid
        naming conflicts with the `success` field in Pydantic v2. Aliases `ok()` and
        `fail()` are also provided for convenience.
    """

    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    duration_ms: Optional[float] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "success": True,
                    "data": {"result": "example data"},
                    "error": None,
                    "duration_ms": 42.5
                },
                {
                    "success": False,
                    "data": None,
                    "error": "Tool execution failed: connection timeout",
                    "duration_ms": 5000.0
                }
            ]
        }
    }

    @classmethod
    def create_success(cls, data: Any, duration_ms: Optional[float] = None) -> "ToolResult":
        """
        Create a successful ToolResult.

        Factory method for creating a result that indicates successful
        tool execution with returned data.

        Args:
            data: The result data from the tool handler. Can be any
                JSON-serializable value (dict, list, str, int, etc.).
            duration_ms: Optional execution time in milliseconds.

        Returns:
            ToolResult: A result instance with success=True and the provided data.

        Example:
            >>> result = ToolResult.create_success(
            ...     data={"drugs": ["Aspirin", "Ibuprofen"]},
            ...     duration_ms=150.5
            ... )
            >>> result.success
            True
            >>> result.data
            {'drugs': ['Aspirin', 'Ibuprofen']}
        """
        return cls(success=True, data=data, duration_ms=duration_ms)

    @classmethod
    def create_failure(cls, error: str, duration_ms: Optional[float] = None) -> "ToolResult":
        """
        Create a failed ToolResult.

        Factory method for creating a result that indicates tool execution
        failure with an error message.

        Args:
            error: Human-readable error message describing what went wrong.
                Should provide enough context for debugging.
            duration_ms: Optional execution time in milliseconds (time until
                the failure occurred).

        Returns:
            ToolResult: A result instance with success=False and the error message.

        Example:
            >>> result = ToolResult.create_failure(
            ...     error="Database connection failed: timeout after 30s",
            ...     duration_ms=30000.0
            ... )
            >>> result.success
            False
            >>> result.error
            'Database connection failed: timeout after 30s'
        """
        return cls(success=False, error=error, duration_ms=duration_ms)

    # Convenience aliases for common Result pattern naming
    ok = create_success
    fail = create_failure
