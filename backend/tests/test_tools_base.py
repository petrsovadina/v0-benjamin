"""
Unit tests for Tool Registry base classes (ToolDefinition and ToolResult).

Tests cover:
- ToolDefinition field validation and constraints
- ToolResult structure and factory methods
"""

import pytest
from pydantic import BaseModel, Field

from backend.tools.base import ToolDefinition, ToolResult


# ============================================================================
# Test Fixtures and Helpers
# ============================================================================

class SampleInput(BaseModel):
    """Sample Pydantic model for testing ToolDefinition."""
    query: str = Field(..., description="Search query")
    limit: int = Field(default=10, ge=1, le=100)


def sample_sync_handler(query: str, limit: int = 10) -> dict:
    """Sample synchronous handler function."""
    return {"query": query, "limit": limit}


async def sample_async_handler(query: str, limit: int = 10) -> dict:
    """Sample asynchronous handler function."""
    return {"query": query, "limit": limit}


@pytest.fixture
def valid_tool_definition() -> ToolDefinition:
    """Create a valid ToolDefinition for testing."""
    return ToolDefinition(
        name="test_tool",
        description="A test tool for unit testing",
        parameters=SampleInput,
        handler=sample_sync_handler
    )


@pytest.fixture
def async_tool_definition() -> ToolDefinition:
    """Create a ToolDefinition with async handler."""
    return ToolDefinition(
        name="async_test_tool",
        description="A test tool with async handler",
        parameters=SampleInput,
        handler=sample_async_handler
    )


# ============================================================================
# ToolDefinition Tests
# ============================================================================

class TestToolDefinitionValidation:
    """Tests for ToolDefinition field validation."""

    def test_tool_definition_requires_name(self):
        """ToolDefinition requires a non-empty name."""
        with pytest.raises(ValueError, match="Tool name must be a non-empty string"):
            ToolDefinition(
                name="",
                description="Description",
                parameters=SampleInput,
                handler=sample_sync_handler
            )

    def test_tool_definition_requires_description(self):
        """ToolDefinition requires a non-empty description."""
        with pytest.raises(ValueError, match="Tool description must be a non-empty string"):
            ToolDefinition(
                name="test_tool",
                description="",
                parameters=SampleInput,
                handler=sample_sync_handler
            )

    def test_tool_definition_requires_all_fields(self):
        """ToolDefinition requires name, description, parameters, and handler."""
        # Missing handler
        with pytest.raises(TypeError):
            ToolDefinition(
                name="test",
                description="desc",
                parameters=SampleInput
            )

        # Missing parameters
        with pytest.raises(TypeError):
            ToolDefinition(
                name="test",
                description="desc",
                handler=sample_sync_handler
            )

    def test_tool_definition_valid_creation(self, valid_tool_definition):
        """ToolDefinition can be created with all required valid fields."""
        assert valid_tool_definition.name == "test_tool"
        assert valid_tool_definition.description == "A test tool for unit testing"
        assert valid_tool_definition.parameters is SampleInput
        assert valid_tool_definition.handler is sample_sync_handler

    def test_tool_definition_name_types(self):
        """ToolDefinition name must be a string."""
        with pytest.raises((ValueError, TypeError)):
            ToolDefinition(
                name=None,
                description="Description",
                parameters=SampleInput,
                handler=sample_sync_handler
            )

        with pytest.raises((ValueError, TypeError)):
            ToolDefinition(
                name=123,
                description="Description",
                parameters=SampleInput,
                handler=sample_sync_handler
            )


class TestToolDefinitionHandlerCallable:
    """Tests for ToolDefinition handler validation."""

    def test_handler_must_be_callable(self):
        """Handler must be a callable (function, method, or callable object)."""
        with pytest.raises(TypeError, match="Handler must be callable"):
            ToolDefinition(
                name="test",
                description="desc",
                parameters=SampleInput,
                handler="not_a_function"
            )

        with pytest.raises(TypeError, match="Handler must be callable"):
            ToolDefinition(
                name="test",
                description="desc",
                parameters=SampleInput,
                handler=42
            )

        with pytest.raises(TypeError, match="Handler must be callable"):
            ToolDefinition(
                name="test",
                description="desc",
                parameters=SampleInput,
                handler=None
            )

    def test_handler_accepts_sync_function(self, valid_tool_definition):
        """Handler can be a synchronous function."""
        assert callable(valid_tool_definition.handler)
        assert valid_tool_definition.is_async is False

    def test_handler_accepts_async_function(self, async_tool_definition):
        """Handler can be an asynchronous function."""
        assert callable(async_tool_definition.handler)
        assert async_tool_definition.is_async is True

    def test_handler_accepts_callable_class(self):
        """Handler can be a callable class instance."""
        class CallableHandler:
            def __call__(self, query: str, limit: int = 10) -> dict:
                return {"query": query}

        tool = ToolDefinition(
            name="callable_class_tool",
            description="Tool with callable class handler",
            parameters=SampleInput,
            handler=CallableHandler()
        )
        assert callable(tool.handler)

    def test_handler_accepts_lambda(self):
        """Handler can be a lambda function."""
        tool = ToolDefinition(
            name="lambda_tool",
            description="Tool with lambda handler",
            parameters=SampleInput,
            handler=lambda query, limit=10: {"query": query}
        )
        assert callable(tool.handler)


class TestToolDefinitionParameters:
    """Tests for ToolDefinition parameters validation."""

    def test_parameters_must_be_pydantic_model(self):
        """Parameters must be a Pydantic BaseModel subclass."""
        with pytest.raises(TypeError, match="Parameters must be a Pydantic BaseModel subclass"):
            ToolDefinition(
                name="test",
                description="desc",
                parameters=dict,  # dict is not a BaseModel
                handler=sample_sync_handler
            )

        with pytest.raises(TypeError, match="Parameters must be a Pydantic BaseModel subclass"):
            ToolDefinition(
                name="test",
                description="desc",
                parameters="NotAModel",
                handler=sample_sync_handler
            )

    def test_parameters_accepts_valid_pydantic_model(self, valid_tool_definition):
        """Parameters accepts a valid Pydantic BaseModel subclass."""
        assert issubclass(valid_tool_definition.parameters, BaseModel)

    def test_parameters_with_nested_model(self):
        """Parameters can be a Pydantic model with nested fields."""
        class NestedModel(BaseModel):
            name: str

        class ComplexInput(BaseModel):
            data: NestedModel
            tags: list[str] = []

        tool = ToolDefinition(
            name="complex_tool",
            description="Tool with nested parameters",
            parameters=ComplexInput,
            handler=lambda data, tags=None: {"data": data}
        )
        assert issubclass(tool.parameters, BaseModel)


class TestToolDefinitionIsAsync:
    """Tests for ToolDefinition.is_async property."""

    def test_is_async_false_for_sync_handler(self, valid_tool_definition):
        """is_async returns False for synchronous handlers."""
        assert valid_tool_definition.is_async is False

    def test_is_async_true_for_async_handler(self, async_tool_definition):
        """is_async returns True for asynchronous handlers."""
        assert async_tool_definition.is_async is True


# ============================================================================
# ToolResult Tests
# ============================================================================

class TestToolResultStructure:
    """Tests for ToolResult structure and fields."""

    def test_tool_result_has_success_field(self):
        """ToolResult has a success field (bool)."""
        result = ToolResult(success=True)
        assert hasattr(result, "success")
        assert isinstance(result.success, bool)

    def test_tool_result_has_data_field(self):
        """ToolResult has an optional data field."""
        result = ToolResult(success=True, data={"key": "value"})
        assert hasattr(result, "data")
        assert result.data == {"key": "value"}

        result_none = ToolResult(success=True)
        assert result_none.data is None

    def test_tool_result_has_error_field(self):
        """ToolResult has an optional error field (str)."""
        result = ToolResult(success=False, error="Something went wrong")
        assert hasattr(result, "error")
        assert result.error == "Something went wrong"

        result_none = ToolResult(success=True)
        assert result_none.error is None

    def test_tool_result_has_duration_ms_field(self):
        """ToolResult has an optional duration_ms field (float)."""
        result = ToolResult(success=True, duration_ms=42.5)
        assert hasattr(result, "duration_ms")
        assert result.duration_ms == 42.5

        result_none = ToolResult(success=True)
        assert result_none.duration_ms is None

    def test_tool_result_all_fields(self):
        """ToolResult can be created with all fields."""
        result = ToolResult(
            success=True,
            data={"items": [1, 2, 3]},
            error=None,
            duration_ms=100.0
        )
        assert result.success is True
        assert result.data == {"items": [1, 2, 3]}
        assert result.error is None
        assert result.duration_ms == 100.0

    def test_tool_result_data_accepts_various_types(self):
        """ToolResult data field accepts various types."""
        # Dict
        result = ToolResult(success=True, data={"key": "value"})
        assert result.data == {"key": "value"}

        # List
        result = ToolResult(success=True, data=[1, 2, 3])
        assert result.data == [1, 2, 3]

        # String
        result = ToolResult(success=True, data="result string")
        assert result.data == "result string"

        # Number
        result = ToolResult(success=True, data=42)
        assert result.data == 42

        # Nested structure
        result = ToolResult(success=True, data={"nested": {"data": [1, 2]}})
        assert result.data["nested"]["data"] == [1, 2]


class TestToolResultSuccessFactory:
    """Tests for ToolResult.create_success() factory method."""

    def test_create_success_sets_success_true(self):
        """create_success() sets success=True."""
        result = ToolResult.create_success(data={"key": "value"})
        assert result.success is True

    def test_create_success_sets_data(self):
        """create_success() sets the data field."""
        data = {"drugs": ["Aspirin", "Ibuprofen"]}
        result = ToolResult.create_success(data=data)
        assert result.data == data

    def test_create_success_with_duration(self):
        """create_success() can set duration_ms."""
        result = ToolResult.create_success(data={"result": 1}, duration_ms=150.5)
        assert result.duration_ms == 150.5

    def test_create_success_error_is_none(self):
        """create_success() leaves error as None."""
        result = ToolResult.create_success(data={"result": 1})
        assert result.error is None

    def test_ok_alias(self):
        """ok() is an alias for create_success()."""
        result = ToolResult.ok(data={"key": "value"}, duration_ms=10.0)
        assert result.success is True
        assert result.data == {"key": "value"}
        assert result.duration_ms == 10.0


class TestToolResultFailureFactory:
    """Tests for ToolResult.create_failure() factory method."""

    def test_create_failure_sets_success_false(self):
        """create_failure() sets success=False."""
        result = ToolResult.create_failure(error="Connection timeout")
        assert result.success is False

    def test_create_failure_sets_error(self):
        """create_failure() sets the error field."""
        error_msg = "Database connection failed"
        result = ToolResult.create_failure(error=error_msg)
        assert result.error == error_msg

    def test_create_failure_with_duration(self):
        """create_failure() can set duration_ms."""
        result = ToolResult.create_failure(error="Timeout", duration_ms=5000.0)
        assert result.duration_ms == 5000.0

    def test_create_failure_data_is_none(self):
        """create_failure() leaves data as None."""
        result = ToolResult.create_failure(error="Error occurred")
        assert result.data is None

    def test_fail_alias(self):
        """fail() is an alias for create_failure()."""
        result = ToolResult.fail(error="Something failed", duration_ms=100.0)
        assert result.success is False
        assert result.error == "Something failed"
        assert result.duration_ms == 100.0


class TestToolResultSerialization:
    """Tests for ToolResult serialization (Pydantic model)."""

    def test_tool_result_to_dict(self):
        """ToolResult can be serialized to dict."""
        result = ToolResult(
            success=True,
            data={"key": "value"},
            duration_ms=42.0
        )
        result_dict = result.model_dump()

        assert result_dict["success"] is True
        assert result_dict["data"] == {"key": "value"}
        assert result_dict["duration_ms"] == 42.0
        assert result_dict["error"] is None

    def test_tool_result_to_json(self):
        """ToolResult can be serialized to JSON."""
        result = ToolResult(
            success=False,
            error="Test error",
            duration_ms=100.0
        )
        json_str = result.model_dump_json()

        assert '"success": false' in json_str or '"success":false' in json_str
        assert "Test error" in json_str

    def test_tool_result_from_dict(self):
        """ToolResult can be created from dict."""
        data = {
            "success": True,
            "data": {"result": 42},
            "error": None,
            "duration_ms": 50.0
        }
        result = ToolResult.model_validate(data)

        assert result.success is True
        assert result.data == {"result": 42}
        assert result.duration_ms == 50.0
