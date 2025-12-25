import asyncio
import os
from dotenv import load_dotenv
from backend.pipeline.retrievers.sukl_retriever import SuklRetriever

# Load env from root
load_dotenv(".env") 

async def test():
    print("Testing SuklRetriever...")
    try:
        retriever = SuklRetriever()
        
        # Debug: List all drugs content
        print("DEBUG: Listing all drugs in DB...")
        debug_response = retriever.supabase.table("drugs").select("*").limit(10).execute()
        print(f"DEBUG: Found {len(debug_response.data)} items.")
        for d in debug_response.data:
            print(f"- {d.get('name')} (Norm: {d.get('name_normalized')})")
            
        query = "Eliquis"
        print(f"Searching for: {query}")
        result = await retriever.search_drugs(query)
        print("--- Result ---")
        print(result)
        print("--------------")
        
        if "Found" in result:
            print("SUCCESS: Retrieved drug info.")
        else:
            print("FAILURE: No info found.")
            
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    asyncio.run(test())
