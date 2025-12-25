import pytest
import io
import tempfile
import os
from fastapi.testclient import TestClient
from backend.main import app
from unittest.mock import patch, MagicMock

client = TestClient(app)


def test_upload_guideline_success(tmp_path):
    """Test successful PDF file upload."""
    upload_dir = str(tmp_path / "guidelines_pdfs")
    os.makedirs(upload_dir, exist_ok=True)

    pdf_content = b"%PDF-1.4 test content"
    files = {"file": ("test_guideline.pdf", io.BytesIO(pdf_content), "application/pdf")}

    with patch("backend.app.api.v1.endpoints.admin.UPLOAD_DIR", upload_dir), \
         patch("backend.app.api.v1.endpoints.admin.run_ingestion_task"):
        response = client.post("/api/v1/admin/upload/guideline", files=files)

    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "test_guideline.pdf"
    assert data["status"] == "uploaded"
    assert "message" in data


def test_upload_guideline_invalid_file_type():
    """Test rejection of non-PDF files."""
    txt_content = b"This is a text file"
    files = {"file": ("document.txt", io.BytesIO(txt_content), "text/plain")}

    response = client.post("/api/v1/admin/upload/guideline", files=files)

    assert response.status_code == 400
    data = response.json()
    assert data["detail"]["error_code"] == "INVALID_FILE_TYPE"
    assert ".pdf" in str(data["detail"]["context"]["allowed_extensions"])


def test_upload_guideline_file_too_large():
    """Test rejection of files exceeding size limit."""
    # Create content larger than 50MB limit
    large_content = b"x" * (51 * 1024 * 1024)
    files = {"file": ("large_file.pdf", io.BytesIO(large_content), "application/pdf")}

    response = client.post("/api/v1/admin/upload/guideline", files=files)

    assert response.status_code == 400
    data = response.json()
    assert data["detail"]["error_code"] == "FILE_TOO_LARGE"
    assert data["detail"]["context"]["max_size_mb"] == 50.0


def test_upload_guideline_no_file():
    """Test error when no file is provided."""
    response = client.post("/api/v1/admin/upload/guideline")

    assert response.status_code == 422


def test_upload_guideline_docx_rejected():
    """Test rejection of Word documents."""
    docx_content = b"PK\x03\x04 fake docx"
    files = {"file": ("document.docx", io.BytesIO(docx_content), "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}

    response = client.post("/api/v1/admin/upload/guideline", files=files)

    assert response.status_code == 400
    data = response.json()
    assert data["detail"]["error_code"] == "INVALID_FILE_TYPE"
