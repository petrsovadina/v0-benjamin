"""
PubMed MCP Server Wrapper

This module provides ToolDefinition wrappers for the PubMed MCP server function.
It enables searching medical literature through the unified Tool Registry interface.

PubMed is a free search engine accessing primarily the MEDLINE database of
references and abstracts on life sciences and biomedical topics.

Tools provided:
    - pubmed_search_literature: Search for medical papers in PubMed

Usage:
    from backend.tools.mcp.pubmed import register_pubmed_tools
    from backend.tools import ToolRegistry

    registry = ToolRegistry()
    register_pubmed_tools(registry)

    # Search for medical literature
    result = await registry.invoke_async(
        "pubmed_search_literature",
        query="diabetes treatment",
        max_results=10
    )

Note:
    The MCP server functions are imported lazily to avoid requiring the MCP
    module to be installed when this module is imported. The actual MCP functions
    are only imported when a tool handler is invoked.
"""

from typing import TYPE_CHECKING

from pydantic import BaseModel, Field

from backend.tools.base import ToolDefinition

if TYPE_CHECKING:
    from backend.tools.registry import ToolRegistry


# ============================================================================
# Lazy Import Handlers
# ============================================================================
# We use wrapper functions to defer importing MCP server functions until
# they are actually called. This allows the tool definitions to be created
# without requiring the MCP module to be installed at import time.


async def _search_literature_handler(query: str, max_results: int = 5) -> str:
    """
    Wrapper handler for search_literature MCP function.

    Imports the actual MCP function lazily and forwards the call.
    """
    from backend.mcp_servers.pubmed_server import search_literature

    return await search_literature(query=query, max_results=max_results)


# ============================================================================
# Pydantic Input Models
# ============================================================================


class PubMedSearchInput(BaseModel):
    """
    Input schema for PubMed literature search.

    Validates input parameters for searching medical literature in PubMed.
    Supports query strings and optional result limit.

    Attributes:
        query: Search query string. Can include medical terms, conditions,
            treatments, drug names, or any biomedical topic.
        max_results: Maximum number of results to return. Defaults to 5.
            Higher values may increase response time.

    Example:
        >>> input_data = PubMedSearchInput(query="diabetes treatment")
        >>> input_data.query
        'diabetes treatment'
        >>> input_data.max_results
        5

        >>> input_data = PubMedSearchInput(query="COVID-19 vaccines", max_results=20)
        >>> input_data.max_results
        20
    """

    query: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description=(
            "Search query for PubMed literature. Can include medical terms, "
            "conditions, treatments, drug names, author names, or any "
            "biomedical topic. Examples: 'diabetes treatment', "
            "'COVID-19 vaccines efficacy', 'aspirin cardiovascular effects'."
        ),
        json_schema_extra={
            "examples": [
                "diabetes treatment",
                "COVID-19 vaccines",
                "breast cancer screening",
            ]
        },
    )

    max_results: int = Field(
        default=5,
        ge=1,
        le=100,
        description=(
            "Maximum number of results to return. Default is 5. "
            "Higher values may increase response time. Maximum 100."
        ),
        json_schema_extra={"examples": [5, 10, 20]},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"query": "diabetes treatment", "max_results": 5},
                {"query": "COVID-19 vaccines efficacy", "max_results": 10},
                {"query": "hypertension management guidelines", "max_results": 20},
            ]
        }
    }


# ============================================================================
# Tool Definitions
# ============================================================================


pubmed_search_literature = ToolDefinition(
    name="pubmed_search_literature",
    description=(
        "Search PubMed for medical and biomedical literature. "
        "Returns papers including title, abstract, authors, publication year, "
        "PMID, DOI, and URL. PubMed contains over 35 million citations from "
        "MEDLINE, life science journals, and online books. Useful for finding "
        "evidence-based medical information, clinical studies, and research papers."
    ),
    parameters=PubMedSearchInput,
    handler=_search_literature_handler,
)
"""
ToolDefinition for searching medical literature in PubMed.

Wraps the `search_literature` MCP server function with Pydantic validation.
The handler is async and uses the PubMedSearcher from paper_search_mcp to
query the PubMed database.

Returns JSON with:
    - status: "success" or "error"
    - source: "pubmed"
    - query: The original search query
    - results: List of papers with title, abstract, authors, year, pmid, doi, url

Example:
    >>> from backend.tools import ToolRegistry
    >>> registry = ToolRegistry()
    >>> registry.register(pubmed_search_literature)
    >>> result = await registry.invoke_async(
    ...     "pubmed_search_literature",
    ...     query="diabetes treatment",
    ...     max_results=5
    ... )
    >>> result.success
    True
"""


# ============================================================================
# Registration Function
# ============================================================================


def register_pubmed_tools(registry: "ToolRegistry") -> None:
    """
    Register all PubMed MCP tools with the provided registry.

    Convenience function to register all PubMed-related tools at once.
    This is the recommended way to add PubMed tools to a registry instance.

    Args:
        registry: The ToolRegistry instance to register tools with.

    Raises:
        ValueError: If any tool is already registered with the same name.

    Example:
        >>> from backend.tools import ToolRegistry
        >>> from backend.tools.mcp.pubmed import register_pubmed_tools
        >>>
        >>> registry = ToolRegistry()
        >>> register_pubmed_tools(registry)
        >>> registry.list_tools()
        ['pubmed_search_literature']
        >>>
        >>> # Tool is now ready to use
        >>> result = await registry.invoke_async(
        ...     "pubmed_search_literature",
        ...     query="cancer immunotherapy"
        ... )
    """
    registry.register(pubmed_search_literature)


# List of all PubMed tools for easy access
PUBMED_TOOLS = [pubmed_search_literature]
"""List of all PubMed tool definitions for batch operations."""


__all__ = [
    # Input models
    "PubMedSearchInput",
    # Tool definitions
    "pubmed_search_literature",
    # Registration function
    "register_pubmed_tools",
    # Tool list
    "PUBMED_TOOLS",
]
