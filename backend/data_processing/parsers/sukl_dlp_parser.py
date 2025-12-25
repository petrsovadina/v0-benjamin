import pandas as pd
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class SuklDlpParser:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def parse(self, limit: int = None) -> List[Dict]:
        """
        Parses the SÚKL DLP CSV file.
        Expected columns (Czech): Kód SÚKL, Název, Doplněk, ...
        """
        logger.info(f"Parsing DLP file: {self.file_path}")
        try:
            # Note: encoding is usually cp1250 or utf-8 for Czech data
            df = pd.read_csv(self.file_path, encoding="cp1250", delimiter=";")
            
            # Rename columns to standardized English names if needed
            # For now, keeping the manual mapping to ensure compatibility
            
            # Sanitize NaNs: replace with None (which becomes JSON null) or empty string
            df = df.where(pd.notnull(df), None)
            
            items = []
            count = 0
            
            for _, row in df.iterrows():
                if limit and count >= limit:
                    break
                    
                item = {
                    "sukl_code": str(row.get("KOD_SUKL", row.get("Kód SÚKL", ""))).zfill(7),
                    "name": row.get("NAZEV", row.get("Název", "")),
                    "strength": row.get("SILA", row.get("Síla", "")),
                    "form": row.get("FORMA", row.get("Léková forma", "")),
                    "package": row.get("BALENI", row.get("Velikost balení", "")),
                    "route": row.get("CESTA", row.get("Cesta podání", "")),
                    "atc_code": row.get("ATC_WHO", row.get("ATC", "")),
                    "active_substances": row.get("LL", row.get("Léčivá látka", "")),
                    "dispensing": row.get("VYDEJ", row.get("Výdej", "")),
                    "registration_status": row.get("REG", row.get("Stav registrace", "")),
                    "holder": row.get("DRZ", row.get("Držitel rozhodnutí", "")),
                    "is_available": row.get("DODAVKY") == "A" or row.get("Dodávky") == "A",
                }
                items.append(item)
                count += 1
            
            # Deduplicate items by sukl_code, keeping the last one (or first?)
            # Usually last update is better, but here it's likely just duplicate lines.
            unique_items = {i['sukl_code']: i for i in items}.values()
            items = list(unique_items)
            
            logger.info(f"Parsed {len(items)} unique drugs from DLP.")
            return items
        except Exception as e:
            logger.error(f"Error parsing DLP file: {e}")
            raise
