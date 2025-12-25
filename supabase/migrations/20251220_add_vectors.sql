-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Update drugs table with missing columns from spec
ALTER TABLE drugs ADD COLUMN IF NOT EXISTS strength VARCHAR(24);
ALTER TABLE drugs ADD COLUMN IF NOT EXISTS form VARCHAR(27);
ALTER TABLE drugs ADD COLUMN IF NOT EXISTS package VARCHAR(22);
ALTER TABLE drugs ADD COLUMN IF NOT EXISTS route VARCHAR(15);
ALTER TABLE drugs ADD COLUMN IF NOT EXISTS atc_name VARCHAR(200);
ALTER TABLE drugs ADD COLUMN IF NOT EXISTS active_substances TEXT;
ALTER TABLE drugs ADD COLUMN IF NOT EXISTS dispensing VARCHAR(1);
ALTER TABLE drugs ADD COLUMN IF NOT EXISTS registration_status VARCHAR(2);
ALTER TABLE drugs ADD COLUMN IF NOT EXISTS is_available BOOLEAN DEFAULT false;
ALTER TABLE drugs ADD COLUMN IF NOT EXISTS holder VARCHAR(200);
ALTER TABLE drugs ADD COLUMN IF NOT EXISTS search_text TEXT;
ALTER TABLE drugs ADD COLUMN IF NOT EXISTS embedding vector(1536);
ALTER TABLE drugs ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ DEFAULT now();

-- Create HNSW index for fast vector search
CREATE INDEX IF NOT EXISTS drugs_embedding_idx ON drugs
  USING hnsw (embedding vector_cosine_ops)
  WITH (m = 16, ef_construction = 64);

-- Create standard indexes
CREATE INDEX IF NOT EXISTS drugs_atc_idx ON drugs(atc_code);
CREATE INDEX IF NOT EXISTS drugs_name_idx ON drugs(name);
CREATE INDEX IF NOT EXISTS drugs_status_idx ON drugs(registration_status);

-- Semantic Search Function
CREATE OR REPLACE FUNCTION search_drugs(
  query_embedding vector(1536),
  match_threshold float DEFAULT 0.7,
  match_count int DEFAULT 10
) RETURNS TABLE (
  id UUID, 
  sukl_code VARCHAR, 
  name VARCHAR,
  active_substances TEXT, 
  atc_name VARCHAR,
  similarity float
) LANGUAGE plpgsql AS $$
BEGIN
  RETURN QUERY SELECT d.id, d.sukl_code, d.name,
    d.active_substances, d.atc_name,
    1 - (d.embedding <=> query_embedding) AS similarity
  FROM drugs d
  WHERE 1 - (d.embedding <=> query_embedding) > match_threshold
  ORDER BY d.embedding <=> query_embedding
  LIMIT match_count;
END; $$;
