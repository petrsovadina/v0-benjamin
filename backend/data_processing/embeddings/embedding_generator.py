import logging
from typing import List
from backend.data_processing.config.settings import settings

logger = logging.getLogger(__name__)

class EmbeddingGenerator:
    """
    Generates embeddings for text chunks.
    """
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        if not self.api_key or "mock" in self.api_key:
            logger.warning("OPENAI_API_KEY is missing or mock. Embeddings will be mocked.")
            self.client = None
        else:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.api_key)
            except ImportError:
                logger.error("openai package not installed.")
                self.client = None

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generates embeddings for a list of texts.
        """
        if not self.client:
            # Mock embeddings (1536 dim for ada-002 compatibility)
            import random
            logger.info(f"Generating {len(texts)} mock embeddings.")
            return [[random.random() for _ in range(1536)] for _ in texts]
        
        try:
            response = self.client.embeddings.create(
                input=texts,
                model="text-embedding-ada-002"
            )
            return [data.embedding for data in response.data]
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            return []
