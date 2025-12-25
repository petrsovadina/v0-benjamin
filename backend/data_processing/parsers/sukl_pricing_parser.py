import csv
import logging
from pathlib import Path
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class SuklPricingParser:
    """
    Parses SÚKL Pricing CSV files (SCAU - Seznam cen a úhrad).
    """

    def parse_pricing(self, file_path: Path) -> List[Dict[str, Any]]:
        results = []
        try:
            import zipfile
            
            # Check if zip
            if file_path.suffix.lower() == '.zip':
                logger.info(f"Detected ZIP archive: {file_path}")
                with zipfile.ZipFile(file_path, 'r') as z:
                    for filename in z.namelist():
                        if filename.lower().endswith('.csv') or filename.lower().endswith('.txt'):
                            logger.info(f"Processing archived file: {filename}")
                            with z.open(filename) as f:
                                # ZipFile opens in bytes mode, need to decode
                                # LEK-13 is typically cp1250
                                content = f.read().decode('cp1250', errors='replace').splitlines()
                                results.extend(self._parse_csv_content(content, filename))
            else:
                # Normal CSV file
                with open(file_path, mode='r', encoding='cp1250', errors='replace') as f:
                    content = f.readlines()
                    results.extend(self._parse_csv_content(content, file_path.name))
                        
        except Exception as e:
            logger.error(f"Failed to parse Pricing file {file_path}: {e}")
            raise
            
        return results

    def _parse_csv_content(self, lines: List[str], source_name: str) -> List[Dict[str, Any]]:
        results = []
        try:
             # Basic heuristic for delimiter
            if not lines:
                return []
                
            first_line = lines[0]
            delimiter = ';' if ';' in first_line else ','
            
            reader = csv.DictReader(lines, delimiter=delimiter)
            
            for row in reader:
                clean_row = {k.strip(): v.strip() for k, v in row.items() if k}
                
                try:
                    # Helper to find key case-insensitive and safe
                    def get_val(candidates: List[str], default=""):
                        for c in candidates:
                            for k in clean_row.keys():
                                if c.lower() in k.lower():
                                    return clean_row[k]
                        return default

                    # LEK-13 column mapping
                    # Try explicit then fuzzy
                    sukl_code = clean_row.get("Kód SÚKL") or get_val(["kód súkl", "kod sukl", "kód"], "")
                    
                    if not sukl_code:
                        continue
                    
                    # Normalize SUKL code to 7 digits
                    sukl_code = sukl_code.zfill(7)
                    
                    name = get_val(["název přípravku", "nazev pripravku", "název", "nazev"], "")

                    # Parse numeric values
                    def parse_num(val):
                        if not val: return None
                        try:
                            return float(val.replace(',', '.').replace(' ', ''))
                        except ValueError:
                            return 0.0
                    
                    price = parse_num(clean_row.get("Nákupní cena bez DPH") or get_val(["nákupní cena", "nakupni cena"], "0"))
                    copay = parse_num(get_val(["konečná", "konecna", "doplatek"], "0")) 
                    dispensed_count = int(parse_num(get_val(["počet balení", "pocet baleni"], "0")) or 0)
                    
                    is_reimbursed = get_val(["hrazeno"], "Ne").lower() == "ano"
                    
                    # Parse date from 'Období' (e.g. 2024.01 or 202401)
                    raw_date = clean_row.get("Období") or get_val(["období", "obdobi"], None)
                    valid_from = None
                    if raw_date:
                        try:
                            # Usually YYYY.MM or YYYYMM
                            clean_date = raw_date.replace('.', '')
                            if len(clean_date) == 6:
                                valid_from = f"{clean_date[:4]}-{clean_date[4:]}-01"
                        except:
                            pass

                    item = {
                        "sukl_code": sukl_code,
                        "name": name,
                        "max_price_manufacturer": price,
                        "reimbursement_amount": 0.0, 
                        "max_copayment": copay, 
                        "dispensed_count": dispensed_count,
                        "coverage_type": "Hrazeno" if is_reimbursed else "Nehrazeno",
                        "is_reimbursed": is_reimbursed,
                        "valid_from": valid_from,
                        "source_file": source_name
                    }
                    results.append(item)
                except Exception as row_e:
                    continue
        except Exception as e:
             logger.error(f"Error parsing content from {source_name}: {e}")
             
        return results
