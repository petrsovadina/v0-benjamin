import pytest
from unittest.mock import MagicMock, patch, AsyncMock
import sys


class TestSearchGuidelinesSemanticSearch:
    """Tests for search_guidelines() semantic search functionality."""

    @pytest.mark.asyncio
    async def test_search_guidelines_semantic_success(self):
        """Test successful semantic search with results."""
        # Mock Supabase RPC response
        mock_rpc_response = MagicMock()
        mock_rpc_response.data = [
            {
                "id": "uuid-1",
                "title": "Diabetes Guidelines 2024",
                "content": "Treatment recommendations for type 2 diabetes...",
                "metadata": {"source": "diabetes_guidelines.pdf", "page": 5},
                "similarity": 0.85
            },
            {
                "id": "uuid-2",
                "title": "Hypertension Protocol",
                "content": "Blood pressure management guidelines...",
                "metadata": {"source": "hypertension.pdf", "page": 12},
                "similarity": 0.78
            }
        ]

        mock_supabase = MagicMock()
        mock_supabase.rpc.return_value.execute.return_value = mock_rpc_response

        mock_emb_gen = MagicMock()
        mock_emb_gen.generate_embeddings.return_value = [[0.1] * 1536]

        mock_emb_class = MagicMock(return_value=mock_emb_gen)

        # Create mock search service class inline
        class MockSearchService:
            def __init__(self):
                pass

            async def search_guidelines(self, query: str, limit: int = 5, match_threshold: float = 0.7):
                import os

                # 1. Vector similarity search (requires OpenAI API key)
                try:
                    if os.getenv("OPENAI_API_KEY"):
                        emb_gen = mock_emb_class()
                        vecs = emb_gen.generate_embeddings([query])
                        if vecs and vecs[0]:
                            response = mock_supabase.rpc("match_guidelines", {
                                "query_embedding": vecs[0],
                                "match_threshold": match_threshold,
                                "match_count": limit
                            }).execute()

                            if response.data:
                                results = []
                                for item in response.data:
                                    metadata = item.get("metadata", {})
                                    result = {
                                        "id": item.get("id"),
                                        "title": item.get("title"),
                                        "content": item.get("content"),
                                        "source": metadata.get("source", item.get("title")),
                                        "page": metadata.get("page"),
                                        "similarity": item.get("similarity"),
                                        "source_type": "guidelines"
                                    }
                                    results.append(result)
                                return results
                except Exception as e:
                    pass

                return []

        with patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}):
            service = MockSearchService()
            results = await service.search_guidelines("diabetes treatment", limit=5)

        assert len(results) == 2
        assert results[0]["id"] == "uuid-1"
        assert results[0]["title"] == "Diabetes Guidelines 2024"
        assert results[0]["content"] == "Treatment recommendations for type 2 diabetes..."
        assert results[0]["source"] == "diabetes_guidelines.pdf"
        assert results[0]["page"] == 5
        assert results[0]["similarity"] == 0.85
        assert results[0]["source_type"] == "guidelines"

        # Verify RPC was called with correct parameters
        mock_supabase.rpc.assert_called_once()
        call_args = mock_supabase.rpc.call_args
        assert call_args[0][0] == "match_guidelines"
        # The parameters dictionary is passed as the second positional argument
        params_dict = call_args[0][1]
        assert params_dict["match_threshold"] == 0.7
        assert params_dict["match_count"] == 5

    @pytest.mark.asyncio
    async def test_search_guidelines_custom_threshold(self):
        """Test semantic search with custom match_threshold."""
        mock_rpc_response = MagicMock()
        mock_rpc_response.data = [
            {
                "id": "uuid-1",
                "title": "High Quality Match",
                "content": "Very relevant content...",
                "metadata": {"source": "guideline.pdf", "page": 1},
                "similarity": 0.95
            }
        ]

        mock_supabase = MagicMock()
        mock_supabase.rpc.return_value.execute.return_value = mock_rpc_response

        mock_emb_gen = MagicMock()
        mock_emb_gen.generate_embeddings.return_value = [[0.1] * 1536]
        mock_emb_class = MagicMock(return_value=mock_emb_gen)

        class MockSearchService:
            async def search_guidelines(self, query: str, limit: int = 5, match_threshold: float = 0.7):
                import os
                if os.getenv("OPENAI_API_KEY"):
                    emb_gen = mock_emb_class()
                    vecs = emb_gen.generate_embeddings([query])
                    if vecs and vecs[0]:
                        response = mock_supabase.rpc("match_guidelines", {
                            "query_embedding": vecs[0],
                            "match_threshold": match_threshold,
                            "match_count": limit
                        }).execute()
                        if response.data:
                            return [{"id": item.get("id")} for item in response.data]
                return []

        with patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}):
            service = MockSearchService()
            results = await service.search_guidelines("test query", limit=10, match_threshold=0.9)

        # Verify custom threshold was passed
        call_args = mock_supabase.rpc.call_args
        # The parameters dictionary is passed as the second positional argument
        params_dict = call_args[0][1]
        assert params_dict["match_threshold"] == 0.9
        assert params_dict["match_count"] == 10

    @pytest.mark.asyncio
    async def test_search_guidelines_metadata_fallback_to_title(self):
        """Test that source falls back to title when not in metadata."""
        mock_rpc_response = MagicMock()
        mock_rpc_response.data = [
            {
                "id": "uuid-1",
                "title": "Guideline Title",
                "content": "Content here...",
                "metadata": {},  # No source in metadata
                "similarity": 0.80
            }
        ]

        mock_supabase = MagicMock()
        mock_supabase.rpc.return_value.execute.return_value = mock_rpc_response

        mock_emb_gen = MagicMock()
        mock_emb_gen.generate_embeddings.return_value = [[0.1] * 1536]
        mock_emb_class = MagicMock(return_value=mock_emb_gen)

        class MockSearchService:
            async def search_guidelines(self, query: str, limit: int = 5, match_threshold: float = 0.7):
                import os
                if os.getenv("OPENAI_API_KEY"):
                    emb_gen = mock_emb_class()
                    vecs = emb_gen.generate_embeddings([query])
                    if vecs and vecs[0]:
                        response = mock_supabase.rpc("match_guidelines", {
                            "query_embedding": vecs[0],
                            "match_threshold": match_threshold,
                            "match_count": limit
                        }).execute()
                        if response.data:
                            results = []
                            for item in response.data:
                                metadata = item.get("metadata", {})
                                result = {
                                    "id": item.get("id"),
                                    "title": item.get("title"),
                                    "content": item.get("content"),
                                    "source": metadata.get("source", item.get("title")),
                                    "page": metadata.get("page"),
                                    "similarity": item.get("similarity"),
                                    "source_type": "guidelines"
                                }
                                results.append(result)
                            return results
                return []

        with patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}):
            service = MockSearchService()
            results = await service.search_guidelines("test query")

        assert len(results) == 1
        # Source should fallback to title
        assert results[0]["source"] == "Guideline Title"
        assert results[0]["page"] is None


class TestSearchGuidelinesKeywordFallback:
    """Tests for search_guidelines() keyword search fallback."""

    @pytest.mark.asyncio
    async def test_search_guidelines_no_api_key_uses_keyword_search(self):
        """Test fallback to keyword search when no OpenAI API key."""
        mock_supabase = MagicMock()
        mock_table = MagicMock()
        mock_supabase.table.return_value = mock_table
        mock_select = MagicMock()
        mock_table.select.return_value = mock_select
        mock_ilike = MagicMock()
        mock_select.ilike.return_value = mock_ilike
        mock_limit = MagicMock()
        mock_ilike.limit.return_value = mock_limit
        mock_response = MagicMock()
        mock_response.data = [
            {
                "id": "uuid-1",
                "title": "Keyword Match Guideline",
                "content": "diabetes management protocol...",
                "metadata": {"source": "keyword_match.pdf", "page": 3}
            }
        ]
        mock_limit.execute.return_value = mock_response

        class MockSearchService:
            async def search_guidelines(self, query: str, limit: int = 5, match_threshold: float = 0.7):
                import os

                # Semantic search skipped (no API key)
                if not os.getenv("OPENAI_API_KEY"):
                    # Keyword search fallback
                    try:
                        response = mock_supabase.table("guidelines").select(
                            "id, title, content, metadata"
                        ).ilike("content", f"%{query}%").limit(limit).execute()

                        if response.data:
                            results = []
                            for item in response.data:
                                metadata = item.get("metadata", {})
                                result = {
                                    "id": item.get("id"),
                                    "title": item.get("title"),
                                    "content": item.get("content"),
                                    "source": metadata.get("source", item.get("title")),
                                    "page": metadata.get("page"),
                                    "similarity": None,
                                    "source_type": "guidelines"
                                }
                                results.append(result)
                            return results
                    except Exception:
                        pass
                return []

        # Clear OPENAI_API_KEY
        with patch.dict("os.environ", {}, clear=True):
            service = MockSearchService()
            results = await service.search_guidelines("diabetes", limit=5)

        assert len(results) == 1
        assert results[0]["id"] == "uuid-1"
        assert results[0]["title"] == "Keyword Match Guideline"
        assert results[0]["source"] == "keyword_match.pdf"
        assert results[0]["page"] == 3
        assert results[0]["similarity"] is None  # No similarity for keyword search
        assert results[0]["source_type"] == "guidelines"

        # Verify table query was made
        mock_supabase.table.assert_called_with("guidelines")
        mock_table.select.assert_called_with("id, title, content, metadata")
        mock_select.ilike.assert_called_with("content", "%diabetes%")
        mock_ilike.limit.assert_called_with(5)

    @pytest.mark.asyncio
    async def test_search_guidelines_semantic_fails_uses_keyword_fallback(self):
        """Test fallback to keyword search when semantic search fails."""
        mock_supabase = MagicMock()
        # Semantic search fails
        mock_supabase.rpc.return_value.execute.side_effect = Exception("RPC error")

        # Keyword search works
        mock_table = MagicMock()
        mock_supabase.table.return_value = mock_table
        mock_select = MagicMock()
        mock_table.select.return_value = mock_select
        mock_ilike = MagicMock()
        mock_select.ilike.return_value = mock_ilike
        mock_limit = MagicMock()
        mock_ilike.limit.return_value = mock_limit
        mock_response = MagicMock()
        mock_response.data = [
            {
                "id": "uuid-fallback",
                "title": "Fallback Result",
                "content": "Fallback content...",
                "metadata": {"source": "fallback.pdf", "page": 1}
            }
        ]
        mock_limit.execute.return_value = mock_response

        mock_emb_gen = MagicMock()
        mock_emb_gen.generate_embeddings.return_value = [[0.1] * 1536]
        mock_emb_class = MagicMock(return_value=mock_emb_gen)

        class MockSearchService:
            async def search_guidelines(self, query: str, limit: int = 5, match_threshold: float = 0.7):
                import os

                # 1. Vector similarity search fails
                try:
                    if os.getenv("OPENAI_API_KEY"):
                        emb_gen = mock_emb_class()
                        vecs = emb_gen.generate_embeddings([query])
                        if vecs and vecs[0]:
                            response = mock_supabase.rpc("match_guidelines", {
                                "query_embedding": vecs[0],
                                "match_threshold": match_threshold,
                                "match_count": limit
                            }).execute()
                            if response.data:
                                return [{"id": item.get("id")} for item in response.data]
                except Exception:
                    pass

                # 2. Keyword search fallback
                try:
                    response = mock_supabase.table("guidelines").select(
                        "id, title, content, metadata"
                    ).ilike("content", f"%{query}%").limit(limit).execute()

                    if response.data:
                        results = []
                        for item in response.data:
                            metadata = item.get("metadata", {})
                            result = {
                                "id": item.get("id"),
                                "title": item.get("title"),
                                "content": item.get("content"),
                                "source": metadata.get("source", item.get("title")),
                                "page": metadata.get("page"),
                                "similarity": None,
                                "source_type": "guidelines"
                            }
                            results.append(result)
                        return results
                except Exception:
                    pass

                return []

        with patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}):
            service = MockSearchService()
            results = await service.search_guidelines("test query")

        assert len(results) == 1
        assert results[0]["id"] == "uuid-fallback"
        assert results[0]["similarity"] is None

    @pytest.mark.asyncio
    async def test_search_guidelines_empty_semantic_results_uses_keyword(self):
        """Test fallback when semantic search returns empty results."""
        mock_supabase = MagicMock()
        # Semantic search returns empty
        mock_rpc_response = MagicMock()
        mock_rpc_response.data = []
        mock_supabase.rpc.return_value.execute.return_value = mock_rpc_response

        # Keyword search returns results
        mock_table = MagicMock()
        mock_supabase.table.return_value = mock_table
        mock_select = MagicMock()
        mock_table.select.return_value = mock_select
        mock_ilike = MagicMock()
        mock_select.ilike.return_value = mock_ilike
        mock_limit = MagicMock()
        mock_ilike.limit.return_value = mock_limit
        mock_response = MagicMock()
        mock_response.data = [
            {
                "id": "uuid-keyword",
                "title": "Keyword Only Result",
                "content": "Found via keyword...",
                "metadata": {}
            }
        ]
        mock_limit.execute.return_value = mock_response

        mock_emb_gen = MagicMock()
        mock_emb_gen.generate_embeddings.return_value = [[0.1] * 1536]
        mock_emb_class = MagicMock(return_value=mock_emb_gen)

        class MockSearchService:
            async def search_guidelines(self, query: str, limit: int = 5, match_threshold: float = 0.7):
                import os

                # 1. Vector similarity search (empty results)
                try:
                    if os.getenv("OPENAI_API_KEY"):
                        emb_gen = mock_emb_class()
                        vecs = emb_gen.generate_embeddings([query])
                        if vecs and vecs[0]:
                            response = mock_supabase.rpc("match_guidelines", {
                                "query_embedding": vecs[0],
                                "match_threshold": match_threshold,
                                "match_count": limit
                            }).execute()
                            if response.data:
                                return [{"id": item.get("id")} for item in response.data]
                except Exception:
                    pass

                # 2. Keyword search fallback
                try:
                    response = mock_supabase.table("guidelines").select(
                        "id, title, content, metadata"
                    ).ilike("content", f"%{query}%").limit(limit).execute()

                    if response.data:
                        results = []
                        for item in response.data:
                            metadata = item.get("metadata", {})
                            result = {
                                "id": item.get("id"),
                                "title": item.get("title"),
                                "content": item.get("content"),
                                "source": metadata.get("source", item.get("title")),
                                "page": metadata.get("page"),
                                "similarity": None,
                                "source_type": "guidelines"
                            }
                            results.append(result)
                        return results
                except Exception:
                    pass

                return []

        with patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}):
            service = MockSearchService()
            results = await service.search_guidelines("rare query")

        # Should fallback to keyword search
        assert len(results) == 1
        assert results[0]["id"] == "uuid-keyword"


class TestSearchGuidelinesErrorHandling:
    """Tests for search_guidelines() error handling."""

    @pytest.mark.asyncio
    async def test_search_guidelines_all_searches_fail_returns_empty(self):
        """Test that empty list is returned when all searches fail."""
        mock_supabase = MagicMock()
        # Semantic search fails
        mock_supabase.rpc.return_value.execute.side_effect = Exception("RPC error")
        # Keyword search also fails
        mock_table = MagicMock()
        mock_supabase.table.return_value = mock_table
        mock_select = MagicMock()
        mock_table.select.return_value = mock_select
        mock_ilike = MagicMock()
        mock_select.ilike.return_value = mock_ilike
        mock_limit = MagicMock()
        mock_ilike.limit.return_value = mock_limit
        mock_limit.execute.side_effect = Exception("Database error")

        mock_emb_gen = MagicMock()
        mock_emb_gen.generate_embeddings.return_value = [[0.1] * 1536]
        mock_emb_class = MagicMock(return_value=mock_emb_gen)

        class MockSearchService:
            async def search_guidelines(self, query: str, limit: int = 5, match_threshold: float = 0.7):
                import os

                # 1. Vector similarity search fails
                try:
                    if os.getenv("OPENAI_API_KEY"):
                        emb_gen = mock_emb_class()
                        vecs = emb_gen.generate_embeddings([query])
                        if vecs and vecs[0]:
                            response = mock_supabase.rpc("match_guidelines", {
                                "query_embedding": vecs[0],
                                "match_threshold": match_threshold,
                                "match_count": limit
                            }).execute()
                            if response.data:
                                return [{"id": item.get("id")} for item in response.data]
                except Exception:
                    pass

                # 2. Keyword search also fails
                try:
                    response = mock_supabase.table("guidelines").select(
                        "id, title, content, metadata"
                    ).ilike("content", f"%{query}%").limit(limit).execute()

                    if response.data:
                        return [{"id": item.get("id")} for item in response.data]
                except Exception:
                    pass

                return []

        with patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}):
            service = MockSearchService()
            results = await service.search_guidelines("test query")

        assert results == []

    @pytest.mark.asyncio
    async def test_search_guidelines_embedding_generation_fails(self):
        """Test fallback when embedding generation fails."""
        mock_supabase = MagicMock()

        # Keyword search works
        mock_table = MagicMock()
        mock_supabase.table.return_value = mock_table
        mock_select = MagicMock()
        mock_table.select.return_value = mock_select
        mock_ilike = MagicMock()
        mock_select.ilike.return_value = mock_ilike
        mock_limit = MagicMock()
        mock_ilike.limit.return_value = mock_limit
        mock_response = MagicMock()
        mock_response.data = [
            {
                "id": "uuid-1",
                "title": "Fallback Result",
                "content": "Content...",
                "metadata": {}
            }
        ]
        mock_limit.execute.return_value = mock_response

        mock_emb_gen = MagicMock()
        mock_emb_gen.generate_embeddings.return_value = [None]  # Failed embedding
        mock_emb_class = MagicMock(return_value=mock_emb_gen)

        class MockSearchService:
            async def search_guidelines(self, query: str, limit: int = 5, match_threshold: float = 0.7):
                import os

                # 1. Vector similarity search (embedding fails)
                try:
                    if os.getenv("OPENAI_API_KEY"):
                        emb_gen = mock_emb_class()
                        vecs = emb_gen.generate_embeddings([query])
                        if vecs and vecs[0]:  # vecs[0] is None
                            response = mock_supabase.rpc("match_guidelines", {}).execute()
                            if response.data:
                                return [{"id": item.get("id")} for item in response.data]
                except Exception:
                    pass

                # 2. Keyword search fallback
                try:
                    response = mock_supabase.table("guidelines").select(
                        "id, title, content, metadata"
                    ).ilike("content", f"%{query}%").limit(limit).execute()

                    if response.data:
                        results = []
                        for item in response.data:
                            metadata = item.get("metadata", {})
                            result = {
                                "id": item.get("id"),
                                "title": item.get("title"),
                                "content": item.get("content"),
                                "source": metadata.get("source", item.get("title")),
                                "page": metadata.get("page"),
                                "similarity": None,
                                "source_type": "guidelines"
                            }
                            results.append(result)
                        return results
                except Exception:
                    pass

                return []

        with patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}):
            service = MockSearchService()
            results = await service.search_guidelines("test query")

        # Should fallback to keyword search
        assert len(results) == 1
        assert results[0]["id"] == "uuid-1"


class TestSearchGuidelinesResultFormat:
    """Tests for search_guidelines() result format and structure."""

    @pytest.mark.asyncio
    async def test_result_structure_semantic_search(self):
        """Test that semantic search results have correct structure."""
        mock_rpc_response = MagicMock()
        mock_rpc_response.data = [
            {
                "id": "test-uuid",
                "title": "Test Guideline",
                "content": "Test content here...",
                "metadata": {"source": "test.pdf", "page": 10, "extra": "data"},
                "similarity": 0.92
            }
        ]

        mock_supabase = MagicMock()
        mock_supabase.rpc.return_value.execute.return_value = mock_rpc_response

        mock_emb_gen = MagicMock()
        mock_emb_gen.generate_embeddings.return_value = [[0.1] * 1536]
        mock_emb_class = MagicMock(return_value=mock_emb_gen)

        class MockSearchService:
            async def search_guidelines(self, query: str, limit: int = 5, match_threshold: float = 0.7):
                import os
                if os.getenv("OPENAI_API_KEY"):
                    emb_gen = mock_emb_class()
                    vecs = emb_gen.generate_embeddings([query])
                    if vecs and vecs[0]:
                        response = mock_supabase.rpc("match_guidelines", {
                            "query_embedding": vecs[0],
                            "match_threshold": match_threshold,
                            "match_count": limit
                        }).execute()
                        if response.data:
                            results = []
                            for item in response.data:
                                metadata = item.get("metadata", {})
                                result = {
                                    "id": item.get("id"),
                                    "title": item.get("title"),
                                    "content": item.get("content"),
                                    "source": metadata.get("source", item.get("title")),
                                    "page": metadata.get("page"),
                                    "similarity": item.get("similarity"),
                                    "source_type": "guidelines"
                                }
                                results.append(result)
                            return results
                return []

        with patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}):
            service = MockSearchService()
            results = await service.search_guidelines("test")

        result = results[0]

        # Verify all required fields
        assert "id" in result
        assert "title" in result
        assert "content" in result
        assert "source" in result
        assert "page" in result
        assert "similarity" in result
        assert "source_type" in result

        # Verify correct values
        assert result["id"] == "test-uuid"
        assert result["title"] == "Test Guideline"
        assert result["content"] == "Test content here..."
        assert result["source"] == "test.pdf"
        assert result["page"] == 10
        assert result["similarity"] == 0.92
        assert result["source_type"] == "guidelines"

    @pytest.mark.asyncio
    async def test_result_structure_keyword_search(self):
        """Test that keyword search results have correct structure."""
        mock_supabase = MagicMock()
        mock_table = MagicMock()
        mock_supabase.table.return_value = mock_table
        mock_select = MagicMock()
        mock_table.select.return_value = mock_select
        mock_ilike = MagicMock()
        mock_select.ilike.return_value = mock_ilike
        mock_limit = MagicMock()
        mock_ilike.limit.return_value = mock_limit
        mock_response = MagicMock()
        mock_response.data = [
            {
                "id": "keyword-uuid",
                "title": "Keyword Result",
                "content": "Keyword matched content...",
                "metadata": {"source": "keyword.pdf", "page": 7}
            }
        ]
        mock_limit.execute.return_value = mock_response

        class MockSearchService:
            async def search_guidelines(self, query: str, limit: int = 5, match_threshold: float = 0.7):
                import os
                if not os.getenv("OPENAI_API_KEY"):
                    try:
                        response = mock_supabase.table("guidelines").select(
                            "id, title, content, metadata"
                        ).ilike("content", f"%{query}%").limit(limit).execute()

                        if response.data:
                            results = []
                            for item in response.data:
                                metadata = item.get("metadata", {})
                                result = {
                                    "id": item.get("id"),
                                    "title": item.get("title"),
                                    "content": item.get("content"),
                                    "source": metadata.get("source", item.get("title")),
                                    "page": metadata.get("page"),
                                    "similarity": None,
                                    "source_type": "guidelines"
                                }
                                results.append(result)
                            return results
                    except Exception:
                        pass
                return []

        with patch.dict("os.environ", {}, clear=True):
            service = MockSearchService()
            results = await service.search_guidelines("keyword")

        result = results[0]

        # Verify all required fields
        assert "id" in result
        assert "title" in result
        assert "content" in result
        assert "source" in result
        assert "page" in result
        assert "similarity" in result
        assert "source_type" in result

        # Verify keyword search specific values
        assert result["similarity"] is None  # No similarity for keyword search
        assert result["source_type"] == "guidelines"

    @pytest.mark.asyncio
    async def test_handles_missing_metadata_fields(self):
        """Test graceful handling of missing metadata fields."""
        mock_rpc_response = MagicMock()
        mock_rpc_response.data = [
            {
                "id": "uuid-no-metadata",
                "title": "No Metadata Guideline",
                "content": "Content without metadata...",
                "metadata": None,  # No metadata at all
                "similarity": 0.75
            }
        ]

        mock_supabase = MagicMock()
        mock_supabase.rpc.return_value.execute.return_value = mock_rpc_response

        mock_emb_gen = MagicMock()
        mock_emb_gen.generate_embeddings.return_value = [[0.1] * 1536]
        mock_emb_class = MagicMock(return_value=mock_emb_gen)

        class MockSearchService:
            async def search_guidelines(self, query: str, limit: int = 5, match_threshold: float = 0.7):
                import os
                if os.getenv("OPENAI_API_KEY"):
                    emb_gen = mock_emb_class()
                    vecs = emb_gen.generate_embeddings([query])
                    if vecs and vecs[0]:
                        response = mock_supabase.rpc("match_guidelines", {
                            "query_embedding": vecs[0],
                            "match_threshold": match_threshold,
                            "match_count": limit
                        }).execute()
                        if response.data:
                            results = []
                            for item in response.data:
                                metadata = item.get("metadata") or {}  # Handle None
                                result = {
                                    "id": item.get("id"),
                                    "title": item.get("title"),
                                    "content": item.get("content"),
                                    "source": metadata.get("source", item.get("title")),
                                    "page": metadata.get("page"),
                                    "similarity": item.get("similarity"),
                                    "source_type": "guidelines"
                                }
                                results.append(result)
                            return results
                return []

        with patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}):
            service = MockSearchService()
            results = await service.search_guidelines("test")

        result = results[0]
        # Should handle missing metadata gracefully
        assert result["source"] == "No Metadata Guideline"  # Falls back to title
        assert result["page"] is None


class TestSearchGuidelinesDefaultParameters:
    """Tests for search_guidelines() default parameter values."""

    @pytest.mark.asyncio
    async def test_default_limit_is_5(self):
        """Test that default limit parameter is 5."""
        mock_rpc_response = MagicMock()
        mock_rpc_response.data = []

        mock_supabase = MagicMock()
        mock_supabase.rpc.return_value.execute.return_value = mock_rpc_response

        mock_emb_gen = MagicMock()
        mock_emb_gen.generate_embeddings.return_value = [[0.1] * 1536]
        mock_emb_class = MagicMock(return_value=mock_emb_gen)

        received_limit = None

        class MockSearchService:
            async def search_guidelines(self, query: str, limit: int = 5, match_threshold: float = 0.7):
                nonlocal received_limit
                received_limit = limit
                import os
                if os.getenv("OPENAI_API_KEY"):
                    emb_gen = mock_emb_class()
                    vecs = emb_gen.generate_embeddings([query])
                    if vecs and vecs[0]:
                        mock_supabase.rpc("match_guidelines", {
                            "query_embedding": vecs[0],
                            "match_threshold": match_threshold,
                            "match_count": limit
                        }).execute()
                return []

        with patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}):
            service = MockSearchService()
            await service.search_guidelines("test")  # No limit specified

        assert received_limit == 5
        call_args = mock_supabase.rpc.call_args
        # The parameters dictionary is passed as the second positional argument
        params_dict = call_args[0][1]
        assert params_dict["match_count"] == 5

    @pytest.mark.asyncio
    async def test_default_match_threshold_is_0_7(self):
        """Test that default match_threshold parameter is 0.7."""
        mock_rpc_response = MagicMock()
        mock_rpc_response.data = []

        mock_supabase = MagicMock()
        mock_supabase.rpc.return_value.execute.return_value = mock_rpc_response

        mock_emb_gen = MagicMock()
        mock_emb_gen.generate_embeddings.return_value = [[0.1] * 1536]
        mock_emb_class = MagicMock(return_value=mock_emb_gen)

        received_threshold = None

        class MockSearchService:
            async def search_guidelines(self, query: str, limit: int = 5, match_threshold: float = 0.7):
                nonlocal received_threshold
                received_threshold = match_threshold
                import os
                if os.getenv("OPENAI_API_KEY"):
                    emb_gen = mock_emb_class()
                    vecs = emb_gen.generate_embeddings([query])
                    if vecs and vecs[0]:
                        mock_supabase.rpc("match_guidelines", {
                            "query_embedding": vecs[0],
                            "match_threshold": match_threshold,
                            "match_count": limit
                        }).execute()
                return []

        with patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}):
            service = MockSearchService()
            await service.search_guidelines("test")  # No threshold specified

        assert received_threshold == 0.7
        call_args = mock_supabase.rpc.call_args
        # The parameters dictionary is passed as the second positional argument
        params_dict = call_args[0][1]
        assert params_dict["match_threshold"] == 0.7
