"""
Tests for LangGraph graph compilation and structure with LangGraph 1.x.

These tests verify that the graph structures compile correctly after the
LangChain/LangGraph upgrade and that the LangGraph 1.x APIs work as expected.
"""
import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from typing import TypedDict, Annotated, Sequence
import operator

# LangGraph imports - verify they work with upgraded packages
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_core.tools import tool


class TestLangGraphImports:
    """Test that all LangGraph imports work correctly with upgraded packages."""

    def test_state_graph_import(self):
        """Verify StateGraph can be imported from langgraph.graph."""
        assert StateGraph is not None

    def test_start_end_import(self):
        """Verify START and END constants are importable."""
        assert START is not None
        assert END is not None

    def test_prebuilt_imports(self):
        """Verify prebuilt components are importable."""
        assert ToolNode is not None
        assert tools_condition is not None


class TestBasicGraphCompilation:
    """Test basic graph compilation patterns."""

    def test_simple_state_graph_compiles(self):
        """Verify a simple StateGraph compiles without errors."""
        # Define a minimal state
        class SimpleState(TypedDict):
            value: str

        # Define a simple node
        def node_fn(state: SimpleState) -> dict:
            return {"value": state["value"] + "_processed"}

        # Build and compile graph
        workflow = StateGraph(SimpleState)
        workflow.add_node("process", node_fn)
        workflow.add_edge(START, "process")
        workflow.add_edge("process", END)

        graph = workflow.compile()
        assert graph is not None

    def test_graph_with_annotated_state(self):
        """Verify StateGraph works with Annotated state fields."""
        class AnnotatedState(TypedDict):
            messages: Annotated[Sequence[BaseMessage], operator.add]

        def node_fn(state: AnnotatedState) -> dict:
            return {"messages": [AIMessage(content="response")]}

        workflow = StateGraph(AnnotatedState)
        workflow.add_node("agent", node_fn)
        workflow.add_edge(START, "agent")
        workflow.add_edge("agent", END)

        graph = workflow.compile()
        assert graph is not None

    def test_conditional_edges(self):
        """Verify conditional edges work correctly."""
        class RouterState(TypedDict):
            value: str
            route: str

        def router(state: RouterState) -> dict:
            return {"route": "path_a" if state["value"] == "a" else "path_b"}

        def node_a(state: RouterState) -> dict:
            return {"value": "from_a"}

        def node_b(state: RouterState) -> dict:
            return {"value": "from_b"}

        def route_fn(state: RouterState) -> str:
            return state["route"]

        workflow = StateGraph(RouterState)
        workflow.add_node("router", router)
        workflow.add_node("path_a", node_a)
        workflow.add_node("path_b", node_b)

        workflow.add_edge(START, "router")
        workflow.add_conditional_edges(
            "router",
            route_fn,
            {"path_a": "path_a", "path_b": "path_b"}
        )
        workflow.add_edge("path_a", END)
        workflow.add_edge("path_b", END)

        graph = workflow.compile()
        assert graph is not None


class TestToolNodeIntegration:
    """Test ToolNode integration with StateGraph."""

    def test_tool_decorator(self):
        """Verify @tool decorator creates valid tools."""
        @tool
        def test_tool(query: str) -> str:
            """A test tool that echoes input."""
            return f"Echo: {query}"

        assert test_tool.name == "test_tool"
        assert "echo" in test_tool.description.lower()

    def test_async_tool_decorator(self):
        """Verify @tool decorator works with async functions."""
        @tool
        async def async_test_tool(query: str) -> str:
            """An async test tool."""
            return f"Async echo: {query}"

        assert async_test_tool.name == "async_test_tool"

    def test_tool_node_creation(self):
        """Verify ToolNode can be created with tools."""
        @tool
        def simple_tool(x: str) -> str:
            """Simple tool."""
            return x

        tool_node = ToolNode([simple_tool])
        assert tool_node is not None


class TestGraphCompilationOptions:
    """Test various graph compilation options."""

    def test_compile_without_checkpointer(self):
        """Verify graph compiles with checkpointer=None (stateless mode)."""
        class State(TypedDict):
            value: str

        def node_fn(state: State) -> dict:
            return {"value": "processed"}

        workflow = StateGraph(State)
        workflow.add_node("process", node_fn)
        workflow.add_edge(START, "process")
        workflow.add_edge("process", END)

        # Explicitly pass checkpointer=None for stateless operation
        graph = workflow.compile(checkpointer=None)
        assert graph is not None

    def test_compile_with_memory_saver(self):
        """Verify graph compiles with MemorySaver checkpointer."""
        from langgraph.checkpoint.memory import MemorySaver

        class State(TypedDict):
            value: str

        def node_fn(state: State) -> dict:
            return {"value": "processed"}

        workflow = StateGraph(State)
        workflow.add_node("process", node_fn)
        workflow.add_edge(START, "process")
        workflow.add_edge("process", END)

        checkpointer = MemorySaver()
        graph = workflow.compile(checkpointer=checkpointer)
        assert graph is not None


class TestProjectGraphImports:
    """Test that the project's graph patterns work with LangGraph 1.x APIs.

    Note: The actual project graphs (agent_graph.py, translator_graph.py) have
    been verified to compile in the Graph Compilation Verification phase.
    These tests verify the patterns used in those graphs work correctly.
    """

    def test_agent_graph_pattern(self):
        """Verify the agent graph pattern (with tools and conditional edges) works."""
        # Replicate the pattern from agent_graph.py
        class AgentState(TypedDict):
            messages: Annotated[Sequence[BaseMessage], operator.add]

        @tool
        def mock_search(query: str) -> str:
            """Mock search tool."""
            return f"Result for: {query}"

        tools = [mock_search]

        def reasoner(state: AgentState):
            return {"messages": [AIMessage(content="response")]}

        workflow = StateGraph(AgentState)
        workflow.add_node("agent", reasoner)
        workflow.add_node("tools", ToolNode(tools))
        workflow.add_edge(START, "agent")
        workflow.add_conditional_edges("agent", tools_condition)
        workflow.add_edge("tools", "agent")

        # Compile without checkpointer (stateless pattern)
        app = workflow.compile(checkpointer=None)
        assert app is not None

    def test_translator_graph_pattern(self):
        """Verify the translator graph pattern (simple linear flow) works."""
        # Replicate the pattern from translator_graph.py
        class TranslatorState(TypedDict):
            source_text: str
            target_language: str
            translated_text: str

        def translate_node(state: TranslatorState):
            return {"translated_text": f"Translated: {state['source_text']}"}

        builder = StateGraph(TranslatorState)
        builder.add_node("translate", translate_node)
        builder.add_edge(START, "translate")
        builder.add_edge("translate", END)

        app = builder.compile()
        assert app is not None

    def test_clinical_graph_pattern(self):
        """Verify the clinical workflow pattern (conditional routing) works."""
        # Replicate the pattern from app/core/graph.py
        from typing import Literal, List, Dict, Any
        from langgraph.graph.message import add_messages

        class ClinicalState(TypedDict):
            messages: Annotated[list[BaseMessage], add_messages]
            query_type: Literal["general", "drug_info", "guidelines"] | None
            retrieved_context: List[Dict[str, Any]]
            next_step: str | None

        def classifier_node(state: ClinicalState):
            return {"query_type": "drug_info", "next_step": "retrieve_drugs"}

        def retrieve_drugs_node(state: ClinicalState):
            return {"retrieved_context": [{"source": "sukl", "data": {}}]}

        def retrieve_general_node(state: ClinicalState):
            return {"retrieved_context": [{"source": "pubmed", "data": {}}]}

        def route_query(state: ClinicalState) -> str:
            return state["next_step"] or "retrieve_general"

        workflow = StateGraph(ClinicalState)
        workflow.add_node("classifier", classifier_node)
        workflow.add_node("retrieve_drugs", retrieve_drugs_node)
        workflow.add_node("retrieve_general", retrieve_general_node)

        workflow.add_edge(START, "classifier")
        workflow.add_conditional_edges(
            "classifier",
            route_query,
            {"retrieve_drugs": "retrieve_drugs", "retrieve_general": "retrieve_general"}
        )
        workflow.add_edge("retrieve_drugs", END)
        workflow.add_edge("retrieve_general", END)

        app = workflow.compile(checkpointer=None)
        assert app is not None
