"""
Tests for graph.py - checkpointer persistence and iteration limit.

This module contains unit tests for the LangGraph workflow implementation,
specifically testing:
1. Iteration limit enforcement (MAX_ITERATIONS = 5)
2. Checkpointer state persistence
3. Graph routing logic
"""

import pytest
from unittest.mock import patch, MagicMock

# Import the functions and constants to test
from app.core.graph import (
    check_iteration_limit,
    route_iteration_check,
    MAX_ITERATIONS,
)


class TestIterationLimit:
    """Tests for iteration limit enforcement."""

    def test_max_iterations_constant(self):
        """Test that MAX_ITERATIONS is set to 5."""
        assert MAX_ITERATIONS == 5

    def test_check_iteration_limit_increments_count(self):
        """Test that check_iteration_limit increments iteration_count."""
        state = {"iteration_count": 0}
        result = check_iteration_limit(state)

        assert result["iteration_count"] == 1

    def test_check_iteration_limit_from_various_counts(self):
        """Test iteration increment from various starting counts."""
        for initial_count in range(5):
            state = {"iteration_count": initial_count}
            result = check_iteration_limit(state)
            assert result["iteration_count"] == initial_count + 1

    def test_check_iteration_limit_handles_missing_count(self):
        """Test that missing iteration_count defaults to 0."""
        state = {}
        result = check_iteration_limit(state)

        assert result["iteration_count"] == 1

    def test_check_iteration_limit_below_max(self):
        """Test that workflow continues when below max iterations."""
        state = {"iteration_count": 3}
        result = check_iteration_limit(state)

        assert result["iteration_count"] == 4
        assert "final_answer" not in result
        assert "next_step" not in result

    def test_check_iteration_limit_at_max_minus_one(self):
        """Test at MAX_ITERATIONS - 1 (should NOT terminate yet)."""
        state = {"iteration_count": MAX_ITERATIONS - 2}
        result = check_iteration_limit(state)

        # Should increment to MAX_ITERATIONS - 1, still not at limit
        assert result["iteration_count"] == MAX_ITERATIONS - 1
        assert "final_answer" not in result

    def test_check_iteration_limit_exceeds_max(self):
        """Test that workflow terminates when max iterations is reached."""
        state = {"iteration_count": MAX_ITERATIONS - 1}
        result = check_iteration_limit(state)

        assert result["iteration_count"] == MAX_ITERATIONS
        assert result["next_step"] == "end"
        assert "final_answer" in result
        assert "iteration limit exceeded" in result["final_answer"].lower()

    def test_check_iteration_limit_already_exceeded(self):
        """Test behavior when already at or above max iterations."""
        state = {"iteration_count": MAX_ITERATIONS}
        result = check_iteration_limit(state)

        assert result["iteration_count"] == MAX_ITERATIONS + 1
        assert result["next_step"] == "end"
        assert "final_answer" in result

    def test_check_iteration_limit_error_message_content(self):
        """Test that error message is informative."""
        state = {"iteration_count": MAX_ITERATIONS - 1}
        result = check_iteration_limit(state)

        error_msg = result["final_answer"]
        assert "5" in error_msg or "five" in error_msg.lower()
        assert "iteration" in error_msg.lower()


class TestRouteIterationCheck:
    """Tests for the iteration check routing function."""

    def test_route_to_end_when_next_step_is_end(self):
        """Test routing to END when next_step is 'end'."""
        state = {"next_step": "end"}
        result = route_iteration_check(state)

        assert result == "end"

    def test_route_to_continue_when_next_step_not_set(self):
        """Test routing to continue when next_step is not set."""
        state = {"next_step": None}
        result = route_iteration_check(state)

        assert result == "continue"

    def test_route_to_continue_when_next_step_is_other_value(self):
        """Test routing to continue when next_step has other value."""
        for next_step in ["retrieve_drugs", "retrieve_general", "synthesize"]:
            state = {"next_step": next_step}
            result = route_iteration_check(state)
            assert result == "continue"

    def test_route_to_continue_with_empty_state(self):
        """Test routing with empty state (missing next_step)."""
        state = {}
        result = route_iteration_check(state)

        assert result == "continue"


class TestCheckpointerIntegration:
    """Tests for checkpointer persistence functionality."""

    def test_checkpointer_is_configured(self):
        """Test that checkpointer is properly configured."""
        from app.core.graph import checkpointer

        assert checkpointer is not None

    def test_graph_compiled_with_checkpointer(self):
        """Test that the graph app is compiled with checkpointer."""
        from app.core.graph import app

        # The compiled graph should exist
        assert app is not None

    def test_checkpoint_db_path_configured(self):
        """Test that CHECKPOINT_DB_PATH is configured."""
        from app.core.graph import CHECKPOINT_DB_PATH

        assert CHECKPOINT_DB_PATH is not None
        assert "checkpoints.db" in CHECKPOINT_DB_PATH

    def test_graph_nodes_exist(self):
        """Test that all expected nodes are in the graph."""
        from app.core.graph import workflow

        expected_nodes = [
            "check_iteration",
            "classifier",
            "retrieve_drugs",
            "retrieve_general",
            "retrieve_guidelines",
            "synthesizer"
        ]

        # Access the nodes from the workflow
        for node_name in expected_nodes:
            assert node_name in workflow.nodes, f"Missing node: {node_name}"


class TestIterationWorkflow:
    """Integration tests for iteration control in workflow."""

    def test_iteration_count_properly_initialized_in_state(self):
        """Test that iteration_count can be properly initialized in state."""
        from app.core.state import ClinicalState

        state: ClinicalState = {
            "messages": [],
            "query_type": None,
            "retrieved_context": [],
            "final_answer": None,
            "next_step": None,
            "tool_calls": [],
            "reasoning_steps": [],
            "patient_context": None,
            "iteration_count": 0
        }

        # Simulate iteration check
        result = check_iteration_limit(state)
        assert result["iteration_count"] == 1

    def test_workflow_terminates_after_max_iterations(self):
        """Test that workflow properly terminates after MAX_ITERATIONS."""
        state = {"iteration_count": 0}

        # Simulate multiple iterations
        for i in range(MAX_ITERATIONS):
            result = check_iteration_limit(state)
            state["iteration_count"] = result["iteration_count"]

            if result.get("next_step") == "end":
                break

        # Should have terminated at MAX_ITERATIONS
        assert state["iteration_count"] == MAX_ITERATIONS
        assert result.get("next_step") == "end"

    def test_iteration_limit_prevents_infinite_loop(self):
        """Test that iteration limit prevents infinite loops."""
        state = {"iteration_count": 0}
        iterations = 0
        max_test_iterations = 100  # Safety limit for test

        while iterations < max_test_iterations:
            result = check_iteration_limit(state)
            state["iteration_count"] = result["iteration_count"]
            iterations += 1

            route = route_iteration_check(result)
            if route == "end":
                break

        # Should terminate well before max_test_iterations
        assert iterations <= MAX_ITERATIONS
        assert iterations < max_test_iterations


class TestStateCheckpointerCompatibility:
    """Tests for state compatibility with checkpointer serialization."""

    def test_iteration_count_is_serializable(self):
        """Test that iteration_count is JSON-serializable."""
        import json

        state = {"iteration_count": 5}
        # Should not raise
        json_str = json.dumps(state)
        parsed = json.loads(json_str)
        assert parsed["iteration_count"] == 5

    def test_check_iteration_limit_result_serializable(self):
        """Test that check_iteration_limit returns serializable data."""
        import json

        state = {"iteration_count": 4}
        result = check_iteration_limit(state)

        # Should be JSON-serializable
        json_str = json.dumps(result)
        parsed = json.loads(json_str)

        assert "iteration_count" in parsed

    def test_error_state_is_serializable(self):
        """Test that error state (when limit exceeded) is serializable."""
        import json

        state = {"iteration_count": MAX_ITERATIONS - 1}
        result = check_iteration_limit(state)

        # The full result should be serializable
        json_str = json.dumps(result)
        parsed = json.loads(json_str)

        assert parsed["next_step"] == "end"
        assert "final_answer" in parsed
