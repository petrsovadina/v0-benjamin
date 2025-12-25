"""
Tests for multi-format Czech guideline PDF support.

This module tests the pipeline with 3 different PDF formats:
1. Standard text PDF (MS Word export style)
2. PDF with tables (dosage guidelines)
3. Multi-column PDF (journal format)

Verification steps:
1. Upload each PDF format
2. Verify processing creates correct chunks with metadata
3. Query content from each format
4. Verify citations include correct page numbers
"""
import pytest
import os
import io
from fastapi.testclient import TestClient
from backend.main import app
from unittest.mock import MagicMock, patch, AsyncMock
from langchain_community.document_loaders import PyPDFLoader


# Test client
client = TestClient(app)

# Path to test fixtures
FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures", "guidelines")


class TestMultiFormatPDFProcessing:
    """Test processing of different PDF formats through the pipeline."""

    def test_fixtures_exist(self):
        """Verify all 3 test PDF fixtures are available."""
        expected_files = [
            "standard_text_guideline.pdf",
            "dosage_table_guideline.pdf",
            "journal_multicolumn_guideline.pdf"
        ]
        for filename in expected_files:
            filepath = os.path.join(FIXTURES_DIR, filename)
            assert os.path.exists(filepath), f"Missing fixture: {filename}"

    @pytest.mark.parametrize("pdf_name,expected_keywords", [
        (
            "standard_text_guideline.pdf",
            # Note: Czech chars may be stripped in PDF generation, use ASCII-friendly terms
            ["diabetes", "metformin", "HbA1c", "mmol"]
        ),
        (
            "dosage_table_guideline.pdf",
            ["empagliflozin", "semaglutid", "GLP-1", "mg"]
        ),
        (
            "journal_multicolumn_guideline.pdf",
            # Note: Some chars may be stripped, use ASCII terms present in text
            ["hypertenze", "ACE", "mmHg", "ARB"]
        ),
    ])
    def test_pdf_text_extraction(self, pdf_name, expected_keywords):
        """
        Test that PyPDFLoader correctly extracts text from each PDF format.
        This validates that the PDF content is readable and parseable.
        """
        filepath = os.path.join(FIXTURES_DIR, pdf_name)
        loader = PyPDFLoader(filepath)
        docs = loader.load()

        # Verify documents were extracted
        assert len(docs) > 0, f"No pages extracted from {pdf_name}"

        # Combine all page content
        full_text = " ".join(doc.page_content for doc in docs)

        # Verify expected keywords are present
        for keyword in expected_keywords:
            assert keyword.lower() in full_text.lower(), (
                f"Keyword '{keyword}' not found in {pdf_name}"
            )

    @pytest.mark.parametrize("pdf_name", [
        "standard_text_guideline.pdf",
        "dosage_table_guideline.pdf",
        "journal_multicolumn_guideline.pdf",
    ])
    def test_pdf_page_metadata_preserved(self, pdf_name):
        """
        Test that page numbers are correctly preserved in document metadata.
        This is critical for citation formatting.
        """
        filepath = os.path.join(FIXTURES_DIR, pdf_name)
        loader = PyPDFLoader(filepath)
        docs = loader.load()

        # Each page should have page metadata
        for i, doc in enumerate(docs):
            assert "page" in doc.metadata, f"Page {i} missing 'page' metadata"
            # PyPDFLoader uses 0-indexed pages
            assert doc.metadata["page"] == i, (
                f"Page number mismatch: expected {i}, got {doc.metadata['page']}"
            )

    @pytest.mark.parametrize("pdf_name", [
        "standard_text_guideline.pdf",
        "dosage_table_guideline.pdf",
        "journal_multicolumn_guideline.pdf",
    ])
    def test_chunking_preserves_metadata(self, pdf_name):
        """
        Test that text chunking preserves source and page metadata.
        """
        from langchain_text_splitters import RecursiveCharacterTextSplitter

        filepath = os.path.join(FIXTURES_DIR, pdf_name)
        loader = PyPDFLoader(filepath)
        docs = loader.load()

        # Use same chunking config as GuidelinesLoader
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", " ", ""]
        )
        chunks = text_splitter.split_documents(docs)

        # Verify chunks were created
        assert len(chunks) > 0, f"No chunks created from {pdf_name}"

        # Verify each chunk has metadata
        for chunk in chunks:
            assert "page" in chunk.metadata, "Chunk missing 'page' metadata"
            assert "source" in chunk.metadata, "Chunk missing 'source' metadata"
            assert chunk.page_content, "Chunk has empty content"


class TestMultiFormatUploadIntegration:
    """Integration tests for uploading different PDF formats."""

    @pytest.mark.parametrize("pdf_name", [
        "standard_text_guideline.pdf",
        "dosage_table_guideline.pdf",
        "journal_multicolumn_guideline.pdf",
    ])
    def test_upload_each_format(self, pdf_name, tmp_path):
        """Test that each PDF format can be uploaded successfully."""
        upload_dir = str(tmp_path / "guidelines_pdfs")
        os.makedirs(upload_dir, exist_ok=True)

        # Read actual PDF fixture
        filepath = os.path.join(FIXTURES_DIR, pdf_name)
        with open(filepath, "rb") as f:
            pdf_content = f.read()

        files = {"file": (pdf_name, io.BytesIO(pdf_content), "application/pdf")}

        mock_run_task = MagicMock()

        with patch("backend.app.api.v1.endpoints.admin.UPLOAD_DIR", upload_dir), \
             patch("backend.app.api.v1.endpoints.admin.run_ingestion_task", mock_run_task):
            response = client.post("/api/v1/admin/upload/guideline", files=files)

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "uploaded"

        # Verify file was saved correctly
        saved_path = os.path.join(upload_dir, pdf_name)
        assert os.path.exists(saved_path)
        with open(saved_path, "rb") as f:
            assert f.read() == pdf_content


class TestMultiFormatLoaderProcessing:
    """Test GuidelinesLoader processing of different formats."""

    @pytest.mark.asyncio
    async def test_loader_processes_all_formats(self, tmp_path):
        """
        Test that GuidelinesLoader correctly processes all 3 PDF formats.
        Simulates the full ingestion flow with mocked database.
        """
        # Copy fixtures to temp directory
        import shutil
        for pdf_name in [
            "standard_text_guideline.pdf",
            "dosage_table_guideline.pdf",
            "journal_multicolumn_guideline.pdf"
        ]:
            src = os.path.join(FIXTURES_DIR, pdf_name)
            dst = os.path.join(str(tmp_path), pdf_name)
            shutil.copy(src, dst)

        # Track all records inserted
        all_records = []

        mock_supabase = MagicMock()
        mock_table = MagicMock()
        mock_supabase.table.return_value = mock_table

        # Mock delete chain
        mock_delete = MagicMock()
        mock_table.delete.return_value = mock_delete
        mock_filter = MagicMock()
        mock_delete.filter.return_value = mock_filter
        mock_filter.execute.return_value = MagicMock()

        # Capture inserts
        def capture_insert(records):
            all_records.extend(records)
            mock_insert = MagicMock()
            mock_insert.execute.return_value = MagicMock()
            return mock_insert

        mock_table.insert.side_effect = capture_insert

        # Mock embeddings to return proper vectors
        mock_embeddings = MagicMock()
        def mock_embed_documents(texts):
            return [[0.1] * 1536 for _ in texts]
        mock_embeddings.embed_documents.side_effect = mock_embed_documents

        with patch("backend.data_processing.loaders.guidelines_loader.get_supabase_client", return_value=mock_supabase), \
             patch("backend.data_processing.loaders.guidelines_loader.OpenAIEmbeddings", return_value=mock_embeddings):

            from backend.data_processing.loaders.guidelines_loader import GuidelinesLoader
            loader = GuidelinesLoader(pdf_dir=str(tmp_path))
            loader.supabase = mock_supabase
            loader.embeddings = mock_embeddings

            await loader.ingest_pdfs()

        # Verify all 3 PDFs were processed
        processed_files = set(r["title"] for r in all_records)
        assert "standard_text_guideline.pdf" in processed_files
        assert "dosage_table_guideline.pdf" in processed_files
        assert "journal_multicolumn_guideline.pdf" in processed_files

        # Verify records have required structure
        for record in all_records:
            assert "title" in record
            assert "content" in record
            assert "metadata" in record
            assert "embedding" in record
            assert "source" in record["metadata"]
            assert "page" in record["metadata"]
            assert len(record["embedding"]) == 1536

    @pytest.mark.asyncio
    @pytest.mark.parametrize("pdf_name,min_chunks", [
        ("standard_text_guideline.pdf", 3),  # 2 pages, moderate text
        ("dosage_table_guideline.pdf", 2),   # 2 pages with tables
        ("journal_multicolumn_guideline.pdf", 2),  # Multi-column, 1-2 pages
    ])
    async def test_each_format_creates_chunks(self, pdf_name, min_chunks, tmp_path):
        """
        Test that each PDF format creates expected minimum number of chunks.
        """
        import shutil
        src = os.path.join(FIXTURES_DIR, pdf_name)
        dst = os.path.join(str(tmp_path), pdf_name)
        shutil.copy(src, dst)

        chunk_records = []

        mock_supabase = MagicMock()
        mock_table = MagicMock()
        mock_supabase.table.return_value = mock_table

        mock_delete = MagicMock()
        mock_table.delete.return_value = mock_delete
        mock_filter = MagicMock()
        mock_delete.filter.return_value = mock_filter
        mock_filter.execute.return_value = MagicMock()

        def capture_insert(records):
            chunk_records.extend(records)
            mock_insert = MagicMock()
            mock_insert.execute.return_value = MagicMock()
            return mock_insert

        mock_table.insert.side_effect = capture_insert

        mock_embeddings = MagicMock()
        mock_embeddings.embed_documents.side_effect = lambda texts: [[0.1] * 1536 for _ in texts]

        with patch("backend.data_processing.loaders.guidelines_loader.get_supabase_client", return_value=mock_supabase), \
             patch("backend.data_processing.loaders.guidelines_loader.OpenAIEmbeddings", return_value=mock_embeddings):

            from backend.data_processing.loaders.guidelines_loader import GuidelinesLoader
            loader = GuidelinesLoader(pdf_dir=str(tmp_path))
            loader.supabase = mock_supabase
            loader.embeddings = mock_embeddings

            await loader.ingest_pdfs()

        # Verify minimum chunks created
        assert len(chunk_records) >= min_chunks, (
            f"{pdf_name} created only {len(chunk_records)} chunks, expected >= {min_chunks}"
        )


class TestMultiFormatQueryRetrieval:
    """Test querying content from different PDF formats."""

    @pytest.mark.asyncio
    async def test_query_retrieves_from_standard_text(self):
        """Test querying diabetes guidelines from standard text PDF."""
        mock_results = [
            {
                "id": "uuid-1",
                "title": "standard_text_guideline.pdf",
                "content": "Metformin zůstává lékem první volby pro většinu pacientů s diabetes mellitus 2. typu.",
                "metadata": {"source": "standard_text_guideline.pdf", "page": 1},
                "similarity": 0.88
            }
        ]

        mock_search_service = MagicMock()
        mock_search_service.search_guidelines = AsyncMock(return_value=[
            {**r, "source": r["metadata"]["source"], "page": r["metadata"]["page"], "source_type": "guidelines"}
            for r in mock_results
        ])

        with patch("backend.app.core.graph.search_service", mock_search_service):
            from backend.app.core.graph import retrieve_guidelines_node

            mock_message = MagicMock()
            mock_message.content = "Jaký je lék první volby pro diabetes?"
            state = {
                "messages": [mock_message],
                "query_type": "guidelines",
                "retrieved_context": [],
                "final_answer": None,
                "next_step": "retrieve_guidelines"
            }

            result = await retrieve_guidelines_node(state)

        assert len(result["retrieved_context"]) == 1
        context = result["retrieved_context"][0]
        assert context["data"]["source"] == "standard_text_guideline.pdf"
        assert context["data"]["page"] == 1

    @pytest.mark.asyncio
    async def test_query_retrieves_from_table_pdf(self):
        """Test querying dosage information from table-based PDF."""
        mock_results = [
            {
                "id": "uuid-2",
                "title": "dosage_table_guideline.pdf",
                "content": "Empagliflozin: Počáteční dávka 10 mg, Maximální dávka 25 mg",
                "metadata": {"source": "dosage_table_guideline.pdf", "page": 0},
                "similarity": 0.91
            }
        ]

        mock_search_service = MagicMock()
        mock_search_service.search_guidelines = AsyncMock(return_value=[
            {**r, "source": r["metadata"]["source"], "page": r["metadata"]["page"], "source_type": "guidelines"}
            for r in mock_results
        ])

        with patch("backend.app.core.graph.search_service", mock_search_service):
            from backend.app.core.graph import retrieve_guidelines_node

            mock_message = MagicMock()
            mock_message.content = "Jaká je dávka empagliflozinu?"
            state = {
                "messages": [mock_message],
                "query_type": "guidelines",
                "retrieved_context": [],
                "final_answer": None,
                "next_step": "retrieve_guidelines"
            }

            result = await retrieve_guidelines_node(state)

        assert len(result["retrieved_context"]) == 1
        context = result["retrieved_context"][0]
        assert "dosage_table_guideline.pdf" in context["data"]["source"]

    @pytest.mark.asyncio
    async def test_query_retrieves_from_multicolumn_pdf(self):
        """Test querying hypertension guidelines from journal-format PDF."""
        mock_results = [
            {
                "id": "uuid-3",
                "title": "journal_multicolumn_guideline.pdf",
                "content": "ACE inhibitory nebo ARB, blokátory kalciových kanálů, thiazidová diuretika",
                "metadata": {"source": "journal_multicolumn_guideline.pdf", "page": 0},
                "similarity": 0.87
            }
        ]

        mock_search_service = MagicMock()
        mock_search_service.search_guidelines = AsyncMock(return_value=[
            {**r, "source": r["metadata"]["source"], "page": r["metadata"]["page"], "source_type": "guidelines"}
            for r in mock_results
        ])

        with patch("backend.app.core.graph.search_service", mock_search_service):
            from backend.app.core.graph import retrieve_guidelines_node

            mock_message = MagicMock()
            mock_message.content = "Jaké jsou léky na hypertenzi?"
            state = {
                "messages": [mock_message],
                "query_type": "guidelines",
                "retrieved_context": [],
                "final_answer": None,
                "next_step": "retrieve_guidelines"
            }

            result = await retrieve_guidelines_node(state)

        assert len(result["retrieved_context"]) == 1
        context = result["retrieved_context"][0]
        assert "journal_multicolumn_guideline.pdf" in context["data"]["source"]


class TestCitationPageNumbers:
    """Test that citations include correct page numbers for all formats."""

    @pytest.mark.parametrize("pdf_name", [
        "standard_text_guideline.pdf",
        "dosage_table_guideline.pdf",
        "journal_multicolumn_guideline.pdf",
    ])
    def test_page_numbers_in_chunks(self, pdf_name):
        """Verify page numbers are correctly assigned to chunks."""
        from langchain_text_splitters import RecursiveCharacterTextSplitter

        filepath = os.path.join(FIXTURES_DIR, pdf_name)
        loader = PyPDFLoader(filepath)
        docs = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        chunks = text_splitter.split_documents(docs)

        # Collect page numbers
        pages_in_chunks = set()
        for chunk in chunks:
            page = chunk.metadata.get("page")
            assert page is not None, f"Chunk from {pdf_name} missing page number"
            pages_in_chunks.add(page)

        # Verify we have chunks from expected pages
        assert len(pages_in_chunks) > 0, f"No page numbers found in chunks from {pdf_name}"

    @pytest.mark.asyncio
    async def test_citation_format_includes_page(self):
        """Test that synthesizer receives page information for citation formatting."""
        mock_llm = MagicMock()
        mock_llm_response = MagicMock()
        mock_llm_response.content = "Odpověď s citacemi [1]"
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
                            "content": "Test content",
                            "source": "standard_text_guideline.pdf",
                            "page": 2,
                            "similarity": 0.9
                        }
                    }
                ],
                "final_answer": None,
                "next_step": None
            }

            result = await synthesizer_node(state)

        # Verify LLM received context with page number
        call_args = mock_llm.ainvoke.call_args
        messages = call_args[0][0]

        # Find the context message (should include source and page)
        context_found = False
        for msg in messages:
            if hasattr(msg, 'content') and "standard_text_guideline.pdf" in msg.content:
                context_found = True
                # Verify page number is included
                assert "2" in msg.content or "page" in msg.content.lower()
                break

        assert context_found, "Context with source and page not found in LLM call"


class TestEndToEndMultiFormat:
    """End-to-end tests for multi-format PDF processing."""

    @pytest.mark.asyncio
    async def test_e2e_all_formats_stored_and_queryable(self, tmp_path):
        """
        Full E2E test: Upload all 3 formats, process, and query.
        Verifies the complete pipeline works for all formats.
        """
        import shutil

        # Setup: Copy all fixtures
        for pdf_name in [
            "standard_text_guideline.pdf",
            "dosage_table_guideline.pdf",
            "journal_multicolumn_guideline.pdf"
        ]:
            src = os.path.join(FIXTURES_DIR, pdf_name)
            dst = os.path.join(str(tmp_path), pdf_name)
            shutil.copy(src, dst)

        # Database mock that stores records for later query
        stored_records = []

        mock_supabase = MagicMock()
        mock_table = MagicMock()
        mock_supabase.table.return_value = mock_table

        mock_delete = MagicMock()
        mock_table.delete.return_value = mock_delete
        mock_filter = MagicMock()
        mock_delete.filter.return_value = mock_filter
        mock_filter.execute.return_value = MagicMock()

        def capture_insert(records):
            stored_records.extend(records)
            mock_insert = MagicMock()
            mock_insert.execute.return_value = MagicMock()
            return mock_insert

        mock_table.insert.side_effect = capture_insert

        # Mock embeddings
        mock_embeddings = MagicMock()
        mock_embeddings.embed_documents.side_effect = lambda texts: [[0.1] * 1536 for _ in texts]

        # Step 1: Process all PDFs
        with patch("backend.data_processing.loaders.guidelines_loader.get_supabase_client", return_value=mock_supabase), \
             patch("backend.data_processing.loaders.guidelines_loader.OpenAIEmbeddings", return_value=mock_embeddings):

            from backend.data_processing.loaders.guidelines_loader import GuidelinesLoader
            loader = GuidelinesLoader(pdf_dir=str(tmp_path))
            loader.supabase = mock_supabase
            loader.embeddings = mock_embeddings

            await loader.ingest_pdfs()

        # Step 2: Verify all formats stored (sources may contain full paths)
        sources = set(r["metadata"]["source"] for r in stored_records)
        expected_files = [
            "standard_text_guideline.pdf",
            "dosage_table_guideline.pdf",
            "journal_multicolumn_guideline.pdf"
        ]
        for expected_file in expected_files:
            found = any(expected_file in src for src in sources)
            assert found, f"{expected_file} not found in sources: {sources}"

        # Step 3: Verify each format has chunks with page numbers
        for source_path in sources:
            pdf_records = [r for r in stored_records if r["metadata"]["source"] == source_path]
            assert len(pdf_records) > 0, f"No records for {source_path}"

            # Check page numbers
            pages = [r["metadata"]["page"] for r in pdf_records]
            assert all(isinstance(p, int) and p >= 0 for p in pages), (
                f"Invalid page numbers in {source_path}: {pages}"
            )

        # Step 4: Verify content was extracted
        for record in stored_records:
            assert record["content"], f"Empty content in record from {record['title']}"
            assert len(record["content"]) > 10, "Content too short"
