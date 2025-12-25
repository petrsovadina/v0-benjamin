from typing import List, Dict, Any
from backend.services.logger import get_logger
from backend.data_processing.utils.supabase_client import SupabaseSingleton
from backend.services.cache import cache

logger = get_logger(__name__)

class SuklRetriever:
    """
    Retrieves drug information from the local SÚKL database (Supabase).
    """
    def __init__(self):
        self.supabase = SupabaseSingleton.get_client()

    async def search_drugs(self, query: str) -> str:
        """
        Searches for drugs by name (using connection to Supabase).
        Returns a formatted string suitable for LLM context.
        """
        # Check cache
        cache_key = f"sukl:{query}"
        cached_result = cache.get(cache_key)
        if cached_result:
            logger.info("SÚKL search cache hit", query=query)
            return cached_result

        logger.info(f"Searching SÚKL for: {query}")
        # Simple ILIKE search for now. 
        # In production, use Full Text Search (to_tsvector) or Semantic Search (vectors).
        try:
            response = self.supabase.table("drugs") \
                .select("*") \
                .ilike("name_normalized", f"%{query.lower()}%") \
                .limit(5) \
                .execute()
            
            drugs = response.data
            if not drugs:
                logger.info("No SÚKL results found", query=query)
                return f"No drugs found matching '{query}'."
            
            # Format results
            result_text = f"Found {len(drugs)} drugs matching '{query}':\n"
            for drug in drugs:
                # Construct official SÚKL info URL
                sukl_url = f"https://www.sukl.cz/modules/medication/detail.php?code={drug['sukl_code']}&tab=info"
                
                result_text += f"- {drug['name']} (SÚKL: {drug['sukl_code']})\n"
                result_text += f"  Reference Link: {sukl_url}\n"
                result_text += f"  Active Substance: {drug.get('active_substance', 'N/A')}\n"
                result_text += f"  Strength: {drug.get('strength', 'N/A')}, Form: {drug.get('pharmaceutical_form', 'N/A')}\n"
                # Add pricing if/when available in joined table
                result_text += "\n"
            
            # Save to cache (TTL 30 mins)
            cache.set(cache_key, result_text, ttl=1800)
            
            logger.info("SÚKL search returned results", count=len(drugs))
            return result_text
            
        except Exception as e:
            logger.error("Error querying drug database", error=e)
            return f"Error querying drug database: {str(e)}"
