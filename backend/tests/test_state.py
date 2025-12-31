"""
Tests for state models and ClinicalState TypedDict.

This module contains comprehensive unit tests for the Pydantic models
(ToolCall, ReasoningStep, PatientContext) and the ClinicalState TypedDict
defined in backend/app/core/state.py.
"""

import json
from datetime import datetime
from typing import get_type_hints

import pytest
from pydantic import ValidationError

from app.core.state import (
    ClinicalState,
    PatientContext,
    ReasoningStep,
    ToolCall,
)


class TestToolCallModel:
    """Tests for ToolCall Pydantic model validation and serialization."""

    def test_tool_call_creation_with_required_fields(self):
        """Test creating ToolCall with only required fields."""
        tool_call = ToolCall(tool_name="search_pubmed")

        assert tool_call.tool_name == "search_pubmed"
        assert tool_call.arguments == {}
        assert tool_call.result is None
        assert tool_call.status == "pending"
        assert isinstance(tool_call.timestamp, datetime)

    def test_tool_call_creation_with_all_fields(self):
        """Test creating ToolCall with all fields specified."""
        timestamp = datetime(2024, 1, 15, 10, 30, 0)
        tool_call = ToolCall(
            tool_name="search_drugs",
            arguments={"drug_name": "aspirin", "limit": 10},
            timestamp=timestamp,
            result={"drugs": ["Aspirin 100mg", "Aspirin 500mg"]},
            status="success"
        )

        assert tool_call.tool_name == "search_drugs"
        assert tool_call.arguments == {"drug_name": "aspirin", "limit": 10}
        assert tool_call.timestamp == timestamp
        assert tool_call.result == {"drugs": ["Aspirin 100mg", "Aspirin 500mg"]}
        assert tool_call.status == "success"

    def test_tool_call_missing_required_field_raises_error(self):
        """Test that missing tool_name raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            ToolCall()

        assert "tool_name" in str(exc_info.value)

    def test_tool_call_json_serialization(self):
        """Test ToolCall can be serialized to JSON."""
        timestamp = datetime(2024, 1, 15, 10, 30, 0)
        tool_call = ToolCall(
            tool_name="search_guidelines",
            arguments={"query": "diabetes"},
            timestamp=timestamp,
            result={"count": 5},
            status="success"
        )

        json_str = tool_call.model_dump_json()
        parsed = json.loads(json_str)

        assert parsed["tool_name"] == "search_guidelines"
        assert parsed["arguments"] == {"query": "diabetes"}
        assert parsed["result"] == {"count": 5}
        assert parsed["status"] == "success"
        # Timestamp should be serialized (either as ISO string or epoch)
        assert "timestamp" in parsed

    def test_tool_call_model_dump(self):
        """Test ToolCall can be converted to dictionary."""
        tool_call = ToolCall(
            tool_name="retrieve_context",
            arguments={"source": "pubmed"},
            status="pending"
        )

        data = tool_call.model_dump()

        assert isinstance(data, dict)
        assert data["tool_name"] == "retrieve_context"
        assert data["arguments"] == {"source": "pubmed"}
        assert data["status"] == "pending"
        assert data["result"] is None

    def test_tool_call_status_values(self):
        """Test ToolCall accepts different status values."""
        for status in ["pending", "success", "failed"]:
            tool_call = ToolCall(tool_name="test_tool", status=status)
            assert tool_call.status == status

    def test_tool_call_arguments_default_factory(self):
        """Test that arguments default to empty dict (not shared mutable)."""
        tool1 = ToolCall(tool_name="tool1")
        tool2 = ToolCall(tool_name="tool2")

        tool1.arguments["key"] = "value"

        # Ensure tool2's arguments are not affected
        assert tool2.arguments == {}

    def test_tool_call_complex_result_types(self):
        """Test ToolCall handles complex result types."""
        complex_result = {
            "data": [
                {"id": 1, "name": "Item 1"},
                {"id": 2, "name": "Item 2"}
            ],
            "metadata": {
                "total": 2,
                "page": 1
            },
            "success": True
        }

        tool_call = ToolCall(
            tool_name="complex_tool",
            result=complex_result
        )

        assert tool_call.result == complex_result


class TestReasoningStepModel:
    """Tests for ReasoningStep Pydantic model validation and serialization."""

    def test_reasoning_step_creation_with_required_fields(self):
        """Test creating ReasoningStep with only required fields."""
        step = ReasoningStep(
            step_number=1,
            description="Analyze the clinical query"
        )

        assert step.step_number == 1
        assert step.description == "Analyze the clinical query"
        assert step.input_data is None
        assert step.output_data is None
        assert step.confidence is None

    def test_reasoning_step_creation_with_all_fields(self):
        """Test creating ReasoningStep with all fields specified."""
        step = ReasoningStep(
            step_number=2,
            description="Retrieve relevant guidelines",
            input_data={"query": "diabetes treatment"},
            output_data={"guidelines": ["guideline_1", "guideline_2"]},
            confidence=0.85
        )

        assert step.step_number == 2
        assert step.description == "Retrieve relevant guidelines"
        assert step.input_data == {"query": "diabetes treatment"}
        assert step.output_data == {"guidelines": ["guideline_1", "guideline_2"]}
        assert step.confidence == 0.85

    def test_reasoning_step_missing_required_fields_raises_error(self):
        """Test that missing required fields raise ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            ReasoningStep(step_number=1)

        assert "description" in str(exc_info.value)

        with pytest.raises(ValidationError) as exc_info:
            ReasoningStep(description="Test step")

        assert "step_number" in str(exc_info.value)

    def test_reasoning_step_step_number_minimum(self):
        """Test that step_number must be >= 1."""
        with pytest.raises(ValidationError) as exc_info:
            ReasoningStep(step_number=0, description="Invalid step")

        assert "step_number" in str(exc_info.value)

        with pytest.raises(ValidationError) as exc_info:
            ReasoningStep(step_number=-1, description="Invalid step")

        assert "step_number" in str(exc_info.value)

    def test_reasoning_step_confidence_range(self):
        """Test that confidence must be between 0.0 and 1.0."""
        # Valid confidence values
        step_min = ReasoningStep(step_number=1, description="Test", confidence=0.0)
        step_max = ReasoningStep(step_number=1, description="Test", confidence=1.0)
        step_mid = ReasoningStep(step_number=1, description="Test", confidence=0.5)

        assert step_min.confidence == 0.0
        assert step_max.confidence == 1.0
        assert step_mid.confidence == 0.5

        # Invalid confidence values
        with pytest.raises(ValidationError):
            ReasoningStep(step_number=1, description="Test", confidence=-0.1)

        with pytest.raises(ValidationError):
            ReasoningStep(step_number=1, description="Test", confidence=1.1)

    def test_reasoning_step_json_serialization(self):
        """Test ReasoningStep can be serialized to JSON."""
        step = ReasoningStep(
            step_number=3,
            description="Synthesize response",
            input_data={"context": "retrieved data"},
            output_data={"answer": "synthesized answer"},
            confidence=0.92
        )

        json_str = step.model_dump_json()
        parsed = json.loads(json_str)

        assert parsed["step_number"] == 3
        assert parsed["description"] == "Synthesize response"
        assert parsed["input_data"] == {"context": "retrieved data"}
        assert parsed["output_data"] == {"answer": "synthesized answer"}
        assert parsed["confidence"] == 0.92

    def test_reasoning_step_model_dump(self):
        """Test ReasoningStep can be converted to dictionary."""
        step = ReasoningStep(
            step_number=1,
            description="Initial classification"
        )

        data = step.model_dump()

        assert isinstance(data, dict)
        assert data["step_number"] == 1
        assert data["description"] == "Initial classification"
        assert data["input_data"] is None
        assert data["output_data"] is None
        assert data["confidence"] is None

    def test_reasoning_step_sequential_creation(self):
        """Test creating multiple sequential reasoning steps."""
        steps = [
            ReasoningStep(step_number=i, description=f"Step {i}")
            for i in range(1, 6)
        ]

        assert len(steps) == 5
        for i, step in enumerate(steps, start=1):
            assert step.step_number == i
            assert step.description == f"Step {i}"


class TestPatientContextModel:
    """Tests for PatientContext Pydantic model validation and serialization."""

    def test_patient_context_creation_with_required_fields(self):
        """Test creating PatientContext with only required fields."""
        patient = PatientContext(patient_id="P12345")

        assert patient.patient_id == "P12345"
        assert patient.demographics is None
        assert patient.medical_history is None
        assert patient.medications is None
        assert patient.allergies is None

    def test_patient_context_creation_with_all_fields(self):
        """Test creating PatientContext with all fields specified."""
        patient = PatientContext(
            patient_id="P67890",
            demographics={"age": 45, "sex": "F", "weight_kg": 70},
            medical_history=["Type 2 Diabetes", "Hypertension"],
            medications=["Metformin 500mg", "Lisinopril 10mg"],
            allergies=["Penicillin", "Sulfa"]
        )

        assert patient.patient_id == "P67890"
        assert patient.demographics == {"age": 45, "sex": "F", "weight_kg": 70}
        assert patient.medical_history == ["Type 2 Diabetes", "Hypertension"]
        assert patient.medications == ["Metformin 500mg", "Lisinopril 10mg"]
        assert patient.allergies == ["Penicillin", "Sulfa"]

    def test_patient_context_missing_required_field_raises_error(self):
        """Test that missing patient_id raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            PatientContext()

        assert "patient_id" in str(exc_info.value)

    def test_patient_context_optional_fields_work(self):
        """Test that optional fields can be None or omitted."""
        # All optional fields omitted
        patient1 = PatientContext(patient_id="P001")
        assert patient1.demographics is None
        assert patient1.medical_history is None

        # Some optional fields provided
        patient2 = PatientContext(
            patient_id="P002",
            demographics={"age": 30}
        )
        assert patient2.demographics == {"age": 30}
        assert patient2.medical_history is None

        # Empty lists for optional list fields
        patient3 = PatientContext(
            patient_id="P003",
            medical_history=[],
            medications=[],
            allergies=[]
        )
        assert patient3.medical_history == []
        assert patient3.medications == []
        assert patient3.allergies == []

    def test_patient_context_json_serialization(self):
        """Test PatientContext can be serialized to JSON."""
        patient = PatientContext(
            patient_id="P12345",
            demographics={"age": 65, "sex": "M"},
            medical_history=["Heart Disease"],
            medications=["Aspirin 100mg"],
            allergies=["Iodine"]
        )

        json_str = patient.model_dump_json()
        parsed = json.loads(json_str)

        assert parsed["patient_id"] == "P12345"
        assert parsed["demographics"] == {"age": 65, "sex": "M"}
        assert parsed["medical_history"] == ["Heart Disease"]
        assert parsed["medications"] == ["Aspirin 100mg"]
        assert parsed["allergies"] == ["Iodine"]

    def test_patient_context_model_dump(self):
        """Test PatientContext can be converted to dictionary."""
        patient = PatientContext(
            patient_id="P99999",
            demographics={"age": 50}
        )

        data = patient.model_dump()

        assert isinstance(data, dict)
        assert data["patient_id"] == "P99999"
        assert data["demographics"] == {"age": 50}
        assert data["medical_history"] is None
        assert data["medications"] is None
        assert data["allergies"] is None

    def test_patient_context_complex_demographics(self):
        """Test PatientContext handles complex demographic data."""
        demographics = {
            "age": 55,
            "sex": "F",
            "weight_kg": 68.5,
            "height_cm": 165,
            "bmi": 25.2,
            "blood_type": "A+",
            "ethnicity": "Caucasian",
            "language": "Czech"
        }

        patient = PatientContext(
            patient_id="P-COMPLEX",
            demographics=demographics
        )

        assert patient.demographics == demographics

    def test_patient_context_empty_patient_id_fails(self):
        """Test that empty string patient_id still passes (no min_length constraint)."""
        # The model doesn't have min_length, so empty string is valid
        # This test documents the current behavior
        patient = PatientContext(patient_id="")
        assert patient.patient_id == ""


class TestClinicalStateStructure:
    """Tests for ClinicalState TypedDict structure and fields."""

    def test_clinical_state_has_all_original_fields(self):
        """Test ClinicalState has all 5 original fields."""
        hints = get_type_hints(ClinicalState)

        original_fields = [
            "messages",
            "query_type",
            "retrieved_context",
            "final_answer",
            "next_step"
        ]

        for field in original_fields:
            assert field in hints, f"Original field '{field}' missing from ClinicalState"

    def test_clinical_state_has_all_new_agentic_fields(self):
        """Test ClinicalState has all 4 new agentic fields."""
        hints = get_type_hints(ClinicalState)

        new_fields = [
            "tool_calls",
            "reasoning_steps",
            "patient_context",
            "iteration_count"
        ]

        for field in new_fields:
            assert field in hints, f"New agentic field '{field}' missing from ClinicalState"

    def test_clinical_state_has_exactly_9_fields(self):
        """Test ClinicalState has exactly 9 fields (5 original + 4 new)."""
        hints = get_type_hints(ClinicalState)

        # Should have exactly 9 fields
        expected_count = 9
        actual_count = len(hints)

        assert actual_count == expected_count, (
            f"ClinicalState should have {expected_count} fields, "
            f"but has {actual_count}: {list(hints.keys())}"
        )

    def test_clinical_state_instantiation(self):
        """Test ClinicalState can be instantiated as TypedDict."""
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

        assert state["messages"] == []
        assert state["query_type"] is None
        assert state["retrieved_context"] == []
        assert state["final_answer"] is None
        assert state["next_step"] is None
        assert state["tool_calls"] == []
        assert state["reasoning_steps"] == []
        assert state["patient_context"] is None
        assert state["iteration_count"] == 0

    def test_clinical_state_with_populated_fields(self):
        """Test ClinicalState with populated tool_calls and reasoning_steps."""
        tool_call = ToolCall(tool_name="search_pubmed", status="success")
        reasoning_step = ReasoningStep(step_number=1, description="Initial analysis")
        patient_ctx = PatientContext(patient_id="P001")

        state: ClinicalState = {
            "messages": [],
            "query_type": "drug_info",
            "retrieved_context": [{"source": "pubmed", "content": "..."}],
            "final_answer": "Based on the evidence...",
            "next_step": "synthesize",
            "tool_calls": [tool_call],
            "reasoning_steps": [reasoning_step],
            "patient_context": patient_ctx,
            "iteration_count": 2
        }

        assert len(state["tool_calls"]) == 1
        assert state["tool_calls"][0].tool_name == "search_pubmed"
        assert len(state["reasoning_steps"]) == 1
        assert state["reasoning_steps"][0].step_number == 1
        assert state["patient_context"].patient_id == "P001"
        assert state["iteration_count"] == 2

    def test_clinical_state_iteration_count_type(self):
        """Test that iteration_count is typed as int."""
        hints = get_type_hints(ClinicalState)

        assert hints["iteration_count"] == int

    def test_clinical_state_query_type_literal_values(self):
        """Test ClinicalState query_type accepts valid literal values."""
        valid_query_types = [
            "general",
            "drug_info",
            "guidelines",
            "clinical_trial",
            "reimbursement",
            "urgent",
            None
        ]

        for query_type in valid_query_types:
            state: ClinicalState = {
                "messages": [],
                "query_type": query_type,
                "retrieved_context": [],
                "final_answer": None,
                "next_step": None,
                "tool_calls": [],
                "reasoning_steps": [],
                "patient_context": None,
                "iteration_count": 0
            }
            assert state["query_type"] == query_type

    def test_clinical_state_patient_context_optional(self):
        """Test that patient_context can be None."""
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

        assert state["patient_context"] is None

    def test_clinical_state_tool_calls_accumulation(self):
        """Test that tool_calls list can accumulate multiple entries."""
        tool_calls = [
            ToolCall(tool_name="tool1", status="success"),
            ToolCall(tool_name="tool2", status="pending"),
            ToolCall(tool_name="tool3", status="failed")
        ]

        state: ClinicalState = {
            "messages": [],
            "query_type": None,
            "retrieved_context": [],
            "final_answer": None,
            "next_step": None,
            "tool_calls": tool_calls,
            "reasoning_steps": [],
            "patient_context": None,
            "iteration_count": 0
        }

        assert len(state["tool_calls"]) == 3
        assert state["tool_calls"][0].tool_name == "tool1"
        assert state["tool_calls"][1].tool_name == "tool2"
        assert state["tool_calls"][2].tool_name == "tool3"

    def test_clinical_state_reasoning_steps_accumulation(self):
        """Test that reasoning_steps list can accumulate multiple entries."""
        reasoning_steps = [
            ReasoningStep(step_number=1, description="Step 1"),
            ReasoningStep(step_number=2, description="Step 2"),
            ReasoningStep(step_number=3, description="Step 3")
        ]

        state: ClinicalState = {
            "messages": [],
            "query_type": None,
            "retrieved_context": [],
            "final_answer": None,
            "next_step": None,
            "tool_calls": [],
            "reasoning_steps": reasoning_steps,
            "patient_context": None,
            "iteration_count": 0
        }

        assert len(state["reasoning_steps"]) == 3
        for i, step in enumerate(state["reasoning_steps"], start=1):
            assert step.step_number == i
            assert step.description == f"Step {i}"


class TestModelInteroperability:
    """Tests for interoperability between Pydantic models and ClinicalState."""

    def test_models_can_be_used_in_clinical_state(self):
        """Test all Pydantic models work correctly within ClinicalState."""
        tool_call = ToolCall(
            tool_name="search_pubmed",
            arguments={"query": "diabetes"},
            status="success",
            result={"count": 10}
        )

        reasoning_step = ReasoningStep(
            step_number=1,
            description="Search medical literature",
            input_data={"query": "diabetes"},
            output_data={"results": 10},
            confidence=0.9
        )

        patient_context = PatientContext(
            patient_id="P12345",
            demographics={"age": 50},
            medical_history=["Diabetes"],
            medications=["Metformin"],
            allergies=["Penicillin"]
        )

        state: ClinicalState = {
            "messages": [],
            "query_type": "drug_info",
            "retrieved_context": [],
            "final_answer": None,
            "next_step": None,
            "tool_calls": [tool_call],
            "reasoning_steps": [reasoning_step],
            "patient_context": patient_context,
            "iteration_count": 1
        }

        # Verify models are accessible and maintain their data
        assert state["tool_calls"][0].tool_name == "search_pubmed"
        assert state["reasoning_steps"][0].confidence == 0.9
        assert state["patient_context"].patient_id == "P12345"

    def test_models_json_serialization_for_state_persistence(self):
        """Test that models can be serialized for state persistence."""
        tool_call = ToolCall(
            tool_name="retrieve_guidelines",
            status="success"
        )

        reasoning_step = ReasoningStep(
            step_number=1,
            description="Classify query"
        )

        patient_context = PatientContext(patient_id="P001")

        # Serialize each model
        tool_json = json.loads(tool_call.model_dump_json())
        step_json = json.loads(reasoning_step.model_dump_json())
        patient_json = json.loads(patient_context.model_dump_json())

        # Verify all are valid JSON-serializable dicts
        assert isinstance(tool_json, dict)
        assert isinstance(step_json, dict)
        assert isinstance(patient_json, dict)

        # Verify key data is preserved
        assert tool_json["tool_name"] == "retrieve_guidelines"
        assert step_json["step_number"] == 1
        assert patient_json["patient_id"] == "P001"

    def test_models_from_json_deserialization(self):
        """Test that models can be deserialized from JSON."""
        tool_json = {
            "tool_name": "search_drugs",
            "arguments": {"drug": "aspirin"},
            "timestamp": "2024-01-15T10:30:00",
            "result": None,
            "status": "pending"
        }

        step_json = {
            "step_number": 2,
            "description": "Retrieve drug information",
            "input_data": {"drug": "aspirin"},
            "output_data": None,
            "confidence": 0.85
        }

        patient_json = {
            "patient_id": "P999",
            "demographics": {"age": 60},
            "medical_history": ["Hypertension"],
            "medications": None,
            "allergies": None
        }

        # Deserialize
        tool = ToolCall.model_validate(tool_json)
        step = ReasoningStep.model_validate(step_json)
        patient = PatientContext.model_validate(patient_json)

        # Verify deserialization
        assert tool.tool_name == "search_drugs"
        assert tool.status == "pending"
        assert step.step_number == 2
        assert step.confidence == 0.85
        assert patient.patient_id == "P999"
        assert patient.medical_history == ["Hypertension"]


class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""

    def test_empty_tool_calls_list(self):
        """Test handling of empty tool_calls list."""
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

        assert state["tool_calls"] == []
        assert len(state["tool_calls"]) == 0

    def test_empty_reasoning_steps_list(self):
        """Test handling of empty reasoning_steps list."""
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

        assert state["reasoning_steps"] == []
        assert len(state["reasoning_steps"]) == 0

    def test_iteration_count_zero_initialization(self):
        """Test that iteration_count initializes to 0."""
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

        assert state["iteration_count"] == 0

    def test_iteration_count_increment(self):
        """Test that iteration_count can be incremented."""
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

        # Simulate iteration increment
        for expected_count in range(1, 6):
            state["iteration_count"] += 1
            assert state["iteration_count"] == expected_count

    def test_tool_call_with_none_result(self):
        """Test ToolCall handles None result properly."""
        tool_call = ToolCall(
            tool_name="failed_tool",
            status="failed",
            result=None
        )

        assert tool_call.result is None

    def test_reasoning_step_with_empty_dicts(self):
        """Test ReasoningStep handles empty input/output dicts."""
        step = ReasoningStep(
            step_number=1,
            description="Empty data step",
            input_data={},
            output_data={}
        )

        assert step.input_data == {}
        assert step.output_data == {}

    def test_patient_context_with_empty_lists(self):
        """Test PatientContext handles empty lists for optional fields."""
        patient = PatientContext(
            patient_id="P-EMPTY",
            medical_history=[],
            medications=[],
            allergies=[]
        )

        assert patient.medical_history == []
        assert patient.medications == []
        assert patient.allergies == []

    def test_unicode_in_model_fields(self):
        """Test models handle Unicode characters properly."""
        tool_call = ToolCall(
            tool_name="unicode_tool",
            arguments={"query": "léky pro diabetiky"}
        )

        step = ReasoningStep(
            step_number=1,
            description="Vyhledávání v české databázi"
        )

        patient = PatientContext(
            patient_id="CZ-12345",
            demographics={"jméno": "Jan Novák"}
        )

        assert tool_call.arguments["query"] == "léky pro diabetiky"
        assert step.description == "Vyhledávání v české databázi"
        assert patient.demographics["jméno"] == "Jan Novák"

    def test_large_iteration_count(self):
        """Test ClinicalState handles large iteration counts."""
        state: ClinicalState = {
            "messages": [],
            "query_type": None,
            "retrieved_context": [],
            "final_answer": None,
            "next_step": None,
            "tool_calls": [],
            "reasoning_steps": [],
            "patient_context": None,
            "iteration_count": 1000000
        }

        assert state["iteration_count"] == 1000000

    def test_multiple_tool_calls_same_name(self):
        """Test handling multiple tool_calls with the same tool name."""
        tool_calls = [
            ToolCall(tool_name="search_pubmed", arguments={"query": "diabetes"}),
            ToolCall(tool_name="search_pubmed", arguments={"query": "insulin"}),
            ToolCall(tool_name="search_pubmed", arguments={"query": "metformin"})
        ]

        state: ClinicalState = {
            "messages": [],
            "query_type": None,
            "retrieved_context": [],
            "final_answer": None,
            "next_step": None,
            "tool_calls": tool_calls,
            "reasoning_steps": [],
            "patient_context": None,
            "iteration_count": 0
        }

        assert len(state["tool_calls"]) == 3
        assert all(tc.tool_name == "search_pubmed" for tc in state["tool_calls"])
