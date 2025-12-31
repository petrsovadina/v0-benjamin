"""
Tests for tool registration and management with LangChain 0.3.x / 1.x.

These tests verify that tools can be registered, listed, and bound to LLMs
correctly after the LangChain dependency upgrade.
"""
import pytest
from typing import List

# Tool imports
from langchain_core.tools import tool, BaseTool
from langgraph.prebuilt import ToolNode


class TestToolCollection:
    """Test managing collections of tools."""

    def test_tools_list_creation(self):
        """Verify a list of tools can be created."""
        @tool
        def tool_a(x: str) -> str:
            """Tool A."""
            return f"A: {x}"

        @tool
        def tool_b(x: str) -> str:
            """Tool B."""
            return f"B: {x}"

        @tool
        def tool_c(x: str) -> str:
            """Tool C."""
            return f"C: {x}"

        tools = [tool_a, tool_b, tool_c]
        assert len(tools) == 3
        assert all(hasattr(t, 'name') for t in tools)

    def test_tools_unique_names(self):
        """Verify tools in collection have unique names."""
        @tool
        def first_tool(x: str) -> str:
            """First tool."""
            return x

        @tool("unique_name")
        def second_tool(x: str) -> str:
            """Second tool with custom name."""
            return x

        tools = [first_tool, second_tool]
        names = [t.name for t in tools]
        assert len(names) == len(set(names)), "Tool names should be unique"

    def test_tools_by_name_lookup(self):
        """Verify tools can be looked up by name."""
        @tool
        def lookup_tool_alpha(x: str) -> str:
            """Alpha tool."""
            return f"Alpha: {x}"

        @tool
        def lookup_tool_beta(x: str) -> str:
            """Beta tool."""
            return f"Beta: {x}"

        tools = [lookup_tool_alpha, lookup_tool_beta]
        tool_map = {t.name: t for t in tools}

        assert "lookup_tool_alpha" in tool_map
        assert "lookup_tool_beta" in tool_map
        assert tool_map["lookup_tool_alpha"].invoke({"x": "test"}) == "Alpha: test"


class TestToolNode:
    """Test ToolNode functionality for managing tools in graphs."""

    def test_tool_node_creation_empty(self):
        """Verify ToolNode can be created with empty tools list."""
        # Empty tools list should work (though not useful)
        tool_node = ToolNode([])
        assert tool_node is not None

    def test_tool_node_creation_with_tools(self):
        """Verify ToolNode can be created with tools."""
        @tool
        def node_tool_a(query: str) -> str:
            """Node tool A."""
            return f"A: {query}"

        @tool
        def node_tool_b(query: str) -> str:
            """Node tool B."""
            return f"B: {query}"

        tool_node = ToolNode([node_tool_a, node_tool_b])
        assert tool_node is not None

    def test_tool_node_with_async_tools(self):
        """Verify ToolNode works with async tools."""
        @tool
        async def async_node_tool(query: str) -> str:
            """Async tool for ToolNode."""
            return f"Async: {query}"

        tool_node = ToolNode([async_node_tool])
        assert tool_node is not None

    def test_tool_node_with_mixed_tools(self):
        """Verify ToolNode works with mixed sync/async tools."""
        @tool
        def sync_tool(x: str) -> str:
            """Sync tool."""
            return f"Sync: {x}"

        @tool
        async def async_tool(x: str) -> str:
            """Async tool."""
            return f"Async: {x}"

        tool_node = ToolNode([sync_tool, async_tool])
        assert tool_node is not None


class TestToolBinding:
    """Test binding tools to LLMs."""

    def test_tools_can_be_schema_formatted(self):
        """Verify tools can be converted to schema format for LLM binding."""
        @tool
        def schema_format_tool(query: str, limit: int = 10) -> str:
            """Tool to test schema formatting."""
            return f"{query}:{limit}"

        # Tools should have schema that can be serialized
        schema = schema_format_tool.args_schema
        assert schema is not None

        # Schema should be convertible to dict for API calls
        schema_dict = schema.model_json_schema() if hasattr(schema, 'model_json_schema') else schema.schema()
        assert isinstance(schema_dict, dict)
        assert "properties" in schema_dict

    def test_multiple_tools_schema_formatting(self):
        """Verify multiple tools can have their schemas formatted."""
        @tool
        def tool_x(a: str) -> str:
            """Tool X."""
            return a

        @tool
        def tool_y(b: int, c: str = "default") -> str:
            """Tool Y with multiple params."""
            return f"{b}:{c}"

        tools = [tool_x, tool_y]
        schemas = []
        for t in tools:
            if hasattr(t.args_schema, 'model_json_schema'):
                schemas.append(t.args_schema.model_json_schema())
            else:
                schemas.append(t.args_schema.schema())

        assert len(schemas) == 2
        assert all(isinstance(s, dict) for s in schemas)


class TestToolNaming:
    """Test tool naming conventions and validation."""

    def test_tool_name_from_function(self):
        """Verify tool name defaults to function name."""
        @tool
        def my_function_name(x: str) -> str:
            """Test tool."""
            return x

        assert my_function_name.name == "my_function_name"

    def test_tool_name_custom(self):
        """Verify tool name can be customized."""
        @tool("custom_tool_name")
        def original_name(x: str) -> str:
            """Test tool with custom name."""
            return x

        assert original_name.name == "custom_tool_name"

    def test_tool_name_with_underscores(self):
        """Verify tool names with underscores work."""
        @tool
        def tool_with_underscores_in_name(x: str) -> str:
            """Tool with underscores."""
            return x

        assert "_" in tool_with_underscores_in_name.name

    def test_tool_description_from_docstring(self):
        """Verify tool description comes from docstring."""
        @tool
        def well_documented_tool(param: str) -> str:
            """This is a comprehensive description of what the tool does.

            It can span multiple lines and provide detailed information
            about the tool's purpose and usage.
            """
            return param

        assert "comprehensive description" in well_documented_tool.description.lower()


class TestToolRegistry:
    """Test tool registry patterns used in the project."""

    def test_registry_pattern(self):
        """Verify tools can be registered in a registry pattern."""
        # Simple registry implementation
        tool_registry = {}

        @tool
        def registered_tool_1(x: str) -> str:
            """Registered tool 1."""
            return f"R1: {x}"

        @tool
        def registered_tool_2(x: str) -> str:
            """Registered tool 2."""
            return f"R2: {x}"

        # Register tools
        tool_registry[registered_tool_1.name] = registered_tool_1
        tool_registry[registered_tool_2.name] = registered_tool_2

        assert len(tool_registry) == 2
        assert "registered_tool_1" in tool_registry
        assert "registered_tool_2" in tool_registry

    def test_get_all_tools_from_registry(self):
        """Verify all tools can be retrieved from registry."""
        # Create tools with proper docstrings
        @tool
        def registry_tool_0(x: str) -> str:
            """Registry tool 0."""
            return f"D0: {x}"

        @tool
        def registry_tool_1(x: str) -> str:
            """Registry tool 1."""
            return f"D1: {x}"

        @tool
        def registry_tool_2(x: str) -> str:
            """Registry tool 2."""
            return f"D2: {x}"

        @tool
        def registry_tool_3(x: str) -> str:
            """Registry tool 3."""
            return f"D3: {x}"

        @tool
        def registry_tool_4(x: str) -> str:
            """Registry tool 4."""
            return f"D4: {x}"

        registry = {
            "tool_0": registry_tool_0,
            "tool_1": registry_tool_1,
            "tool_2": registry_tool_2,
            "tool_3": registry_tool_3,
            "tool_4": registry_tool_4,
        }

        all_tools = list(registry.values())
        assert len(all_tools) == 5

    def test_registry_with_categories(self):
        """Verify tools can be organized by category."""
        categorized_registry = {
            "search": [],
            "retrieval": [],
            "computation": []
        }

        @tool
        def search_web(query: str) -> str:
            """Search the web."""
            return f"Web: {query}"

        @tool
        def search_db(query: str) -> str:
            """Search database."""
            return f"DB: {query}"

        @tool
        def retrieve_docs(doc_id: str) -> str:
            """Retrieve documents."""
            return f"Doc: {doc_id}"

        @tool
        def compute_sum(a: int, b: int) -> str:
            """Compute sum."""
            return str(a + b)

        categorized_registry["search"].extend([search_web, search_db])
        categorized_registry["retrieval"].append(retrieve_docs)
        categorized_registry["computation"].append(compute_sum)

        assert len(categorized_registry["search"]) == 2
        assert len(categorized_registry["retrieval"]) == 1
        assert len(categorized_registry["computation"]) == 1

        # Get all tools flattened
        all_tools = []
        for category_tools in categorized_registry.values():
            all_tools.extend(category_tools)
        assert len(all_tools) == 4
