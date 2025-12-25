import asyncio
import os
import sys
from pathlib import Path

# Add backend directory to path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from backend.agent_graph import app
from langchain_core.messages import HumanMessage

async def test_agent():
    print("--- 🧪 STARTING SYSTEM PROMPT VERIFICATION ---\n")

    # 1. Test: Medical Query (Should be answered with citations)
    print("📋 TEST 1: Medical Query (Diabetes)")
    medical_query = "Jaké jsou doporučené léky pro diabetes 2. typu dle českých guidelines?"
    print(f"User: {medical_query}")
    
    try:
        response = await app.ainvoke({"messages": [HumanMessage(content=medical_query)]})
        last_message = response["messages"][-1].content
        print(f"\n🤖 Agent:\n{last_message[:500]}...") # Print first 500 chars

        # Verification
        validation_errors = []
        if "[SÚKL" not in last_message and "[SPC" not in last_message and "guidelines" not in last_message.lower():
            validation_errors.append("❌ Missing citations/references")
        
        if "http" not in last_message:
            validation_errors.append("❌ Missing URLs")

        if not validation_errors:
            print("\n✅ TEST 1 PASSED: References found.")
        else:
            print(f"\n⚠️ TEST 1 WARNINGS: {', '.join(validation_errors)}")

    except Exception as e:
        print(f"\n❌ TEST 1 FAILED with Error: {e}")


    print("\n--------------------------------------------------\n")

    # 2. Test: Off-topic Query (Should be rejected)
    print("🚫 TEST 2: Off-topic Query (Cooking)")
    off_topic_query = "Jaký je nejlepší recept na svíčkovou?"
    print(f"User: {off_topic_query}")

    try:
        response = await app.ainvoke({"messages": [HumanMessage(content=off_topic_query)]})
        last_message = response["messages"][-1].content
        print(f"\n🤖 Agent:\n{last_message}")

        # Verification
        if "nemohu" in last_message.lower() or "jsem klinický" in last_message.lower() or "nesouvisí s medicínou" in last_message.lower():
             print("\n✅ TEST 2 PASSED: Query rejected.")
        else:
             print("\n⚠️ TEST 2 WARNING: Agent might not have rejected the query properly.")

    except Exception as e:
        print(f"\n❌ TEST 2 FAILED with Error: {e}")

    print("\n--- 🏁 VERIFICATION COMPLETE ---")

if __name__ == "__main__":
    asyncio.run(test_agent())
