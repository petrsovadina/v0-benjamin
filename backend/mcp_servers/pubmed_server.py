from mcp.server.fastmcp import FastMCP
from typing import List, Dict, Any
import json
import logging
from paper_search_mcp.academic_platforms.pubmed import PubMedSearcher

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("pubmed_server")

# Initialize FastMCP server
mcp = FastMCP("Czech MedAI PubMed Server")

# Initialize Searcher
pubmed_searcher = PubMedSearcher()

@mcp.tool()
async def search_literature(query: str, max_results: int = 5) -> str:
    """
    Search PubMed for medical literature.
    Returns JSON string with list of papers including title, abstract, and citation info.
    
    Args:
        query: Search query (e.g. "diabetes treatment")
        max_results: Max number of results (default 5)
    """
    logger.info(f"Searching PubMed for: {query}")
    try:
        # Note: PubMedSearcher.search is synchronous using 'requests'
        # In a high-concurrency production env, this should be offloaded to a thread
        # papers = await to_thread(pubmed_searcher.search, query, max_results)
        
        papers = pubmed_searcher.search(query, max_results=max_results)
        
        results = []
        for p in papers:
            # Convert Paper object to dict
            # Paper class usually has to_dict(), if not we construct it
            if hasattr(p, 'to_dict'):
                p_data = p.to_dict()
            else:
                p_data = {
                    "title": p.title,
                    "url": p.url,
                    "abstract": p.abstract,
                    "authors": p.authors,
                    "year": p.published_date.year if p.published_date else None,
                    "pmid": p.paper_id,
                    "doi": p.doi
                }
            results.append(p_data)
            
        return json.dumps({
            "status": "success",
            "source": "pubmed",
            "query": query,
            "results": results
        })
        
    except Exception as e:
        logger.error(f"PubMed search failed: {e}")
        return json.dumps({
            "status": "error",
            "message": str(e)
        })

if __name__ == "__main__":
    mcp.run()
