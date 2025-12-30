"""
Unit tests for ToolRegistry functionality.

Tests cover:
- Tool registration (register, has_tool, unregister, clear)
- Tool invocation (invoke, invoke_async)
- Input validation (Pydantic ValidationError)
- Error handling (handler exceptions)
- Logging integration
- Async handler support
- Tool discovery (list_tools, get_tool)
- Registry utility methods (__len__, __contains__, __repr__)
"""

import asyncio
import logging
import pytest
from unittest.mock import patch, MagicMock
from pydantic import BaseModel, Field, ValidationError

from backend.tools.base import ToolDefinition, ToolResult
from backend.tools.registry import ToolRegistry, sanitize_inputs, SENSITIVE_KEYS


# ============================================================================
# Test Fixtures and Helpers
# ============================================================================

class SimpleInput(BaseModel):
    """Simple Pydantic model for testing."""
    message: str = Field(..., description="A message to process")


class SearchInput(BaseModel):
    """Pydantic model with optional fields for testing."""
    query: str = Field(..., description="Search query")
    limit: int = Field(default=10, ge=1, le=100)


class ComplexInput(BaseModel):
    """Pydantic model with multiple fields for testing."""
    name: str
    count: int = Field(default=1, ge=0)
    tags: list[str] = []


def simple_handler(message: str) -> dict:
    """Simple synchronous handler."""
    return {"result": message}


def search_handler(query: str, limit: int = 10) -> dict:
    """Handler with optional parameter."""
    return {"query": query, "limit": limit, "results": []}


def complex_handler(name: str, count: int = 1, tags: list = None) -> dict:
    """Handler with complex parameters."""
    return {"name": name, "count": count, "tags": tags or []}


def failing_handler(message: str) -> dict:
    """Handler that always raises an exception."""
    raise RuntimeError("Intentional handler failure")


def value_error_handler(message: str) -> dict:
    """Handler that raises ValueError."""
    raise ValueError("Invalid value provided")


async def async_handler(message: str) -> dict:
    """Async handler for testing."""
    await asyncio.sleep(0.01)
    return {"async_result": message}


async def async_failing_handler(message: str) -> dict:
    """Async handler that fails."""
    await asyncio.sleep(0.01)
    raise RuntimeError("Async handler failure")


@pytest.fixture
def registry() -> ToolRegistry:
    """Create a fresh ToolRegistry for each test."""
    return ToolRegistry()


@pytest.fixture
def simple_tool() -> ToolDefinition:
    """Create a simple tool definition."""
    return ToolDefinition(
        name="simple_tool",
        description="A simple test tool",
        parameters=SimpleInput,
        handler=simple_handler
    )


@pytest.fixture
def search_tool() -> ToolDefinition:
    """Create a search tool definition."""
    return ToolDefinition(
        name="search_tool",
        description="A search tool with optional params",
        parameters=SearchInput,
        handler=search_handler
    )


@pytest.fixture
def async_tool() -> ToolDefinition:
    """Create an async tool definition."""
    return ToolDefinition(
        name="async_tool",
        description="An async test tool",
        parameters=SimpleInput,
        handler=async_handler
    )


@pytest.fixture
def failing_tool() -> ToolDefinition:
    """Create a tool that always fails."""
    return ToolDefinition(
        name="failing_tool",
        description="A tool that always fails",
        parameters=SimpleInput,
        handler=failing_handler
    )


@pytest.fixture
def populated_registry(registry, simple_tool, search_tool, async_tool) -> ToolRegistry:
    """Create a registry with multiple tools registered."""
    registry.register(simple_tool)
    registry.register(search_tool)
    registry.register(async_tool)
    return registry


# ============================================================================
# Tool Registration Tests
# ============================================================================

class TestRegistryRegistration:
    """Tests for tool registration functionality."""

    def test_register_tool_successfully(self, registry, simple_tool):
        """Tools can be registered with unique names."""
        registry.register(simple_tool)

        assert "simple_tool" in registry
        assert len(registry) == 1

    def test_register_multiple_tools(self, registry, simple_tool, search_tool, async_tool):
        """Multiple tools can be registered."""
        registry.register(simple_tool)
        registry.register(search_tool)
        registry.register(async_tool)

        assert len(registry) == 3
        assert "simple_tool" in registry
        assert "search_tool" in registry
        assert "async_tool" in registry

    def test_register_tool_stores_definition(self, registry, simple_tool):
        """Registered tool definition is stored correctly."""
        registry.register(simple_tool)

        stored_tool = registry.get_tool("simple_tool")
        assert stored_tool is simple_tool
        assert stored_tool.name == "simple_tool"
        assert stored_tool.description == "A simple test tool"


class TestDuplicateRegistrationError:
    """Tests for duplicate registration error handling."""

    def test_duplicate_registration_raises_valueerror(self, registry, simple_tool):
        """Registering a tool with duplicate name raises ValueError."""
        registry.register(simple_tool)

        with pytest.raises(ValueError, match="Tool 'simple_tool' already registered"):
            registry.register(simple_tool)

    def test_duplicate_name_different_tool_raises_valueerror(self, registry, simple_tool):
        """Registering different tool with same name raises ValueError."""
        registry.register(simple_tool)

        # Create a different tool with the same name
        duplicate_tool = ToolDefinition(
            name="simple_tool",  # Same name
            description="Different description",
            parameters=SimpleInput,
            handler=lambda message: {"different": message}
        )

        with pytest.raises(ValueError, match="already registered"):
            registry.register(duplicate_tool)


# ============================================================================
# Tool Invocation Tests
# ============================================================================

class TestToolInvocation:
    """Tests for tool invocation functionality."""

    def test_invoke_registered_tool(self, registry, simple_tool):
        """Registered tools can be invoked via registry.invoke()."""
        registry.register(simple_tool)

        result = registry.invoke("simple_tool", message="Hello World")

        assert isinstance(result, ToolResult)
        assert result.success is True
        assert result.data == {"result": "Hello World"}
        assert result.error is None

    def test_invoke_returns_toolresult(self, registry, simple_tool):
        """invoke() always returns a ToolResult instance."""
        registry.register(simple_tool)

        result = registry.invoke("simple_tool", message="test")

        assert isinstance(result, ToolResult)
        assert hasattr(result, "success")
        assert hasattr(result, "data")
        assert hasattr(result, "error")
        assert hasattr(result, "duration_ms")

    def test_invoke_includes_duration(self, registry, simple_tool):
        """invoke() includes duration_ms in the result."""
        registry.register(simple_tool)

        result = registry.invoke("simple_tool", message="test")

        assert result.duration_ms is not None
        assert result.duration_ms >= 0

    def test_invoke_with_optional_params(self, registry, search_tool):
        """invoke() works with optional parameters."""
        registry.register(search_tool)

        # With default value
        result = registry.invoke("search_tool", query="test")
        assert result.success is True
        assert result.data["limit"] == 10

        # With explicit value
        result = registry.invoke("search_tool", query="test", limit=50)
        assert result.success is True
        assert result.data["limit"] == 50

    def test_invoke_with_complex_params(self, registry):
        """invoke() works with complex parameter types."""
        complex_tool = ToolDefinition(
            name="complex_tool",
            description="Tool with complex params",
            parameters=ComplexInput,
            handler=complex_handler
        )
        registry.register(complex_tool)

        result = registry.invoke("complex_tool", name="test", count=5, tags=["a", "b"])

        assert result.success is True
        assert result.data["name"] == "test"
        assert result.data["count"] == 5
        assert result.data["tags"] == ["a", "b"]


class TestToolNotFoundError:
    """Tests for tool not found error handling."""

    def test_invoke_nonexistent_tool_raises_keyerror(self, registry):
        """Invoking non-existent tool raises KeyError."""
        with pytest.raises(KeyError, match="Tool 'nonexistent' not registered"):
            registry.invoke("nonexistent", message="test")

    def test_get_tool_nonexistent_raises_keyerror(self, registry):
        """Getting non-existent tool raises KeyError."""
        with pytest.raises(KeyError, match="Tool 'unknown' not registered"):
            registry.get_tool("unknown")

    def test_unregister_nonexistent_raises_keyerror(self, registry):
        """Unregistering non-existent tool raises KeyError."""
        with pytest.raises(KeyError, match="Tool 'missing' not registered"):
            registry.unregister("missing")


# ============================================================================
# Input Validation Tests
# ============================================================================

class TestInputValidation:
    """Tests for Pydantic input validation."""

    def test_missing_required_param_returns_validation_error(self, registry, simple_tool):
        """Missing required parameter returns ToolResult with validation error."""
        registry.register(simple_tool)

        # Missing 'message' parameter
        result = registry.invoke("simple_tool")

        assert result.success is False
        assert "Validation error" in result.error
        assert result.data is None

    def test_wrong_type_param_returns_validation_error(self, registry, search_tool):
        """Wrong type parameter returns ToolResult with validation error."""
        registry.register(search_tool)

        # 'limit' should be int, not string
        result = registry.invoke("search_tool", query="test", limit="not_an_int")

        assert result.success is False
        assert "Validation error" in result.error

    def test_constraint_violation_returns_validation_error(self, registry, search_tool):
        """Constraint violation returns ToolResult with validation error."""
        registry.register(search_tool)

        # limit must be between 1 and 100
        result = registry.invoke("search_tool", query="test", limit=200)

        assert result.success is False
        assert "Validation error" in result.error

    def test_extra_params_are_ignored(self, registry, simple_tool):
        """Extra parameters not in schema are handled by Pydantic."""
        registry.register(simple_tool)

        # This behavior depends on Pydantic model config
        # By default, extra params are ignored
        result = registry.invoke("simple_tool", message="test", extra_param="ignored")

        assert result.success is True

    def test_validation_error_includes_duration(self, registry, simple_tool):
        """Validation errors still include duration_ms."""
        registry.register(simple_tool)

        result = registry.invoke("simple_tool")  # Missing required param

        assert result.duration_ms is not None
        assert result.duration_ms >= 0


# ============================================================================
# Handler Exception Handling Tests
# ============================================================================

class TestHandlerExceptionHandling:
    """Tests for handler exception handling."""

    def test_handler_exception_returns_failure_result(self, registry, failing_tool):
        """Handler exceptions are caught and returned as ToolResult with success=False."""
        registry.register(failing_tool)

        result = registry.invoke("failing_tool", message="test")

        assert result.success is False
        assert "Handler error" in result.error
        assert "Intentional handler failure" in result.error
        assert result.data is None

    def test_handler_exception_includes_error_message(self, registry):
        """Handler error message is included in the result."""
        tool = ToolDefinition(
            name="value_error_tool",
            description="Tool that raises ValueError",
            parameters=SimpleInput,
            handler=value_error_handler
        )
        registry.register(tool)

        result = registry.invoke("value_error_tool", message="test")

        assert result.success is False
        assert "Invalid value provided" in result.error

    def test_handler_exception_includes_duration(self, registry, failing_tool):
        """Failed invocations still include duration_ms."""
        registry.register(failing_tool)

        result = registry.invoke("failing_tool", message="test")

        assert result.duration_ms is not None
        assert result.duration_ms >= 0


# ============================================================================
# Logging Tests
# ============================================================================

class TestLoggingToolCalls:
    """Tests for tool invocation logging."""

    def test_successful_invocation_logs_info(self, registry, simple_tool):
        """Successful invocations generate INFO log entries."""
        registry.register(simple_tool)

        with patch("backend.tools.registry.logger") as mock_logger:
            result = registry.invoke("simple_tool", message="test")

            mock_logger.info.assert_called_once()
            call_kwargs = mock_logger.info.call_args[1]
            assert call_kwargs["tool_name"] == "simple_tool"
            assert call_kwargs["success"] is True
            assert "duration_ms" in call_kwargs

    def test_failed_invocation_logs_error(self, registry, failing_tool):
        """Failed invocations generate ERROR log entries."""
        registry.register(failing_tool)

        with patch("backend.tools.registry.logger") as mock_logger:
            result = registry.invoke("failing_tool", message="test")

            mock_logger.error.assert_called_once()
            call_kwargs = mock_logger.error.call_args[1]
            assert call_kwargs["tool_name"] == "failing_tool"
            assert call_kwargs["success"] is False
            assert call_kwargs["error_type"] == "RuntimeError"

    def test_validation_error_logs_error(self, registry, simple_tool):
        """Validation errors generate ERROR log entries."""
        registry.register(simple_tool)

        with patch("backend.tools.registry.logger") as mock_logger:
            result = registry.invoke("simple_tool")  # Missing required param

            mock_logger.error.assert_called_once()
            call_kwargs = mock_logger.error.call_args[1]
            assert call_kwargs["error_type"] == "ValidationError"
            assert call_kwargs["success"] is False

    def test_logging_includes_sanitized_inputs(self, registry, simple_tool):
        """Log entries include inputs (sanitized)."""
        registry.register(simple_tool)

        with patch("backend.tools.registry.logger") as mock_logger:
            registry.invoke("simple_tool", message="test message")

            call_kwargs = mock_logger.info.call_args[1]
            assert "inputs" in call_kwargs
            assert call_kwargs["inputs"]["message"] == "test message"


# ============================================================================
# Async Handler Support Tests
# ============================================================================

class TestAsyncHandlerSupport:
    """Tests for async handler functionality."""

    def test_invoke_with_async_handler(self, registry, async_tool):
        """invoke() works with async handlers."""
        registry.register(async_tool)

        result = registry.invoke("async_tool", message="async test")

        assert result.success is True
        assert result.data == {"async_result": "async test"}

    def test_invoke_async_with_sync_handler(self, registry, simple_tool):
        """invoke_async() works with sync handlers."""
        registry.register(simple_tool)

        async def run_test():
            return await registry.invoke_async("simple_tool", message="sync test")

        result = asyncio.run(run_test())

        assert result.success is True
        assert result.data == {"result": "sync test"}

    def test_invoke_async_with_async_handler(self, registry, async_tool):
        """invoke_async() properly awaits async handlers."""
        registry.register(async_tool)

        async def run_test():
            return await registry.invoke_async("async_tool", message="async test")

        result = asyncio.run(run_test())

        assert result.success is True
        assert result.data == {"async_result": "async test"}

    def test_invoke_async_handler_exception(self, registry):
        """invoke_async() handles async handler exceptions."""
        async_failing_tool = ToolDefinition(
            name="async_failing_tool",
            description="Async tool that fails",
            parameters=SimpleInput,
            handler=async_failing_handler
        )
        registry.register(async_failing_tool)

        async def run_test():
            return await registry.invoke_async("async_failing_tool", message="test")

        result = asyncio.run(run_test())

        assert result.success is False
        assert "Async handler failure" in result.error

    def test_invoke_async_nonexistent_tool_raises_keyerror(self, registry):
        """invoke_async() raises KeyError for non-existent tools."""
        async def run_test():
            return await registry.invoke_async("nonexistent", message="test")

        with pytest.raises(KeyError, match="not registered"):
            asyncio.run(run_test())

    def test_invoke_async_validation_error(self, registry, async_tool):
        """invoke_async() returns validation error for invalid inputs."""
        registry.register(async_tool)

        async def run_test():
            return await registry.invoke_async("async_tool")  # Missing required param

        result = asyncio.run(run_test())

        assert result.success is False
        assert "Validation error" in result.error


# ============================================================================
# Tool Discovery Tests
# ============================================================================

class TestListTools:
    """Tests for list_tools() functionality."""

    def test_list_tools_empty_registry(self, registry):
        """list_tools() returns empty list for empty registry."""
        assert registry.list_tools() == []

    def test_list_tools_returns_all_names(self, populated_registry):
        """list_tools() returns all registered tool names."""
        tools = populated_registry.list_tools()

        assert len(tools) == 3
        assert "simple_tool" in tools
        assert "search_tool" in tools
        assert "async_tool" in tools

    def test_list_tools_returns_sorted_list(self, populated_registry):
        """list_tools() returns alphabetically sorted list."""
        tools = populated_registry.list_tools()

        assert tools == sorted(tools)
        assert tools == ["async_tool", "search_tool", "simple_tool"]


class TestGetTool:
    """Tests for get_tool() functionality."""

    def test_get_tool_returns_definition(self, registry, simple_tool):
        """get_tool() returns the ToolDefinition."""
        registry.register(simple_tool)

        retrieved = registry.get_tool("simple_tool")

        assert retrieved is simple_tool
        assert isinstance(retrieved, ToolDefinition)

    def test_get_tool_preserves_all_fields(self, registry, simple_tool):
        """get_tool() returns ToolDefinition with all fields intact."""
        registry.register(simple_tool)

        retrieved = registry.get_tool("simple_tool")

        assert retrieved.name == "simple_tool"
        assert retrieved.description == "A simple test tool"
        assert retrieved.parameters is SimpleInput
        assert retrieved.handler is simple_handler


# ============================================================================
# Additional Registry Methods Tests
# ============================================================================

class TestHasTool:
    """Tests for has_tool() functionality."""

    def test_has_tool_returns_true_for_registered(self, registry, simple_tool):
        """has_tool() returns True for registered tools."""
        registry.register(simple_tool)
        assert registry.has_tool("simple_tool") is True

    def test_has_tool_returns_false_for_unregistered(self, registry):
        """has_tool() returns False for unregistered tools."""
        assert registry.has_tool("nonexistent") is False


class TestUnregister:
    """Tests for unregister() functionality."""

    def test_unregister_removes_tool(self, registry, simple_tool):
        """unregister() removes the tool from registry."""
        registry.register(simple_tool)
        assert "simple_tool" in registry

        registry.unregister("simple_tool")

        assert "simple_tool" not in registry

    def test_unregister_allows_reregistration(self, registry, simple_tool):
        """After unregister(), the same name can be registered again."""
        registry.register(simple_tool)
        registry.unregister("simple_tool")

        # Should not raise
        registry.register(simple_tool)
        assert "simple_tool" in registry


class TestClear:
    """Tests for clear() functionality."""

    def test_clear_removes_all_tools(self, populated_registry):
        """clear() removes all tools from registry."""
        assert len(populated_registry) == 3

        populated_registry.clear()

        assert len(populated_registry) == 0
        assert populated_registry.list_tools() == []


class TestRegistryDunderMethods:
    """Tests for __len__, __contains__, __repr__."""

    def test_len_returns_tool_count(self, populated_registry):
        """__len__ returns number of registered tools."""
        assert len(populated_registry) == 3

    def test_len_empty_registry(self, registry):
        """__len__ returns 0 for empty registry."""
        assert len(registry) == 0

    def test_contains_for_registered_tool(self, registry, simple_tool):
        """__contains__ returns True for registered tools."""
        registry.register(simple_tool)
        assert "simple_tool" in registry

    def test_contains_for_unregistered_tool(self, registry):
        """__contains__ returns False for unregistered tools."""
        assert "nonexistent" not in registry

    def test_repr(self, populated_registry):
        """__repr__ returns informative string representation."""
        repr_str = repr(populated_registry)

        assert "ToolRegistry" in repr_str
        assert "3" in repr_str or "tools" in repr_str


# ============================================================================
# Sanitize Inputs Tests
# ============================================================================

class TestSanitizeInputs:
    """Tests for sanitize_inputs() utility function."""

    def test_sanitize_preserves_normal_values(self):
        """Normal values are preserved unchanged."""
        inputs = {"query": "test", "limit": 10}
        sanitized = sanitize_inputs(inputs)

        assert sanitized == {"query": "test", "limit": 10}

    def test_sanitize_redacts_api_key(self):
        """api_key values are redacted."""
        inputs = {"query": "test", "api_key": "secret123"}
        sanitized = sanitize_inputs(inputs)

        assert sanitized["query"] == "test"
        assert sanitized["api_key"] == "[REDACTED]"

    def test_sanitize_redacts_password(self):
        """password values are redacted."""
        inputs = {"username": "user", "password": "secret"}
        sanitized = sanitize_inputs(inputs)

        assert sanitized["username"] == "user"
        assert sanitized["password"] == "[REDACTED]"

    def test_sanitize_redacts_token(self):
        """token values are redacted."""
        inputs = {"access_token": "abc123", "data": "safe"}
        sanitized = sanitize_inputs(inputs)

        assert sanitized["access_token"] == "[REDACTED]"
        assert sanitized["data"] == "safe"

    def test_sanitize_case_insensitive(self):
        """Sanitization is case-insensitive."""
        inputs = {"API_KEY": "secret", "Password": "secret", "TOKEN": "secret"}
        sanitized = sanitize_inputs(inputs)

        assert sanitized["API_KEY"] == "[REDACTED]"
        assert sanitized["Password"] == "[REDACTED]"
        assert sanitized["TOKEN"] == "[REDACTED]"

    def test_sanitize_nested_dictionaries(self):
        """Nested dictionaries are sanitized recursively."""
        inputs = {
            "config": {
                "api_key": "secret",
                "settings": {
                    "password": "secret"
                }
            },
            "query": "test"
        }
        sanitized = sanitize_inputs(inputs)

        assert sanitized["query"] == "test"
        assert sanitized["config"]["api_key"] == "[REDACTED]"
        assert sanitized["config"]["settings"]["password"] == "[REDACTED]"

    def test_sanitize_all_sensitive_keys(self):
        """All known sensitive keys are redacted."""
        inputs = {
            "api_key": "x", "apikey": "x", "api-key": "x",
            "password": "x", "passwd": "x", "pwd": "x",
            "token": "x", "access_token": "x", "refresh_token": "x",
            "secret": "x", "secret_key": "x",
            "authorization": "x", "auth": "x",
            "credential": "x", "credentials": "x",
            "private_key": "x", "privatekey": "x"
        }
        sanitized = sanitize_inputs(inputs)

        for key in inputs:
            assert sanitized[key] == "[REDACTED]", f"Key '{key}' was not redacted"


# ============================================================================
# Edge Cases Tests
# ============================================================================

class TestEdgeCases:
    """Tests for edge cases and special scenarios."""

    def test_handler_returns_none(self, registry):
        """Handler returning None is handled correctly."""
        def none_handler(message: str):
            return None

        tool = ToolDefinition(
            name="none_tool",
            description="Returns None",
            parameters=SimpleInput,
            handler=none_handler
        )
        registry.register(tool)

        result = registry.invoke("none_tool", message="test")

        assert result.success is True
        assert result.data is None

    def test_handler_returns_primitive(self, registry):
        """Handler returning primitive values works correctly."""
        def string_handler(message: str) -> str:
            return "result"

        def int_handler(message: str) -> int:
            return 42

        tool1 = ToolDefinition(
            name="string_tool",
            description="Returns string",
            parameters=SimpleInput,
            handler=string_handler
        )
        tool2 = ToolDefinition(
            name="int_tool",
            description="Returns int",
            parameters=SimpleInput,
            handler=int_handler
        )
        registry.register(tool1)
        registry.register(tool2)

        result1 = registry.invoke("string_tool", message="test")
        result2 = registry.invoke("int_tool", message="test")

        assert result1.success is True
        assert result1.data == "result"
        assert result2.success is True
        assert result2.data == 42

    def test_handler_returns_list(self, registry):
        """Handler returning list works correctly."""
        def list_handler(message: str) -> list:
            return [1, 2, 3, message]

        tool = ToolDefinition(
            name="list_tool",
            description="Returns list",
            parameters=SimpleInput,
            handler=list_handler
        )
        registry.register(tool)

        result = registry.invoke("list_tool", message="test")

        assert result.success is True
        assert result.data == [1, 2, 3, "test"]

    def test_registry_isolation(self):
        """Multiple registry instances are isolated."""
        registry1 = ToolRegistry()
        registry2 = ToolRegistry()

        tool = ToolDefinition(
            name="isolated_tool",
            description="Test isolation",
            parameters=SimpleInput,
            handler=simple_handler
        )

        registry1.register(tool)

        assert "isolated_tool" in registry1
        assert "isolated_tool" not in registry2

    def test_empty_dict_input(self, registry, simple_tool):
        """Invoking with empty dict for required params fails validation."""
        registry.register(simple_tool)

        result = registry.invoke("simple_tool")

        assert result.success is False
        assert "Validation error" in result.error

    def test_unicode_in_inputs(self, registry, simple_tool):
        """Unicode characters in inputs work correctly."""
        registry.register(simple_tool)

        result = registry.invoke("simple_tool", message="Hello \u4e16\u754c \U0001f44b")

        assert result.success is True
        assert "\u4e16\u754c" in result.data["result"]
