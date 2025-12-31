"""
Tests for LangChain message classes and state handling with LangChain 0.3.x.

These tests verify that message classes, state definitions, and message handling
work correctly after the LangChain upgrade.
"""
import pytest
from typing import TypedDict, Annotated, Sequence, List, Literal, Dict, Any
import operator

# LangChain message imports
from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
    AIMessage,
    SystemMessage,
    ToolMessage,
)

# LangGraph state utilities
from langgraph.graph.message import add_messages


class TestMessageClassInstantiation:
    """Test that all message classes instantiate correctly."""

    def test_human_message_creation(self):
        """Verify HumanMessage can be created with content."""
        msg = HumanMessage(content="Hello, I have a question.")
        assert msg.content == "Hello, I have a question."
        assert msg.type == "human"

    def test_ai_message_creation(self):
        """Verify AIMessage can be created with content."""
        msg = AIMessage(content="I'm here to help!")
        assert msg.content == "I'm here to help!"
        assert msg.type == "ai"

    def test_system_message_creation(self):
        """Verify SystemMessage can be created with content."""
        msg = SystemMessage(content="You are a helpful assistant.")
        assert msg.content == "You are a helpful assistant."
        assert msg.type == "system"

    def test_tool_message_creation(self):
        """Verify ToolMessage can be created with required fields."""
        msg = ToolMessage(content="Tool result", tool_call_id="call_123")
        assert msg.content == "Tool result"
        assert msg.tool_call_id == "call_123"
        assert msg.type == "tool"


class TestMessageSerialization:
    """Test message serialization and deserialization."""

    def test_human_message_to_dict(self):
        """Verify HumanMessage serializes to dict."""
        msg = HumanMessage(content="Test content")
        msg_dict = msg.model_dump()
        assert "content" in msg_dict
        assert msg_dict["content"] == "Test content"

    def test_ai_message_to_dict(self):
        """Verify AIMessage serializes to dict."""
        msg = AIMessage(content="AI response")
        msg_dict = msg.model_dump()
        assert "content" in msg_dict
        assert msg_dict["content"] == "AI response"

    def test_message_from_dict(self):
        """Verify messages can be reconstructed from dict."""
        original = HumanMessage(content="Original message")
        msg_dict = original.model_dump()

        # Reconstruct using the model_validate method
        reconstructed = HumanMessage.model_validate(msg_dict)
        assert reconstructed.content == original.content


class TestAddMessagesReducer:
    """Test the add_messages reducer from LangGraph."""

    def test_add_messages_import(self):
        """Verify add_messages can be imported from langgraph.graph.message."""
        assert add_messages is not None

    def test_add_messages_basic(self):
        """Verify add_messages combines message lists."""
        existing = [HumanMessage(content="First")]
        new = [AIMessage(content="Second")]

        result = add_messages(existing, new)

        assert len(result) == 2
        assert result[0].content == "First"
        assert result[1].content == "Second"

    def test_add_messages_with_empty_list(self):
        """Verify add_messages handles empty lists."""
        existing = [HumanMessage(content="Only message")]
        result = add_messages(existing, [])

        assert len(result) == 1
        assert result[0].content == "Only message"


class TestStateDefinitionPatterns:
    """Test state definition patterns used in the project."""

    def test_basic_typed_dict_state(self):
        """Verify basic TypedDict state pattern works."""
        class SimpleState(TypedDict):
            value: str

        state: SimpleState = {"value": "test"}
        assert state["value"] == "test"

    def test_annotated_messages_state(self):
        """Verify Annotated state with operator.add pattern works."""
        class AgentState(TypedDict):
            messages: Annotated[Sequence[BaseMessage], operator.add]

        state: AgentState = {"messages": [HumanMessage(content="Hello")]}
        assert len(state["messages"]) == 1
        assert state["messages"][0].content == "Hello"

    def test_annotated_messages_with_add_messages(self):
        """Verify Annotated state with add_messages reducer works."""
        class ChatState(TypedDict):
            messages: Annotated[list[BaseMessage], add_messages]

        state: ChatState = {"messages": [HumanMessage(content="Hello")]}
        assert len(state["messages"]) == 1

    def test_complex_state_definition(self):
        """Verify complex state definition pattern (like ClinicalState) works."""
        class ComplexState(TypedDict):
            messages: Annotated[list[BaseMessage], add_messages]
            query_type: Literal["general", "drug_info", "guidelines"] | None
            retrieved_context: List[Dict[str, Any]]
            final_answer: str | None
            next_step: str | None

        state: ComplexState = {
            "messages": [HumanMessage(content="What is aspirin?")],
            "query_type": "drug_info",
            "retrieved_context": [{"source": "sukl", "data": {"name": "Aspirin"}}],
            "final_answer": None,
            "next_step": "retrieve_drugs"
        }

        assert state["query_type"] == "drug_info"
        assert len(state["retrieved_context"]) == 1
        assert state["retrieved_context"][0]["source"] == "sukl"


class TestMessageTypeChecking:
    """Test message type checking and isinstance behavior."""

    def test_isinstance_base_message(self):
        """Verify all message types are instances of BaseMessage."""
        messages = [
            HumanMessage(content="human"),
            AIMessage(content="ai"),
            SystemMessage(content="system"),
            ToolMessage(content="tool", tool_call_id="123"),
        ]

        for msg in messages:
            assert isinstance(msg, BaseMessage)

    def test_message_type_discrimination(self):
        """Verify message types can be discriminated."""
        messages = [
            HumanMessage(content="human"),
            AIMessage(content="ai"),
            SystemMessage(content="system"),
        ]

        types = [msg.type for msg in messages]
        assert types == ["human", "ai", "system"]


class TestMessageWithAdditionalFields:
    """Test messages with additional metadata fields."""

    def test_ai_message_with_tool_calls(self):
        """Verify AIMessage can have tool_calls field."""
        msg = AIMessage(
            content="",
            tool_calls=[{
                "id": "call_123",
                "name": "search",
                "args": {"query": "test"}
            }]
        )
        assert len(msg.tool_calls) == 1
        assert msg.tool_calls[0]["name"] == "search"

    def test_message_with_additional_kwargs(self):
        """Verify messages accept additional_kwargs."""
        msg = HumanMessage(
            content="Test",
            additional_kwargs={"custom_field": "value"}
        )
        assert msg.additional_kwargs.get("custom_field") == "value"
