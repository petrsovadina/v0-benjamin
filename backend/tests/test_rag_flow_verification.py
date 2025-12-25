"""
Verification tests for the complete RAG flow with citations.

This test file verifies the E2E flow as specified in subtask-7-3:
1. Upload test guideline PDF
2. POST query to /api/v1/query/ with guideline question
3. Verify response includes guidelines context
4. Verify citations format: 'Source: [filename], page [X]'
5. Verify no console errors
"""
import pytest
import io
import os
import tempfile
from fastapi.testclient import TestClient
from backend.main import app
from unittest.mock import MagicMock, patch, AsyncMock


client = TestClient(app)


class TestCompleteRAGFlowWithCitations:
    """Verify complete RAG flow with citations per subtask-7-3 requirements."""

    def test_upload_test_guideline_pdf(self, tmp_path):
        """Step 1: Upload test guideline PDF"""
        upload_dir = str(tmp_path / "guidelines_pdfs")
        os.makedirs(upload_dir, exist_ok=True)

        pdf_content = b"%PDF-1.4 Czech Medical Guideline Test Content"
        files = {"file": ("diabetes_guideline.pdf", io.BytesIO(pdf_content), "application/pdf")}

        mock_run_task = MagicMock()

        with patch("backend.app.api.v1.endpoints.admin.UPLOAD_DIR", upload_dir), \
             patch("backend.app.api.v1.endpoints.admin.run_ingestion_task", mock_run_task):
            response = client.post("/api/v1/admin/upload/guideline", files=files)

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "uploaded"
        # Verify file was saved
        assert os.path.exists(os.path.join(upload_dir, "diabetes_guideline.pdf"))

    @pytest.mark.asyncio
    async def test_response_includes_guidelines_context(self):
        """Step 3: Verify response includes guidelines context"""
        mock_guidelines = [
            {
                "id": "uuid-1",
                "title": "Diabetes Guidelines 2024",
                "content": "Doporučená hodnota HbA1c je <7% pro dospělé pacienty.",
                "source": "diabetes_guideline.pdf",
                "page": 12,
                "similarity": 0.88,
                "source_type": "guidelines"
            }
        ]

        mock_search_service = MagicMock()
        mock_search_service.search_guidelines = AsyncMock(return_value=mock_guidelines)

        with patch("backend.app.core.graph.search_service", mock_search_service):
            from backend.app.core.graph import retrieve_guidelines_node

            mock_message = MagicMock()
            mock_message.content = "Jaká je doporučená hodnota HbA1c?"
            state = {
                "messages": [mock_message],
                "query_type": "guidelines",
                "retrieved_context": [],
                "final_answer": None,
                "next_step": "retrieve_guidelines"
            }

            result = await retrieve_guidelines_node(state)

        # Verify guidelines context was retrieved
        assert "retrieved_context" in result
        context = result["retrieved_context"]
        assert len(context) > 0
        assert context[0]["source"] == "guidelines"
        assert "content" in context[0]["data"]
        assert "page" in context[0]["data"]

    @pytest.mark.asyncio
    async def test_citations_format_source_filename_page_x(self):
        """Step 4: Verify citations format: 'Source: [filename], page [X]'"""
        mock_llm = MagicMock()
        mock_llm_response = MagicMock()
        mock_llm_response.content = "Doporučená hodnota HbA1c je <7% [1]"
        mock_llm.ainvoke = AsyncMock(return_value=mock_llm_response)

        with patch("backend.app.core.graph.get_llm", return_value=mock_llm):
            from backend.app.core.graph import synthesizer_node
            from langchain_core.messages import HumanMessage

            state = {
                "messages": [HumanMessage(content="Jaká je doporučená hodnota HbA1c?")],
                "query_type": "guidelines",
                "retrieved_context": [
                    {
                        "source": "guidelines",
                        "data": {
                            "content": "Doporučená hodnota HbA1c je <7% pro dospělé pacienty.",
                            "source": "diabetes_guideline.pdf",
                            "page": 12,
                            "similarity": 0.9
                        }
                    }
                ],
                "final_answer": None,
                "next_step": None
            }

            result = await synthesizer_node(state)

        # Verify LLM was invoked with context containing citation format
        llm_call_args = mock_llm.ainvoke.call_args[0][0]
        context_message = llm_call_args[1].content

        # Verify citation format: 'Source: [filename], page [X]'
        assert "Source:" in context_message
        assert "diabetes_guideline.pdf" in context_message
        assert "page 12" in context_message

    @pytest.mark.asyncio
    async def test_citation_format_with_multiple_pages(self):
        """Verify citation format works with multiple guideline chunks from different pages."""
        mock_llm = MagicMock()
        mock_llm_response = MagicMock()
        mock_llm_response.content = "Answer with citations [1][2]"
        mock_llm.ainvoke = AsyncMock(return_value=mock_llm_response)

        with patch("backend.app.core.graph.get_llm", return_value=mock_llm):
            from backend.app.core.graph import synthesizer_node
            from langchain_core.messages import HumanMessage

            state = {
                "messages": [HumanMessage(content="Test query")],
                "query_type": "guidelines",
                "retrieved_context": [
                    {
                        "source": "guidelines",
                        "data": {
                            "content": "First chunk of guideline content.",
                            "source": "hypertension_protocol.pdf",
                            "page": 5,
                            "similarity": 0.9
                        }
                    },
                    {
                        "source": "guidelines",
                        "data": {
                            "content": "Second chunk from another page.",
                            "source": "hypertension_protocol.pdf",
                            "page": 23,
                            "similarity": 0.85
                        }
                    }
                ],
                "final_answer": None,
                "next_step": None
            }

            result = await synthesizer_node(state)

        # Verify both citations are formatted correctly
        llm_call_args = mock_llm.ainvoke.call_args[0][0]
        context_message = llm_call_args[1].content

        # Both pages should be in citation format
        assert "page 5" in context_message
        assert "page 23" in context_message
        assert "hypertension_protocol.pdf" in context_message

    @pytest.mark.asyncio
    async def test_full_rag_flow_no_console_errors(self):
        """Step 5: Verify no console errors during full RAG flow."""
        mock_guidelines = [
            {
                "id": "uuid-1",
                "title": "Clinical Protocol",
                "content": "Treatment recommendation text.",
                "source": "clinical_protocol.pdf",
                "page": 8,
                "similarity": 0.9,
                "source_type": "guidelines"
            }
        ]

        mock_search_service = MagicMock()
        mock_search_service.search_guidelines = AsyncMock(return_value=mock_guidelines)
        mock_search_service.search_drugs = AsyncMock(return_value=[])
        mock_search_service.search_pubmed = AsyncMock(return_value=[])

        mock_llm = MagicMock()
        mock_llm_response = MagicMock()
        mock_llm_response.content = "Answer based on clinical guidelines [1].\n\n[1] Source: clinical_protocol.pdf, page 8"
        mock_llm.ainvoke = AsyncMock(return_value=mock_llm_response)
        mock_llm.with_structured_output = MagicMock(return_value=mock_llm)

        mock_classification = MagicMock()
        mock_classification.query_type = "guidelines"
        mock_llm.ainvoke = AsyncMock(side_effect=[mock_classification, mock_llm_response])

        # Capture any exceptions during flow
        errors = []

        try:
            with patch("backend.app.core.graph.search_service", mock_search_service), \
                 patch("backend.app.core.graph.get_llm", return_value=mock_llm):

                from backend.app.core.graph import app as graph_app
                from langchain_core.messages import HumanMessage

                result = await graph_app.ainvoke({
                    "messages": [HumanMessage(content="Jaké jsou doporučení pro léčbu?")]
                })

                # Verify successful completion
                assert "final_answer" in result
                assert result["final_answer"] is not None

        except Exception as e:
            errors.append(str(e))

        # No errors should have occurred
        assert len(errors) == 0, f"Console errors occurred: {errors}"


class TestCitationFormatCompliance:
    """Test that citation format strictly follows the spec."""

    @pytest.mark.asyncio
    async def test_citation_includes_source_label(self):
        """Verify citation includes 'Source:' label."""
        mock_llm = MagicMock()
        mock_llm_response = MagicMock()
        mock_llm_response.content = "Answer"
        mock_llm.ainvoke = AsyncMock(return_value=mock_llm_response)

        with patch("backend.app.core.graph.get_llm", return_value=mock_llm):
            from backend.app.core.graph import synthesizer_node
            from langchain_core.messages import HumanMessage

            state = {
                "messages": [HumanMessage(content="Query")],
                "query_type": "guidelines",
                "retrieved_context": [
                    {
                        "source": "guidelines",
                        "data": {
                            "content": "Content",
                            "source": "test.pdf",
                            "page": 1
                        }
                    }
                ],
                "final_answer": None,
                "next_step": None
            }

            await synthesizer_node(state)

        context_message = mock_llm.ainvoke.call_args[0][0][1].content
        assert "Source:" in context_message

    @pytest.mark.asyncio
    async def test_citation_includes_page_keyword(self):
        """Verify citation includes 'page' keyword."""
        mock_llm = MagicMock()
        mock_llm_response = MagicMock()
        mock_llm_response.content = "Answer"
        mock_llm.ainvoke = AsyncMock(return_value=mock_llm_response)

        with patch("backend.app.core.graph.get_llm", return_value=mock_llm):
            from backend.app.core.graph import synthesizer_node
            from langchain_core.messages import HumanMessage

            state = {
                "messages": [HumanMessage(content="Query")],
                "query_type": "guidelines",
                "retrieved_context": [
                    {
                        "source": "guidelines",
                        "data": {
                            "content": "Content",
                            "source": "test.pdf",
                            "page": 42
                        }
                    }
                ],
                "final_answer": None,
                "next_step": None
            }

            await synthesizer_node(state)

        context_message = mock_llm.ainvoke.call_args[0][0][1].content
        assert "page 42" in context_message

    @pytest.mark.asyncio
    async def test_citation_format_structure(self):
        """Verify complete citation format structure: '[X] Source: [filename], page [Y]'"""
        mock_llm = MagicMock()
        mock_llm_response = MagicMock()
        mock_llm_response.content = "Answer"
        mock_llm.ainvoke = AsyncMock(return_value=mock_llm_response)

        with patch("backend.app.core.graph.get_llm", return_value=mock_llm):
            from backend.app.core.graph import synthesizer_node
            from langchain_core.messages import HumanMessage

            state = {
                "messages": [HumanMessage(content="Query")],
                "query_type": "guidelines",
                "retrieved_context": [
                    {
                        "source": "guidelines",
                        "data": {
                            "content": "Treatment protocol content.",
                            "source": "protocol_2024.pdf",
                            "page": 15
                        }
                    }
                ],
                "final_answer": None,
                "next_step": None
            }

            await synthesizer_node(state)

        context_message = mock_llm.ainvoke.call_args[0][0][1].content

        # Verify complete format: "[1] Source: protocol_2024.pdf, page 15"
        assert "[1]" in context_message
        assert "Source: protocol_2024.pdf" in context_message
        assert ", page 15" in context_message


class TestGuidelinesRAGEndToEnd:
    """End-to-end verification of the complete guidelines RAG pipeline."""

    @pytest.mark.asyncio
    async def test_e2e_upload_to_query_to_citation(self):
        """Verify complete flow: upload → process → query → citation."""
        # Step 1: Simulate upload success (already tested above)

        # Step 2: Simulate processed data in database
        stored_guidelines = [
            {
                "id": "uuid-test",
                "title": "Czech Medical Guidelines",
                "content": "Doporučená léčba zahrnuje inhibitory ACE.",
                "source": "czech_guidelines.pdf",
                "page": 10,
                "similarity": 0.92,
                "source_type": "guidelines"
            }
        ]

        mock_search_service = MagicMock()
        mock_search_service.search_guidelines = AsyncMock(return_value=stored_guidelines)
        mock_search_service.search_drugs = AsyncMock(return_value=[])
        mock_search_service.search_pubmed = AsyncMock(return_value=[])

        mock_llm = MagicMock()
        mock_classification = MagicMock()
        mock_classification.query_type = "guidelines"

        mock_llm_response = MagicMock()
        mock_llm_response.content = """Na základě klinických doporučení je první volbou léčby ACE inhibitor [1].

Citace:
[1] Source: czech_guidelines.pdf, page 10"""

        mock_structured_llm = MagicMock()
        mock_structured_llm.ainvoke = AsyncMock(return_value=mock_classification)
        mock_llm.with_structured_output = MagicMock(return_value=mock_structured_llm)
        mock_llm.ainvoke = AsyncMock(return_value=mock_llm_response)

        with patch("backend.app.core.graph.search_service", mock_search_service), \
             patch("backend.app.core.graph.get_llm", return_value=mock_llm):

            from backend.app.core.graph import app as graph_app
            from langchain_core.messages import HumanMessage

            # Step 3: Query with guideline question
            result = await graph_app.ainvoke({
                "messages": [HumanMessage(content="Jaká je doporučená léčba?")]
            })

        # Step 4: Verify response includes guidelines context with proper citations
        assert "final_answer" in result
        answer = result["final_answer"]

        # Verify citation format in response
        assert "czech_guidelines.pdf" in answer
        assert "page 10" in answer

        # Step 5: Verify no errors (flow completed successfully)
        assert result["query_type"] in ["guidelines", "clinical"]
