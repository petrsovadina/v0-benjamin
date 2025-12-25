from fastapi import APIRouter, HTTPException, Depends
from backend.app.api.v1.deps import get_current_user
from backend.app.services.search_service import search_service
from typing import List, Dict, Any
from pydantic import BaseModel
from backend.pipeline.retrievers.vzp_retriever import VzpRetriever
from backend.services.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()

class VzpSearchRequest(BaseModel):
    query: str

@router.get("/search", response_model=List[Dict[str, Any]])
async def search_drugs(
    q: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Search for drugs by name or active substance.
    """
    if len(q) < 2:
         raise HTTPException(status_code=400, detail="Query too short")
    return await search_service.search_drugs(q)

@router.post("/vzp-search")
async def vzp_search_endpoint(
    body: VzpSearchRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Search for VZP pricing data.
    """
    try:
        retriever = VzpRetriever()
        results = await retriever.search_drugs_with_pricing(body.query)
        return {"results": results, "source": "sukl-db"}
    except Exception as e:
        logger.error("Error processing VZP search", error=e)
        return {"results": [], "error": str(e)}

@router.get("/{sukl_code}")
async def get_drug_detail(
    sukl_code: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get detailed information about a specific drug.
    """
    # We can use search_service or direct db access logic
    # Adding a specific method to search_service would be cleaner, but for now accessing via helper:
    from app.core.database import get_supabase_client
    supabase = get_supabase_client()
    
    res = supabase.table("drugs").select("*").eq("sukl_code", sukl_code).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Drug not found")
        
    return res.data[0]
