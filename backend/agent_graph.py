from typing import TypedDict, Annotated, Sequence, Literal
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition
import operator
import os
from dotenv import load_dotenv

# Import our custom retrievers
from backend.pipeline.retrievers.pubmed import PubMedRetriever
from backend.pipeline.retrievers.sukl_retriever import SuklRetriever
from pathlib import Path

# Load settings (handles .env validation)
from backend.data_processing.config.settings import settings

# Define the state
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]

# Define tools
@tool
async def search_pubmed(query: str):
    """
    Search PubMed for medical articles. Use this when the user asks about clinical studies, 
    drugs, or medical conditions that require evidence.
    """
    retriever = PubMedRetriever()
    return await retriever.search(query)

@tool
async def search_sukl_drugs(query: str):
    """
    Search for official drug information in the Czech SÚKL database.
    Use this when user asks about specific drugs, prices, active substances, or packaging available in Czechia.
    """
    retriever = SuklRetriever()
    return await retriever.search_drugs(query)

tools = [search_pubmed, search_sukl_drugs]

# Define LLM (Claude 3.5 Sonnet)
llm = ChatAnthropic(
    model="claude-3-haiku-20240307",
    temperature=0,
    api_key=settings.ANTHROPIC_API_KEY
)

# Bind tools to LLM
llm_with_tools = llm.bind_tools(tools)

# Import System Prompt
from backend.services.prompts import SYSTEM_PROMPT

# Define nodes
def reasoner(state: AgentState):
    """
    The main reasoning node. Decides whether to call a tool or answer directly.
    Injects System Message tailored for clinical accuracy.
    """
    messages = list(state["messages"])
    
    # Ensure System Message is at the start
    if not isinstance(messages[0], SystemMessage):
        messages.insert(0, SystemMessage(content=SYSTEM_PROMPT))
        
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

# Build the graph
workflow = StateGraph(AgentState)

workflow.add_node("agent", reasoner)
workflow.add_node("tools", ToolNode(tools))

workflow.add_edge(START, "agent")

# Conditional edge: If agent wants to call a tool -> "tools", else -> END
workflow.add_conditional_edges(
    "agent",
    tools_condition,
)

workflow.add_edge("tools", "agent") # Loop back after tool usage

# --- CHECKPOINTER CONFIGURATION ---
# SqliteSaver provides persistent state storage for session recovery.
# Uses the same checkpoint database as the clinical workflow graph.
# Thread IDs are required when invoking the graph for session isolation.
CHECKPOINT_DB_PATH = "backend/checkpoints.db"
checkpointer = SqliteSaver.from_conn_string(CHECKPOINT_DB_PATH)

# Compile the graph with checkpointer for state persistence.
# When invoking, use config={"configurable": {"thread_id": "session_123"}}
app = workflow.compile(checkpointer=checkpointer)
