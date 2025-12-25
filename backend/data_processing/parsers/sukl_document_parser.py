import csv
import logging
from pathlib import Path
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class SuklDocumentParser:
    """
    Parses 'dlp_nazvydokumentu.csv' to map SUKL codes to SPC/PIL filenames.
    """

    def parse_mapping(self, file_path: Path) -> List[Dict[str, Any]]:
        results = []
        try:
            # SÚKL CSVs in this set are usually cp1250 encoded
            encoding = 'cp1250'
            
            with open(file_path, mode='r', encoding=encoding, errors='replace') as f:
                # Detect delimiter
                content_snippet = f.read(1024)
                f.seek(0)
                delimiter = ';' if ';' in content_snippet else ','
                
                reader = csv.DictReader(f, delimiter=delimiter)
                
                for row in reader:
                    clean_row = {k.strip(): v.strip() for k, v in row.items() if k}
                    
                    sukl_code = clean_row.get("KOD_SUKL", "")
                    if not sukl_code:
                        continue
                        
                    sukl_code = sukl_code.zfill(7)
                    
                    spc = clean_row.get("SPC", "")
                    pil = clean_row.get("PIL", "")
                    
                    # Some validity check?
                    if not spc and not pil:
                        continue
                        
                    results.append({
                        "sukl_code": sukl_code,
                        "spc_file": spc if spc else None,
                        "pil_file": pil if pil else None
                    })
                    
        except Exception as e:
            logger.error(f"Failed to parse Document Mapping file {file_path}: {e}")
            raise
            
        return results
