from typing import List, Dict, Any, Literal
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from backend.app.core.llm import get_llm
from backend.app.core.state import ClinicalState
from backend.app.services.search_service import search_service
from pydantic import BaseModel, Field

# --- STATE DEFINITION ---
# ClinicalState is now imported from backend.app.core.state
# It includes the original 5 fields plus 4 new agentic fields:
# - tool_calls: Annotated[List[ToolCall], operator.add]
# - reasoning_steps: Annotated[List[ReasoningStep], operator.add]
# - patient_context: Optional[PatientContext]
# - iteration_count: int

# --- MODELS FOR CLASSIFICATION ---
class QueryClassification(BaseModel):
    query_type: Literal["drug_info", "guidelines", "clinical", "urgent", "reimbursement"] = Field(
        ..., description="Type of clinical query based on content and intent."
    )
    reasoning: str = Field(..., description="Brief reasoning for the classification.")

# --- NODES ---

async def classifier_node(state: ClinicalState):
    """
    Classifies the user query using LLM (or heuristic fallback).
    """
    llm = get_llm()
    last_msg = state["messages"][-1].content
    
    if not llm:
        # Fallback if no LLM configured/mock mode
        lower_msg = last_msg.lower()
        if "lék" in lower_msg or "sukl" in lower_msg:
            return {"query_type": "drug_info", "next_step": "retrieve_drugs"}
        if any(kw in lower_msg for kw in ["guideline", "doporučení", "protokol", "standard", "postup"]):
            return {"query_type": "guidelines", "next_step": "retrieve_guidelines"}
        return {"query_type": "clinical", "next_step": "retrieve_general"}

    # Structured output classification
    structured_llm = llm.with_structured_output(QueryClassification)
    
    classification_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a classification system for a medical assistant. 
        Analyze the query and determine the best category:
        1. drug_info: Specific drug questions, dosage, interactions, SÚKL, prices.
        2. guidelines: Requests for clinical guidelines, protocols, standards.
        3. clinical: General clinical questions, diagnosis, symptoms, treatment options.
        4. urgent: Emergency situations, life-threatening conditions (AIM, CPR).
        5. reimbursement: Insurance coverage, VZP conditions.
        """),
        ("user", "{query}")
    ])
    
    try:
        result = await structured_llm.ainvoke(classification_prompt.format(query=last_msg))
        q_type = result.query_type
    except Exception as e:
        # Fallback on error
        print(f"Classification error: {e}")
        q_type = "clinical"

    # Map to next step
    if q_type == "drug_info":
        next_step = "retrieve_drugs"
    elif q_type == "reimbursement":
        # SÚKL data often contains reimbursement info
        next_step = "retrieve_drugs" 
    elif q_type == "guidelines":
        # Route to dedicated guidelines retrieval (vector similarity search)
        next_step = "retrieve_guidelines"
    elif q_type == "urgent":
        # Urgent queries might skip complex RAG or use specific "emergency" RAG
        next_step = "retrieve_general"
    else:
        next_step = "retrieve_general"

    return {"query_type": q_type, "next_step": next_step}

async def retrieve_drugs_node(state: ClinicalState):
    """
    Retrieves drug information using SearchService (SÚKL).
    """
    query = state["messages"][-1].content
    drugs = await search_service.search_drugs(query)
    
    # Format context
    context_str = ""
    raw_data = []
    for d in drugs:
        context_str += f"Lék: {d.get('name')} (SÚKL: {d.get('sukl_code')})\n"
        context_str += f"Účinná látka: {d.get('active_substance')}\n"
        context_str += f"Dostupnost: {'Dostupný' if d.get('is_available') else 'Nedostupný'}\n\n"
        raw_data.append({"source": "sukl", "data": d})
    
    return {"retrieved_context": raw_data}

async def retrieve_general_node(state: ClinicalState):
    """
    Retrieves literature using SearchService (PubMed).
    """
    query = state["messages"][-1].content
    # Depending on query type, we might adjust queries (e.g. add "guidelines" content)
    papers = await search_service.search_pubmed(query, max_results=3)

    raw_data = []
    for p in papers:
        raw_data.append({"source": "pubmed", "data": p})

    return {"retrieved_context": raw_data}

async def retrieve_guidelines_node(state: ClinicalState):
    """
    Retrieves clinical guidelines using SearchService (vector similarity search).
    Returns guideline chunks with source metadata for citations.
    """
    query = state["messages"][-1].content
    guidelines = await search_service.search_guidelines(query, limit=5)

    raw_data = []
    for g in guidelines:
        raw_data.append({"source": "guidelines", "data": g})

    return {"retrieved_context": raw_data}

async def synthesizer_node(state: ClinicalState):
    """
    Synthesizes the final answer using the Retrieved Context and System Prompt.
    """
    llm = get_llm()
    if not llm:
        return {"final_answer": "LLM not configured."}
        
    context = state.get("retrieved_context", [])
    query_type = state.get("query_type", "clinical")
    
    # Construct Context String for LLM
    context_text = "NALEZENÉ ZDROJE:\n\n"
    citations_data = []
    
    for idx, item in enumerate(context, 1):
        data = item["data"]
        source = item["source"]
        
        if source == "sukl":
            context_text += f"[{idx}] SÚKL: {data.get('name')}\n{data}\n\n"
            citations_data.append(f"[{idx}] SÚKL - {data.get('name')} (Kód: {data.get('sukl_code')})")
        elif source == "pubmed":
            context_text += f"[{idx}] PubMed: {data.get('title')}\nAbstract: {data.get('abstract')}\nUrl: {data.get('url')}\n\n"
            citations_data.append(f"[{idx}] {data.get('authors')[0] if data.get('authors') else 'Unknown'} et al. {data.get('title')}. {data.get('url')}")
        elif source == "guidelines":
            # Format guideline chunks with source and page info for citations
            # Format: 'Source: [filename], page [X]' as per spec
            guideline_source = data.get('source', 'Klinická doporučení')
            page_num = data.get('page', '')
            content = data.get('content', data.get('text', ''))
            page_info = f", page {page_num}" if page_num else ""
            context_text += f"[{idx}] Source: {guideline_source}{page_info}\n{content}\n\n"
            citations_data.append(f"[{idx}] Source: {guideline_source}{page_info}")
    
    # System Prompt (simplified version of the full spec for code brevity, 
    # but capturing the key 'Identity' and 'Principles')
    system_prompt_text = """Jsi Czech MedAI — důvěryhodný AI asistent pro české zdravotnické profesionály.
    
    ZÁKLADNÍ PRINCIPY:
    1. Evidence-based: Odpovědi podložené citacemi [1][2].
    2. Transparentnost: Uváděj zdroje.
    3. Česká lokalizace: Používej české guidelines a terminologii (TK, DM).
    4. Bezpečnost: Neposkytuj diagnózy, jen informace. Při akutních stavech (AIM, CMP) varuj.
    
    FORMÁT ODPOVĚDI:
    1. Přímá odpověď s inline citacemi.
    2. Seznam citací na konci.
    
    Použij poskytnutý kontext k zodpovězení dotazu. Pokud kontext nestačí, přiznej to.
    """
    
    messages = [
        SystemMessage(content=system_prompt_text),
        HumanMessage(content=f"DOTAZ: {state['messages'][-1].content}\n\n{context_text}")
    ]
    
    response = await llm.ainvoke(messages)
    
    return {"final_answer": response.content}

# --- CHECKPOINTER CONFIGURATION ---
# SqliteSaver provides persistent state storage for session recovery.
# The checkpoints.db file is created in the backend directory.
# Thread IDs are required when invoking the graph for session isolation.
CHECKPOINT_DB_PATH = "backend/checkpoints.db"
checkpointer = SqliteSaver.from_conn_string(CHECKPOINT_DB_PATH)

# --- GRAPH CONSTRUCTION ---
workflow = StateGraph(ClinicalState)

workflow.add_node("classifier", classifier_node)
workflow.add_node("retrieve_drugs", retrieve_drugs_node)
workflow.add_node("retrieve_general", retrieve_general_node)
workflow.add_node("retrieve_guidelines", retrieve_guidelines_node)
workflow.add_node("synthesizer", synthesizer_node)

workflow.add_edge(START, "classifier")

def route_query(state: ClinicalState) -> str:
    """Route the query to the appropriate retrieval node based on classification."""
    return state["next_step"]

workflow.add_conditional_edges(
    "classifier",
    route_query,
    {
        "retrieve_drugs": "retrieve_drugs",
        "retrieve_general": "retrieve_general",
        "retrieve_guidelines": "retrieve_guidelines"
    }
)

workflow.add_edge("retrieve_drugs", "synthesizer")
workflow.add_edge("retrieve_general", "synthesizer")
workflow.add_edge("retrieve_guidelines", "synthesizer")
workflow.add_edge("synthesizer", END)

# Compile the graph with checkpointer for state persistence.
# When invoking, use config={"configurable": {"thread_id": "session_123"}}
app = workflow.compile(checkpointer=checkpointer)
