import json
import logging
from paper_search_mcp.academic_platforms.pubmed import PubMedSearcher
from backend.app.core.database import get_supabase_client
from typing import List, Dict, Any

logger = logging.getLogger("search_service")

class SearchService:
    def __init__(self):
        self.pubmed = PubMedSearcher()
        
    async def search_drugs(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Search SÚKL data via Supabase (Semantic + Keyword fallback).
        """
        supabase = get_supabase_client()
        
        # 1. semantic search (if configured)
        try:
             import os
             if os.getenv("OPENAI_API_KEY"):
                 from backend.data_processing.generators.embedding_generator import EmbeddingGenerator
                 emb_gen = EmbeddingGenerator()
                 # Generate embedding for the query
                 vecs = emb_gen.generate_embeddings([query])
                 if vecs and vecs[0]:
                     response = supabase.rpc("search_drugs", {
                         "query_embedding": vecs[0],
                         "match_threshold": 0.5,
                         "match_count": limit
                     }).execute()
                     if response.data:
                         return response.data
        except Exception as e:
             logger.warning(f"Semantic search failed (falling back to simple search): {e}")

        # 2. simple keyword search fallback
        try:
            # Note: Checking both name and active_substances
            response = supabase.table("drugs").select("*").or_(f"name.ilike.%{query}%,active_substances.ilike.%{query}%").limit(limit).execute()
            return response.data
        except Exception as e:
            logger.error(f"SÚKL simple search error: {e}")
            return []

    async def search_pubmed(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Search PubMed using paper-search-mcp logic.
        """
        try:
            # Calling synchronous library method
            papers = self.pubmed.search(query, max_results)
            
            results = []
            for p in papers:
                p_data = {
                    "title": p.title,
                    "url": p.url,
                    "abstract": p.abstract,
                    "authors": p.authors,
                    "year": p.published_date.year if p.published_date else None,
                    "pmid": p.paper_id,
                    "doi": p.doi,
                    "source": "pubmed"
                }
                results.append(p_data)
            return results
        except Exception as e:
            logger.error(f"PubMed search error: {e}")
            return []
            
    async def search_guidelines(self, query: str, limit: int = 5, match_threshold: float = 0.7) -> List[Dict[str, Any]]:
        """
        Search Guidelines via Supabase using vector similarity search.

        Args:
            query: Search query text
            limit: Maximum number of results to return (default: 5)
            match_threshold: Minimum similarity threshold (default: 0.7)

        Returns:
            List of guideline chunks with metadata for citations
        """
        import os
        supabase = get_supabase_client()

        # 1. Vector similarity search (requires OpenAI API key)
        try:
            if os.getenv("OPENAI_API_KEY"):
                from backend.data_processing.generators.embedding_generator import EmbeddingGenerator
                emb_gen = EmbeddingGenerator()
                # Generate embedding for the query
                vecs = emb_gen.generate_embeddings([query])
                if vecs and vecs[0]:
                    response = supabase.rpc("match_guidelines", {
                        "query_embedding": vecs[0],
                        "match_threshold": match_threshold,
                        "match_count": limit
                    }).execute()

                    if response.data:
                        # Format results with citation metadata
                        results = []
                        for item in response.data:
                            metadata = item.get("metadata", {})
                            result = {
                                "id": item.get("id"),
                                "title": item.get("title"),
                                "content": item.get("content"),
                                "source": metadata.get("source", item.get("title")),
                                "page": metadata.get("page"),
                                "similarity": item.get("similarity"),
                                "source_type": "guidelines"
                            }
                            results.append(result)
                        return results
        except Exception as e:
            logger.warning(f"Guidelines semantic search failed: {e}", extra={
                "step": "semantic_search",
                "error": str(e)
            })

        # 2. Keyword search fallback (if semantic search fails or no API key)
        try:
            response = supabase.table("guidelines").select(
                "id, title, content, metadata"
            ).ilike("content", f"%{query}%").limit(limit).execute()

            if response.data:
                results = []
                for item in response.data:
                    metadata = item.get("metadata", {})
                    result = {
                        "id": item.get("id"),
                        "title": item.get("title"),
                        "content": item.get("content"),
                        "source": metadata.get("source", item.get("title")),
                        "page": metadata.get("page"),
                        "similarity": None,
                        "source_type": "guidelines"
                    }
                    results.append(result)
                return results
        except Exception as e:
            logger.error(f"Guidelines keyword search error: {e}", extra={
                "step": "keyword_search",
                "error": str(e)
            })

        return []

search_service = SearchService()
