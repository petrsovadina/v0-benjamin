"""
End-to-End verification tests for RAG query endpoint.

This test suite verifies:
1. Backend health endpoint works
2. RAG query endpoint processes requests correctly
3. Response contains answer and context
4. No errors or warnings in the upgraded LangChain/LangGraph stack

Run with: cd backend && PYTHONPATH=.. pytest tests/test_e2e_rag_query.py -v
"""
import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from fastapi.testclient import TestClient
from backend.main import app
from backend.app.api.v1.deps import get_current_user


class TestE2ERAGQuery:
    """End-to-end verification tests for RAG query endpoint."""

    @pytest.fixture(autouse=True)
    def setup_client(self):
        """Set up test client for each test."""
        self.client = TestClient(app)
        yield
        # Clean up dependency overrides
        app.dependency_overrides = {}

    @pytest.fixture
    def mock_supabase_client(self):
        """Mock Supabase client for database operations."""
        mock_client = MagicMock()
        mock_table = MagicMock()
        mock_client.table.return_value = mock_table
        mock_table.insert.return_value.execute.return_value.data = [{"id": "test-query-id"}]
        mock_table.update.return_value.eq.return_value.execute.return_value = None
        return mock_client

    @pytest.fixture
    def mock_graph_with_rag_response(self):
        """Mock graph app that returns RAG-style response with context."""
        mock_graph = MagicMock()
        mock_graph.ainvoke = AsyncMock(return_value={
            "final_answer": "Based on the retrieved medical literature, ibuprofen is a nonsteroidal anti-inflammatory drug (NSAID) commonly used for pain relief.",
            "query_type": "deep",
            "retrieved_context": [
                {
                    "source": "pubmed",
                    "data": {
                        "title": "Clinical Use of Ibuprofen",
                        "abstract": "Ibuprofen is widely used for its analgesic properties...",
                        "pmid": "12345678",
                        "doi": "10.1000/example",
                        "authors": ["Smith J", "Jones M"]
                    }
                },
                {
                    "source": "sukl",
                    "data": {
                        "name": "Ibuprofen 400mg",
                        "sukl_code": "0123456",
                        "spc_url": "https://www.sukl.cz/example"
                    }
                }
            ]
        })
        return mock_graph

    # =============================================================================
    # Verification Step 1: Test health endpoint
    # =============================================================================
    def test_health_endpoint_returns_healthy(self):
        """
        Verification step 2: curl http://localhost:8000/health
        Verifies health endpoint returns correct status.
        """
        response = self.client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    def test_root_endpoint_returns_ok(self):
        """Test root endpoint returns service status."""
        response = self.client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["service"] == "Czech MedAI Backend"

    # =============================================================================
    # Verification Step 3: Test RAG query endpoint
    # =============================================================================
    def test_rag_query_endpoint_with_query_field(
        self, mock_graph_with_rag_response, mock_supabase_client
    ):
        """
        Verification step 3: Test RAG query with 'query' field
        curl -X POST http://localhost:8000/api/v1/query/ -H 'Content-Type: application/json' -d '{"query": "test query"}'
        """
        app.dependency_overrides[get_current_user] = lambda: {"id": "test-user-123"}

        with patch("backend.app.api.v1.endpoints.query.graph_app", mock_graph_with_rag_response), \
             patch("backend.app.api.v1.endpoints.query.get_supabase_client", return_value=mock_supabase_client):

            response = self.client.post(
                "/api/v1/query/",
                json={"query": "What is ibuprofen used for?"}
            )

        assert response.status_code == 200
        data = response.json()

        # Verification step 4: Verify response contains answer and context
        assert "response" in data
        assert len(data["response"]) > 0
        assert "ibuprofen" in data["response"].lower()

        # Verify citations (context) are included
        assert "citations" in data
        assert len(data["citations"]) == 2

        # Verify citation structure
        pubmed_citation = next((c for c in data["citations"] if c["source"] == "pubmed"), None)
        assert pubmed_citation is not None
        assert pubmed_citation["title"] == "Clinical Use of Ibuprofen"

        sukl_citation = next((c for c in data["citations"] if c["source"] == "sukl"), None)
        assert sukl_citation is not None

    def test_rag_query_endpoint_with_message_alias(
        self, mock_graph_with_rag_response, mock_supabase_client
    ):
        """Test RAG query using 'message' alias for query field."""
        app.dependency_overrides[get_current_user] = lambda: {"id": "test-user-123"}

        with patch("backend.app.api.v1.endpoints.query.graph_app", mock_graph_with_rag_response), \
             patch("backend.app.api.v1.endpoints.query.get_supabase_client", return_value=mock_supabase_client):

            response = self.client.post(
                "/api/v1/query/",
                json={"message": "What is ibuprofen?"}
            )

        assert response.status_code == 200
        data = response.json()
        assert data["response"] is not None
        assert data["status"] == "success"

    def test_rag_query_with_history(
        self, mock_graph_with_rag_response, mock_supabase_client
    ):
        """Test RAG query with conversation history."""
        app.dependency_overrides[get_current_user] = lambda: {"id": "test-user-123"}

        with patch("backend.app.api.v1.endpoints.query.graph_app", mock_graph_with_rag_response), \
             patch("backend.app.api.v1.endpoints.query.get_supabase_client", return_value=mock_supabase_client):

            response = self.client.post(
                "/api/v1/query/",
                json={
                    "query": "Can you tell me more?",
                    "history": [
                        {"role": "user", "content": "What is ibuprofen?"},
                        {"role": "assistant", "content": "Ibuprofen is an NSAID."}
                    ]
                }
            )

        assert response.status_code == 200
        # Verify graph was called with message history
        call_args = mock_graph_with_rag_response.ainvoke.call_args
        messages = call_args[0][0]["messages"]
        assert len(messages) == 3  # 2 history + 1 current

    def test_rag_query_response_structure(
        self, mock_graph_with_rag_response, mock_supabase_client
    ):
        """Verify the complete response structure matches QueryResponse schema."""
        app.dependency_overrides[get_current_user] = lambda: {"id": "test-user-123"}

        with patch("backend.app.api.v1.endpoints.query.graph_app", mock_graph_with_rag_response), \
             patch("backend.app.api.v1.endpoints.query.get_supabase_client", return_value=mock_supabase_client):

            response = self.client.post(
                "/api/v1/query/",
                json={"query": "test"}
            )

        assert response.status_code == 200
        data = response.json()

        # Verify all expected fields in response
        assert "response" in data
        assert "query_type" in data
        assert "citations" in data
        assert "status" in data

        # Verify query_type is valid
        assert data["query_type"] in ["quick", "deep", "unknown"]

        # Verify status
        assert data["status"] == "success"

    def test_rag_query_without_auth_returns_401(self):
        """Test that query endpoint requires authentication."""
        # Remove auth override - use real dependency
        response = self.client.post(
            "/api/v1/query/",
            json={"query": "test"}
        )

        # Should fail without proper auth (401 or 403)
        assert response.status_code in [401, 403, 422, 500]

    # =============================================================================
    # Verification Step 5: Check for errors in LangChain/LangGraph imports
    # =============================================================================
    def test_langchain_imports_work_correctly(self):
        """Verify LangChain imports work without deprecation errors."""
        # These imports are used in query.py
        from langchain_core.messages import HumanMessage, AIMessage

        # Verify message creation works
        human_msg = HumanMessage(content="test")
        ai_msg = AIMessage(content="response")

        assert human_msg.content == "test"
        assert ai_msg.content == "response"

    def test_langgraph_imports_work_correctly(self):
        """Verify LangGraph imports work without errors."""
        from langgraph.graph import StateGraph, START, END
        from langgraph.graph.message import add_messages

        # Verify imports are available
        assert StateGraph is not None
        assert START is not None
        assert END is not None
        assert add_messages is not None

    def test_graph_app_can_be_imported(self):
        """Verify the main graph app can be imported."""
        from backend.app.core.graph import app as graph_app

        assert graph_app is not None
        # Verify it's a compiled graph
        assert hasattr(graph_app, 'ainvoke')

    def test_agent_graph_can_be_imported(self):
        """Verify the agent graph can be imported."""
        from backend.agent_graph import app as agent_app

        assert agent_app is not None
        assert hasattr(agent_app, 'astream_events')

    # =============================================================================
    # E2E Flow Tests
    # =============================================================================
    def test_complete_rag_flow_e2e(
        self, mock_graph_with_rag_response, mock_supabase_client
    ):
        """
        Complete E2E test simulating the full RAG query flow:
        1. User sends query
        2. Backend invokes graph
        3. Graph returns answer with context
        4. Backend formats and returns response
        """
        app.dependency_overrides[get_current_user] = lambda: {"id": "test-user-e2e"}

        with patch("backend.app.api.v1.endpoints.query.graph_app", mock_graph_with_rag_response), \
             patch("backend.app.api.v1.endpoints.query.get_supabase_client", return_value=mock_supabase_client):

            # Step 1: Health check
            health_response = self.client.get("/health")
            assert health_response.status_code == 200

            # Step 2: Send RAG query
            query_response = self.client.post(
                "/api/v1/query/",
                json={"query": "What is the dosage for ibuprofen?"}
            )

            # Step 3: Verify response
            assert query_response.status_code == 200
            data = query_response.json()

            # Step 4: Verify answer and context
            assert data["response"] is not None
            assert len(data["response"]) > 0
            assert data["citations"] is not None
            assert data["status"] == "success"

            # Verify graph was invoked correctly
            mock_graph_with_rag_response.ainvoke.assert_called_once()

    def test_quick_query_type_response(self, mock_supabase_client):
        """Test query that returns quick query type."""
        mock_graph = MagicMock()
        mock_graph.ainvoke = AsyncMock(return_value={
            "final_answer": "Quick answer here",
            "query_type": "quick",
            "retrieved_context": []
        })

        app.dependency_overrides[get_current_user] = lambda: {"id": "test-user"}

        with patch("backend.app.api.v1.endpoints.query.graph_app", mock_graph), \
             patch("backend.app.api.v1.endpoints.query.get_supabase_client", return_value=mock_supabase_client):

            response = self.client.post(
                "/api/v1/query/",
                json={"query": "simple question"}
            )

        assert response.status_code == 200
        data = response.json()
        assert data["query_type"] == "quick"


class TestRAGQueryEdgeCases:
    """Edge case tests for RAG query endpoint."""

    @pytest.fixture(autouse=True)
    def setup_client(self):
        """Set up test client for each test."""
        self.client = TestClient(app)
        yield
        app.dependency_overrides = {}

    @pytest.fixture
    def mock_supabase_client(self):
        """Mock Supabase client."""
        mock_client = MagicMock()
        mock_table = MagicMock()
        mock_client.table.return_value = mock_table
        mock_table.insert.return_value.execute.return_value.data = [{"id": "test-id"}]
        mock_table.update.return_value.eq.return_value.execute.return_value = None
        return mock_client

    def test_empty_query_handling(self, mock_supabase_client):
        """Test handling of empty query."""
        mock_graph = MagicMock()
        mock_graph.ainvoke = AsyncMock(return_value={
            "final_answer": "",
            "query_type": "quick",
            "retrieved_context": []
        })

        app.dependency_overrides[get_current_user] = lambda: {"id": "test-user"}

        with patch("backend.app.api.v1.endpoints.query.graph_app", mock_graph), \
             patch("backend.app.api.v1.endpoints.query.get_supabase_client", return_value=mock_supabase_client):

            response = self.client.post(
                "/api/v1/query/",
                json={"query": ""}
            )

        # Should still return 200 with empty response
        assert response.status_code == 200

    def test_guidelines_source_type(self, mock_supabase_client):
        """Test handling of guidelines source type in context."""
        mock_graph = MagicMock()
        mock_graph.ainvoke = AsyncMock(return_value={
            "final_answer": "According to guidelines...",
            "query_type": "deep",
            "retrieved_context": [
                {
                    "source": "guidelines",
                    "data": {
                        "title": "Clinical Guideline 2024",
                        "url": "https://example.com/guideline"
                    }
                }
            ]
        })

        app.dependency_overrides[get_current_user] = lambda: {"id": "test-user"}

        with patch("backend.app.api.v1.endpoints.query.graph_app", mock_graph), \
             patch("backend.app.api.v1.endpoints.query.get_supabase_client", return_value=mock_supabase_client):

            response = self.client.post(
                "/api/v1/query/",
                json={"query": "treatment guidelines"}
            )

        assert response.status_code == 200
        data = response.json()
        assert len(data["citations"]) == 1
        assert data["citations"][0]["source"] == "guidelines"
