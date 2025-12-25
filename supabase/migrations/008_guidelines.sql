-- Migration 008: Guidelines Table for RAG Pipeline
-- Stores Czech medical guideline chunks with embeddings for vector similarity search

-- Enable pgvector extension if not already enabled
CREATE EXTENSION IF NOT EXISTS vector;

-- Create guidelines table for storing chunked guideline content
CREATE TABLE IF NOT EXISTS guidelines (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    organization TEXT DEFAULT 'Unknown',
    publication_year TEXT,
    content TEXT NOT NULL,
    embedding vector(1536),
    metadata JSONB DEFAULT '{}',
    is_czech BOOLEAN DEFAULT TRUE,
    full_content TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create HNSW index for fast cosine similarity search on embeddings
CREATE INDEX IF NOT EXISTS idx_guidelines_embedding
ON guidelines
USING hnsw (embedding vector_cosine_ops);

-- Create index on metadata for efficient filtering by source
CREATE INDEX IF NOT EXISTS idx_guidelines_metadata
ON guidelines
USING gin (metadata);

-- Create index on title for duplicate detection
CREATE INDEX IF NOT EXISTS idx_guidelines_title
ON guidelines (title);

-- RPC function for vector similarity search on guidelines
CREATE OR REPLACE FUNCTION match_guidelines(
    query_embedding vector(1536),
    match_threshold float,
    match_count int
)
RETURNS TABLE (
    id uuid,
    title text,
    content text,
    metadata jsonb,
    similarity float
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        guidelines.id,
        guidelines.title,
        guidelines.content,
        guidelines.metadata,
        1 - (guidelines.embedding <=> query_embedding) AS similarity
    FROM guidelines
    WHERE 1 - (guidelines.embedding <=> query_embedding) > match_threshold
    ORDER BY guidelines.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;

-- Trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_guidelines_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER guidelines_updated_at_trigger
    BEFORE UPDATE ON guidelines
    FOR EACH ROW
    EXECUTE FUNCTION update_guidelines_updated_at();

-- Grant permissions (adjust based on your RLS policies)
ALTER TABLE guidelines ENABLE ROW LEVEL SECURITY;

-- Policy for authenticated users to read guidelines
CREATE POLICY "Allow authenticated users to read guidelines"
    ON guidelines
    FOR SELECT
    TO authenticated
    USING (true);

-- Policy for service role to manage guidelines (for background processing)
CREATE POLICY "Allow service role full access"
    ON guidelines
    FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

COMMENT ON TABLE guidelines IS 'Stores chunked Czech medical guidelines with embeddings for RAG retrieval';
COMMENT ON COLUMN guidelines.content IS 'Chunk text content for vector search';
COMMENT ON COLUMN guidelines.embedding IS '1536-dimensional OpenAI text-embedding-3-small vector';
COMMENT ON COLUMN guidelines.metadata IS 'JSONB containing source filename, page number, and other metadata for citations';
