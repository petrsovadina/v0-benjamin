from typing import List, Dict, Any
import logging
from backend.data_processing.utils.supabase_client import SupabaseSingleton

logger = logging.getLogger(__name__)

class DrugLoader:
    """
    Loads drug data into Supabase 'drugs' table.
    """
    def __init__(self):
        self.supabase = SupabaseSingleton.get_client()

    def load_drugs(self, drugs: List[Dict[str, Any]], batch_size: int = 100):
        """
        Upserts drugs in batches.
        """
        total = len(drugs)
        logger.info(f"Starting upload of {total} drugs to Supabase...")
        
        for i in range(0, total, batch_size):
            batch = drugs[i : i + batch_size]
            try:
                # Upsert based on 'sukl_code'. 
                data = self.supabase.table("drugs").upsert(
                    batch, 
                    on_conflict="sukl_code"
                ).execute()
                logger.info(f"Uploaded batch {i//batch_size + 1}/{(total//batch_size) + 1}")
            except Exception as e:
                logger.error(f"Error uploading batch starting at index {i}: {e}")
                import traceback
                traceback.print_exc()
                
        logger.info("Upload complete.")
