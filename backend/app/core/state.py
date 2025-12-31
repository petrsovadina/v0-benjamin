"""
State models for agentic workflow state management.

This module defines Pydantic models for tracking tool invocations, reasoning steps,
and patient context within the clinical workflow. These models are used by the
extended ClinicalState TypedDict for LangGraph state management.

The ClinicalState TypedDict extends the original 5 fields with 4 new agentic fields:
- tool_calls: Tracks all tool invocations for audit trails
- reasoning_steps: Documents multi-step reasoning chains
- patient_context: Stores patient-specific data for personalized responses
- iteration_count: Controls workflow iteration limits
"""

import operator
from datetime import datetime
from typing import Annotated, Any, Dict, List, Literal, Optional, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
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


# --- STATE DEFINITION ---

class ClinicalState(TypedDict):
    """
    Extended state for clinical query processing with agentic workflow capabilities.

    This TypedDict defines the complete state structure for LangGraph-based clinical
    workflows. It preserves the original 5 fields for backward compatibility while
    adding 4 new fields to support advanced agentic capabilities.

    Original Fields (preserved for backward compatibility):
        messages: Conversation history with automatic message accumulation.
        query_type: Classification of the clinical query type.
        retrieved_context: Documents/data retrieved from various sources.
        final_answer: The synthesized response to the user.
        next_step: Router indicator for conditional workflow branching.

    New Agentic Fields:
        tool_calls: Accumulated list of all tool invocations for audit trails.
        reasoning_steps: Documented chain of reasoning for transparency.
        patient_context: Optional patient-specific data for personalization.
        iteration_count: Counter for workflow iterations (max 5 enforced).

    Usage:
        The state is used with LangGraph's StateGraph and Checkpointer for
        persistent, resumable workflow execution.

    Example:
        >>> state: ClinicalState = {
        ...     "messages": [],
        ...     "query_type": None,
        ...     "retrieved_context": [],
        ...     "final_answer": None,
        ...     "next_step": None,
        ...     "tool_calls": [],
        ...     "reasoning_steps": [],
        ...     "patient_context": None,
        ...     "iteration_count": 0
        ... }
    """
    # Original fields (backward compatible)
    messages: Annotated[List[BaseMessage], add_messages]
    query_type: Optional[
        Literal["general", "drug_info", "guidelines", "clinical_trial", "reimbursement", "urgent"]
    ]
    retrieved_context: List[Dict[str, Any]]
    final_answer: Optional[str]
    next_step: Optional[str]

    # New agentic workflow fields
    tool_calls: Annotated[List[ToolCall], operator.add]
    reasoning_steps: Annotated[List[ReasoningStep], operator.add]
    patient_context: Optional[PatientContext]
    iteration_count: int
