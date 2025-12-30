"""
State models for agentic workflow state management.

This module defines Pydantic models for tracking tool invocations, reasoning steps,
and patient context within the clinical workflow. These models are used by the
extended ClinicalState TypedDict for LangGraph state management.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ToolCall(BaseModel):
    """
    Represents a single tool invocation within the workflow.

    Tracks metadata about tool calls including the tool name, arguments,
    execution timestamp, result, and status. Used for audit trails and
    debugging multi-step agent workflows.

    Attributes:
        tool_name: Name of the invoked tool (e.g., 'search_pubmed', 'search_drugs').
        arguments: Dictionary of arguments passed to the tool.
        timestamp: When the tool was invoked.
        result: The result returned by the tool, if any.
        status: Execution status - one of 'pending', 'success', or 'failed'.
    """

    tool_name: str = Field(
        ...,
        description="Name of the invoked tool"
    )
    arguments: Dict[str, Any] = Field(
        default_factory=dict,
        description="Arguments passed to the tool"
    )
    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="When the tool was called"
    )
    result: Optional[Any] = Field(
        default=None,
        description="Tool execution result"
    )
    status: str = Field(
        default="pending",
        description="Status: pending|success|failed"
    )

    class Config:
        """Pydantic configuration for JSON serialization."""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class ReasoningStep(BaseModel):
    """
    Represents a single step in the multi-step reasoning process.

    Documents the agent's reasoning chain including step ordering,
    description, input/output data, and confidence scores. Enables
    transparency and auditability of AI decision-making.

    Attributes:
        step_number: Sequential step number (1-indexed).
        description: Human-readable description of this reasoning step.
        input_data: Data or context that was input to this step.
        output_data: Result or conclusion from this step.
        confidence: Confidence score for this step (0.0 to 1.0).
    """

    step_number: int = Field(
        ...,
        ge=1,
        description="Sequential step number (1-indexed)"
    )
    description: str = Field(
        ...,
        description="Human-readable description of the reasoning step"
    )
    input_data: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Input data or context for this step"
    )
    output_data: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Output or conclusion from this step"
    )
    confidence: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Confidence score for this step (0.0 to 1.0)"
    )


class PatientContext(BaseModel):
    """
    Stores patient-specific context for personalized clinical responses.

    Contains demographic information, medical history, current medications,
    and known allergies. All fields except patient_id are optional to
    support progressive data collection.

    Attributes:
        patient_id: Unique identifier for the patient.
        demographics: Patient demographic info (age, sex, etc.).
        medical_history: List of relevant medical conditions/history.
        medications: List of current medications.
        allergies: List of known allergies.
    """

    patient_id: str = Field(
        ...,
        description="Unique identifier for the patient"
    )
    demographics: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Patient demographic information (age, sex, weight, etc.)"
    )
    medical_history: Optional[List[str]] = Field(
        default=None,
        description="List of relevant medical conditions and history"
    )
    medications: Optional[List[str]] = Field(
        default=None,
        description="List of current medications"
    )
    allergies: Optional[List[str]] = Field(
        default=None,
        description="List of known allergies"
    )
