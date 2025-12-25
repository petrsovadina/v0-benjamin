import pandas as pd
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class ActiveSubstanceParser:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def parse(self, limit: int = None) -> List[Dict]:
        """
        Parses the SÚKL Active Substances CSV file.
        Expected columns: KOD_LATKY, NAZEV_INN, NAZEV_EN, NAZEV, ZAV
        """
        logger.info(f"Parsing Active Substances file: {self.file_path}")
        try:
            # Encoding is usually cp1250 for Czech data, csv usually comma separated for this file?
            # From previous 'head' command: 1,ABSINTHII HERBA,... (comma separated)
            df = pd.read_csv(self.file_path, encoding="utf-8", delimiter=",")
            
            # Sanitize NaNs
            df = df.where(pd.notnull(df), None)
            
            items = []
            count = 0
            
            for _, row in df.iterrows():
                if limit and count >= limit:
                    break
                    
                item = {
                    "kod_latky": str(row.get("KOD_LATKY", "")).strip(),
                    "nazev_inn": row.get("NAZEV_INN", ""),
                    "nazev_en": row.get("NAZEV_EN", ""),
                    "nazev_cs": row.get("NAZEV", ""), # Czech Name
                }
                items.append(item)
                count += 1
            
            # Deduplicate by kod_latky just in case
            unique_items = {i['kod_latky']: i for i in items}.values()
            items = list(unique_items)
            
            logger.info(f"Parsed {len(items)} unique active substances.")
            return items
        except Exception as e:
            logger.error(f"Error parsing Active Substances file: {e}")
            raise
