from typing import List, Dict, Any, Optional
import logging
from backend.data_processing.utils.supabase_client import SupabaseSingleton

logger = logging.getLogger(__name__)

class VzpRetriever:
    """
    Retrieves drug information combined with pricing data for VZP Navigator.
    """
    def __init__(self):
        self.supabase = SupabaseSingleton.get_client()


    async def search_drugs_with_pricing(self, query: str) -> List[Dict[str, Any]]:
        """
        Searches for drugs and manually joins pricing info.
        """
        try:
            # 1. Search Drugs
            normalized_query = query.lower().strip()
            
            response = self.supabase.table("drugs") \
                .select("*") \
                .ilike("name_normalized", f"%{normalized_query}%") \
                .limit(10) \
                .execute()


            
            drugs = response.data
            if not drugs:
                return []
                
            # 2. Fetch Pricing for these drugs
            # Collect SUKL codes
            codes = [d["sukl_code"] for d in drugs]
            
            pricing_map = {}
            if codes:
                try:
                    pricing_response = self.supabase.table("drug_pricing") \
                        .select("*") \
                        .in_("sukl_code", codes) \
                        .execute()
                    
                    # Map code -> pricing object (using the first match if duplicate)
                    for p in pricing_response.data:
                        if p["sukl_code"] not in pricing_map:
                            pricing_map[p["sukl_code"]] = p
                except Exception as pe:
                    logger.warning(f"Failed to fetch pricing: {pe}")
            
            formatted_results = []
            
            for drug in drugs:
                code = drug["sukl_code"]
                pricing = pricing_map.get(code, {})
                
                # Determine coverage status
                max_price = pricing.get("max_price_manufacturer") or 0
                reimbursement = pricing.get("reimbursement_amount") or 0
                copayment = pricing.get("max_copayment") or 0
                
                coverage_status = "limited"
                if reimbursement > 0:
                    if reimbursement >= max_price and max_price > 0:
                         coverage_status = "full"
                    else:
                         coverage_status = "partial"
                
                formatted_results.append({
                    "id": code,
                    "name": drug["name"],
                    "inn": drug["active_substance"] or "N/A",
                    "atc": drug["atc_code"] or "N/A",
                    "form": f"{drug.get('strength', '')} {drug.get('pharmaceutical_form', '')}".strip(),
                    "coverage": coverage_status,
                    "pricing": {
                        "max_price": max_price,
                        "reimbursement": reimbursement,
                        "copayment": copayment
                    },
                    "conditions": ["Dle SPC"], 
                    "alternatives": ["Konzultujte s lékařem"] 
                })
                
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error querying VZP data: {str(e)}")
            return []

