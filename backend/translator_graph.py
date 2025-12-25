from typing import TypedDict, List
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import StateGraph, END
from langchain_anthropic import ChatAnthropic
import os
from dotenv import load_dotenv
from pathlib import Path

# Load env
env_path = Path(__file__).resolve().parents[1] / '.env'
load_dotenv(dotenv_path=env_path)

# Define State
class TranslatorState(TypedDict):
    source_text: str
    target_language: str
    translated_text: str

# Define LLM
llm = ChatAnthropic(
    model="claude-3-haiku-20240307",
    temperature=0,
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

# Define Node
def translate_node(state: TranslatorState):
    source_text = state["source_text"]
    target_lang = state["target_language"]
    
    system_prompt = f"""You are an expert medical translator. 
    Translate the following text into professional medical {target_lang}.
    Ensure high accuracy for medical terminology (e.g., Latin terms, drug names, dosage instructions).
    Maintain the tone and formatting of the original text.
    """
    
    messages = [
        HumanMessage(content=f"{system_prompt}\n\ntext:\n{source_text}")
    ]
    
    response = llm.invoke(messages)
    return {"translated_text": response.content}

# Build Graph
builder = StateGraph(TranslatorState)
builder.add_node("translate", translate_node)
builder.set_entry_point("translate")
builder.add_edge("translate", END)

app = builder.compile()
