import os
import requests
import logging
from typing import Optional, Dict, Any, Union, Tuple
from pathlib import Path

logger = logging.getLogger(__name__)

class SuklApiClient:
    """
    Client for interacting with SÚKL API (testapi.sukl.cz).
    Requires a client certificate for authentication.
    """
    
    BASE_URL_TEST = "https://testapi.sukl.cz"
    BASE_URL_PROD = "https://api.sukl.cz"
    
    def __init__(self, use_test_env: bool = True):
        self.base_url = self.BASE_URL_TEST if use_test_env else self.BASE_URL_PROD
        self.cert_path = os.environ.get("SUKL_CERT_PATH")
        self.cert_pass = os.environ.get("SUKL_CERT_PASS")
        
        if not self.cert_path:
            logger.warning("SUKL_CERT_PATH not set. API calls requiring auth will fail.")
        
        # Requests expects cert as a tuple (cert_file, key_file) or a single PEM file containing both.
        # If it's a .p12, it needs conversion. For now assuming PEM or handled by user.
        self.cert = self.cert_path
        
        # Verify SSL? usually SÚKL has valid certs, but test env might need CA bundle.
        self.verify_ssl = False if use_test_env else True 

    def get_public_data(self, endpoint: str) -> Dict[str, Any]:
        """
        Generic GET wrapper.
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            # Note: Explicitly disabling verify for testapi if needed
            response = requests.get(
                url, 
                cert=self.cert, 
                verify=self.verify_ssl,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP Error calling {url}: {e.response.status_code} - {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Error calling {url}: {e}")
            raise

    def check_connection(self) -> bool:
        """
        Probes the API to verify connectivity and auth.
        """
        try:
            # Using a harmless endpoint, hopefully root or docs or specific ping
            # Often /cis/verze or similar
            self.get_public_data("/docs") 
            return True
        except Exception:
            return False
