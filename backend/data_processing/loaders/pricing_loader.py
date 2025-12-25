from typing import List, Dict, Any
import logging
from backend.data_processing.utils.supabase_client import SupabaseSingleton

logger = logging.getLogger(__name__)

class PricingLoader:
    """
    Loads pricing data into Supabase 'drug_pricing' table.
    """
    def __init__(self):
        self.supabase = SupabaseSingleton.get_client()

    def load_pricing(self, pricing_items: List[Dict[str, Any]], batch_size: int = 100):
        total = len(pricing_items)
        logger.info(f"Starting update of pricing for {total} items in 'drugs' table...")
        
        # We need to transform items to match 'drugs' columns
        # parser returns: sukl_code, max_price_manufacturer, reimbursement_amount, max_copayment, coverage_type, is_reimbursed, valid_from
        # drugs table has: sukl_code, max_price, patient_copay, is_reimbursed, reimbursement_group...
        
        for i in range(0, total, batch_size):
            batch = pricing_items[i : i + batch_size]
            
            # Prepare updates batch
            updates = []
            for item in batch:
                updates.append({
                    "sukl_code": item["sukl_code"],
                    "name": item.get("name", "Neznámý lék"), # Fallback if missing
                    "max_price": item["max_price_manufacturer"], 
                    "patient_copay": item["max_copayment"],
                    "is_reimbursed": item["is_reimbursed"],
                    "reimbursement_group": item["coverage_type"],
                })

            try:
                # Upsert is safer than update if we are not sure if drug exists, 
                # but we only want to update existing drugs.
                # However, supabase-py upsert works well.
                # Important: We must use on_conflict on sukl_code to update.
                
                data = self.supabase.table("drugs").upsert(
                    updates, 
                    on_conflict="sukl_code"
                ).execute()
                
                logger.info(f"Updated pricing for batch {i//batch_size + 1}/{(total//batch_size) + 1}")
            except Exception as e:
                logger.error(f"Error updating pricing batch {i}: {e}")
                # Log a few details for debugging
                if updates:
                    logger.error(f"Sample data: {updates[0]}")
                
        logger.info("Pricing update complete.")
