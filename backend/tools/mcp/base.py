"""
MCP Server Wrapper Base Utilities

This module provides helper functions for wrapping MCP server functions
as ToolDefinition instances. It enables seamless integration of existing
MCP servers into the unified Tool Registry system.

Key functionality:
- create_mcp_tool(): Factory function to create ToolDefinition from MCP functions
- Automatic Pydantic schema generation from function signatures
- Support for both sync and async MCP server functions
- Preservation of original function metadata (docstrings, names)
"""

import asyncio
import inspect
from typing import Any, Callable, Dict, List, Optional, Type, Union, get_type_hints

from pydantic import BaseModel, Field, create_model

from backend.tools.base import ToolDefinition


def extract_function_metadata(func: Callable[..., Any]) -> Dict[str, Any]:
    """
    Extract metadata from a function for tool creation.

    Analyzes the function signature and docstring to extract:
    - Parameter names and types
    - Default values
    - Docstring for description

    Args:
        func: The function to extract metadata from.

    Returns:
        Dict containing:
            - name: Function name
            - description: Docstring or default description
            - parameters: List of parameter info dicts

    Example:
        >>> async def search(query: str, limit: int = 10) -> str:
        ...     '''Search for items.'''
        ...     pass
        >>> meta = extract_function_metadata(search)
        >>> meta['name']
        'search'
        >>> meta['description']
        'Search for items.'
    """
    sig = inspect.signature(func)
    type_hints = {}

    # Safely get type hints (may fail for some functions)
    try:
        type_hints = get_type_hints(func)
    except Exception:
        # Fall back to annotation inspection if get_type_hints fails
        type_hints = {
            name: param.annotation
            for name, param in sig.parameters.items()
            if param.annotation != inspect.Parameter.empty
        }

    # Extract docstring, stripping leading/trailing whitespace
    description = inspect.getdoc(func) or f"Execute {func.__name__} function"

    # Extract parameters
    parameters: List[Dict[str, Any]] = []
    for name, param in sig.parameters.items():
        # Skip 'self' and 'cls' parameters
        if name in ("self", "cls"):
            continue

        param_info: Dict[str, Any] = {
            "name": name,
            "type": type_hints.get(name, str),  # Default to str if no type hint
            "required": param.default == inspect.Parameter.empty,
        }

        if param.default != inspect.Parameter.empty:
            param_info["default"] = param.default

        parameters.append(param_info)

    return {
        "name": func.__name__,
        "description": description,
        "parameters": parameters,
    }


def create_pydantic_model_from_params(
    model_name: str,
    parameters: List[Dict[str, Any]],
) -> Type[BaseModel]:
    """
    Dynamically create a Pydantic model from parameter definitions.

    Creates a Pydantic model class suitable for input validation,
    with fields matching the provided parameter definitions.

    Args:
        model_name: Name for the generated model class.
        parameters: List of parameter info dicts from extract_function_metadata.

    Returns:
        Type[BaseModel]: A dynamically created Pydantic model class.

    Example:
        >>> params = [
        ...     {"name": "query", "type": str, "required": True},
        ...     {"name": "limit", "type": int, "required": False, "default": 10}
        ... ]
        >>> Model = create_pydantic_model_from_params("SearchInput", params)
        >>> Model(query="test")
        SearchInput(query='test', limit=10)
    """
    field_definitions: Dict[str, Any] = {}

    for param in parameters:
        param_name = param["name"]
        param_type = param.get("type", str)
        is_required = param.get("required", True)
        default_value = param.get("default")

        # Handle special type annotations that might cause issues
        if param_type == inspect.Parameter.empty:
            param_type = str

        # Create field with appropriate default
        if is_required:
            # Required field with no default
            field_definitions[param_name] = (param_type, ...)
        elif default_value is not None:
            # Optional field with default value
            field_definitions[param_name] = (param_type, default_value)
        else:
            # Optional field with None default
            field_definitions[param_name] = (Optional[param_type], None)

    # Create the model dynamically
    model = create_model(model_name, **field_definitions)
    return model


def create_mcp_tool(
    func: Callable[..., Any],
    name: Optional[str] = None,
    description: Optional[str] = None,
    input_model: Optional[Type[BaseModel]] = None,
) -> ToolDefinition:
    """
    Create a ToolDefinition from an MCP server function.

    Factory function that wraps an MCP server function (typically decorated
    with @mcp.tool()) into a ToolDefinition instance compatible with the
    Tool Registry system.

    This function automatically:
    - Extracts metadata from the function (name, docstring)
    - Creates a Pydantic input schema from function signature
    - Preserves async/sync nature of the handler
    - Handles default values for optional parameters

    Args:
        func: The MCP server function to wrap. Can be sync or async.
        name: Override for the tool name. Defaults to function name.
        description: Override for description. Defaults to function docstring.
        input_model: Optional custom Pydantic model for inputs. If not provided,
            a model is automatically generated from the function signature.

    Returns:
        ToolDefinition: A tool definition ready for registry registration.

    Raises:
        TypeError: If func is not callable.

    Example:
        >>> # Basic usage - wrap an MCP function
        >>> from backend.mcp_servers.sukl_server import search_drugs
        >>> tool = create_mcp_tool(search_drugs)
        >>> tool.name
        'search_drugs'
        >>> tool.is_async
        True

        >>> # With custom name and description
        >>> tool = create_mcp_tool(
        ...     search_drugs,
        ...     name="sukl_search",
        ...     description="Search the SUKL drug database"
        ... )
        >>> tool.name
        'sukl_search'

        >>> # With custom input model
        >>> class CustomInput(BaseModel):
        ...     query: str = Field(..., min_length=1)
        >>> tool = create_mcp_tool(search_drugs, input_model=CustomInput)
    """
    if not callable(func):
        raise TypeError(f"Expected callable, got {type(func).__name__}")

    # Extract metadata from function
    metadata = extract_function_metadata(func)

    # Use provided values or fall back to extracted metadata
    tool_name = name or metadata["name"]
    tool_description = description or metadata["description"]

    # Use provided input model or create one from function signature
    if input_model is not None:
        parameters_model = input_model
    else:
        # Generate model name: function_name + "Input"
        model_name = f"{func.__name__.title().replace('_', '')}Input"
        parameters_model = create_pydantic_model_from_params(
            model_name=model_name,
            parameters=metadata["parameters"],
        )

    return ToolDefinition(
        name=tool_name,
        description=tool_description,
        parameters=parameters_model,
        handler=func,
    )


def create_mcp_tools_batch(
    functions: List[Callable[..., Any]],
    name_prefix: Optional[str] = None,
) -> List[ToolDefinition]:
    """
    Create multiple ToolDefinition instances from a list of MCP functions.

    Convenience function for wrapping multiple MCP server functions at once.
    Optionally adds a prefix to all tool names for namespacing.

    Args:
        functions: List of MCP server functions to wrap.
        name_prefix: Optional prefix to add to all tool names (e.g., "sukl_").

    Returns:
        List[ToolDefinition]: List of tool definitions ready for registration.

    Example:
        >>> from backend.mcp_servers.sukl_server import search_drugs, get_drug_details
        >>> tools = create_mcp_tools_batch(
        ...     [search_drugs, get_drug_details],
        ...     name_prefix="sukl_"
        ... )
        >>> [t.name for t in tools]
        ['sukl_search_drugs', 'sukl_get_drug_details']
    """
    tools = []
    for func in functions:
        tool = create_mcp_tool(func)
        if name_prefix:
            # Create new tool with prefixed name
            tool = ToolDefinition(
                name=f"{name_prefix}{tool.name}",
                description=tool.description,
                parameters=tool.parameters,
                handler=tool.handler,
            )
        tools.append(tool)
    return tools
