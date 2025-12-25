from typing import List, Dict, Any
import logging
from backend.data_processing.utils.supabase_client import SupabaseSingleton

logger = logging.getLogger(__name__)

class DocumentLoader:
    """
    Loads SPC/PIL documents into Supabase tables.
    """
    def __init__(self):
        self.supabase = SupabaseSingleton.get_client()

    def load_documents(self, spc_docs: List[Dict[str, Any]], pil_docs: List[Dict[str, Any]], batch_size: int = 100):
        
        def _upload(table: str, items: List[Dict]):
            total = len(items)
            if total == 0: return
            logger.info(f"Uploading {total} to {table}...")
            for i in range(0, total, batch_size):
                batch = items[i : i + batch_size]
                try:
                    # Workaround for missing unique constraint on sukl_code
                    # 1. Delete existing for this batch
                    codes = [item["sukl_code"] for item in batch]
                    self.supabase.table(table).delete().in_("sukl_code", codes).execute()
                    
                    # 2. Insert new
                    self.supabase.table(table).insert(batch).execute()
                    logger.info(f"Uploaded {table} batch {i//batch_size + 1}")
                except Exception as e:
                    logger.error(f"Error uploading to {table}: {e}")

        if spc_docs:
            _upload("spc_documents", spc_docs)
            
        if pil_docs:
            _upload("pil_documents", pil_docs)

            
        logger.info("Documents upload complete.")

    # Helper to fetch drugs for processing
    def fetch_all_drugs_codes(self) -> List[Dict[str, Any]]:
        # Limit to 100 for MVP testing to avoid massive fetch
        resp = self.supabase.table("drugs").select("sukl_code, name").limit(100).execute()
        return resp.data
