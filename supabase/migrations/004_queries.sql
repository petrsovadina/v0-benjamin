-- Migration: 004_create_queries.sql
CREATE TABLE IF NOT EXISTS queries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    query_text TEXT NOT NULL CHECK (char_length(query_text) BETWEEN 3 AND 2000),
    query_type query_type DEFAULT 'quick',
    query_language TEXT DEFAULT 'cs' CHECK (query_language IN ('cs', 'en')),
    status query_status DEFAULT 'pending',
    sources_requested source_type[] DEFAULT ARRAY['pubmed', 'sukl', 'guidelines']::source_type[],
    sources_searched source_type[],
    response_text TEXT,
    response_model TEXT,
    confidence_score DECIMAL(3,2) CHECK (confidence_score BETWEEN 0 AND 1),
    processing_time_ms INTEGER,
    tokens_used INTEGER,
    client_ip INET,
    user_agent TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    completed_at TIMESTAMPTZ,
    deleted_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_queries_user_id ON queries(user_id);
CREATE INDEX IF NOT EXISTS idx_queries_status ON queries(status);
CREATE INDEX IF NOT EXISTS idx_queries_created_at ON queries(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_queries_active ON queries(user_id, created_at DESC) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_queries_fts ON queries USING gin(to_tsvector('simple', query_text));
ALTER TABLE queries ENABLE ROW LEVEL SECURITY;
