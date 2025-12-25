-- Migration 008_guidelines_add_columns: Add missing columns to guidelines table
-- The guidelines table exists but is missing content and metadata columns

-- Add content column for storing chunk text (required for RAG)
ALTER TABLE guidelines ADD COLUMN IF NOT EXISTS content TEXT;

-- Add metadata column for storing source/page info (required for citations)
ALTER TABLE guidelines ADD COLUMN IF NOT EXISTS metadata JSONB DEFAULT '{}';

-- Create index on metadata for efficient filtering by source
CREATE INDEX IF NOT EXISTS idx_guidelines_metadata
ON guidelines
USING gin (metadata);

-- Create/replace RPC function for vector similarity search on guidelines
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

-- Add comments for documentation
COMMENT ON COLUMN guidelines.content IS 'Chunk text content for vector search';
COMMENT ON COLUMN guidelines.metadata IS 'JSONB containing source filename, page number, and other metadata for citations';
