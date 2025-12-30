"""
SUKL MCP Server Wrapper

This module provides ToolDefinition wrappers for the SUKL (State Institute for
Drug Control) MCP server functions. It enables searching the Czech drug database
and retrieving drug details through the unified Tool Registry interface.

The SUKL database contains information about drugs approved for use in the
Czech Republic, including drug names, active substances, and regulatory codes.

Tools provided:
    - sukl_search_drugs: Search for drugs by name or active substance
    - sukl_get_drug_details: Get detailed information about a drug by SUKL code

Usage:
    from backend.tools.mcp.sukl import register_sukl_tools
    from backend.tools import ToolRegistry

    registry = ToolRegistry()
    register_sukl_tools(registry)

    # Search for drugs
    result = await registry.invoke_async("sukl_search_drugs", query="aspirin")

    # Get drug details
    result = await registry.invoke_async("sukl_get_drug_details", sukl_code="0012345")

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


async def _search_drugs_handler(query: str) -> str:
    """
    Wrapper handler for search_drugs MCP function.

    Imports the actual MCP function lazily and forwards the call.
    """
    from backend.mcp_servers.sukl_server import search_drugs

    return await search_drugs(query=query)


async def _get_drug_details_handler(sukl_code: str) -> str:
    """
    Wrapper handler for get_drug_details MCP function.

    Imports the actual MCP function lazily and forwards the call.
    """
    from backend.mcp_servers.sukl_server import get_drug_details

    return await get_drug_details(sukl_code=sukl_code)


# ============================================================================
# Pydantic Input Models
# ============================================================================


class SuklSearchInput(BaseModel):
    """
    Input schema for SUKL drug search.

    Validates input parameters for searching drugs in the SUKL database
    by drug name or active substance.

    Attributes:
        query: Search query string. Can be a drug name (e.g., "Aspirin"),
            active substance (e.g., "ibuprofen"), or partial match.

    Example:
        >>> input_data = SuklSearchInput(query="paracetamol")
        >>> input_data.query
        'paracetamol'
    """

    query: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description=(
            "Search query for drugs. Can be a drug name (e.g., 'Paralen'), "
            "active substance (e.g., 'paracetamol'), or partial match. "
            "Minimum 1 character required."
        ),
        json_schema_extra={"examples": ["aspirin", "ibuprofen", "paracetamol"]},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"query": "Paralen"},
                {"query": "ibuprofen"},
                {"query": "aspirin"},
            ]
        }
    }


class SuklDrugDetailInput(BaseModel):
    """
    Input schema for SUKL drug detail retrieval.

    Validates input parameters for retrieving detailed information about
    a specific drug using its SUKL regulatory code.

    Attributes:
        sukl_code: The SUKL regulatory code (registration number) of the drug.
            This is a unique identifier assigned by the State Institute for
            Drug Control.

    Example:
        >>> input_data = SuklDrugDetailInput(sukl_code="0012345")
        >>> input_data.sukl_code
        '0012345'
    """

    sukl_code: str = Field(
        ...,
        min_length=1,
        max_length=20,
        description=(
            "SUKL regulatory code (registration number) of the drug. "
            "This unique identifier is assigned by the State Institute "
            "for Drug Control (SUKL) in the Czech Republic."
        ),
        json_schema_extra={"examples": ["0012345", "0098765"]},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"sukl_code": "0012345"},
                {"sukl_code": "0098765"},
            ]
        }
    }


# ============================================================================
# Tool Definitions
# ============================================================================


sukl_search_drugs = ToolDefinition(
    name="sukl_search_drugs",
    description=(
        "Search for drugs in the SUKL (State Institute for Drug Control) database. "
        "Searches by drug name or active substance using case-insensitive partial "
        "matching. Returns up to 10 matching drugs with their details including "
        "name, active substance, SUKL code, and other regulatory information."
    ),
    parameters=SuklSearchInput,
    handler=_search_drugs_handler,
)
"""
ToolDefinition for searching drugs in the SUKL database.

Wraps the `search_drugs` MCP server function with Pydantic validation.
The handler is async and queries the Supabase 'drugs' table with ILIKE
pattern matching on both drug name (nazev) and active substance (ucinna_latka).

Example:
    >>> from backend.tools import ToolRegistry
    >>> registry = ToolRegistry()
    >>> registry.register(sukl_search_drugs)
    >>> result = await registry.invoke_async("sukl_search_drugs", query="ibuprofen")
    >>> result.success
    True
"""


sukl_get_drug_details = ToolDefinition(
    name="sukl_get_drug_details",
    description=(
        "Get detailed information about a specific drug from the SUKL database "
        "using its SUKL regulatory code. Returns complete drug information "
        "including name, active substance, dosage form, strength, manufacturer, "
        "and regulatory status."
    ),
    parameters=SuklDrugDetailInput,
    handler=_get_drug_details_handler,
)
"""
ToolDefinition for retrieving drug details from the SUKL database.

Wraps the `get_drug_details` MCP server function with Pydantic validation.
The handler is async and queries the Supabase 'drugs' table for a single
drug record matching the provided SUKL code.

Example:
    >>> from backend.tools import ToolRegistry
    >>> registry = ToolRegistry()
    >>> registry.register(sukl_get_drug_details)
    >>> result = await registry.invoke_async("sukl_get_drug_details", sukl_code="0012345")
    >>> result.success
    True
"""


# ============================================================================
# Registration Function
# ============================================================================


def register_sukl_tools(registry: "ToolRegistry") -> None:
    """
    Register all SUKL MCP tools with the provided registry.

    Convenience function to register all SUKL-related tools at once.
    This is the recommended way to add SUKL tools to a registry instance.

    Args:
        registry: The ToolRegistry instance to register tools with.

    Raises:
        ValueError: If any tool is already registered with the same name.

    Example:
        >>> from backend.tools import ToolRegistry
        >>> from backend.tools.mcp.sukl import register_sukl_tools
        >>>
        >>> registry = ToolRegistry()
        >>> register_sukl_tools(registry)
        >>> registry.list_tools()
        ['sukl_get_drug_details', 'sukl_search_drugs']
        >>>
        >>> # Tools are now ready to use
        >>> result = await registry.invoke_async("sukl_search_drugs", query="aspirin")
    """
    registry.register(sukl_search_drugs)
    registry.register(sukl_get_drug_details)


# List of all SUKL tools for easy access
SUKL_TOOLS = [sukl_search_drugs, sukl_get_drug_details]
"""List of all SUKL tool definitions for batch operations."""


__all__ = [
    # Input models
    "SuklSearchInput",
    "SuklDrugDetailInput",
    # Tool definitions
    "sukl_search_drugs",
    "sukl_get_drug_details",
    # Registration function
    "register_sukl_tools",
    # Tool list
    "SUKL_TOOLS",
]
