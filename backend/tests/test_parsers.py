import pytest
from unittest.mock import MagicMock, patch, mock_open
from backend.data_processing.parsers.spc_pil_parser import SpcPilParser

@pytest.fixture
def parser():
    return SpcPilParser()

def test_process_drugs(parser):
    drugs = [{"sukl_code": "0001", "name": "TEST DRUG"}]
    result = parser.process_drugs(drugs)
    
    assert "spc" in result
    assert "pil" in result
    assert len(result["spc"]) == 1
    assert result["spc"][0]["sukl_code"] == "0001"
    assert "https://www.sukl.cz/modules/medication/detail.php?code=0001" in result["spc"][0]["document_url"]

import sys
from unittest.mock import MagicMock, patch

@pytest.fixture
def mock_pdfplumber_module():
    mock_module = MagicMock()
    return mock_module

def test_extract_text_from_pdf_success(parser, mock_pdfplumber_module):
    # Setup mock PDF structure
    mock_page = MagicMock()
    mock_page.extract_text.return_value = "Extracted text page 1"
    
    mock_pdf = MagicMock()
    mock_pdf.pages = [mock_page, mock_page]
    mock_pdf.__enter__.return_value = mock_pdf 
    
    mock_pdfplumber_module.open.return_value = mock_pdf
    
    # Patch sys.modules to return our mock when 'pdfplumber' is imported
    with patch.dict(sys.modules, {'pdfplumber': mock_pdfplumber_module}):
        text = parser.extract_text_from_pdf("fake_path.pdf")
    
    # Verify
    assert "Extracted text page 1" in text
    assert text.count("Extracted text page 1") == 2
    mock_pdfplumber_module.open.assert_called_with("fake_path.pdf")

def test_extract_text_from_pdf_error(parser, mock_pdfplumber_module):
    # Setup mock to raise exception
    mock_pdfplumber_module.open.side_effect = Exception("PDF Corrupt")
    
    with patch.dict(sys.modules, {'pdfplumber': mock_pdfplumber_module}):
        text = parser.extract_text_from_pdf("bad_file.pdf")
    
    # Verify
    assert text == ""
