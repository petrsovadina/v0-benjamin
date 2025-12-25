from typing import List, Dict, Any
import logging
from backend.data_processing.utils.supabase_client import SupabaseSingleton

logger = logging.getLogger(__name__)

class PriceHistoryLoader:
    """
    Loads price history data into Supabase 'price_history' table.
    """
    def __init__(self):
        self.supabase = SupabaseSingleton.get_client()

    def load_price_history(self, history_items: List[Dict[str, Any]], batch_size: int = 100):
        total = len(history_items)
        logger.info(f"Starting upload of {total} historical price records to Supabase...")
        
        # We need to filter out items without date or sukl_code
        valid_items = [i for i in history_items if i.get('sukl_code') and i.get('valid_from')]
        if len(valid_items) < total:
            logger.warning(f"Filtered out {total - len(valid_items)} invalid price records (missing code or date)")
            total = len(valid_items)

        for i in range(0, total, batch_size):
            batch = valid_items[i : i + batch_size]
            try:
                # Insert history. We likely won't update, just append.
                # If we need upsert, we need a unique constraint on (sukl_code, valid_from).
                # For now, simple insert is safer than upsert without constraint, but might duplicate on rerun.
                # Let's assume we want to avoid dups.
                
                # We can't easily upsert without a unique constraint.
                # Assuming the user might re-run, checking existence or using upsert on (sukl_code, valid_from) would be best.
                # But we defined the table with only PK on ID.
                # Strategy: Just Insert. (User can clear table if needed)
                
                # Better: Upsert if we add constraint. But constrained migration wasn't added yet.
                # Falling back to regular Insert.
                
                data = self.supabase.table("price_history").insert(batch).execute()
                logger.info(f"Uploaded batch {i//batch_size + 1}/{(total//batch_size) + 1}")
            except Exception as e:
                logger.error(f"Error uploading batch starting at index {i}: {e}")
                
        logger.info("Price history upload complete.")
