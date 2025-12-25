-- Migration: 005_create_citations.sql
CREATE TABLE IF NOT EXISTS citations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    query_id UUID NOT NULL REFERENCES queries(id) ON DELETE CASCADE,
    document_id UUID,
    citation_order INTEGER NOT NULL CHECK (citation_order > 0),
    source_type source_type NOT NULL,
    external_id TEXT,
    pmid TEXT,
    doi TEXT,
    title TEXT NOT NULL,
    authors TEXT[],
    journal TEXT,
    publication_year INTEGER,
    url TEXT,
    relevance_score DECIMAL(3,2),
    snippet TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(query_id, citation_order)
);

CREATE INDEX IF NOT EXISTS idx_citations_query_id ON citations(query_id);
ALTER TABLE citations ENABLE ROW LEVEL SECURITY;
