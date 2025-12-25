-- Migration: 003_create_user_preferences.sql
CREATE TABLE IF NOT EXISTS user_preferences (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    preferred_language TEXT DEFAULT 'cs' CHECK (preferred_language IN ('cs', 'en')),
    preferred_sources TEXT[] DEFAULT ARRAY['pubmed', 'sukl', 'guidelines'],
    max_citations INTEGER DEFAULT 5 CHECK (max_citations BETWEEN 1 AND 10),
    email_notifications BOOLEAN DEFAULT TRUE,
    new_guidelines_alerts BOOLEAN DEFAULT TRUE,
    theme TEXT DEFAULT 'system' CHECK (theme IN ('light', 'dark', 'system')),
    compact_mode BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id)
);

CREATE INDEX IF NOT EXISTS idx_user_prefs_user_id ON user_preferences(user_id);
ALTER TABLE user_preferences ENABLE ROW LEVEL SECURITY;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'user_prefs_updated_at') THEN
        CREATE TRIGGER user_prefs_updated_at BEFORE UPDATE ON user_preferences FOR EACH ROW EXECUTE FUNCTION update_updated_at();
    END IF;
END $$;
