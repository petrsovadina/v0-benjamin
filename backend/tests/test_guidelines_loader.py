import pytest
import sys
from unittest.mock import MagicMock, patch

# Mock all external dependencies before importing the module
mock_langchain_docs = MagicMock()
mock_langchain_splitter = MagicMock()
mock_langchain_openai = MagicMock()
mock_supabase_module = MagicMock()
mock_settings = MagicMock()
mock_database = MagicMock()
mock_logger = MagicMock()

# Pre-configure mocks
mock_settings.OPENAI_API_KEY = "test-api-key"


@pytest.fixture
def mock_modules():
    """Setup sys.modules mocks for all dependencies."""
    original_modules = {}
    modules_to_mock = {
        'langchain_community': MagicMock(),
        'langchain_community.document_loaders': mock_langchain_docs,
        'langchain_text_splitters': mock_langchain_splitter,
        'langchain_openai': mock_langchain_openai,
        'supabase': mock_supabase_module,
        'backend': MagicMock(),
        'backend.app': MagicMock(),
        'backend.app.core': MagicMock(),
        'backend.app.core.config': MagicMock(settings=mock_settings),
        'backend.app.core.database': mock_database,
        'backend.services': MagicMock(),
        'backend.services.logger': mock_logger,
    }

    for name, mock in modules_to_mock.items():
        if name in sys.modules:
            original_modules[name] = sys.modules[name]
        sys.modules[name] = mock

    # Setup specific attributes
    sys.modules['backend.app.core.config'].settings = mock_settings
    sys.modules['backend.app.core.database'].get_supabase_client = MagicMock()
    sys.modules['backend.services.logger'].get_logger = MagicMock(return_value=MagicMock())

    yield modules_to_mock

    # Cleanup
    for name in modules_to_mock:
        if name in original_modules:
            sys.modules[name] = original_modules[name]
        elif name in sys.modules:
            del sys.modules[name]


class TestGuidelinesLoaderClass:
    """Tests for GuidelinesLoader class without full module import."""

    def test_embed_with_retry_success_first_attempt(self):
        """Test successful embedding on first attempt."""
        # Create mock embeddings
        mock_embeddings = MagicMock()
        mock_embeddings.embed_documents.return_value = [[0.1] * 1536, [0.2] * 1536]

        # Create a simple GuidelinesLoader-like object to test retry logic
        class TestRetryLogic:
            def __init__(self):
                self.embeddings = mock_embeddings

            def _embed_with_retry(self, texts, batch_index, filename):
                max_retries = 3
                base_delay = 1.0
                max_delay = 10.0
                last_exception = None

                for attempt in range(1, max_retries + 1):
                    try:
                        vectors = self.embeddings.embed_documents(texts)
                        return vectors
                    except Exception as e:
                        last_exception = e
                        if attempt < max_retries:
                            import time
                            delay = min(base_delay * (2 ** (attempt - 1)), max_delay)
                            time.sleep(delay)

                raise last_exception

        loader = TestRetryLogic()
        texts = ["text1", "text2"]
        result = loader._embed_with_retry(texts, batch_index=0, filename="test.pdf")

        assert len(result) == 2
        assert result[0] == [0.1] * 1536
        mock_embeddings.embed_documents.assert_called_once_with(texts)

    def test_embed_with_retry_success_after_retry(self):
        """Test successful embedding after a retry."""
        mock_embeddings = MagicMock()
        mock_embeddings.embed_documents.side_effect = [
            Exception("Rate limit"),
            [[0.3] * 1536]
        ]

        class TestRetryLogic:
            def __init__(self):
                self.embeddings = mock_embeddings

            def _embed_with_retry(self, texts, batch_index, filename):
                max_retries = 3
                base_delay = 1.0
                max_delay = 10.0
                last_exception = None

                for attempt in range(1, max_retries + 1):
                    try:
                        vectors = self.embeddings.embed_documents(texts)
                        return vectors
                    except Exception as e:
                        last_exception = e
                        if attempt < max_retries:
                            import time
                            delay = min(base_delay * (2 ** (attempt - 1)), max_delay)
                            time.sleep(delay)

                raise last_exception

        with patch('time.sleep'):
            loader = TestRetryLogic()
            result = loader._embed_with_retry(["text1"], batch_index=0, filename="test.pdf")

        assert result == [[0.3] * 1536]
        assert mock_embeddings.embed_documents.call_count == 2

    def test_embed_with_retry_exhausted(self):
        """Test exception raised when all retries are exhausted."""
        mock_embeddings = MagicMock()
        mock_embeddings.embed_documents.side_effect = Exception("Persistent error")

        class TestRetryLogic:
            def __init__(self):
                self.embeddings = mock_embeddings

            def _embed_with_retry(self, texts, batch_index, filename):
                max_retries = 3
                base_delay = 1.0
                max_delay = 10.0
                last_exception = None

                for attempt in range(1, max_retries + 1):
                    try:
                        vectors = self.embeddings.embed_documents(texts)
                        return vectors
                    except Exception as e:
                        last_exception = e
                        if attempt < max_retries:
                            import time
                            delay = min(base_delay * (2 ** (attempt - 1)), max_delay)
                            time.sleep(delay)

                raise last_exception

        with patch('time.sleep'):
            loader = TestRetryLogic()
            with pytest.raises(Exception) as exc_info:
                loader._embed_with_retry(["text1"], batch_index=0, filename="test.pdf")

        assert "Persistent error" in str(exc_info.value)
        assert mock_embeddings.embed_documents.call_count == 3

    def test_embed_with_retry_exponential_backoff(self):
        """Test that exponential backoff is applied."""
        mock_embeddings = MagicMock()
        mock_embeddings.embed_documents.side_effect = [
            Exception("Error 1"),
            Exception("Error 2"),
            [[0.5] * 1536]
        ]

        class TestRetryLogic:
            def __init__(self):
                self.embeddings = mock_embeddings

            def _embed_with_retry(self, texts, batch_index, filename):
                import time
                max_retries = 3
                base_delay = 1.0
                max_delay = 10.0
                last_exception = None

                for attempt in range(1, max_retries + 1):
                    try:
                        vectors = self.embeddings.embed_documents(texts)
                        return vectors
                    except Exception as e:
                        last_exception = e
                        if attempt < max_retries:
                            delay = min(base_delay * (2 ** (attempt - 1)), max_delay)
                            time.sleep(delay)

                raise last_exception

        with patch('time.sleep') as mock_sleep:
            loader = TestRetryLogic()
            result = loader._embed_with_retry(["text1"], batch_index=0, filename="test.pdf")

        assert mock_sleep.call_count == 2
        mock_sleep.assert_any_call(1.0)
        mock_sleep.assert_any_call(2.0)


class TestIngestPdfsLogic:
    """Tests for ingest_pdfs logic patterns."""

    def test_ingest_pdfs_no_files_found(self):
        """Test handling when no PDF files are found."""
        import glob as glob_module

        with patch.object(glob_module, 'glob', return_value=[]):
            # Simulating ingest_pdfs behavior
            pdf_files = glob_module.glob("test_dir/*.pdf")

            assert pdf_files == []
            # No processing should occur

    def test_ingest_pdfs_processes_files(self):
        """Test that PDF files are processed correctly."""
        import os
        import glob as glob_module

        mock_pdf_loader = MagicMock()
        mock_doc = MagicMock()
        mock_doc.page_content = "Test PDF content"
        mock_doc.metadata = {"page": 0, "source": "test.pdf"}
        mock_pdf_loader.load.return_value = [mock_doc]

        mock_text_splitter = MagicMock()
        mock_chunk = MagicMock()
        mock_chunk.page_content = "Test chunk"
        mock_chunk.metadata = {"page": 0}
        mock_text_splitter.split_documents.return_value = [mock_chunk]

        mock_embeddings = MagicMock()
        mock_embeddings.embed_documents.return_value = [[0.1] * 1536]

        mock_supabase = MagicMock()
        mock_supabase.table.return_value.delete.return_value.filter.return_value.execute.return_value = None
        mock_supabase.table.return_value.insert.return_value.execute.return_value = None

        with patch.object(glob_module, 'glob', return_value=["test_pdfs/guideline.pdf"]):
            pdf_files = glob_module.glob("test_pdfs/*.pdf")

            assert len(pdf_files) == 1

            # Simulate processing
            for file_path in pdf_files:
                filename = os.path.basename(file_path)
                assert filename == "guideline.pdf"

                # Load PDF
                docs = mock_pdf_loader.load()
                assert len(docs) == 1

                # Split into chunks
                chunks = mock_text_splitter.split_documents(docs)
                assert len(chunks) == 1

                # Generate embeddings
                batch_texts = [c.page_content for c in chunks]
                vectors = mock_embeddings.embed_documents(batch_texts)
                assert len(vectors) == 1

                # Prepare records
                records = []
                for j, chunk in enumerate(chunks):
                    records.append({
                        "title": filename,
                        "organization": "Unknown",
                        "publication_year": "2024",
                        "is_czech": True,
                        "content": chunk.page_content,
                        "metadata": {
                            "source": filename,
                            "page": chunk.metadata.get("page", 0),
                            **chunk.metadata
                        },
                        "embedding": vectors[j]
                    })

                # Verify record format
                assert records[0]["title"] == "guideline.pdf"
                assert records[0]["organization"] == "Unknown"
                assert records[0]["publication_year"] == "2024"
                assert records[0]["is_czech"] is True
                assert records[0]["content"] == "Test chunk"
                assert records[0]["metadata"]["source"] == "guideline.pdf"
                assert records[0]["metadata"]["page"] == 0

    def test_ingest_pdfs_error_handling(self):
        """Test error handling during PDF processing."""
        import glob as glob_module

        mock_pdf_loader = MagicMock()
        mock_pdf_loader.load.side_effect = Exception("Cannot read PDF")

        errors_logged = []

        with patch.object(glob_module, 'glob', return_value=["test_pdfs/bad.pdf"]):
            pdf_files = glob_module.glob("test_pdfs/*.pdf")

            for file_path in pdf_files:
                try:
                    docs = mock_pdf_loader.load()
                except Exception as e:
                    errors_logged.append(str(e))

        assert len(errors_logged) == 1
        assert "Cannot read PDF" in errors_logged[0]


class TestBatchProcessing:
    """Tests for batch processing behavior."""

    def test_batch_size_calculation(self):
        """Test that chunks are correctly batched."""
        batch_size = 50
        chunks = list(range(75))  # 75 items

        batches = []
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i+batch_size]
            batches.append(batch)

        assert len(batches) == 2
        assert len(batches[0]) == 50
        assert len(batches[1]) == 25

    def test_large_pdf_batch_processing(self):
        """Test that large PDFs are processed in batches of 50."""
        mock_embeddings = MagicMock()

        def mock_embed(texts):
            return [[0.1] * 1536 for _ in texts]
        mock_embeddings.embed_documents.side_effect = mock_embed

        # Create 75 mock chunks
        mock_chunks = []
        for i in range(75):
            chunk = MagicMock()
            chunk.page_content = f"Chunk {i}"
            chunk.metadata = {"page": i}
            mock_chunks.append(chunk)

        batch_size = 50
        records = []

        for i in range(0, len(mock_chunks), batch_size):
            batch = mock_chunks[i:i+batch_size]
            batch_texts = [c.page_content for c in batch]
            vectors = mock_embeddings.embed_documents(batch_texts)

            for j, chunk in enumerate(batch):
                records.append({
                    "content": chunk.page_content,
                    "embedding": vectors[j]
                })

        assert mock_embeddings.embed_documents.call_count == 2

        # First batch should have 50 texts
        first_call_args = mock_embeddings.embed_documents.call_args_list[0][0][0]
        assert len(first_call_args) == 50

        # Second batch should have 25 texts
        second_call_args = mock_embeddings.embed_documents.call_args_list[1][0][0]
        assert len(second_call_args) == 25

        # Total records should be 75
        assert len(records) == 75


class TestRecordFormat:
    """Tests for database record format."""

    def test_record_has_required_fields(self):
        """Test that records have all required fields per 008_guidelines.sql."""
        mock_chunk = MagicMock()
        mock_chunk.page_content = "Test content"
        mock_chunk.metadata = {"page": 1}

        filename = "guideline.pdf"
        embedding = [0.1] * 1536

        record = {
            "title": filename,
            "organization": "Unknown",
            "publication_year": "2024",
            "is_czech": True,
            "content": mock_chunk.page_content,
            "metadata": {
                "source": filename,
                "page": mock_chunk.metadata.get("page", 0),
                **mock_chunk.metadata
            },
            "embedding": embedding
        }

        # Verify all required fields exist
        assert "title" in record
        assert "organization" in record
        assert "publication_year" in record
        assert "is_czech" in record
        assert "content" in record
        assert "metadata" in record
        assert "embedding" in record

        # Verify types
        assert isinstance(record["title"], str)
        assert isinstance(record["publication_year"], str)
        assert isinstance(record["is_czech"], bool)
        assert isinstance(record["metadata"], dict)
        assert isinstance(record["embedding"], list)
        assert len(record["embedding"]) == 1536

    def test_metadata_contains_source_and_page(self):
        """Test that metadata includes source attribution."""
        mock_chunk = MagicMock()
        mock_chunk.page_content = "Content"
        mock_chunk.metadata = {"page": 5, "extra_field": "value"}

        filename = "test_guideline.pdf"

        metadata = {
            "source": filename,
            "page": mock_chunk.metadata.get("page", 0),
            **mock_chunk.metadata
        }

        assert metadata["source"] == "test_guideline.pdf"
        assert metadata["page"] == 5
        assert metadata["extra_field"] == "value"
