import asyncio
import sys
import os

# Ensure backend modules are found
sys.path.append(os.getcwd())

from backend.pipeline.retrievers.sukl_retriever import SuklRetriever

async def verify_rag():
    print("--- Verifying RAG (SuklRetriever) ---")
    retriever = SuklRetriever()
    query = "Eliquis"
    print(f"Searching for: '{query}'")
    
    try:
        result = await retriever.search_drugs(query)
        print("\n--- Search Result ---")
        print(result)
        print("---------------------")
        
        if "Eliquis" in result and "SÚKL" in result:
             print("✅ RAG Verification PASSED: Found drug in DB.")
        else:
             print("❌ RAG Verification FAILED: Results empty or malformed.")
             
    except Exception as e:
        print(f"❌ RAG Verification EXCEPTION: {e}")

if __name__ == "__main__":
    asyncio.run(verify_rag())
