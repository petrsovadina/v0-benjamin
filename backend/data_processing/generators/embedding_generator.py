import openai
from typing import List, Dict, Any
import logging
import os
import asyncio
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)

class EmbeddingGenerator:
    """
    Generates embeddings for drugs using OpenAI API.
    """
    def __init__(self, model: str = "text-embedding-ada-002"):
        self.model = model
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            self.client = openai.Client(api_key=api_key)
        else:
            self.client = None
            logger.warning("OPENAI_API_KEY not found. Embeddings will fail if requested.")
        
    def create_search_text(self, drug: Dict[str, Any], atc_name: str = "") -> str:
        """
        Constructs the text to be embedded.
        Includes name, strength, form, substances, ATC info.
        """
        parts = [
            f"Léčivý přípravek: {drug.get('name', '')}",
            f"Síla: {drug.get('strength', '')}" if drug.get('strength') else "",
            f"Forma: {drug.get('form', '')}" if drug.get('form') else "",
            f"Léčivé látky: {drug.get('active_substances', '')}" if drug.get('active_substances') else "",
            f"ATC: {drug.get('atc_code', '')} - {atc_name}" if atc_name else f"ATC: {drug.get('atc_code', '')}",
            f"Cesta: {drug.get('route', '')}" if drug.get('route') else ""
        ]
        return " | ".join([p for p in parts if p])

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts in batches.
        """
        if not self.client:
            logger.warning("OpenAI client not initialized. Returning None for embeddings.")
            return [None] * len(texts)

        if not texts:
            return []

        embeddings_list = []
        try:
            # OpenAI API handles batching, but we can also batch here if needed
            response = self.client.embeddings.create(
                input=texts,
                model=self.model
            )
            data = response.data
            # Ensure order is preserved
            embeddings_list = [item.embedding for item in data]
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            # Return None for failed items to keep length consistent matching input
            return [None] * len(texts)
            
        return embeddings_list

    async def generate_embeddings_async(self, texts: List[str]) -> List[List[float]]:
        """
        Async wrapper for embedding generation (using sync client in thread or async client if available).
        For simplicity, using blocking call here as we batch heavily.
        """
        return self.generate_embeddings(texts)
