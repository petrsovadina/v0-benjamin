from typing import TypedDict, List
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from langchain_anthropic import ChatAnthropic
import os
from dotenv import load_dotenv

# Load env variables explicitly
from pathlib import Path
env_path = Path(__file__).resolve().parents[1] / '.env'
load_dotenv(dotenv_path=env_path)

# Define State
class EpicrisisState(TypedDict):
    raw_input: str
    report_content: str

# Define LLM
llm = ChatAnthropic(
    model="claude-3-haiku-20240307",
    temperature=0,
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

# Define Node
def generate_report_node(state: EpicrisisState):
    raw_input = state["raw_input"]
    
    system_prompt = """You are an expert medical scribe assisting a Czech doctor. 
    Your task is to convert raw, unstructured notes into a professional "Epikríza" (Medical Report).
    
    Output Format: Markdown.
    Structure:
    # Epikríza
    ## Nynější onemocnění
    [Content]
    
    ## Osobní anamnéza
    [Content]
    
    ## Medikace
    [Content]
    
    ## Fyzikální vyšetření
    [Content]
    
    ## Závěr a Doporučení
    [Content]
    
    Rules:
    - Use professional Czech medical terminology.
    - If information is missing, omit the section or state "Neuvádí se".
    - Be concise and factual.
    """
    
    messages = [
        HumanMessage(content=f"{system_prompt}\n\nRaw Notes:\n{raw_input}")
    ]
    
    response = llm.invoke(messages)
    return {"report_content": response.content}

# Build Graph
builder = StateGraph(EpicrisisState)
builder.add_node("generate", generate_report_node)
builder.add_edge(START, "generate")
builder.add_edge("generate", END)

app = builder.compile()
