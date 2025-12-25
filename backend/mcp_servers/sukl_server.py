from mcp.server.fastmcp import FastMCP
from app.core.database import get_supabase_client
from typing import List, Dict, Any

mcp = FastMCP("Czech MedAI SÚKL Server")

@mcp.tool()
async def search_drugs(query: str) -> str:
    """
    Search for drugs in the SÚKL database by name or active substance.
    """
    supabase = get_supabase_client()
    
    # Simple ILIKE search for MVP, ensuring we have 'drugs' table
    # Note: Real implementation might use vector search if embeddings are ready
    response = supabase.table("drugs").select("*").or_(f"nazev.ilike.%{query}%,ucinna_latka.ilike.%{query}%").limit(10).execute()
    
    return str(response.data)

@mcp.tool()
async def get_drug_details(sukl_code: str) -> str:
    """
    Get detailed information about a drug by its SÚKL code.
    """
    supabase = get_supabase_client()
    response = supabase.table("drugs").select("*").eq("sukl_kod", sukl_code).single().execute()
    return str(response.data)

if __name__ == "__main__":
    mcp.run()
