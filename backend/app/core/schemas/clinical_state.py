from typing import Annotated, List, Optional, Literal, TypedDict
from pydantic import BaseModel, Field
from langgraph.graph.message import add_messages


class Citation(BaseModel):
    source_type: str = Field(
        ..., description="Type of source (e.g., 'pubmed', 'sukl', 'guideline')"
    )
    identifier: str = Field(
        ..., description="Unique identifier (e.g., PMID, SÚKL code)"
    )
    title: str = Field(..., description="Title of the source")
    url: Optional[str] = Field(None, description="URL to the source")
    relevance_score: float = Field(..., description="Relevance score of the citation")
    snippet: str = Field(..., description="Relevant snippet from the source")


class RetrievalResult(BaseModel):
    content: str = Field(..., description="The retrieved content")
    citations: List[Citation] = Field(
        default_factory=list, description="List of citations associated with the result"
    )
    confidence: float = Field(..., description="Confidence score of the retrieval")
    agent_source: str = Field(
        ..., description="Source agent/tool that retrieved the result"
    )


class QueryClassification(BaseModel):
    primary_intent: Literal[
        "drug_info",
        "drug_interaction",
        "guideline_lookup",
        "clinical_question",
        "pricing_coverage",
        "urgent_diagnostic",
        "compound_query",
        "general",
    ] = Field(..., description="Primary intent of the query")
    secondary_intents: List[str] = Field(
        default_factory=list, description="Secondary intents if applicable"
    )
    entities: List[str] = Field(
        default_factory=list,
        description="Extracted entities (drugs, conditions, ATC codes)",
    )
    urgency: Literal["routine", "priority", "urgent"] = Field(
        ..., description="Urgency level of the query"
    )


class ClinicalState(TypedDict):
    messages: Annotated[list, add_messages]
    classification: Optional[QueryClassification]
    drug_results: Optional[RetrievalResult]
    pubmed_results: Optional[RetrievalResult]
    all_citations: List[Citation]
    overall_confidence: float
    response_complete: bool
