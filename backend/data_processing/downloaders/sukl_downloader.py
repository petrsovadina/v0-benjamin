import httpx
import logging
import aiofiles
from pathlib import Path
from backend.data_processing.config.settings import settings

logger = logging.getLogger(__name__)

class SuklDownloader:
    """
    Downloads SÚKL datasets (DLP, Pricing) from OpenData.
    Migrated to backend.data_processing.
    """
    
    # URLs verified as of Dec 2025
    URLS = {
        "dlp_monthly": "https://opendata.sukl.cz/soubory/SOD20251127/DLP20251127.zip",
        "dlp_current": "https://opendata.sukl.cz/soubory/SODERECEPT/DLPAKTUALNI.zip",
        "dlp_interface": "https://opendata.sukl.cz/soubory/DLP_datove_rozhrani20250601.csv",
        "substances": "https://opendata.sukl.cz/soubory/NKOD/DLP/nkod_dlp_lecivelatky.csv",
        "prices": "https://opendata.sukl.cz/soubory/LEK13/LEK13_2025/LEK13_202511v01.csv",
        "lek13_2024": "https://opendata.sukl.cz/soubory/LEK13/LEK13_2024/LEK13_2024.zip",
        "lek13_2023": "https://opendata.sukl.cz/soubory/LEK13/LEK13_2023/LEK13_2023.zip",
        "lek13_prev_month": "https://opendata.sukl.cz/soubory/LEK13/LEK13_2025/LEK13_202510v01.csv"
    }

    def __init__(self, download_dir: str = None):
        if download_dir:
            self.download_dir = Path(download_dir)
        else:
            self.download_dir = settings.RAW_DATA_DIR
            
        self.download_dir.mkdir(parents=True, exist_ok=True)

    async def download_all(self):
        """
        Attempts to download all configured datasets.
        """
        # 1. Download DLP Monthly (Drugs)
        await self.download_with_retry("dlp_monthly", "dlp_leciva.csv")
        
        # 2. Download DLP Current (eRecept)
        await self.download_with_retry("dlp_current", "dlp_erecept.csv")

        # 2b. Download Documents Mapping & Auxiliary Files
        await self.download_with_retry("dlp_monthly", "dlp_nazvydokumentu.csv", file_pattern="nazvydokumentu")
        await self.download_with_retry("dlp_monthly", "dlp_atc.csv", file_pattern="dlp_atc.csv")
        await self.download_with_retry("dlp_monthly", "dlp_latky.csv", file_pattern="dlp_latky.csv")

        # 3. Download Data Interface
        await self.download_with_retry("dlp_interface", "dlp_datove_rozhrani.csv")
        
        # 4. Download Active Substances
        await self.download_with_retry("substances", "nkod_dlp_lecivelatky.csv")

        # 5. Download Pricing (Current)
        await self.download_with_retry("prices", "scau_leciva.csv")
        
        # 6. Download Pricing Archives (Keep as ZIP)
        await self.download_with_retry("lek13_2024", "lek13_2024.zip", extract=False)
        await self.download_with_retry("lek13_2023", "lek13_2023.zip", extract=False)
        await self.download_with_retry("lek13_prev_month", "lek13_2025_10.csv")

    async def download_with_retry(self, key: str, target_filename: str, extract: bool = True, file_pattern: str = None):
        url = self.URLS.get(key)
        if not url:
            logger.warning(f"No URL found for {key}")
            return

        logger.info(f"Downloading {key} from {url}...")
        try:
            await self.download_file(url, target_filename, extract=extract, file_pattern=file_pattern)
        except Exception as e:
            logger.error(f"Failed to download {key}: {e}. Ensure URL is correct or file is manually placed in {self.download_dir}")

    async def download_file(self, url: str, target_filename: str, extract: bool = True, file_pattern: str = None):
        import zipfile
        import io
        
        async with httpx.AsyncClient(timeout=60.0, follow_redirects=True) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            
            # Check if it is a zip file and extraction is requested
            is_zip = url.endswith(".zip") or resp.headers.get("content-type") == "application/zip"
            
            if is_zip and extract:
                logger.info(f"Extracting zip from {url}...")
                with zipfile.ZipFile(io.BytesIO(resp.content)) as z:
                    file_list = z.namelist()
                    logger.info(f"Files in ZIP: {file_list}")
                    
                    csv_files = [f for f in file_list if f.lower().endswith(".csv") or f.lower().endswith(".txt")]
                    if not csv_files:
                        logger.error("No CSV/TXT found in zip")
                        return
                    
                    source_filename = None
                    
                    # 0. Prefer explicit pattern if provided
                    if file_pattern:
                        pattern_matches = [f for f in csv_files if file_pattern.lower() in f.lower()]
                        if pattern_matches:
                            source_filename = pattern_matches[0]
                            logger.info(f"Found file matching pattern '{file_pattern}': {source_filename}")

                    if not source_filename:
                        # Heuristic to find the main DLP file
                        candidates = []
                        
                        # 1. Look for 'lecivepripravky' specifically (common in DLP)
                        priority_files = [f for f in csv_files if "lecivepripravky" in f.lower()]
                        
                        if priority_files:
                            source_filename = priority_files[0]
                        else:
                            # 2. Filtering
                            for f in csv_files:
                                lower_f = f.lower()
                                # Avoid these unless they are the only option
                                if any(x in lower_f for x in ["atc", "inn", "text", "obal", "cest", "doping", "soli", "formy", "jednotky", "zavislost", "vydej"]):
                                    continue
                                candidates.append(f)
                            
                            if candidates:
                                # Pick one, ideally the one starting with dlp and looks like main file
                                source_filename = candidates[0]
                            else:
                                # Fallback: largest CSV
                                source_filename = max(csv_files, key=lambda x: z.getinfo(x).file_size)
                        
                    logger.info(f"Selected {source_filename} for extraction as {target_filename}")
                    
                    content = z.read(source_filename)
                    target_path = self.download_dir / target_filename
                    async with aiofiles.open(target_path, 'wb') as f:
                        await f.write(content)
            else:
                # Direct file download (or save zip as is)
                target_path = self.download_dir / target_filename
                async with aiofiles.open(target_path, 'wb') as f:
                    await f.write(resp.content)
            
            logger.info(f"Downloaded {target_filename} to {self.download_dir}")
