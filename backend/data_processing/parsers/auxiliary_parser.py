import pandas as pd
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class AuxiliaryParser:
    """
    Parses auxiliary SÚKL CSV files like ATC codes and Active Substances.
    """
    
    def parse_atc(self, file_path: str) -> Dict[str, str]:
        """
        Parses dlp_atc.csv to map ATC_CODE -> ATC_NAME_CS.
        Format: ATC;NT;NAZEV;NAZEV_EN
        Returns: Dict[atc_code, atc_name]
        """
        logger.info(f"Parsing ATC file: {file_path}")
        try:
            df = pd.read_csv(file_path, encoding="cp1250", delimiter=";")
            mapping = {}
            for _, row in df.iterrows():
                code = row.get("ATC", "")
                name = row.get("NAZEV", row.get("NAZEV_EN", ""))
                if code and name:
                    mapping[str(code).strip()] = str(name).strip()
            
            logger.info(f"Parsed {len(mapping)} ATC codes.")
            return mapping
        except Exception as e:
            logger.error(f"Error parsing ATC file: {e}")
            return {}

    def parse_substances(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Parses dlp_latky.csv.
        Format: KOD_LATKY;...;NAZEV_INN;NAZEV_EN;NAZEV;...
        """
        logger.info(f"Parsing Substances file: {file_path}")
        try:
            df = pd.read_csv(file_path, encoding="cp1250", delimiter=";")
            items = []
            for _, row in df.iterrows():
                item = {
                    "kod_latky": str(row.get("KOD_LATKY", "")),
                    "nazev_inn": row.get("NAZEV_INN", ""),
                    "nazev_en": row.get("NAZEV_EN", ""),
                    "nazev_cs": row.get("NAZEV", "")
                }
                items.append(item)
            
            logger.info(f"Parsed {len(items)} active substances.")
            return items
        except Exception as e:
            logger.error(f"Error parsing Substances file: {e}")
            return []
