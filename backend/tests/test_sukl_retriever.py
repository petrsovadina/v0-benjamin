import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from backend.pipeline.retrievers.sukl_retriever import SuklRetriever

@pytest.fixture
def mock_supabase():
    with patch("backend.pipeline.retrievers.sukl_retriever.SupabaseSingleton") as MockSingleton:
        mock_client = MagicMock()
        MockSingleton.get_client.return_value = mock_client
        yield mock_client

@pytest.mark.asyncio
async def test_search_drugs_found(mock_supabase):
    # Setup mock response
    mock_response = MagicMock()
    mock_response.data = [
        {
            "name": "PARALEN",
            "sukl_code": "0123456",
            "active_substance": "paracetamol",
            "strength": "500MG",
            "pharmaceutical_form": "TBL NOB"
        }
    ]
    
    # Mock chain: table().select().ilike().limit().execute()
    mock_supabase.table.return_value \
        .select.return_value \
        .ilike.return_value \
        .limit.return_value \
        .execute.return_value = mock_response

    retriever = SuklRetriever()
    result = await retriever.search_drugs("paralen")

    assert "Found 1 drugs" in result
    assert "PARALEN" in result
    assert "SÚKL: 0123456" in result
    # Check URL generation
    assert "https://www.sukl.cz/modules/medication/detail.php?code=0123456" in result

@pytest.mark.asyncio
async def test_search_drugs_not_found(mock_supabase):
    mock_response = MagicMock()
    mock_response.data = []
    
    mock_supabase.table.return_value \
        .select.return_value \
        .ilike.return_value \
        .limit.return_value \
        .execute.return_value = mock_response

    retriever = SuklRetriever()
    result = await retriever.search_drugs("nonexistent")

    assert "No drugs found" in result
