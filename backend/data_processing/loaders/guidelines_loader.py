import os
import glob
import time
from typing import List, Optional
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from supabase import Client

from backend.app.core.config import settings
from backend.app.core.database import get_supabase_client
from backend.services.logger import get_logger

logger = get_logger(__name__)

# Retry configuration for embedding generation
EMBEDDING_MAX_RETRIES = 3
EMBEDDING_BASE_DELAY = 1.0  # seconds
EMBEDDING_MAX_DELAY = 10.0  # seconds

class GuidelinesLoader:
    """
    Handles loading, chunking, and embedding of Guideline PDFs.
    """
    
    def __init__(self, pdf_dir: str = "backend/data/guidelines_pdfs"):
        self.pdf_dir = pdf_dir
        self.supabase: Client = get_supabase_client()
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small", 
            api_key=settings.OPENAI_API_KEY
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", " ", ""]
        )

    def _embed_with_retry(self, texts: List[str], batch_index: int, filename: str) -> List[List[float]]:
        """
        Generate embeddings with exponential backoff retry logic.

        Args:
            texts: List of text chunks to embed
            batch_index: Current batch index for logging
            filename: Source filename for logging context

        Returns:
            List of embedding vectors

        Raises:
            Exception: If all retries are exhausted
        """
        last_exception = None

        for attempt in range(1, EMBEDDING_MAX_RETRIES + 1):
            try:
                vectors = self.embeddings.embed_documents(texts)
                if attempt > 1:
                    logger.info(
                        "Embedding generation succeeded after retry",
                        filename=filename,
                        step="embed_with_retry",
                        batch_index=batch_index,
                        attempt=attempt
                    )
                return vectors
            except Exception as e:
                last_exception = e

                if attempt < EMBEDDING_MAX_RETRIES:
                    # Calculate delay with exponential backoff
                    delay = min(EMBEDDING_BASE_DELAY * (2 ** (attempt - 1)), EMBEDDING_MAX_DELAY)

                    logger.warning(
                        "Embedding generation failed, retrying",
                        error_message=str(e),
                        filename=filename,
                        step="embed_with_retry",
                        batch_index=batch_index,
                        texts_count=len(texts),
                        attempt=attempt,
                        max_retries=EMBEDDING_MAX_RETRIES,
                        retry_delay_seconds=delay
                    )

                    time.sleep(delay)
                else:
                    logger.error(
                        "Embedding generation failed after max retries",
                        error=last_exception,
                        filename=filename,
                        step="embed_with_retry",
                        batch_index=batch_index,
                        texts_count=len(texts),
                        max_retries=EMBEDDING_MAX_RETRIES
                    )

        # Re-raise the last exception if all retries exhausted
        raise last_exception

    async def ingest_pdfs(self):
        """
        Scans the PDF directory, processes each file, and upserts chunks to Supabase.
        """
        pdf_files = glob.glob(os.path.join(self.pdf_dir, "*.pdf"))
        
        if not pdf_files:
            logger.warning(
                "No PDF files found in directory",
                pdf_dir=self.pdf_dir,
                step="ingest_pdfs"
            )
            return

        logger.info(
            "Found PDF files to process",
            pdf_count=len(pdf_files),
            pdf_dir=self.pdf_dir,
            step="ingest_pdfs"
        )

        total_chunks = 0
        
        for file_path in pdf_files:
            filename = os.path.basename(file_path)
            logger.info(
                "Processing PDF file",
                filename=filename,
                file_path=file_path,
                step="ingest_pdfs"
            )
            
            try:
                # 1. Load PDF
                loader = PyPDFLoader(file_path)
                docs = loader.load()
                
                # 2. Split into chunks
                chunks = self.text_splitter.split_documents(docs)
                logger.info(
                    "Split PDF into chunks",
                    filename=filename,
                    chunk_count=len(chunks),
                    step="split_documents"
                )
                
                # 3. Generate Embeddings & Prepare for DB
                records = []
                # We process in batches to avoid hitting API limits or huge payloads
                batch_size = 50
                
                for i in range(0, len(chunks), batch_size):
                    batch = chunks[i:i+batch_size]
                    batch_texts = [c.page_content for c in batch]
                    batch_index = i // batch_size

                    # Generate embeddings with retry logic
                    vectors = self._embed_with_retry(batch_texts, batch_index, filename)

                    for j, chunk in enumerate(batch):
                        records.append({
                            # Required fields by 008_guidelines.sql
                            "title": filename,
                            "organization": "Unknown",
                            "publication_year": "2024",  # TEXT type in schema
                            "is_czech": True,
                            # Chunk content for RAG retrieval
                            "content": chunk.page_content,
                            # Metadata JSONB for source attribution and citations
                            "metadata": {
                                "source": filename,
                                "page": chunk.metadata.get("page", 0),
                                **chunk.metadata
                            },
                            "embedding": vectors[j]
                        })
                
                # 4. Upsert to Supabase
                # Note: 'guidelines' table must exist with (id, content, metadata, embedding)
                # We let Supabase generate IDs (if table is set up that way) or we ignore conflicts?
                # Usually standard RAG doesn't have a unique key other than ID. 
                # We will just insert them. To avoid duplicates on re-run, we might want to delete old ones for this file first.
                
                # Delete existing chunks for this file to ensure idempotency
                self.supabase.table("guidelines").delete().filter("metadata->>source", "eq", filename).execute()
                
                # Insert new ones in batches
                for i in range(0, len(records), batch_size):
                    self.supabase.table("guidelines").insert(records[i:i+batch_size]).execute()
                
                logger.info(
                    "Successfully stored chunks in database",
                    filename=filename,
                    chunks_stored=len(records),
                    step="store_to_database"
                )
                total_chunks += len(records)
                
            except Exception as e:
                logger.error(
                    "Failed to process PDF file",
                    error=e,
                    filename=filename,
                    step="ingest_pdfs",
                    file_path=file_path
                )
                
        logger.info(
            "Ingestion complete",
            total_chunks_stored=total_chunks,
            pdf_count=len(pdf_files),
            step="ingest_pdfs"
        )
