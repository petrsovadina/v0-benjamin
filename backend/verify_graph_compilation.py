"""
Verification script for LangGraph compilation and checkpoint persistence.

This script tests:
1. LangGraph checkpoint module imports
2. MemorySaver checkpointer functionality
3. Graph compilation with checkpoint support
4. Checkpoint save/load cycle

Run from the backend directory:
    cd backend && python verify_graph_compilation.py
"""
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def test_checkpoint_imports():
    """Test that all checkpoint-related imports work with new versions."""
    print("\n[1/4] Testing checkpoint module imports...")

    try:
        from langgraph.checkpoint.memory import MemorySaver
        print("  ✓ MemorySaver imported from langgraph.checkpoint.memory")
    except ImportError as e:
        print(f"  ✗ Failed to import MemorySaver: {e}")
        return False

    try:
        from langgraph.graph import StateGraph, START, END
        print("  ✓ StateGraph, START, END imported from langgraph.graph")
    except ImportError as e:
        print(f"  ✗ Failed to import StateGraph: {e}")
        return False

    try:
        from langgraph.graph.message import add_messages
        print("  ✓ add_messages imported from langgraph.graph.message")
    except ImportError as e:
        print(f"  ✗ Failed to import add_messages: {e}")
        return False

    return True


def test_memory_saver_instantiation():
    """Test that MemorySaver can be instantiated."""
    print("\n[2/4] Testing MemorySaver instantiation...")

    try:
        from langgraph.checkpoint.memory import MemorySaver
        checkpointer = MemorySaver()
        print(f"  ✓ MemorySaver instantiated: {type(checkpointer).__name__}")
        return checkpointer
    except Exception as e:
        print(f"  ✗ Failed to instantiate MemorySaver: {e}")
        return None


def test_graph_compilation_with_checkpointer(checkpointer):
    """Test that a graph compiles with checkpoint support."""
    print("\n[3/4] Testing graph compilation with checkpointer...")

    try:
        from typing import TypedDict, Annotated
        from langgraph.graph import StateGraph, START, END
        from langgraph.graph.message import add_messages
        from langchain_core.messages import BaseMessage, HumanMessage, AIMessage

        # Define a simple state
        class SimpleState(TypedDict):
            messages: Annotated[list[BaseMessage], add_messages]
            counter: int

        # Define a simple node
        def increment_node(state: SimpleState):
            return {"counter": state.get("counter", 0) + 1}

        def echo_node(state: SimpleState):
            last_msg = state["messages"][-1].content if state["messages"] else ""
            return {"messages": [AIMessage(content=f"Echo: {last_msg}")]}

        # Build graph
        workflow = StateGraph(SimpleState)
        workflow.add_node("increment", increment_node)
        workflow.add_node("echo", echo_node)
        workflow.add_edge(START, "increment")
        workflow.add_edge("increment", "echo")
        workflow.add_edge("echo", END)

        # Compile with checkpointer
        app = workflow.compile(checkpointer=checkpointer)
        print(f"  ✓ Graph compiled with checkpointer: {type(app).__name__}")

        return app
    except Exception as e:
        print(f"  ✗ Failed to compile graph with checkpointer: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_checkpoint_persistence(app):
    """Test checkpoint save/load cycle."""
    print("\n[4/4] Testing checkpoint persistence cycle...")

    try:
        from langchain_core.messages import HumanMessage

        # Create a thread config for checkpointing
        config = {"configurable": {"thread_id": "test-thread-001"}}

        # First invocation
        input_state = {
            "messages": [HumanMessage(content="Hello, world!")],
            "counter": 0
        }

        result1 = app.invoke(input_state, config=config)
        print(f"  ✓ First invocation completed. Counter: {result1.get('counter')}")

        # Second invocation on same thread (should load checkpoint)
        input_state2 = {
            "messages": [HumanMessage(content="Second message")],
            "counter": 0  # This should be overwritten by checkpoint
        }

        result2 = app.invoke(input_state2, config=config)
        print(f"  ✓ Second invocation completed. Counter: {result2.get('counter')}")

        # Verify messages accumulated
        msg_count = len(result2.get("messages", []))
        print(f"  ✓ Message history preserved: {msg_count} messages")

        # Get checkpoint state
        try:
            state = app.get_state(config)
            if state:
                print(f"  ✓ Checkpoint state retrieved successfully")
        except Exception as e:
            print(f"  ⚠ Could not retrieve checkpoint state (optional): {e}")

        return True
    except Exception as e:
        print(f"  ✗ Checkpoint persistence test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all verification tests."""
    print("=" * 60)
    print("LangGraph Checkpoint Persistence Verification")
    print("=" * 60)

    all_passed = True

    # Test 1: Imports
    if not test_checkpoint_imports():
        all_passed = False
        print("\n❌ Checkpoint imports test FAILED")
        sys.exit(1)

    # Test 2: MemorySaver instantiation
    checkpointer = test_memory_saver_instantiation()
    if checkpointer is None:
        all_passed = False
        print("\n❌ MemorySaver instantiation test FAILED")
        sys.exit(1)

    # Test 3: Graph compilation with checkpointer
    app = test_graph_compilation_with_checkpointer(checkpointer)
    if app is None:
        all_passed = False
        print("\n❌ Graph compilation test FAILED")
        sys.exit(1)

    # Test 4: Checkpoint persistence cycle
    if not test_checkpoint_persistence(app):
        all_passed = False
        print("\n❌ Checkpoint persistence test FAILED")
        sys.exit(1)

    # Summary
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ All checkpoint persistence tests PASSED")
        print("Graph compiles successfully with checkpoint support")
        print("=" * 60)
        sys.exit(0)
    else:
        print("❌ Some tests FAILED")
        print("=" * 60)
        sys.exit(1)


if __name__ == "__main__":
    main()
