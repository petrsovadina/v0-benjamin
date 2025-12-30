"""
Tool Registry Implementation

This module implements the central ToolRegistry class for managing
tool registration, invocation, and logging. It provides a unified
interface for invoking tools with type-safe validation and timing metrics.
"""

import asyncio
import time
from typing import Any, Dict, List, Set

from pydantic import ValidationError

from backend.services.logger import get_logger
from backend.tools.base import ToolDefinition, ToolResult

# Initialize structured logger for tool registry
logger = get_logger("backend.tools.registry")

# Keys that should be sanitized in log outputs
SENSITIVE_KEYS: Set[str] = {
    "api_key", "apikey", "api-key",
    "password", "passwd", "pwd",
    "token", "access_token", "refresh_token", "auth_token",
    "secret", "secret_key",
    "authorization", "auth",
    "credential", "credentials",
    "private_key", "privatekey",
}


def sanitize_inputs(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sanitize sensitive data from input dictionary for safe logging.

    Replaces values of sensitive keys with "[REDACTED]" to prevent
    accidental exposure of secrets in logs.

    Args:
        inputs: Dictionary of input parameters.

    Returns:
        Dict[str, Any]: A new dictionary with sensitive values redacted.

    Example:
        >>> sanitize_inputs({"query": "test", "api_key": "secret123"})
        {'query': 'test', 'api_key': '[REDACTED]'}
    """
    sanitized = {}
    for key, value in inputs.items():
        # Check if key matches any sensitive pattern (case-insensitive)
        key_lower = key.lower()
        if any(sensitive in key_lower for sensitive in SENSITIVE_KEYS):
            sanitized[key] = "[REDACTED]"
        elif isinstance(value, dict):
            # Recursively sanitize nested dictionaries
            sanitized[key] = sanitize_inputs(value)
        else:
            sanitized[key] = value
    return sanitized


class ToolRegistry:
    """
    Central registry for managing and invoking tools.

    The ToolRegistry provides a unified interface for:
    - Registering tools with unique name validation
    - Invoking tools with Pydantic-based input validation
    - Discovering registered tools
    - Retrieving tool metadata

    The registry supports both synchronous and asynchronous tool handlers,
    automatically detecting and handling each appropriately.

    Attributes:
        _tools: Internal dictionary mapping tool names to definitions.

    Example:
        >>> from pydantic import BaseModel
        >>> from backend.tools import ToolRegistry, ToolDefinition

        >>> class EchoInput(BaseModel):
        ...     message: str

        >>> def echo_handler(message: str) -> dict:
        ...     return {"echoed": message}

        >>> registry = ToolRegistry()
        >>> tool = ToolDefinition(
        ...     name="echo",
        ...     description="Echoes back the input",
        ...     parameters=EchoInput,
        ...     handler=echo_handler
        ... )
        >>> registry.register(tool)
        >>> result = registry.invoke("echo", message="Hello!")
        >>> result.success
        True
        >>> result.data
        {'echoed': 'Hello!'}

    Note:
        For async handlers, use `invoke_async()` or wrap `invoke()` in an
        event loop. The `invoke()` method will handle async handlers by
        running them in the current event loop or creating a new one.
    """

    def __init__(self) -> None:
        """Initialize an empty tool registry."""
        self._tools: Dict[str, ToolDefinition] = {}

    def register(self, tool: ToolDefinition) -> None:
        """
        Register a tool with the registry.

        Adds a tool definition to the registry, making it available for
        invocation. Tool names must be unique within a registry.

        Args:
            tool: The tool definition to register. Must be a valid
                ToolDefinition instance with a unique name.

        Raises:
            ValueError: If a tool with the same name is already registered.
                The error message includes the conflicting tool name.

        Example:
            >>> registry = ToolRegistry()
            >>> registry.register(my_tool)  # Registers successfully
            >>> registry.register(my_tool)  # Raises ValueError
            ValueError: Tool 'my_tool' already registered
        """
        if tool.name in self._tools:
            raise ValueError(f"Tool '{tool.name}' already registered")
        self._tools[tool.name] = tool

    def invoke(self, name: str, **kwargs: Any) -> ToolResult:
        """
        Invoke a registered tool by name with input validation.

        This method performs the following steps:
        1. Looks up the tool by name
        2. Validates inputs against the tool's Pydantic parameter schema
        3. Executes the handler (sync or async)
        4. Returns a ToolResult with timing information

        Args:
            name: The name of the tool to invoke.
            **kwargs: Arguments to pass to the tool handler. Must match
                the tool's parameter schema.

        Returns:
            ToolResult: A result object containing:
                - success: True if execution completed without errors
                - data: Handler return value (if successful)
                - error: Error message (if failed)
                - duration_ms: Execution time in milliseconds

        Raises:
            KeyError: If the tool is not registered.

        Note:
            Pydantic ValidationError is caught and returned as a failed
            ToolResult rather than re-raised, allowing calling code to
            handle validation errors uniformly.

        Example:
            >>> result = registry.invoke("echo", message="Hello!")
            >>> if result.success:
            ...     print(result.data)
            ... else:
            ...     print(f"Error: {result.error}")

            >>> # Invalid input returns failure result
            >>> result = registry.invoke("echo", wrong_param="test")
            >>> result.success
            False
            >>> "validation error" in result.error.lower()
            True
        """
        if name not in self._tools:
            raise KeyError(f"Tool '{name}' not registered")

        tool = self._tools[name]
        start_time = time.perf_counter()

        # Sanitize inputs for logging (before validation to capture all inputs)
        sanitized_inputs = sanitize_inputs(kwargs)

        # Validate inputs against the tool's parameter schema
        try:
            validated_params = tool.parameters(**kwargs)
        except ValidationError as e:
            duration_ms = (time.perf_counter() - start_time) * 1000
            logger.error(
                "Tool invocation failed: validation error",
                tool_name=name,
                inputs=sanitized_inputs,
                success=False,
                duration_ms=round(duration_ms, 2),
                error_type="ValidationError",
                error_message=str(e),
            )
            return ToolResult.create_failure(
                error=f"Validation error: {e}",
                duration_ms=duration_ms
            )

        # Convert validated params to dict for handler invocation
        params_dict = validated_params.model_dump()

        # Execute the handler (sync or async)
        try:
            if tool.is_async:
                # Handle async handler
                result = self._run_async_handler(tool.handler, params_dict)
            else:
                # Handle sync handler
                result = tool.handler(**params_dict)

            duration_ms = (time.perf_counter() - start_time) * 1000

            # Log successful invocation
            logger.info(
                "Tool invoked successfully",
                tool_name=name,
                inputs=sanitized_inputs,
                success=True,
                duration_ms=round(duration_ms, 2),
            )

            return ToolResult.create_success(data=result, duration_ms=duration_ms)

        except Exception as e:
            duration_ms = (time.perf_counter() - start_time) * 1000

            # Log failed invocation with exception details
            logger.error(
                "Tool invocation failed: handler error",
                error=e,
                tool_name=name,
                inputs=sanitized_inputs,
                success=False,
                duration_ms=round(duration_ms, 2),
                error_type=type(e).__name__,
                error_message=str(e),
            )

            return ToolResult.create_failure(
                error=f"Handler error: {str(e)}",
                duration_ms=duration_ms
            )

    async def invoke_async(self, name: str, **kwargs: Any) -> ToolResult:
        """
        Async version of invoke for use in async contexts.

        This method is preferred when calling from an async function,
        as it properly awaits async handlers without creating a new
        event loop.

        Args:
            name: The name of the tool to invoke.
            **kwargs: Arguments to pass to the tool handler.

        Returns:
            ToolResult: Same as invoke().

        Raises:
            KeyError: If the tool is not registered.

        Example:
            >>> async def main():
            ...     result = await registry.invoke_async("echo", message="Hi!")
            ...     print(result.data)
        """
        if name not in self._tools:
            raise KeyError(f"Tool '{name}' not registered")

        tool = self._tools[name]
        start_time = time.perf_counter()

        # Sanitize inputs for logging (before validation to capture all inputs)
        sanitized_inputs = sanitize_inputs(kwargs)

        # Validate inputs against the tool's parameter schema
        try:
            validated_params = tool.parameters(**kwargs)
        except ValidationError as e:
            duration_ms = (time.perf_counter() - start_time) * 1000
            logger.error(
                "Tool invocation failed: validation error",
                tool_name=name,
                inputs=sanitized_inputs,
                success=False,
                duration_ms=round(duration_ms, 2),
                error_type="ValidationError",
                error_message=str(e),
            )
            return ToolResult.create_failure(
                error=f"Validation error: {e}",
                duration_ms=duration_ms
            )

        # Convert validated params to dict for handler invocation
        params_dict = validated_params.model_dump()

        # Execute the handler (sync or async)
        try:
            if tool.is_async:
                # Await async handler directly
                result = await tool.handler(**params_dict)
            else:
                # Run sync handler in executor to avoid blocking
                result = tool.handler(**params_dict)

            duration_ms = (time.perf_counter() - start_time) * 1000

            # Log successful invocation
            logger.info(
                "Tool invoked successfully",
                tool_name=name,
                inputs=sanitized_inputs,
                success=True,
                duration_ms=round(duration_ms, 2),
            )

            return ToolResult.create_success(data=result, duration_ms=duration_ms)

        except Exception as e:
            duration_ms = (time.perf_counter() - start_time) * 1000

            # Log failed invocation with exception details
            logger.error(
                "Tool invocation failed: handler error",
                error=e,
                tool_name=name,
                inputs=sanitized_inputs,
                success=False,
                duration_ms=round(duration_ms, 2),
                error_type=type(e).__name__,
                error_message=str(e),
            )

            return ToolResult.create_failure(
                error=f"Handler error: {str(e)}",
                duration_ms=duration_ms
            )

    def _run_async_handler(self, handler: Any, params: Dict[str, Any]) -> Any:
        """
        Run an async handler from a sync context.

        Attempts to run the async handler in the current event loop
        if one exists. Otherwise, creates a new event loop.

        Args:
            handler: The async handler function.
            params: Parameters to pass to the handler.

        Returns:
            The handler's return value.
        """
        try:
            # Try to get the current event loop
            loop = asyncio.get_running_loop()
            # If we're in an async context, we can't use run_until_complete
            # This path handles the case where invoke() is called from sync code
            # but an event loop happens to be running (e.g., in Jupyter)
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(
                    asyncio.run,
                    handler(**params)
                )
                return future.result()
        except RuntimeError:
            # No running event loop, we can create one
            return asyncio.run(handler(**params))

    def list_tools(self) -> List[str]:
        """
        List all registered tool names.

        Returns an alphabetically sorted list of all tool names
        currently registered in the registry.

        Returns:
            List[str]: Sorted list of tool names.

        Example:
            >>> registry.register(tool_a)  # name="alpha"
            >>> registry.register(tool_b)  # name="beta"
            >>> registry.list_tools()
            ['alpha', 'beta']
        """
        return sorted(self._tools.keys())

    def get_tool(self, name: str) -> ToolDefinition:
        """
        Get a tool definition by name.

        Retrieves the full ToolDefinition for a registered tool,
        including its description, parameter schema, and handler.

        Args:
            name: The name of the tool to retrieve.

        Returns:
            ToolDefinition: The tool's definition.

        Raises:
            KeyError: If the tool is not registered.

        Example:
            >>> tool = registry.get_tool("echo")
            >>> tool.description
            'Echoes back the input message'
            >>> tool.parameters.model_json_schema()
            {'properties': {'message': {'type': 'string'}}, ...}
        """
        if name not in self._tools:
            raise KeyError(f"Tool '{name}' not registered")
        return self._tools[name]

    def has_tool(self, name: str) -> bool:
        """
        Check if a tool is registered.

        Args:
            name: The name of the tool to check.

        Returns:
            bool: True if the tool is registered, False otherwise.

        Example:
            >>> registry.has_tool("echo")
            True
            >>> registry.has_tool("nonexistent")
            False
        """
        return name in self._tools

    def unregister(self, name: str) -> None:
        """
        Remove a tool from the registry.

        Args:
            name: The name of the tool to remove.

        Raises:
            KeyError: If the tool is not registered.

        Example:
            >>> registry.unregister("echo")
            >>> registry.has_tool("echo")
            False
        """
        if name not in self._tools:
            raise KeyError(f"Tool '{name}' not registered")
        del self._tools[name]

    def clear(self) -> None:
        """
        Remove all tools from the registry.

        Useful for testing or resetting the registry state.

        Example:
            >>> registry.clear()
            >>> registry.list_tools()
            []
        """
        self._tools.clear()

    def __len__(self) -> int:
        """Return the number of registered tools."""
        return len(self._tools)

    def __contains__(self, name: str) -> bool:
        """Check if a tool name is registered."""
        return name in self._tools

    def __repr__(self) -> str:
        """Return a string representation of the registry."""
        tool_count = len(self._tools)
        return f"ToolRegistry(tools={tool_count})"
