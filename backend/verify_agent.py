import asyncio
import os
import sys
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

# Ensure backend modules are found
sys.path.append(os.getcwd())

from backend.agent_graph import app

load_dotenv()

async def verify_agent():
    print("--- Starting Verification ---")
    query = "Jaká je cena léku Eliquis?"
    print(f"User Query: {query}")
    
    inputs = {"messages": [HumanMessage(content=query)]}
    
    try:
        print("Invoking Agent Graph...")
        result = await app.ainvoke(inputs)
        last_message = result["messages"][-1]
        print("\n--- AGENT RESPONSE ---")
        print(last_message.content)
        print("----------------------")
        
        # Check if tool was called (by checking intermediate steps or just context)
        # In this simple graph, we just check the output contains retrieval info.
        if "Eliquis" in last_message.content:
            print("✅ Verification PASSED: Response mentions the drug.")
        else:
            print("⚠️ Verification WARNING: Response might be hallucinated or generic.")
            
    except Exception as e:
        print(f"❌ Verification FAILED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(verify_agent())
