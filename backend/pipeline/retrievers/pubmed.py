from typing import List, Dict, Any, Optional
from backend.services.logger import get_logger
from backend.services.cache import cache
from backend.data_processing.config.settings import settings
import httpx
import xml.etree.ElementTree as ET

logger = get_logger(__name__)

class PubMedRetriever:
    """
    Simple retriever for PubMed using E-utilities.
    No MCP overhead, just direct API calls.
    """
    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

    def __init__(self, email: str = None):
        self.email = email or settings.PUBMED_EMAIL or "benjamin-ai@example.com"  # NCBI requires an email

    async def search(self, query: str, max_results: int = 3) -> str:
        """
        Performs a search and returns a formatted string with results.
        This is the method the Agent will call.
        """
        # Check cache
        cache_key = f"pubmed:{query}:{max_results}"
        cached_result = cache.get(cache_key)
        if cached_result:
            logger.info("PubMed search cache hit", query=query)
            return cached_result

        logger.info(f"Searching PubMed for: {query}")
        try:
            ids = await self._get_ids(query, max_results)
            if not ids:
                logger.info("No PubMed results found", query=query)
                return "No results found on PubMed."
            
            articles = await self._fetch_details(ids)
            result = self._format_results(articles)
            
            # Save to cache (TTL 1 hour for PubMed calls)
            cache.set(cache_key, result, ttl=3600)
            
            logger.info("PubMed search returned results", count=len(articles))
            return result
        except Exception as e:
            logger.error("Error connecting to PubMed", error=e)
            return f"Error connecting to PubMed: {str(e)}"

    async def _get_ids(self, query: str, max_results: int) -> List[str]:
        params = {
            "db": "pubmed",
            "term": query,
            "retmode": "json",
            "retmax": max_results,
            "email": self.email
        }
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(f"{self.BASE_URL}/esearch.fcgi", params=params)
            resp.raise_for_status()
            data = resp.json()
            return data.get("esearchresult", {}).get("idlist", [])

    async def _fetch_details(self, ids: List[str]) -> List[Dict[str, Any]]:
        if not ids:
            return []
            
        params = {
            "db": "pubmed",
            "id": ",".join(ids),
            "retmode": "xml",
            "email": self.email
        }
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(f"{self.BASE_URL}/efetch.fcgi", params=params)
            resp.raise_for_status()
            return self._parse_xml(resp.text)

    def _parse_xml(self, xml_content: str) -> List[Dict[str, Any]]:
        root = ET.fromstring(xml_content)
        articles = []
        
        for article in root.findall(".//PubmedArticle"):
            title = article.find(".//ArticleTitle")
            title_text = title.text if title is not None else "No Title"
            
            abstract_texts = article.findall(".//AbstractText")
            abstract = " ".join([t.text for t in abstract_texts if t.text])
            
            pmid = article.find(".//PMID")
            pmid_text = pmid.text if pmid is not None else "N/A"
            
            articles.append({
                "title": title_text,
                "abstract": abstract,
                "pmid": pmid_text,
                "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid_text}/"
            })
        return articles

    def _format_results(self, articles: List[Dict[str, Any]]) -> str:
        output = "PubMed Search Results:\n\n"
        for i, art in enumerate(articles, 1):
            output += f"{i}. {art['title']}\n"
            output += f"   PMID: {art['pmid']} | URL: {art['url']}\n"
            output += f"   Abstract: {art['abstract'][:500]}...\n\n" # Truncate abstract
        return output
