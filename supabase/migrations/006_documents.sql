-- Migration: 006_create_documents.sql
CREATE TABLE IF NOT EXISTS documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_type source_type NOT NULL,
    external_id TEXT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    abstract TEXT,
    authors TEXT[],
    journal TEXT,
    publication_date DATE,
    publication_year INTEGER,
    url TEXT,
    pmid TEXT,
    doi TEXT,
    embedding vector(1536),
    metadata JSONB DEFAULT '{}',
    language TEXT DEFAULT 'cs',
    is_indexed BOOLEAN DEFAULT FALSE,
    indexed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(source_type, external_id)
);

CREATE INDEX IF NOT EXISTS idx_documents_source ON documents(source_type);
CREATE INDEX IF NOT EXISTS idx_documents_embedding ON documents USING hnsw (embedding vector_cosine_ops) WITH (m = 16, ef_construction = 64);
CREATE INDEX IF NOT EXISTS idx_documents_fts ON documents USING gin(to_tsvector('simple', title || ' ' || COALESCE(abstract, '')));

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'documents_updated_at') THEN
        CREATE TRIGGER documents_updated_at BEFORE UPDATE ON documents FOR EACH ROW EXECUTE FUNCTION update_updated_at();
    END IF;
END $$;
