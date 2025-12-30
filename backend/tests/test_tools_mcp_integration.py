"""
Integration tests for MCP server wrappers through the Tool Registry.

Tests verify that:
- SUKL MCP wrapper is callable through the registry
- PubMed MCP wrapper is callable through the registry
- Registry lists all registered MCP tools correctly
- Tool metadata (description, parameter schema) is retrievable

External dependencies (Supabase, PubMed API) are mocked to ensure
tests are isolated and repeatable.

NOTE: The actual MCP servers require external dependencies (mcp, paper_search_mcp,
supabase) which may not be available in all environments. This test module creates
mock tool definitions with the same schemas as the real tools to verify the
registry integration works correctly without requiring external dependencies.
"""

import asyncio
import json
import pytest
from unittest.mock import patch, MagicMock

from backend.tools import ToolRegistry, ToolDefinition, ToolResult
from backend.tools import get_registry, init_default_registry
from backend.tools.mcp.sukl import (
    SuklSearchInput,
    SuklDrugDetailInput,
    sukl_search_drugs,
    sukl_get_drug_details,
    register_sukl_tools,
    SUKL_TOOLS,
)
from backend.tools.mcp.pubmed import (
    PubMedSearchInput,
    pubmed_search_literature,
    register_pubmed_tools,
    PUBMED_TOOLS,
)


# ============================================================================
# Mock Handler Functions
# ============================================================================


async def mock_sukl_search_drugs(query: str) -> str:
    """Mock handler for SUKL drug search."""
    return json.dumps([
        {"nazev": "Paralen", "ucinna_latka": "paracetamol", "sukl_kod": "0012345"},
        {"nazev": "Panadol", "ucinna_latka": "paracetamol", "sukl_kod": "0067890"},
    ])


async def mock_sukl_get_drug_details(sukl_code: str) -> str:
    """Mock handler for SUKL drug details."""
    return json.dumps({
        "nazev": "Paralen",
        "ucinna_latka": "paracetamol",
        "sukl_kod": sukl_code,
        "forma": "tablety",
        "sila": "500mg",
    })


async def mock_pubmed_search_literature(query: str, max_results: int = 5) -> str:
    """Mock handler for PubMed literature search."""
    return json.dumps({
        "status": "success",
        "source": "pubmed",
        "query": query,
        "results": [
            {"title": "Diabetes Study 1", "pmid": "12345"},
            {"title": "Diabetes Study 2", "pmid": "67890"},
        ][:max_results]
    })


async def mock_sukl_search_error(query: str) -> str:
    """Mock handler that raises an error."""
    raise Exception("Database connection failed")


async def mock_pubmed_search_error(query: str, max_results: int = 5) -> str:
    """Mock handler that raises an error."""
    raise Exception("API request failed")


# ============================================================================
# Test Fixtures
# ============================================================================


@pytest.fixture
def fresh_registry() -> ToolRegistry:
    """Create a fresh, empty ToolRegistry for each test."""
    return ToolRegistry()


@pytest.fixture
def mock_sukl_search_tool() -> ToolDefinition:
    """Create a mock SUKL search tool with same schema as real tool."""
    return ToolDefinition(
        name="sukl_search_drugs",
        description=sukl_search_drugs.description,
        parameters=SuklSearchInput,
        handler=mock_sukl_search_drugs,
    )


@pytest.fixture
def mock_sukl_details_tool() -> ToolDefinition:
    """Create a mock SUKL details tool with same schema as real tool."""
    return ToolDefinition(
        name="sukl_get_drug_details",
        description=sukl_get_drug_details.description,
        parameters=SuklDrugDetailInput,
        handler=mock_sukl_get_drug_details,
    )


@pytest.fixture
def mock_pubmed_tool() -> ToolDefinition:
    """Create a mock PubMed tool with same schema as real tool."""
    return ToolDefinition(
        name="pubmed_search_literature",
        description=pubmed_search_literature.description,
        parameters=PubMedSearchInput,
        handler=mock_pubmed_search_literature,
    )


@pytest.fixture
def registry_with_mock_sukl(
    fresh_registry, mock_sukl_search_tool, mock_sukl_details_tool
) -> ToolRegistry:
    """Create a registry with mock SUKL tools registered."""
    fresh_registry.register(mock_sukl_search_tool)
    fresh_registry.register(mock_sukl_details_tool)
    return fresh_registry


@pytest.fixture
def registry_with_mock_pubmed(fresh_registry, mock_pubmed_tool) -> ToolRegistry:
    """Create a registry with mock PubMed tool registered."""
    fresh_registry.register(mock_pubmed_tool)
    return fresh_registry


@pytest.fixture
def registry_with_all_mock_mcp(
    fresh_registry, mock_sukl_search_tool, mock_sukl_details_tool, mock_pubmed_tool
) -> ToolRegistry:
    """Create a registry with all mock MCP tools registered."""
    fresh_registry.register(mock_sukl_search_tool)
    fresh_registry.register(mock_sukl_details_tool)
    fresh_registry.register(mock_pubmed_tool)
    return fresh_registry


@pytest.fixture
def registry_with_real_tool_definitions(fresh_registry) -> ToolRegistry:
    """Create a registry with real tool definitions (for metadata tests)."""
    register_sukl_tools(fresh_registry)
    register_pubmed_tools(fresh_registry)
    return fresh_registry


# ============================================================================
# SUKL MCP Wrapper Integration Tests
# ============================================================================


class TestMcpSuklWrapper:
    """Tests for SUKL MCP wrapper through the registry."""

    def test_sukl_search_drugs_through_registry(self, registry_with_mock_sukl):
        """SUKL search_drugs is callable through registry."""
        result = registry_with_mock_sukl.invoke("sukl_search_drugs", query="paracetamol")

        assert isinstance(result, ToolResult)
        assert result.success is True
        assert result.data is not None
        assert result.error is None
        assert result.duration_ms is not None
        assert result.duration_ms >= 0

        # Verify response content
        data = json.loads(result.data)
        assert len(data) == 2
        assert data[0]["nazev"] == "Paralen"

    def test_sukl_search_drugs_async_through_registry(self, registry_with_mock_sukl):
        """SUKL search_drugs works via invoke_async."""

        async def run_test():
            return await registry_with_mock_sukl.invoke_async(
                "sukl_search_drugs", query="paracetamol"
            )

        result = asyncio.run(run_test())

        assert result.success is True
        assert result.data is not None

    def test_sukl_get_drug_details_through_registry(self, registry_with_mock_sukl):
        """SUKL get_drug_details is callable through registry."""
        result = registry_with_mock_sukl.invoke(
            "sukl_get_drug_details", sukl_code="0012345"
        )

        assert isinstance(result, ToolResult)
        assert result.success is True
        assert result.data is not None

        # Verify response content
        data = json.loads(result.data)
        assert data["sukl_kod"] == "0012345"
        assert data["nazev"] == "Paralen"

    def test_sukl_tools_validation_error(self, registry_with_mock_sukl):
        """SUKL tools return validation error for invalid inputs."""
        # Empty query should fail validation (min_length=1)
        result = registry_with_mock_sukl.invoke("sukl_search_drugs", query="")

        assert result.success is False
        assert "Validation error" in result.error

    def test_sukl_tools_missing_param_error(self, registry_with_mock_sukl):
        """SUKL tools return validation error for missing required params."""
        # Missing required 'query' parameter
        result = registry_with_mock_sukl.invoke("sukl_search_drugs")

        assert result.success is False
        assert "Validation error" in result.error

    def test_sukl_wrapper_returns_expected_data_structure(self, registry_with_mock_sukl):
        """SUKL wrapper returns expected data structure."""
        result = registry_with_mock_sukl.invoke(
            "sukl_search_drugs", query="paracetamol"
        )

        assert result.success is True
        data = json.loads(result.data)
        assert isinstance(data, list)
        assert len(data) > 0
        assert "nazev" in data[0]
        assert "ucinna_latka" in data[0]


# ============================================================================
# PubMed MCP Wrapper Integration Tests
# ============================================================================


class TestMcpPubmedWrapper:
    """Tests for PubMed MCP wrapper through the registry."""

    def test_pubmed_search_through_registry(self, registry_with_mock_pubmed):
        """PubMed search_literature is callable through registry."""
        result = registry_with_mock_pubmed.invoke(
            "pubmed_search_literature", query="diabetes treatment"
        )

        assert isinstance(result, ToolResult)
        assert result.success is True
        assert result.data is not None
        assert result.error is None
        assert result.duration_ms is not None

    def test_pubmed_search_async_through_registry(self, registry_with_mock_pubmed):
        """PubMed search_literature works via invoke_async."""

        async def run_test():
            return await registry_with_mock_pubmed.invoke_async(
                "pubmed_search_literature", query="diabetes treatment"
            )

        result = asyncio.run(run_test())

        assert result.success is True
        assert result.data is not None

    def test_pubmed_search_with_max_results(self, registry_with_mock_pubmed):
        """PubMed search respects max_results parameter."""
        result = registry_with_mock_pubmed.invoke(
            "pubmed_search_literature", query="diabetes", max_results=1
        )

        assert result.success is True
        data = json.loads(result.data)
        # Mock handler respects max_results
        assert len(data["results"]) <= 1

    def test_pubmed_search_default_max_results(self, registry_with_mock_pubmed):
        """PubMed search uses default max_results=5."""
        result = registry_with_mock_pubmed.invoke(
            "pubmed_search_literature", query="diabetes"
        )

        assert result.success is True
        data = json.loads(result.data)
        assert data["status"] == "success"

    def test_pubmed_validation_error_empty_query(self, registry_with_mock_pubmed):
        """PubMed returns validation error for empty query."""
        result = registry_with_mock_pubmed.invoke("pubmed_search_literature", query="")

        assert result.success is False
        assert "Validation error" in result.error

    def test_pubmed_validation_error_invalid_max_results(self, registry_with_mock_pubmed):
        """PubMed returns validation error for invalid max_results."""
        # max_results must be >= 1
        result = registry_with_mock_pubmed.invoke(
            "pubmed_search_literature", query="test", max_results=0
        )
        assert result.success is False
        assert "Validation error" in result.error

        # max_results must be <= 100
        result = registry_with_mock_pubmed.invoke(
            "pubmed_search_literature", query="test", max_results=200
        )
        assert result.success is False
        assert "Validation error" in result.error

    def test_pubmed_returns_json_structure(self, registry_with_mock_pubmed):
        """PubMed wrapper returns properly formatted JSON response."""
        result = registry_with_mock_pubmed.invoke(
            "pubmed_search_literature", query="diabetes"
        )

        assert result.success is True
        # Parse the JSON response
        response_data = json.loads(result.data)
        assert response_data["status"] == "success"
        assert response_data["source"] == "pubmed"
        assert response_data["query"] == "diabetes"
        assert "results" in response_data
        assert len(response_data["results"]) == 2


# ============================================================================
# Registry Tool Listing Tests
# ============================================================================


class TestRegistryListTools:
    """Tests for listing registered MCP tools."""

    def test_list_sukl_tools(self, registry_with_mock_sukl):
        """Registry lists all SUKL tools."""
        tools = registry_with_mock_sukl.list_tools()

        assert len(tools) == 2
        assert "sukl_search_drugs" in tools
        assert "sukl_get_drug_details" in tools

    def test_list_pubmed_tools(self, registry_with_mock_pubmed):
        """Registry lists all PubMed tools."""
        tools = registry_with_mock_pubmed.list_tools()

        assert len(tools) == 1
        assert "pubmed_search_literature" in tools

    def test_list_all_mcp_tools(self, registry_with_all_mock_mcp):
        """Registry lists all registered MCP tools."""
        tools = registry_with_all_mock_mcp.list_tools()

        assert len(tools) == 3
        assert "sukl_search_drugs" in tools
        assert "sukl_get_drug_details" in tools
        assert "pubmed_search_literature" in tools

    def test_list_tools_returns_sorted(self, registry_with_all_mock_mcp):
        """list_tools() returns alphabetically sorted list."""
        tools = registry_with_all_mock_mcp.list_tools()

        assert tools == sorted(tools)
        assert tools == [
            "pubmed_search_literature",
            "sukl_get_drug_details",
            "sukl_search_drugs",
        ]

    def test_sukl_tools_constant(self):
        """SUKL_TOOLS contains all SUKL tool definitions."""
        assert len(SUKL_TOOLS) == 2
        assert sukl_search_drugs in SUKL_TOOLS
        assert sukl_get_drug_details in SUKL_TOOLS

    def test_pubmed_tools_constant(self):
        """PUBMED_TOOLS contains all PubMed tool definitions."""
        assert len(PUBMED_TOOLS) == 1
        assert pubmed_search_literature in PUBMED_TOOLS


# ============================================================================
# Tool Metadata Retrieval Tests
# ============================================================================


class TestToolMetadataRetrieval:
    """Tests for retrieving tool metadata through the registry."""

    def test_get_sukl_search_tool_definition(self, registry_with_real_tool_definitions):
        """Can retrieve SUKL search tool definition."""
        tool = registry_with_real_tool_definitions.get_tool("sukl_search_drugs")

        assert isinstance(tool, ToolDefinition)
        assert tool.name == "sukl_search_drugs"
        assert "SUKL" in tool.description
        assert "drug" in tool.description.lower()

    def test_get_sukl_details_tool_definition(self, registry_with_real_tool_definitions):
        """Can retrieve SUKL details tool definition."""
        tool = registry_with_real_tool_definitions.get_tool("sukl_get_drug_details")

        assert isinstance(tool, ToolDefinition)
        assert tool.name == "sukl_get_drug_details"
        assert "SUKL" in tool.description

    def test_get_pubmed_tool_definition(self, registry_with_real_tool_definitions):
        """Can retrieve PubMed tool definition."""
        tool = registry_with_real_tool_definitions.get_tool("pubmed_search_literature")

        assert isinstance(tool, ToolDefinition)
        assert tool.name == "pubmed_search_literature"
        assert "PubMed" in tool.description

    def test_sukl_search_parameters_schema(self, registry_with_real_tool_definitions):
        """SUKL search tool has correct parameter schema."""
        tool = registry_with_real_tool_definitions.get_tool("sukl_search_drugs")

        assert tool.parameters is SuklSearchInput
        # Verify schema has expected fields
        schema = tool.parameters.model_json_schema()
        assert "query" in schema["properties"]
        assert schema["required"] == ["query"]

    def test_sukl_details_parameters_schema(self, registry_with_real_tool_definitions):
        """SUKL details tool has correct parameter schema."""
        tool = registry_with_real_tool_definitions.get_tool("sukl_get_drug_details")

        assert tool.parameters is SuklDrugDetailInput
        schema = tool.parameters.model_json_schema()
        assert "sukl_code" in schema["properties"]
        assert schema["required"] == ["sukl_code"]

    def test_pubmed_parameters_schema(self, registry_with_real_tool_definitions):
        """PubMed tool has correct parameter schema."""
        tool = registry_with_real_tool_definitions.get_tool("pubmed_search_literature")

        assert tool.parameters is PubMedSearchInput
        schema = tool.parameters.model_json_schema()
        assert "query" in schema["properties"]
        assert "max_results" in schema["properties"]
        assert schema["required"] == ["query"]

    def test_tool_has_callable_handler(self, registry_with_real_tool_definitions):
        """All MCP tools have callable handlers."""
        for tool_name in registry_with_real_tool_definitions.list_tools():
            tool = registry_with_real_tool_definitions.get_tool(tool_name)
            assert callable(tool.handler)

    def test_tool_handlers_are_async(self, registry_with_real_tool_definitions):
        """All MCP tool handlers are async."""
        for tool_name in registry_with_real_tool_definitions.list_tools():
            tool = registry_with_real_tool_definitions.get_tool(tool_name)
            assert tool.is_async is True


# ============================================================================
# Singleton Registry Tests
# ============================================================================


class TestSingletonRegistry:
    """Tests for the singleton registry pattern."""

    def test_get_registry_returns_same_instance(self):
        """get_registry() returns the same singleton instance."""
        # Reset the singleton for testing
        import backend.tools

        original_registry = backend.tools._default_registry
        backend.tools._default_registry = None

        try:
            registry1 = get_registry()
            registry2 = get_registry()

            assert registry1 is registry2
        finally:
            # Restore original
            backend.tools._default_registry = original_registry

    def test_init_default_registry_registers_all_tools(self):
        """init_default_registry() registers all MCP tools."""
        import backend.tools

        original_registry = backend.tools._default_registry
        backend.tools._default_registry = None

        try:
            registry = init_default_registry()

            tools = registry.list_tools()
            assert len(tools) == 3
            assert "sukl_search_drugs" in tools
            assert "sukl_get_drug_details" in tools
            assert "pubmed_search_literature" in tools
        finally:
            backend.tools._default_registry = original_registry

    def test_init_default_registry_is_idempotent(self):
        """init_default_registry() can be called multiple times safely."""
        import backend.tools

        original_registry = backend.tools._default_registry
        backend.tools._default_registry = None

        try:
            # Call multiple times
            registry1 = init_default_registry()
            registry2 = init_default_registry()

            # Should be same instance
            assert registry1 is registry2
            # Should still have correct tools
            assert len(registry1.list_tools()) == 3
        finally:
            backend.tools._default_registry = original_registry


# ============================================================================
# Error Handling Tests
# ============================================================================


class TestMcpErrorHandling:
    """Tests for MCP wrapper error handling."""

    def test_sukl_handler_error_returns_failure_result(self, fresh_registry):
        """SUKL handler errors are caught and returned as ToolResult failure."""
        error_tool = ToolDefinition(
            name="sukl_search_drugs",
            description="Test tool that errors",
            parameters=SuklSearchInput,
            handler=mock_sukl_search_error,
        )
        fresh_registry.register(error_tool)

        result = fresh_registry.invoke("sukl_search_drugs", query="test")

        assert result.success is False
        assert "Handler error" in result.error
        assert "Database connection failed" in result.error

    def test_pubmed_handler_error_returns_failure_result(self, fresh_registry):
        """PubMed handler errors are caught and returned as ToolResult failure."""
        error_tool = ToolDefinition(
            name="pubmed_search_literature",
            description="Test tool that errors",
            parameters=PubMedSearchInput,
            handler=mock_pubmed_search_error,
        )
        fresh_registry.register(error_tool)

        result = fresh_registry.invoke("pubmed_search_literature", query="test")

        # Handler exception is caught and returned as ToolResult failure
        assert result.success is False
        assert "Handler error" in result.error
        assert "API request failed" in result.error

    def test_nonexistent_tool_raises_keyerror(self, registry_with_all_mock_mcp):
        """Invoking non-existent tool raises KeyError."""
        with pytest.raises(KeyError, match="not registered"):
            registry_with_all_mock_mcp.invoke("nonexistent_tool", query="test")


# ============================================================================
# Input Model Validation Tests
# ============================================================================


class TestInputModelValidation:
    """Tests for Pydantic input model validation."""

    def test_sukl_search_input_valid(self):
        """SuklSearchInput accepts valid data."""
        input_data = SuklSearchInput(query="aspirin")
        assert input_data.query == "aspirin"

    def test_sukl_search_input_min_length(self):
        """SuklSearchInput enforces min_length on query."""
        with pytest.raises(Exception):  # Pydantic ValidationError
            SuklSearchInput(query="")

    def test_sukl_drug_detail_input_valid(self):
        """SuklDrugDetailInput accepts valid data."""
        input_data = SuklDrugDetailInput(sukl_code="0012345")
        assert input_data.sukl_code == "0012345"

    def test_pubmed_search_input_valid(self):
        """PubMedSearchInput accepts valid data."""
        input_data = PubMedSearchInput(query="diabetes", max_results=10)
        assert input_data.query == "diabetes"
        assert input_data.max_results == 10

    def test_pubmed_search_input_default_max_results(self):
        """PubMedSearchInput uses default max_results."""
        input_data = PubMedSearchInput(query="test")
        assert input_data.max_results == 5

    def test_pubmed_search_input_max_results_bounds(self):
        """PubMedSearchInput enforces max_results bounds (1-100)."""
        # Valid boundary values
        PubMedSearchInput(query="test", max_results=1)
        PubMedSearchInput(query="test", max_results=100)

        # Invalid values
        with pytest.raises(Exception):
            PubMedSearchInput(query="test", max_results=0)
        with pytest.raises(Exception):
            PubMedSearchInput(query="test", max_results=101)


# ============================================================================
# Logging Integration Tests
# ============================================================================


class TestMcpLogging:
    """Tests for logging integration with MCP wrappers."""

    def test_sukl_invocation_logs_info(self, registry_with_mock_sukl):
        """SUKL tool invocations generate INFO log entries."""
        with patch("backend.tools.registry.logger") as mock_logger:
            registry_with_mock_sukl.invoke("sukl_search_drugs", query="test")

            mock_logger.info.assert_called_once()
            call_kwargs = mock_logger.info.call_args[1]
            assert call_kwargs["tool_name"] == "sukl_search_drugs"
            assert call_kwargs["success"] is True
            assert "duration_ms" in call_kwargs

    def test_pubmed_invocation_logs_info(self, registry_with_mock_pubmed):
        """PubMed tool invocations generate INFO log entries."""
        with patch("backend.tools.registry.logger") as mock_logger:
            registry_with_mock_pubmed.invoke("pubmed_search_literature", query="test")

            mock_logger.info.assert_called_once()
            call_kwargs = mock_logger.info.call_args[1]
            assert call_kwargs["tool_name"] == "pubmed_search_literature"
            assert call_kwargs["success"] is True

    def test_validation_error_logs_error(self, registry_with_mock_sukl):
        """Validation errors generate ERROR log entries."""
        with patch("backend.tools.registry.logger") as mock_logger:
            registry_with_mock_sukl.invoke("sukl_search_drugs")  # Missing required param

            mock_logger.error.assert_called_once()
            call_kwargs = mock_logger.error.call_args[1]
            assert call_kwargs["error_type"] == "ValidationError"
            assert call_kwargs["success"] is False

    def test_handler_error_logs_error(self, fresh_registry):
        """Handler errors generate ERROR log entries."""
        error_tool = ToolDefinition(
            name="error_tool",
            description="Tool that errors",
            parameters=SuklSearchInput,
            handler=mock_sukl_search_error,
        )
        fresh_registry.register(error_tool)

        with patch("backend.tools.registry.logger") as mock_logger:
            fresh_registry.invoke("error_tool", query="test")

            mock_logger.error.assert_called_once()
            call_kwargs = mock_logger.error.call_args[1]
            assert call_kwargs["success"] is False
            assert "Database connection failed" in call_kwargs["error_message"]
