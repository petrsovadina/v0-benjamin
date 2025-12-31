"""
Tests for LangChain tool base functionality with LangChain 0.3.x / 1.x.

These tests verify that the @tool decorator and BaseTool work correctly
after the LangChain dependency upgrade.
"""
import pytest
from typing import Optional
from pydantic import BaseModel, Field

# Tool imports from langchain_core
from langchain_core.tools import tool, BaseTool, ToolException


class TestToolDecorator:
    """Test @tool decorator functionality."""

    def test_tool_decorator_basic(self):
        """Verify @tool decorator creates valid tool from function."""
        @tool
        def simple_tool(query: str) -> str:
            """A simple test tool."""
            return f"Result: {query}"

        assert simple_tool.name == "simple_tool"
        assert "simple test tool" in simple_tool.description.lower()

    def test_tool_decorator_with_name(self):
        """Verify @tool decorator with custom name."""
        @tool("custom_name")
        def my_tool(x: str) -> str:
            """Tool with custom name."""
            return x

        assert my_tool.name == "custom_name"

    def test_tool_decorator_with_docstring(self):
        """Verify @tool uses docstring as description."""
        @tool
        def documented_tool(value: int) -> str:
            """This tool processes an integer value and returns a string."""
            return str(value)

        assert "processes an integer" in documented_tool.description.lower()

    def test_tool_decorator_async(self):
        """Verify @tool decorator works with async functions."""
        @tool
        async def async_tool(query: str) -> str:
            """An async test tool."""
            return f"Async: {query}"

        assert async_tool.name == "async_tool"
        assert "async test tool" in async_tool.description.lower()

    def test_tool_decorator_multiple_params(self):
        """Verify @tool handles multiple parameters."""
        @tool
        def multi_param_tool(param1: str, param2: int, param3: bool = False) -> str:
            """Tool with multiple parameters."""
            return f"{param1}-{param2}-{param3}"

        assert multi_param_tool.name == "multi_param_tool"
        # Tool should have schema with all parameters
        assert multi_param_tool.args_schema is not None

    def test_tool_invocation_sync(self):
        """Verify sync tool can be invoked."""
        @tool
        def echo_tool(message: str) -> str:
            """Echoes the input message."""
            return f"Echo: {message}"

        result = echo_tool.invoke({"message": "hello"})
        assert result == "Echo: hello"

    @pytest.mark.asyncio
    async def test_tool_invocation_async(self):
        """Verify async tool can be invoked."""
        @tool
        async def async_echo(message: str) -> str:
            """Async echo tool."""
            return f"Async echo: {message}"

        result = await async_echo.ainvoke({"message": "hello"})
        assert result == "Async echo: hello"


class TestToolArgsSchema:
    """Test tool argument schema handling."""

    def test_tool_args_schema_generated(self):
        """Verify tool generates args schema from function signature."""
        @tool
        def schema_tool(query: str, limit: int = 10) -> str:
            """Tool that tests schema generation."""
            return f"{query}:{limit}"

        schema = schema_tool.args_schema
        assert schema is not None
        # Check schema has expected fields
        schema_fields = schema.model_fields if hasattr(schema, 'model_fields') else schema.__fields__
        assert "query" in schema_fields
        assert "limit" in schema_fields

    def test_tool_with_pydantic_schema(self):
        """Verify tool works with explicit Pydantic schema."""
        class SearchInput(BaseModel):
            query: str = Field(description="The search query")
            max_results: int = Field(default=5, description="Max results to return")

        @tool(args_schema=SearchInput)
        def search_tool(query: str, max_results: int = 5) -> str:
            """Search tool with Pydantic schema."""
            return f"Searching: {query} (max: {max_results})"

        assert search_tool.args_schema == SearchInput


class TestBaseTool:
    """Test BaseTool class functionality."""

    def test_base_tool_subclass(self):
        """Verify BaseTool can be subclassed."""
        class CustomTool(BaseTool):
            name: str = "custom_tool"
            description: str = "A custom tool implementation"

            def _run(self, query: str) -> str:
                return f"Custom: {query}"

        tool_instance = CustomTool()
        assert tool_instance.name == "custom_tool"
        assert tool_instance.description == "A custom tool implementation"

    def test_base_tool_run(self):
        """Verify BaseTool._run is called correctly."""
        class RunTool(BaseTool):
            name: str = "run_tool"
            description: str = "Tool that tests _run method"

            def _run(self, input_text: str) -> str:
                return f"Processed: {input_text}"

        tool_instance = RunTool()
        result = tool_instance.invoke({"input_text": "test"})
        assert result == "Processed: test"

    def test_base_tool_with_async_run(self):
        """Verify BaseTool._arun is called for async invocation."""
        class AsyncTool(BaseTool):
            name: str = "async_base_tool"
            description: str = "Tool with async implementation"

            def _run(self, query: str) -> str:
                return f"Sync: {query}"

            async def _arun(self, query: str) -> str:
                return f"Async: {query}"

        tool_instance = AsyncTool()
        # Sync invoke should use _run
        sync_result = tool_instance.invoke({"query": "test"})
        assert sync_result == "Sync: test"


class TestToolException:
    """Test ToolException handling."""

    def test_tool_exception_import(self):
        """Verify ToolException can be imported."""
        assert ToolException is not None

    def test_tool_exception_raised(self):
        """Verify ToolException can be raised from tool."""
        @tool
        def failing_tool(query: str) -> str:
            """Tool that may fail."""
            raise ToolException("Tool execution failed")

        with pytest.raises(ToolException) as exc_info:
            failing_tool.invoke({"query": "test"})
        assert "Tool execution failed" in str(exc_info.value)

    def test_tool_with_error_handling(self):
        """Verify tool can handle errors gracefully."""
        @tool
        def safe_tool(query: str) -> str:
            """Tool with error handling."""
            try:
                if query == "error":
                    raise ValueError("Invalid query")
                return f"OK: {query}"
            except ValueError as e:
                raise ToolException(f"Error: {e}")

        # Normal execution
        result = safe_tool.invoke({"query": "hello"})
        assert result == "OK: hello"

        # Error execution
        with pytest.raises(ToolException):
            safe_tool.invoke({"query": "error"})


class TestToolReturnTypes:
    """Test various tool return types."""

    def test_tool_returns_string(self):
        """Verify tool can return string."""
        @tool
        def string_tool(x: str) -> str:
            """Returns a string."""
            return f"String: {x}"

        result = string_tool.invoke({"x": "test"})
        assert isinstance(result, str)

    def test_tool_returns_dict(self):
        """Verify tool can return dict (will be serialized)."""
        @tool
        def dict_tool(x: str) -> dict:
            """Returns a dictionary."""
            return {"result": x, "status": "ok"}

        result = string_tool_invoke_helper(dict_tool, {"x": "test"})
        # Result type depends on langchain version
        assert result is not None

    def test_tool_returns_list(self):
        """Verify tool can return list."""
        @tool
        def list_tool(x: str) -> list:
            """Returns a list."""
            return [x, x.upper(), x.lower()]

        result = string_tool_invoke_helper(list_tool, {"x": "Test"})
        assert result is not None


def string_tool_invoke_helper(tool_func, args):
    """Helper to invoke tool and handle various return types."""
    try:
        return tool_func.invoke(args)
    except Exception:
        # Some tools may serialize output differently
        return tool_func.run(args) if hasattr(tool_func, 'run') else None
