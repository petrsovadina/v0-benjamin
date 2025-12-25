-- Migration: 002_create_users.sql
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    auth_id UUID UNIQUE REFERENCES auth.users(id) ON DELETE CASCADE,
    email TEXT UNIQUE NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    license_number TEXT,
    license_type license_type,
    license_verified BOOLEAN DEFAULT FALSE,
    license_verified_at TIMESTAMPTZ,
    specialty TEXT,
    workplace TEXT,
    role user_role DEFAULT 'physician',
    subscription_plan subscription_plan DEFAULT 'free',
    subscription_valid_until TIMESTAMPTZ,
    queries_used_this_month INTEGER DEFAULT 0,
    queries_limit INTEGER DEFAULT 10,
    is_active BOOLEAN DEFAULT TRUE,
    last_login_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_auth_id ON users(auth_id);
CREATE INDEX IF NOT EXISTS idx_users_license_number ON users(license_number);

ALTER TABLE users ENABLE ROW LEVEL SECURITY;

CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'users_updated_at') THEN
        CREATE TRIGGER users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at();
    END IF;
END $$;
