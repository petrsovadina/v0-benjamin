from fastapi import APIRouter, HTTPException, Request, File, UploadFile
from pydantic import BaseModel
from backend.services.logger import get_logger
from slowapi import Limiter
from slowapi.util import get_remote_address
import os
import aiofiles
from pathlib import Path

router = APIRouter()
logger = get_logger(__name__)
limiter = Limiter(key_func=get_remote_address)

# Epicrisis
class EpicrisisRequest(BaseModel):
    items: str

@router.post("/epicrisis")
@limiter.limit("10/minute")
async def epicrisis_endpoint(body: EpicrisisRequest, request: Request):
    """
    Generates a medical report from raw notes.
    """
    logger.info("Received epicrisis request", input_length=len(body.items))
    try:
        from backend.epicrisis_graph import app as epicrisis_app
        
        inputs = {"raw_input": body.items}
        result = await epicrisis_app.ainvoke(inputs)
        
        logger.info("Epicrisis generated successfully")
        return {
            "response": result["report_content"],
            "source": "claude-3-haiku"
        }
    except Exception as e:
        logger.error("Error processing epicrisis", error=e)
        raise HTTPException(status_code=500, detail=str(e))

# Translation
class TranslateRequest(BaseModel):
    text: str
    language: str = "Czech"

@router.post("/translate")
@limiter.limit("20/minute")
async def translate_endpoint(body: TranslateRequest, request: Request):
    """
    Translates medical text.
    """
    logger.info("Received translation request", target_language=body.language)
    try:
        from backend.translator_graph import app as translator_app
        
        inputs = {"source_text": body.text, "target_language": body.language}
        result = await translator_app.ainvoke(inputs)
        
        logger.info("Translation successful")
        return {
            "response": result["translated_text"],
            "source": "claude-3-haiku"
        }
    except Exception as e:
        logger.error("Error processing translation", error=e)
        raise HTTPException(status_code=500, detail=str(e))

# Transcription
@router.post("/transcribe")
async def transcribe_endpoint(file: UploadFile = File(...)):
    """
    Transcribes audio file using Google Gemini 1.5 Pro.
    """
    logger.info("Received transcription request", filename=file.filename)
    try:
        from backend.services.transcription import TranscriptionService
        
        # Save temp file
        temp_dir = Path("backend/data/temp_uploads")
        temp_dir.mkdir(parents=True, exist_ok=True)
        temp_path = temp_dir / file.filename
        
        async with aiofiles.open(temp_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
            
        # Process
        service = TranscriptionService()
        transcript = await service.transcribe_audio(temp_path)
        
        # Cleanup
        try:
            os.remove(temp_path)
        except Exception as cleanup_err:
             logger.warning(f"Failed to cleanup temp file: {temp_path}", error=cleanup_err)
            
        logger.info("Transcription successful")
        return {
            "transcript": transcript,
            "source": "gemini-1.5-pro"
        }
    except Exception as e:
        logger.error("Error processing transcription", error=e)
        raise HTTPException(status_code=500, detail=str(e))
