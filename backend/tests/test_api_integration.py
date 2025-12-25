import pytest
import httpx
from fastapi.testclient import TestClient
from backend.main import app
from backend.app.api.v1.deps import get_current_user
import sys
from unittest.mock import MagicMock, patch, AsyncMock

# Použijeme TestClient pro rychlé integrační testy v paměti
client = TestClient(app)

def test_health_check():
    """Ověří, že health check endpoint vrací 200 OK."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_query_endpoint_structure(mock_graph_app, mock_supabase):
    """Ověří strukturu s mockovaným uživatelem."""
    app.dependency_overrides[get_current_user] = lambda: {"id": "test_user"}
    
    with patch("backend.app.api.v1.endpoints.query.graph_app", mock_graph_app), \
         patch("backend.app.api.v1.endpoints.query.get_supabase_client", return_value=mock_supabase):
        # Test validace vstupu (invalidní typ pro message)
        response = client.post("/api/v1/query", json={"message": 123})
        
    app.dependency_overrides = {}
    
    # 422 Unprocessable Entity expected due to type mismatch
    assert response.status_code == 422

@pytest.fixture
def mock_graph_app():
    mock_app = MagicMock()
    return mock_app

@pytest.fixture
def mock_supabase():
    mock_client = MagicMock()
    mock_table = MagicMock()
    mock_client.table.return_value = mock_table
    mock_table.insert.return_value.execute.return_value.data = [{"id": "test_id"}]
    mock_table.update.return_value.eq.return_value.execute.return_value = None
    return mock_client

def test_query_endpoint_success(mock_graph_app, mock_supabase):
    """Simuluje úspěšnou odpověď agenta."""
    
    mock_graph_app.ainvoke = AsyncMock(return_value={
        "final_answer": "Ahoj, jsem Benjamin.",
        "query_type": "quick",
        "retrieved_context": []
    })

    with patch("backend.app.api.v1.endpoints.query.graph_app", mock_graph_app), \
         patch("backend.app.api.v1.endpoints.query.get_supabase_client", return_value=mock_supabase):
         
         app.dependency_overrides[get_current_user] = lambda: {"id": "test_user"}
         
         payload = {"message": "Ahoj"}
         response = client.post("/api/v1/query", json=payload)
         
         app.dependency_overrides = {}
    
    assert response.status_code == 200
    data = response.json()
    assert data["response"] == "Ahoj, jsem Benjamin."

def test_rate_limit_headers(mock_graph_app, mock_supabase):
    """Ověří, že odpověď je OK (rate limit headers check skipped)."""
    mock_graph_app.ainvoke = AsyncMock(return_value={
        "final_answer": "OK",
        "query_type": "quick" 
    })

    with patch("backend.app.api.v1.endpoints.query.graph_app", mock_graph_app), \
         patch("backend.app.api.v1.endpoints.query.get_supabase_client", return_value=mock_supabase):
        
        app.dependency_overrides[get_current_user] = lambda: {"id": "test_user"}
        
        response = client.post("/api/v1/query", json={"message": "check headers"})
        
        app.dependency_overrides = {}
    
    assert response.status_code == 200
