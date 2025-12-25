-- Migration: 009_create_feedback.sql
CREATE TABLE IF NOT EXISTS feedback (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    query_id UUID NOT NULL REFERENCES queries(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    rating INTEGER CHECK (rating BETWEEN 1 AND 5),
    is_helpful BOOLEAN,
    accuracy_rating INTEGER CHECK (accuracy_rating BETWEEN 1 AND 5),
    relevance_rating INTEGER CHECK (relevance_rating BETWEEN 1 AND 5),
    completeness_rating INTEGER CHECK (completeness_rating BETWEEN 1 AND 5),
    comment TEXT,
    suggested_improvement TEXT,
    has_incorrect_info BOOLEAN DEFAULT FALSE,
    has_missing_info BOOLEAN DEFAULT FALSE,
    has_outdated_info BOOLEAN DEFAULT FALSE,
    has_citation_issue BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(query_id, user_id)
);

CREATE INDEX IF NOT EXISTS idx_feedback_rating ON feedback(rating);
ALTER TABLE feedback ENABLE ROW LEVEL SECURITY;
