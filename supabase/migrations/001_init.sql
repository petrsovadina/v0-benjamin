-- Migration: 001_init_extensions.sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "vector";

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'user_role') THEN
        CREATE TYPE user_role AS ENUM ('physician', 'specialist', 'admin', 'readonly');
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'license_type') THEN
        CREATE TYPE license_type AS ENUM ('CLK', 'ICP', 'OTHER');
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'query_type') THEN
        CREATE TYPE query_type AS ENUM ('quick', 'deep');
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'query_status') THEN
        CREATE TYPE query_status AS ENUM ('pending', 'processing', 'completed', 'failed');
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'source_type') THEN
        CREATE TYPE source_type AS ENUM ('pubmed', 'sukl', 'guidelines', 'vzp', 'cochrane', 'other');
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'subscription_plan') THEN
        CREATE TYPE subscription_plan AS ENUM ('free', 'professional', 'enterprise');
    END IF;
END $$;
