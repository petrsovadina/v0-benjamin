"""Test that the START/END pattern imports work correctly."""
# Test that langgraph imports work with START/END
from langgraph.graph import StateGraph, START, END
print('LangGraph imports: OK')

# Test that we can build a simple graph with START/END pattern
from typing import TypedDict

class TestState(TypedDict):
    value: str

graph = StateGraph(TestState)

def test_node(state: TestState):
    return {"value": "test"}

graph.add_node("test", test_node)
graph.add_edge(START, "test")
graph.add_edge("test", END)
app = graph.compile()
print('Graph construction with START/END: OK')

# Verify the syntax in agent_graph.py file is correct
import ast
with open('agent_graph.py', 'r') as f:
    source = f.read()
    # Check that START is imported
    assert 'from langgraph.graph import StateGraph, START, END' in source, "Missing START import"
    # Check that add_edge(START, ...) is used instead of set_entry_point
    assert 'add_edge(START,' in source, "Missing add_edge(START, ...)"
    assert 'set_entry_point' not in source, "Old set_entry_point pattern still present"

print('agent_graph.py syntax check: OK')
print('OK')
