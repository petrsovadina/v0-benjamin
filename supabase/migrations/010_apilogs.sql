-- Migration: 010_create_api_logs.sql
CREATE TABLE IF NOT EXISTS api_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    endpoint TEXT NOT NULL,
    method TEXT NOT NULL,
    request_body JSONB,
    query_params JSONB,
    headers JSONB,
    status_code INTEGER NOT NULL,
    response_time_ms INTEGER,
    client_ip INET,
    user_agent TEXT,
    error_code TEXT,
    error_message TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_api_logs_created ON api_logs(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_api_logs_status ON api_logs(status_code);
