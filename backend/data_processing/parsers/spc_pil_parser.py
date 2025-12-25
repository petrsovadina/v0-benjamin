import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class SpcPilParser:
    """
    Parses/Generates SPC and PIL document metadata.
    For MVP, this constructs the official SÚKL details URL.
    Real implementation would scrape this URL to find the actual PDF links.
    """
    
    BASE_URL = "https://www.sukl.cz/modules/medication/detail.php?code={}&tab=texts"

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extracts text from a PDF file using pdfplumber.
        """
        text = ""
        try:
            import pdfplumber
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
        except ImportError:
            logger.error("pdfplumber not installed.")
        except Exception as e:
            logger.error(f"Error extracting text from {pdf_path}: {e}")
        return text


    def process_drugs(self, drugs: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Takes a list of drugs (dict with 'sukl_code') and returns SPC and PIL docs.
        """
        spc_docs = []
        pil_docs = []
        
        for drug in drugs:
            code = drug.get("sukl_code")
            if not code:
                continue
                
            # Construct the main SÚKL page URL
            main_url = self.BASE_URL.format(code)
            
            # Create a placeholder SPC document record
            spc_docs.append({
                "sukl_code": code,
                "document_url": main_url, # Points to the text tab
                "title": f"SPC: {drug.get('name', code)}",
                "extracted_text": "Link to SÚKL database (PDF scraping pending)"
            })

            # Create a placeholder PIL document record
            pil_docs.append({
                "sukl_code": code,
                "document_url": main_url,
                "title": f"PIL: {drug.get('name', code)}",
                "extracted_text": "Link to SÚKL database (PDF scraping pending)"
            })
            
        return {
            "spc": spc_docs,
            "pil": pil_docs
        }
