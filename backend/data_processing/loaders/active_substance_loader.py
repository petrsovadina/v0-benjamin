from typing import List, Dict, Any
import logging
from backend.data_processing.utils.supabase_client import SupabaseSingleton

logger = logging.getLogger(__name__)

class ActiveSubstanceLoader:
    """
    Loads active substances into Supabase 'active_substances' table.
    """
    def __init__(self):
        self.supabase = SupabaseSingleton.get_client()

    def load_substances(self, substances: List[Dict[str, Any]], batch_size: int = 100):
        """
        Upserts active substances in batches.
        """
        total = len(substances)
        logger.info(f"Starting upload of {total} active substances to Supabase...")
        
        for i in range(0, total, batch_size):
            batch = substances[i : i + batch_size]
            try:
                # Upsert based on 'kod_latky'
                data = self.supabase.table("active_substances").upsert(
                    batch, 
                    on_conflict="kod_latky"
                ).execute()
                logger.info(f"Uploaded batch {i//batch_size + 1}/{(total//batch_size) + 1}")
            except Exception as e:
                logger.error(f"Error uploading batch starting at index {i}: {e}")
                # Don't crash the whole pipeline, but log error
                
        logger.info("Active substances upload complete.")
