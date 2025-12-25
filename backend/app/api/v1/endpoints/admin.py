import shutil
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, File, UploadFile, HTTPException, BackgroundTasks, Depends
from backend.services.logger import get_logger
from backend.services.sukl_api_client import SuklApiClient
from backend.data_processing.loaders.guidelines_loader import GuidelinesLoader

router = APIRouter()
logger = get_logger(__name__)


def create_error_detail(
    code: str,
    message: str,
    context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Create a structured error detail for HTTPException responses.

    Args:
        code: Error code identifier (e.g., "INVALID_FILE_TYPE", "FILE_TOO_LARGE")
        message: Human-readable error message
        context: Additional context about the error (optional)

    Returns:
        Structured error detail dictionary
    """
    error_detail = {
        "error_code": code,
        "message": message,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }

    if context:
        error_detail["context"] = context

    return error_detail

UPLOAD_DIR = "backend/data/guidelines_pdfs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Maximum file size: 50MB in bytes
MAX_FILE_SIZE = 50 * 1024 * 1024

async def run_ingestion_task():
    """
    Background task to run the ingestion pipeline.
    """
    logger.info("Starting background ingestion task...")
    loader = GuidelinesLoader(pdf_dir=UPLOAD_DIR)
    await loader.ingest_pdfs()
    logger.info("Background ingestion task finished.")

@router.post("/upload/guideline")
async def upload_guideline(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    """
    Upload a PDF file to the guidelines knowledge base.
    The file is saved and indexed in the background.
    """
    if not file.filename.endswith(".pdf"):
        file_extension = os.path.splitext(file.filename)[1] if file.filename else "unknown"
        logger.warning(
            "Invalid file type uploaded",
            filename=file.filename,
            extension=file_extension,
            endpoint="/upload/guideline"
        )
        raise HTTPException(
            status_code=400,
            detail=create_error_detail(
                code="INVALID_FILE_TYPE",
                message="Only PDF files are supported.",
                context={
                    "filename": file.filename,
                    "provided_extension": file_extension,
                    "allowed_extensions": [".pdf"]
                }
            )
        )

    # Read file content to check size
    content = await file.read()
    file_size = len(content)

    if file_size > MAX_FILE_SIZE:
        file_size_mb = file_size / (1024 * 1024)
        max_size_mb = MAX_FILE_SIZE / (1024 * 1024)
        logger.warning(
            "File size exceeds limit",
            filename=file.filename,
            file_size_bytes=file_size,
            file_size_mb=round(file_size_mb, 2),
            max_size_mb=max_size_mb,
            endpoint="/upload/guideline"
        )
        raise HTTPException(
            status_code=400,
            detail=create_error_detail(
                code="FILE_TOO_LARGE",
                message=f"File size exceeds maximum allowed size of {max_size_mb:.0f}MB.",
                context={
                    "filename": file.filename,
                    "file_size_bytes": file_size,
                    "file_size_mb": round(file_size_mb, 2),
                    "max_size_bytes": MAX_FILE_SIZE,
                    "max_size_mb": max_size_mb
                }
            )
        )

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    try:
        with open(file_path, "wb") as buffer:
            buffer.write(content)
            
        logger.info(
            "File saved successfully",
            filename=file.filename,
            file_path=file_path,
            file_size_bytes=file_size,
            endpoint="/upload/guideline"
        )
        
        # Trigger ingestion in background
        background_tasks.add_task(run_ingestion_task)
        
        return {
            "filename": file.filename, 
            "status": "uploaded", 
            "message": "File uploaded successfully. Indexing started in background."
        }
        
    except Exception as e:
        logger.error(
            "File upload failed",
            error=e,
            filename=file.filename,
            file_path=file_path,
            file_size_bytes=file_size,
            endpoint="/upload/guideline"
        )
        raise HTTPException(
            status_code=500,
            detail=create_error_detail(
                code="UPLOAD_FAILED",
                message="Failed to save the uploaded file.",
                context={
                    "filename": file.filename,
                    "file_size_bytes": file_size,
                    "error_type": type(e).__name__,
                    "error_message": str(e)
                }
            )
        )
