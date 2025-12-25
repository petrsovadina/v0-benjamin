import os
import logging
import google.generativeai as genai
from pathlib import Path
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Load env variables explicitly
env_path = Path(__file__).resolve().parents[2] / '.env'
load_dotenv(dotenv_path=env_path)

class TranscriptionService:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            logger.warning("GOOGLE_API_KEY not found. Transcription will fail.")
        else:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-pro-latest') # Using 1.5 Pro as "3 Pro" proxy

    async def transcribe_audio(self, file_path: Path) -> str:
        """
        Uploads audio to Gemini and requests transcription.
        """
        if not self.api_key:
             return "Error: GOOGLE_API_KEY is missing."

        try:
            logger.info(f"Uploading file {file_path} to Gemini...")
            audio_file = genai.upload_file(path=file_path)
            
            logger.info("Generating transcript...")
            response = self.model.generate_content(
                [
                    "Transcribe this medical audio file into Czech text exactly as spoken. format: text.",
                    audio_file
                ]
            )
            
            # Cleanup remote file
            # user might want to keep it? For now, we rely on GenAI expiry (2 days) or delete explicitely
            # genai.delete_file(audio_file.name)
            
            return response.text
        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            return f"Error during transcription: {str(e)}"
