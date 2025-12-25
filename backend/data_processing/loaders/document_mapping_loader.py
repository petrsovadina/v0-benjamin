from typing import List, Dict, Any
import logging
from backend.data_processing.utils.supabase_client import SupabaseSingleton

logger = logging.getLogger(__name__)

class DocumentMappingLoader:
    """
    Updates 'drugs' table with spc_file and pil_file names.
    """
    def __init__(self):
        self.supabase = SupabaseSingleton.get_client()

    def load_mapping(self, mapping_items: List[Dict[str, Any]], batch_size: int = 100):
        total = len(mapping_items)
        logger.info(f"Starting update of document mapping for {total} items...")
        
        # 1. Fetch existing SUKL codes to avoid inserting ghosts (which fails on name NOT NULL)
        # 60k is manageable. Use pagination or large CSV export if needed, but simple select works for <100k
        # 1. Fetch existing SUKL codes and names to avoid inserting ghosts and satisfy NOT NULL name
        try:
            logger.info("Fetching existing SUKL codes and names from DB...")
            existing_drugs = {} # sukl_code -> name
            count = 0 
            page_size = 1000
            
            # Simple paging loop
            while True:
                res = self.supabase.table("drugs").select("sukl_code, name").range(count, count + page_size - 1).execute()
                batch_data = res.data
                if not batch_data:
                    break
                for r in batch_data:
                    if r.get('sukl_code'):
                        existing_drugs[r['sukl_code']] = r.get('name', 'Neznámý')
                
                count += len(batch_data)
                if len(batch_data) < page_size:
                    break
            
            logger.info(f"Loaded {len(existing_drugs)} existing drugs.")
        except Exception as e:
            logger.error(f"Failed to fetch existing drugs: {e}")
            return

        # 2. Filter mapping items and enrich with name
        valid_items = []
        for item in mapping_items:
            code = item["sukl_code"]
            if code in existing_drugs:
                # Add name to satisfy constraint
                item_with_name = item.copy()
                item_with_name['name'] = existing_drugs[code]
                valid_items.append(item_with_name)

        logger.info(f"Filtered {len(valid_items)} valid mapping items (matching existing drugs).")

        for i in range(0, len(valid_items), batch_size):
            batch = valid_items[i : i + batch_size]
            
            try:
                data = self.supabase.table("drugs").upsert(
                    batch, 
                    on_conflict="sukl_code"
                ).execute()
                
                logger.info(f"Updated document mapping for batch {i//batch_size + 1}/{(len(valid_items)//batch_size) + 1}")
            except Exception as e:
                logger.error(f"Error updating document mapping batch {i}: {e}")
                
        logger.info("Document mapping update complete.")
