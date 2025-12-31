"""
Tests for tool integration with LangGraph and message passing (MCP patterns).

These tests verify that tools integrate correctly with LangGraph's ToolNode
and the tools_condition routing logic after the dependency upgrade.
"""
import pytest
from typing import TypedDict, Annotated, Sequence
import operator
import json

# LangGraph imports
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition

# LangChain imports
from langchain_core.tools import tool
from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
    AIMessage,
    ToolMessage,
)


class TestToolsCondition:
    """Test the tools_condition routing function."""

    def test_tools_condition_import(self):
        """Verify tools_condition can be imported from langgraph.prebuilt."""
        assert tools_condition is not None
        assert callable(tools_condition)

    def test_tools_condition_with_tool_calls(self):
        """Verify tools_condition routes to tools when tool calls present."""
        # Create a state with an AIMessage that has tool_calls
        class TestState(TypedDict):
            messages: Annotated[Sequence[BaseMessage], operator.add]

        # AIMessage with tool_calls should route to "tools"
        ai_msg_with_tools = AIMessage(
            content="",
            tool_calls=[
                {
                    "id": "call_123",
                    "name": "test_tool",
                    "args": {"query": "test"}
                }
            ]
        )

        state = {"messages": [ai_msg_with_tools]}
        result = tools_condition(state)
        assert result == "tools"

    def test_tools_condition_without_tool_calls(self):
        """Verify tools_condition routes to END when no tool calls."""
        class TestState(TypedDict):
            messages: Annotated[Sequence[BaseMessage], operator.add]

        # AIMessage without tool_calls should route to END
        ai_msg_no_tools = AIMessage(content="Final answer")

        state = {"messages": [ai_msg_no_tools]}
        result = tools_condition(state)
        assert result == END


class TestToolNodeIntegration:
    """Test ToolNode integration with state graphs."""

    def test_tool_node_in_graph(self):
        """Verify ToolNode can be added to a StateGraph."""
        class AgentState(TypedDict):
            messages: Annotated[Sequence[BaseMessage], operator.add]

        @tool
        def test_tool(query: str) -> str:
            """Test tool for graph integration."""
            return f"Result: {query}"

        def agent_node(state: AgentState):
            return {"messages": [AIMessage(content="Done")]}

        workflow = StateGraph(AgentState)
        workflow.add_node("agent", agent_node)
        workflow.add_node("tools", ToolNode([test_tool]))
        workflow.add_edge(START, "agent")
        workflow.add_edge("tools", "agent")
        workflow.add_conditional_edges("agent", tools_condition)

        app = workflow.compile()
        assert app is not None

    def test_tool_node_with_multiple_tools(self):
        """Verify ToolNode handles multiple tools."""
        class State(TypedDict):
            messages: Annotated[Sequence[BaseMessage], operator.add]

        @tool
        def search_tool(query: str) -> str:
            """Search for information."""
            return f"Search: {query}"

        @tool
        def calculate_tool(expression: str) -> str:
            """Calculate an expression."""
            return f"Calculate: {expression}"

        @tool
        def lookup_tool(key: str) -> str:
            """Look up a value."""
            return f"Lookup: {key}"

        tools = [search_tool, calculate_tool, lookup_tool]
        tool_node = ToolNode(tools)

        def agent(state: State):
            return {"messages": [AIMessage(content="Response")]}

        workflow = StateGraph(State)
        workflow.add_node("agent", agent)
        workflow.add_node("tools", tool_node)
        workflow.add_edge(START, "agent")
        workflow.add_conditional_edges("agent", tools_condition)
        workflow.add_edge("tools", "agent")

        app = workflow.compile()
        assert app is not None


class TestToolMessageFlow:
    """Test tool message flow in graphs."""

    def test_tool_message_creation(self):
        """Verify ToolMessage can be created correctly."""
        tool_msg = ToolMessage(
            content="Tool result",
            tool_call_id="call_123"
        )
        assert tool_msg.content == "Tool result"
        assert tool_msg.tool_call_id == "call_123"

    def test_tool_message_in_state(self):
        """Verify ToolMessage integrates with state."""
        class State(TypedDict):
            messages: Annotated[Sequence[BaseMessage], operator.add]

        state: State = {"messages": []}

        # Simulate tool call flow
        human_msg = HumanMessage(content="Search for Python")
        ai_msg = AIMessage(
            content="",
            tool_calls=[{"id": "call_1", "name": "search", "args": {"q": "Python"}}]
        )
        tool_msg = ToolMessage(content="Python results...", tool_call_id="call_1")
        final_msg = AIMessage(content="Here are the Python results...")

        messages = [human_msg, ai_msg, tool_msg, final_msg]
        state["messages"] = messages

        assert len(state["messages"]) == 4
        assert isinstance(state["messages"][2], ToolMessage)

    def test_tool_message_serialization(self):
        """Verify ToolMessage can be serialized."""
        tool_msg = ToolMessage(
            content='{"result": "success", "data": [1, 2, 3]}',
            tool_call_id="call_456"
        )

        # Serialize and deserialize
        msg_dict = tool_msg.model_dump() if hasattr(tool_msg, 'model_dump') else tool_msg.dict()
        assert "content" in msg_dict
        assert "tool_call_id" in msg_dict

        # Content should be parseable JSON
        content_data = json.loads(tool_msg.content)
        assert content_data["result"] == "success"


class TestAsyncToolIntegration:
    """Test async tool integration."""

    def test_async_tools_in_tool_node(self):
        """Verify async tools work in ToolNode."""
        @tool
        async def async_search(query: str) -> str:
            """Async search tool."""
            return f"Async result: {query}"

        tool_node = ToolNode([async_search])
        assert tool_node is not None

    def test_mixed_sync_async_tools(self):
        """Verify mixed sync/async tools work together."""
        @tool
        def sync_tool(x: str) -> str:
            """Sync tool."""
            return f"Sync: {x}"

        @tool
        async def async_tool(x: str) -> str:
            """Async tool."""
            return f"Async: {x}"

        class State(TypedDict):
            messages: Annotated[Sequence[BaseMessage], operator.add]

        tools = [sync_tool, async_tool]
        tool_node = ToolNode(tools)

        def agent(state: State):
            return {"messages": [AIMessage(content="Done")]}

        workflow = StateGraph(State)
        workflow.add_node("agent", agent)
        workflow.add_node("tools", tool_node)
        workflow.add_edge(START, "agent")
        workflow.add_conditional_edges("agent", tools_condition)
        workflow.add_edge("tools", "agent")

        app = workflow.compile()
        assert app is not None


class TestToolCallParsing:
    """Test parsing of tool calls from AI messages."""

    def test_ai_message_tool_calls_attribute(self):
        """Verify AIMessage has tool_calls attribute."""
        ai_msg = AIMessage(content="Testing")
        # tool_calls should be empty list or None by default
        tool_calls = getattr(ai_msg, 'tool_calls', None)
        assert tool_calls is not None or hasattr(ai_msg, 'tool_calls')

    def test_ai_message_with_tool_calls_structure(self):
        """Verify tool_calls structure is correct."""
        tool_calls = [
            {
                "id": "call_abc123",
                "name": "search",
                "args": {"query": "test"}
            },
            {
                "id": "call_def456",
                "name": "calculate",
                "args": {"expr": "2+2"}
            }
        ]

        ai_msg = AIMessage(content="", tool_calls=tool_calls)

        assert len(ai_msg.tool_calls) == 2
        assert ai_msg.tool_calls[0]["name"] == "search"
        assert ai_msg.tool_calls[1]["name"] == "calculate"

    def test_tool_call_id_matching(self):
        """Verify tool call IDs match between AIMessage and ToolMessage."""
        call_id = "call_unique_123"

        ai_msg = AIMessage(
            content="",
            tool_calls=[{"id": call_id, "name": "test", "args": {}}]
        )

        tool_msg = ToolMessage(content="Result", tool_call_id=call_id)

        assert ai_msg.tool_calls[0]["id"] == tool_msg.tool_call_id


class TestProjectPatterns:
    """Test tool patterns used in the project (agent_graph.py)."""

    def test_project_agent_pattern(self):
        """Verify the agent graph pattern from agent_graph.py compiles."""
        class AgentState(TypedDict):
            messages: Annotated[Sequence[BaseMessage], operator.add]

        @tool
        async def mock_pubmed_search(query: str) -> str:
            """Search PubMed for medical articles."""
            return f"PubMed results for: {query}"

        @tool
        async def mock_sukl_search(query: str) -> str:
            """Search SUKL drug database."""
            return f"SUKL results for: {query}"

        tools = [mock_pubmed_search, mock_sukl_search]

        def reasoner(state: AgentState):
            """Main reasoning node."""
            return {"messages": [AIMessage(content="Response")]}

        workflow = StateGraph(AgentState)
        workflow.add_node("agent", reasoner)
        workflow.add_node("tools", ToolNode(tools))
        workflow.add_edge(START, "agent")
        workflow.add_conditional_edges("agent", tools_condition)
        workflow.add_edge("tools", "agent")

        app = workflow.compile(checkpointer=None)
        assert app is not None

    def test_tool_binding_pattern(self):
        """Verify tools can be bound to LLM pattern."""
        @tool
        def test_tool_for_binding(query: str) -> str:
            """Test tool for LLM binding."""
            return f"Result: {query}"

        tools = [test_tool_for_binding]

        # Verify tools have the necessary attributes for binding
        for t in tools:
            assert hasattr(t, 'name')
            assert hasattr(t, 'description')
            assert hasattr(t, 'args_schema')

        # Tools should be listable for bind_tools()
        tool_names = [t.name for t in tools]
        assert "test_tool_for_binding" in tool_names
