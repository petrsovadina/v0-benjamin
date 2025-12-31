#!/usr/bin/env python3
"""
Comprehensive verification of agent → ToolNode → agent → response loop.

This script verifies that:
1. The agent graph structure is correct
2. tools_condition correctly routes tool calls
3. ToolNode executes tools and returns results
4. The loop back to agent works correctly
5. The final response is generated after tool execution

Uses mocks to avoid requiring real API calls.
"""

import asyncio
import os
import sys
from unittest.mock import AsyncMock, MagicMock, patch
from pathlib import Path

# Ensure project root is in path (run from project root or backend/)
script_dir = Path(__file__).parent.resolve()
project_root = script_dir.parent if script_dir.name == 'backend' else script_dir
sys.path.insert(0, str(project_root))

from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_core.messages.tool import ToolCall


def test_graph_structure():
    """Test 1: Verify the graph has the correct structure."""
    print("\n" + "=" * 60)
    print("TEST 1: Graph Structure Verification")
    print("=" * 60)

    try:
        from backend.agent_graph import workflow, app, tools

        # Check nodes exist
        nodes = list(workflow.nodes.keys())
        print(f"  Graph nodes: {nodes}")

        assert "agent" in nodes, "Missing 'agent' node"
        assert "tools" in nodes, "Missing 'tools' node"
        print("  ✓ Both 'agent' and 'tools' nodes exist")

        # Check tools are registered
        tool_names = [t.name for t in tools]
        print(f"  Registered tools: {tool_names}")
        assert len(tools) >= 2, f"Expected at least 2 tools, got {len(tools)}"
        print(f"  ✓ {len(tools)} tools registered")

        # Check graph compiles
        assert app is not None, "Graph failed to compile"
        print("  ✓ Graph compiles successfully")

        # Check graph structure via mermaid (shows edges)
        mermaid = app.get_graph().draw_mermaid()
        print(f"\n  Graph structure (Mermaid):")
        for line in mermaid.split('\n'):
            if '-->' in line or 'agent' in line or 'tools' in line:
                print(f"    {line}")

        # Verify edges
        assert 'tools --> agent' in mermaid or 'tools --> ' in mermaid.replace(' ', '')
        print("  ✓ tools → agent edge exists (loop back)")

        return True
    except Exception as e:
        print(f"  ✗ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_tools_condition_routing():
    """Test 2: Verify tools_condition routes correctly."""
    print("\n" + "=" * 60)
    print("TEST 2: tools_condition Routing Verification")
    print("=" * 60)

    try:
        from langgraph.prebuilt import tools_condition
        from backend.agent_graph import AgentState

        # Test case 1: Message with tool call -> should route to "tools"
        tool_call = ToolCall(name="search_sukl_drugs", args={"query": "Eliquis"}, id="test-1")
        msg_with_tool = AIMessage(content="", tool_calls=[tool_call])
        state_with_tool: AgentState = {"messages": [HumanMessage(content="test"), msg_with_tool]}

        route = tools_condition(state_with_tool)
        print(f"  Message with tool_call routes to: {route}")
        assert route == "tools", f"Expected 'tools', got '{route}'"
        print("  ✓ Message with tool_calls correctly routes to 'tools'")

        # Test case 2: Message without tool call -> should route to END
        msg_without_tool = AIMessage(content="Here's the answer to your question.")
        state_without_tool: AgentState = {"messages": [HumanMessage(content="test"), msg_without_tool]}

        route = tools_condition(state_without_tool)
        print(f"  Message without tool_call routes to: {route}")
        assert route == "__end__", f"Expected '__end__', got '{route}'"
        print("  ✓ Message without tool_calls correctly routes to '__end__'")

        return True
    except Exception as e:
        print(f"  ✗ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_tool_node_execution():
    """Test 3: Verify ToolNode can execute tools via graph execution."""
    print("\n" + "=" * 60)
    print("TEST 3: ToolNode Execution Verification")
    print("=" * 60)

    try:
        from langgraph.prebuilt import ToolNode
        from langgraph.graph import StateGraph, END
        from langchain_core.tools import tool
        from typing import TypedDict, Annotated, Sequence
        import operator

        # Create a simple sync tool for testing
        @tool
        def test_add(a: int, b: int) -> int:
            """Add two numbers."""
            return a + b

        @tool
        def test_multiply(a: int, b: int) -> int:
            """Multiply two numbers."""
            return a * b

        test_tools = [test_add, test_multiply]
        print(f"  Created tools: {[t.name for t in test_tools]}")

        # Define a simple state
        class ToolTestState(TypedDict):
            messages: Annotated[Sequence[AIMessage | ToolMessage], operator.add]

        # Build a minimal graph to test ToolNode
        def start_node(state):
            tool_call = ToolCall(name="test_add", args={"a": 5, "b": 3}, id="test-add-1")
            return {"messages": [AIMessage(content="", tool_calls=[tool_call])]}

        workflow = StateGraph(ToolTestState)
        workflow.add_node("start", start_node)
        workflow.add_node("tools", ToolNode(test_tools))
        workflow.set_entry_point("start")
        workflow.add_edge("start", "tools")
        workflow.add_edge("tools", END)

        test_app = workflow.compile(checkpointer=None)
        print("  Built test graph: start → tools → END")

        # Execute the graph
        result = test_app.invoke({"messages": []})
        print(f"  Graph execution result: {len(result['messages'])} messages")

        # Verify result
        assert "messages" in result, "Result missing 'messages' key"
        tool_messages = [m for m in result["messages"] if isinstance(m, ToolMessage)]
        assert len(tool_messages) > 0, "No ToolMessage in result"

        tool_result = tool_messages[0]
        print(f"  Tool result content: {tool_result.content}")
        assert "8" in str(tool_result.content), f"Expected result '8', got '{tool_result.content}'"
        print("  ✓ ToolNode correctly executes tools")

        return True
    except Exception as e:
        print(f"  ✗ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_complete_loop_with_mocks():
    """Test 4: Verify complete agent → ToolNode → agent → response loop."""
    print("\n" + "=" * 60)
    print("TEST 4: Complete Loop Verification (with mocks)")
    print("=" * 60)

    try:
        from langchain_core.tools import tool
        from langgraph.graph import StateGraph, END
        from langgraph.prebuilt import ToolNode, tools_condition
        from langchain_core.messages import BaseMessage, SystemMessage
        from typing import TypedDict, Annotated, Sequence
        import operator

        # Define state
        class TestAgentState(TypedDict):
            messages: Annotated[Sequence[BaseMessage], operator.add]

        # Create a simple test tool
        @tool
        def get_drug_info(drug_name: str) -> str:
            """Get information about a drug."""
            return f"Drug info for {drug_name}: This is a blood thinner used to prevent stroke."

        test_tools = [get_drug_info]

        # Track execution steps
        execution_log = []

        # Create mock LLM responses
        # First call: LLM decides to call tool
        # Second call: LLM gives final answer after receiving tool result
        mock_responses = [
            # First response: call the tool
            AIMessage(content="", tool_calls=[
                ToolCall(name="get_drug_info", args={"drug_name": "Eliquis"}, id="call-1")
            ]),
            # Second response: final answer using tool result
            AIMessage(content="Based on my search, Eliquis is a blood thinner used to prevent stroke.")
        ]
        response_index = [0]  # Use list to allow mutation in closure

        def mock_agent(state: TestAgentState):
            """Mock agent node that simulates LLM behavior."""
            execution_log.append(f"agent_call_{response_index[0] + 1}")
            response = mock_responses[response_index[0]]
            response_index[0] += 1
            return {"messages": [response]}

        # Build test graph
        workflow = StateGraph(TestAgentState)
        workflow.add_node("agent", mock_agent)
        workflow.add_node("tools", ToolNode(test_tools))
        workflow.set_entry_point("agent")
        workflow.add_conditional_edges("agent", tools_condition)
        workflow.add_edge("tools", "agent")

        test_app = workflow.compile(checkpointer=None)
        print("  Created test graph with mock agent")

        # Run the graph
        inputs = {"messages": [HumanMessage(content="What is Eliquis?")]}
        result = await test_app.ainvoke(inputs)

        print(f"\n  Execution log: {execution_log}")
        print(f"  Total messages: {len(result['messages'])}")

        # Verify the flow
        messages = result["messages"]

        # Should have: HumanMessage, AIMessage(tool_call), ToolMessage, AIMessage(response)
        print("\n  Message flow:")
        for i, msg in enumerate(messages):
            msg_type = type(msg).__name__
            content = getattr(msg, 'content', '')[:50] if hasattr(msg, 'content') else ''
            tool_calls = getattr(msg, 'tool_calls', None)
            if tool_calls:
                print(f"    {i+1}. {msg_type} with tool_calls: {[tc['name'] for tc in tool_calls]}")
            else:
                print(f"    {i+1}. {msg_type}: {content}...")

        # Verify agent was called twice (before and after tool)
        assert len(execution_log) == 2, f"Expected agent called 2 times, got {len(execution_log)}"
        print("\n  ✓ Agent called twice (before and after tool execution)")

        # Verify tool was executed
        tool_messages = [m for m in messages if isinstance(m, ToolMessage)]
        assert len(tool_messages) == 1, f"Expected 1 ToolMessage, got {len(tool_messages)}"
        assert "Eliquis" in tool_messages[0].content
        print("  ✓ Tool was executed and returned result")

        # Verify final response
        final_msg = messages[-1]
        assert isinstance(final_msg, AIMessage), "Final message should be AIMessage"
        assert not final_msg.tool_calls, "Final message should not have tool_calls"
        assert "blood thinner" in final_msg.content.lower() or "stroke" in final_msg.content.lower()
        print("  ✓ Final response generated after tool execution")

        print("\n  Complete loop verified: agent → ToolNode → agent → END")
        return True

    except Exception as e:
        print(f"  ✗ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_actual_agent_graph_structure():
    """Test 5: Verify the actual agent_graph.py has correct structure for the loop."""
    print("\n" + "=" * 60)
    print("TEST 5: Actual Agent Graph Loop Structure")
    print("=" * 60)

    try:
        from backend.agent_graph import app, workflow, tools, llm_with_tools, reasoner

        # Verify LLM has tools bound
        print(f"  LLM type: {type(llm_with_tools).__name__}")
        assert hasattr(llm_with_tools, 'bound'), "LLM should have bound tools"
        print("  ✓ LLM has tools bound")

        # Verify reasoner function exists and is callable
        assert callable(reasoner), "reasoner should be callable"
        print("  ✓ reasoner function is callable")

        # Verify the compiled app has the correct graph type
        app_type = type(app).__name__
        print(f"  Compiled app type: {app_type}")
        assert "CompiledStateGraph" in app_type or "CompiledGraph" in app_type
        print("  ✓ App is a compiled state graph")

        # Check the graph can be introspected
        graph = app.get_graph()
        nodes = [n for n in graph.nodes]
        edges = [(e.source, e.target) for e in graph.edges]

        print(f"  Nodes: {nodes}")
        print(f"  Edges: {edges}")

        # Verify the loop edge exists
        loop_exists = any(e[0] == 'tools' and e[1] == 'agent' for e in edges)
        assert loop_exists, "Missing tools → agent edge (loop back)"
        print("  ✓ Loop edge (tools → agent) exists")

        return True
    except Exception as e:
        print(f"  ✗ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run all verification tests."""
    print("\n" + "=" * 60)
    print("AGENT → TOOLNODE → AGENT LOOP VERIFICATION")
    print("=" * 60)
    print("Testing agent tool loop with LangGraph")

    results = []

    # Run tests
    results.append(("Graph Structure", test_graph_structure()))
    results.append(("tools_condition Routing", test_tools_condition_routing()))
    results.append(("ToolNode Execution", test_tool_node_execution()))
    results.append(("Complete Loop (Mocked)", await test_complete_loop_with_mocks()))
    results.append(("Actual Agent Graph Structure", test_actual_agent_graph_structure()))

    # Summary
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)

    passed = 0
    failed = 0
    for name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"  {status}: {name}")
        if result:
            passed += 1
        else:
            failed += 1

    print(f"\n  Total: {passed}/{len(results)} tests passed")

    if failed == 0:
        print("\n✅ ALL VERIFICATIONS PASSED")
        print("   Agent → ToolNode → Agent → Response loop works correctly!")
        return 0
    else:
        print(f"\n❌ {failed} VERIFICATION(S) FAILED")
        return 1


if __name__ == "__main__":
    # Set up minimal environment for imports
    os.environ.setdefault("SUPABASE_URL", "http://dummy.supabase.co")
    os.environ.setdefault("SUPABASE_KEY", "dummy_key")
    os.environ.setdefault("ANTHROPIC_API_KEY", "dummy_key_for_compile_test")
    os.environ.setdefault("PUBMED_EMAIL", "test@example.com")

    exit_code = asyncio.run(main())
    sys.exit(exit_code)
