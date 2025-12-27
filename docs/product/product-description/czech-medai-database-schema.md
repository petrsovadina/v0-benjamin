# Czech MedAI — Database Schema

**Projekt:** Czech MedAI (kódové označení: Benjamin)  
**Databáze:** Supabase (PostgreSQL 15+ s pgvector)  
**Verze schématu:** 1.0.0  
**Datum:** 15.12.2025

---

## 📋 Přehled

Tento dokument obsahuje kompletní databázové schéma pro Czech MedAI včetně:
- SQL migrace
- RLS (Row Level Security) politiky
- Indexy pro optimalizaci
- pgvector pro sémantické vyhledávání
- Funkce a triggery

---

## 🗄️ Entity Relationship Diagram

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   users     │────<│   queries   │     │  documents  │
└─────────────┘     └─────────────┘     └─────────────┘
       │                   │                   │
       │            ┌──────┴──────┐            │
       │            │             │            │
       ▼            ▼             ▼            │
┌─────────────┐ ┌─────────┐ ┌──────────┐      │
│ user_prefs  │ │citations│ │ feedback │      │
└─────────────┘ └─────────┘ └──────────┘      │
                     │                        │
                     └────────────────────────┘
                              references
```

---

## 📜 SQL Migrace

### Migration 001: Extensions a základní nastavení

```sql
-- Migration: 001_init_extensions.sql
-- Popis: Inicializace PostgreSQL extensions

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "vector";

-- Create custom types
CREATE TYPE user_role AS ENUM ('physician', 'specialist', 'admin', 'readonly');
CREATE TYPE license_type AS ENUM ('CLK', 'ICP', 'OTHER');
CREATE TYPE query_type AS ENUM ('quick', 'deep');
CREATE TYPE query_status AS ENUM ('pending', 'processing', 'completed', 'failed');
CREATE TYPE source_type AS ENUM ('pubmed', 'sukl', 'guidelines', 'vzp', 'cochrane', 'other');
CREATE TYPE subscription_plan AS ENUM ('free', 'professional', 'enterprise');
```

---

### Migration 002: Tabulka users

```sql
-- Migration: 002_create_users.sql
-- Popis: Tabulka uživatelů (lékařů)

CREATE TABLE users (
    -- Primary key
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Auth (linked to Supabase Auth)
    auth_id UUID UNIQUE REFERENCES auth.users(id) ON DELETE CASCADE,
    
    -- Basic info
    email TEXT UNIQUE NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    
    -- Professional info
    license_number TEXT,
    license_type license_type,
    license_verified BOOLEAN DEFAULT FALSE,
    license_verified_at TIMESTAMPTZ,
    specialty TEXT,
    workplace TEXT,
    
    -- Role & permissions
    role user_role DEFAULT 'physician',
    
    -- Subscription
    subscription_plan subscription_plan DEFAULT 'free',
    subscription_valid_until TIMESTAMPTZ,
    queries_used_this_month INTEGER DEFAULT 0,
    queries_limit INTEGER DEFAULT 10,
    
    -- Metadata
    is_active BOOLEAN DEFAULT TRUE,
    last_login_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_auth_id ON users(auth_id);
CREATE INDEX idx_users_license_number ON users(license_number);
CREATE INDEX idx_users_specialty ON users(specialty);
CREATE INDEX idx_users_subscription ON users(subscription_plan, subscription_valid_until);

-- RLS
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Policy: Users can read their own profile
CREATE POLICY "users_select_own"
ON users FOR SELECT
TO authenticated
USING ((SELECT auth.uid()) = auth_id);

-- Policy: Users can update their own profile
CREATE POLICY "users_update_own"
ON users FOR UPDATE
TO authenticated
USING ((SELECT auth.uid()) = auth_id)
WITH CHECK ((SELECT auth.uid()) = auth_id);

-- Policy: Admins can read all users
CREATE POLICY "users_admin_select"
ON users FOR SELECT
TO authenticated
USING (
    EXISTS (
        SELECT 1 FROM users u 
        WHERE u.auth_id = (SELECT auth.uid()) 
        AND u.role = 'admin'
    )
);

-- Trigger: Update timestamp
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();
```

---

### Migration 003: Tabulka user_preferences

```sql
-- Migration: 003_create_user_preferences.sql
-- Popis: Uživatelské preference

CREATE TABLE user_preferences (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- Display preferences
    preferred_language TEXT DEFAULT 'cs' CHECK (preferred_language IN ('cs', 'en')),
    preferred_sources TEXT[] DEFAULT ARRAY['pubmed', 'sukl', 'guidelines'],
    max_citations INTEGER DEFAULT 5 CHECK (max_citations BETWEEN 1 AND 10),
    
    -- Notification preferences
    email_notifications BOOLEAN DEFAULT TRUE,
    new_guidelines_alerts BOOLEAN DEFAULT TRUE,
    
    -- UI preferences
    theme TEXT DEFAULT 'system' CHECK (theme IN ('light', 'dark', 'system')),
    compact_mode BOOLEAN DEFAULT FALSE,
    
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Constraints
    UNIQUE(user_id)
);

-- Indexes
CREATE INDEX idx_user_prefs_user_id ON user_preferences(user_id);

-- RLS
ALTER TABLE user_preferences ENABLE ROW LEVEL SECURITY;

CREATE POLICY "user_prefs_select_own"
ON user_preferences FOR SELECT
TO authenticated
USING (
    user_id IN (
        SELECT id FROM users WHERE auth_id = (SELECT auth.uid())
    )
);

CREATE POLICY "user_prefs_insert_own"
ON user_preferences FOR INSERT
TO authenticated
WITH CHECK (
    user_id IN (
        SELECT id FROM users WHERE auth_id = (SELECT auth.uid())
    )
);

CREATE POLICY "user_prefs_update_own"
ON user_preferences FOR UPDATE
TO authenticated
USING (
    user_id IN (
        SELECT id FROM users WHERE auth_id = (SELECT auth.uid())
    )
);

-- Trigger
CREATE TRIGGER user_prefs_updated_at
    BEFORE UPDATE ON user_preferences
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();
```

---

### Migration 004: Tabulka queries

```sql
-- Migration: 004_create_queries.sql
-- Popis: Klinické dotazy a odpovědi

CREATE TABLE queries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Foreign keys
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- Query details
    query_text TEXT NOT NULL CHECK (char_length(query_text) BETWEEN 3 AND 2000),
    query_type query_type DEFAULT 'quick',
    query_language TEXT DEFAULT 'cs' CHECK (query_language IN ('cs', 'en')),
    
    -- Processing
    status query_status DEFAULT 'pending',
    sources_requested source_type[] DEFAULT ARRAY['pubmed', 'sukl', 'guidelines']::source_type[],
    sources_searched source_type[],
    
    -- Response
    response_text TEXT,
    response_model TEXT,
    confidence_score DECIMAL(3,2) CHECK (confidence_score BETWEEN 0 AND 1),
    
    -- Performance
    processing_time_ms INTEGER,
    tokens_used INTEGER,
    
    -- Metadata
    client_ip INET,
    user_agent TEXT,
    
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    completed_at TIMESTAMPTZ,
    
    -- Soft delete
    deleted_at TIMESTAMPTZ
);

-- Indexes
CREATE INDEX idx_queries_user_id ON queries(user_id);
CREATE INDEX idx_queries_status ON queries(status);
CREATE INDEX idx_queries_created_at ON queries(created_at DESC);
CREATE INDEX idx_queries_user_created ON queries(user_id, created_at DESC);

-- Partial index for active queries
CREATE INDEX idx_queries_active ON queries(user_id, created_at DESC) 
WHERE deleted_at IS NULL;

-- Full text search index
CREATE INDEX idx_queries_fts ON queries 
USING gin(to_tsvector('simple', query_text));

-- RLS
ALTER TABLE queries ENABLE ROW LEVEL SECURITY;

-- Optimized policy with (SELECT auth.uid()) wrapper
CREATE POLICY "queries_select_own"
ON queries FOR SELECT
TO authenticated
USING (
    user_id IN (
        SELECT id FROM users WHERE auth_id = (SELECT auth.uid())
    )
    AND deleted_at IS NULL
);

CREATE POLICY "queries_insert_own"
ON queries FOR INSERT
TO authenticated
WITH CHECK (
    user_id IN (
        SELECT id FROM users WHERE auth_id = (SELECT auth.uid())
    )
);

CREATE POLICY "queries_update_own"
ON queries FOR UPDATE
TO authenticated
USING (
    user_id IN (
        SELECT id FROM users WHERE auth_id = (SELECT auth.uid())
    )
);
```

---

### Migration 005: Tabulka citations

```sql
-- Migration: 005_create_citations.sql
-- Popis: Citace připojené k odpovědím

CREATE TABLE citations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Foreign keys
    query_id UUID NOT NULL REFERENCES queries(id) ON DELETE CASCADE,
    document_id UUID REFERENCES documents(id) ON DELETE SET NULL,
    
    -- Citation details
    citation_order INTEGER NOT NULL CHECK (citation_order > 0),
    source_type source_type NOT NULL,
    
    -- External identifiers
    external_id TEXT,  -- PMID, SUKL code, etc.
    pmid TEXT,
    doi TEXT,
    
    -- Content
    title TEXT NOT NULL,
    authors TEXT[],
    journal TEXT,
    publication_year INTEGER CHECK (publication_year BETWEEN 1900 AND 2100),
    url TEXT,
    
    -- Relevance
    relevance_score DECIMAL(3,2) CHECK (relevance_score BETWEEN 0 AND 1),
    snippet TEXT,  -- Relevant excerpt
    
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Constraints
    UNIQUE(query_id, citation_order)
);

-- Indexes
CREATE INDEX idx_citations_query_id ON citations(query_id);
CREATE INDEX idx_citations_pmid ON citations(pmid) WHERE pmid IS NOT NULL;
CREATE INDEX idx_citations_doi ON citations(doi) WHERE doi IS NOT NULL;
CREATE INDEX idx_citations_source ON citations(source_type);

-- RLS
ALTER TABLE citations ENABLE ROW LEVEL SECURITY;

CREATE POLICY "citations_select_via_query"
ON citations FOR SELECT
TO authenticated
USING (
    query_id IN (
        SELECT q.id FROM queries q
        JOIN users u ON q.user_id = u.id
        WHERE u.auth_id = (SELECT auth.uid())
    )
);
```

---

### Migration 006: Tabulka documents (RAG)

```sql
-- Migration: 006_create_documents.sql
-- Popis: Dokumenty pro RAG vektorové vyhledávání

CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Source identification
    source_type source_type NOT NULL,
    external_id TEXT,  -- PMID, SUKL code, guideline ID
    
    -- Content
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    abstract TEXT,
    
    -- Authors & publication
    authors TEXT[],
    journal TEXT,
    publication_date DATE,
    publication_year INTEGER,
    
    -- External links
    url TEXT,
    pmid TEXT,
    doi TEXT,
    
    -- Vector embedding for semantic search
    embedding vector(1536),  -- OpenAI ada-002 dimension
    
    -- Metadata
    metadata JSONB DEFAULT '{}',
    language TEXT DEFAULT 'cs',
    
    -- Processing status
    is_indexed BOOLEAN DEFAULT FALSE,
    indexed_at TIMESTAMPTZ,
    
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Constraints
    UNIQUE(source_type, external_id)
);

-- Indexes
CREATE INDEX idx_documents_source ON documents(source_type);
CREATE INDEX idx_documents_pmid ON documents(pmid) WHERE pmid IS NOT NULL;
CREATE INDEX idx_documents_doi ON documents(doi) WHERE doi IS NOT NULL;
CREATE INDEX idx_documents_external_id ON documents(source_type, external_id);
CREATE INDEX idx_documents_year ON documents(publication_year DESC);
CREATE INDEX idx_documents_indexed ON documents(is_indexed) WHERE is_indexed = FALSE;

-- HNSW index for vector similarity search
CREATE INDEX idx_documents_embedding ON documents 
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- Full text search
CREATE INDEX idx_documents_fts ON documents 
USING gin(to_tsvector('simple', title || ' ' || COALESCE(abstract, '')));

-- GIN index for JSONB metadata
CREATE INDEX idx_documents_metadata ON documents USING gin(metadata);

-- Trigger
CREATE TRIGGER documents_updated_at
    BEFORE UPDATE ON documents
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();
```

---

### Migration 007: Tabulka drugs (SÚKL cache)

```sql
-- Migration: 007_create_drugs.sql
-- Popis: Cache SÚKL databáze léčiv

CREATE TABLE drugs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- SÚKL identifiers
    sukl_code TEXT UNIQUE NOT NULL,
    registration_number TEXT,
    
    -- Basic info
    name TEXT NOT NULL,
    active_substance TEXT,
    atc_code TEXT,
    
    -- Form & strength
    pharmaceutical_form TEXT,
    strength TEXT,
    package_size TEXT,
    
    -- Manufacturer
    manufacturer TEXT,
    registration_holder TEXT,
    
    -- Status
    is_available BOOLEAN DEFAULT TRUE,
    requires_prescription BOOLEAN DEFAULT TRUE,
    is_narcotic BOOLEAN DEFAULT FALSE,
    
    -- Dates
    first_registration DATE,
    registration_valid_until DATE,
    
    -- SPC content (cached)
    spc_indications TEXT,
    spc_contraindications TEXT,
    spc_dosage TEXT,
    spc_interactions TEXT,
    spc_side_effects TEXT,
    spc_pregnancy TEXT,
    spc_url TEXT,
    
    -- Reimbursement (VZP)
    is_reimbursed BOOLEAN DEFAULT FALSE,
    reimbursement_group TEXT,
    max_price DECIMAL(10,2),
    patient_copay DECIMAL(10,2),
    reimbursement_conditions TEXT,
    reimbursement_valid_from DATE,
    reimbursement_valid_to DATE,
    
    -- Vector for semantic search
    embedding vector(1536),
    search_text TEXT,
    
    -- Metadata
    raw_data JSONB,
    
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    sukl_updated_at TIMESTAMPTZ  -- Last SÚKL data sync
);

-- Indexes
CREATE INDEX idx_drugs_sukl_code ON drugs(sukl_code);
CREATE INDEX idx_drugs_name ON drugs(name);
CREATE INDEX idx_drugs_active_substance ON drugs(active_substance);
CREATE INDEX idx_drugs_atc ON drugs(atc_code);
CREATE INDEX idx_drugs_available ON drugs(is_available) WHERE is_available = TRUE;
CREATE INDEX idx_drugs_reimbursed ON drugs(is_reimbursed) WHERE is_reimbursed = TRUE;

-- Vector index
CREATE INDEX idx_drugs_embedding ON drugs 
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- Full text search
CREATE INDEX idx_drugs_fts ON drugs 
USING gin(to_tsvector('simple', name || ' ' || COALESCE(active_substance, '')));

-- Trigger
CREATE TRIGGER drugs_updated_at
    BEFORE UPDATE ON drugs
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();
```

---

### Migration 008: Tabulka guidelines

```sql
-- Migration: 008_create_guidelines.sql
-- Popis: Klinické doporučené postupy

CREATE TABLE guidelines (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Identification
    external_id TEXT UNIQUE,
    
    -- Basic info
    title TEXT NOT NULL,
    organization TEXT NOT NULL,  -- ČDS, ČKS, ESC, ADA...
    
    -- Classification
    specialty TEXT,
    source_type source_type DEFAULT 'guidelines',
    is_czech BOOLEAN DEFAULT TRUE,
    
    -- Version info
    version TEXT,
    publication_year INTEGER NOT NULL,
    publication_date DATE,
    valid_until DATE,
    
    -- Authors
    authors TEXT[],
    
    -- Content
    summary TEXT,
    key_recommendations TEXT[],
    full_content TEXT,
    
    -- URLs
    url TEXT,
    pdf_url TEXT,
    
    -- Keywords for search
    keywords TEXT[],
    icd10_codes TEXT[],  -- Related diagnosis codes
    
    -- Vector for semantic search
    embedding vector(1536),
    
    -- Status
    is_current BOOLEAN DEFAULT TRUE,
    superseded_by UUID REFERENCES guidelines(id),
    
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_guidelines_org ON guidelines(organization);
CREATE INDEX idx_guidelines_specialty ON guidelines(specialty);
CREATE INDEX idx_guidelines_year ON guidelines(publication_year DESC);
CREATE INDEX idx_guidelines_czech ON guidelines(is_czech);
CREATE INDEX idx_guidelines_current ON guidelines(is_current) WHERE is_current = TRUE;
CREATE INDEX idx_guidelines_keywords ON guidelines USING gin(keywords);
CREATE INDEX idx_guidelines_icd ON guidelines USING gin(icd10_codes);

-- Vector index
CREATE INDEX idx_guidelines_embedding ON guidelines 
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- Full text search
CREATE INDEX idx_guidelines_fts ON guidelines 
USING gin(to_tsvector('simple', title || ' ' || COALESCE(summary, '')));

-- Trigger
CREATE TRIGGER guidelines_updated_at
    BEFORE UPDATE ON guidelines
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();
```

---

### Migration 009: Tabulka feedback

```sql
-- Migration: 009_create_feedback.sql
-- Popis: Zpětná vazba na odpovědi

CREATE TABLE feedback (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Foreign keys
    query_id UUID NOT NULL REFERENCES queries(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- Rating
    rating INTEGER CHECK (rating BETWEEN 1 AND 5),
    is_helpful BOOLEAN,
    
    -- Detailed feedback
    accuracy_rating INTEGER CHECK (accuracy_rating BETWEEN 1 AND 5),
    relevance_rating INTEGER CHECK (relevance_rating BETWEEN 1 AND 5),
    completeness_rating INTEGER CHECK (completeness_rating BETWEEN 1 AND 5),
    
    -- Text feedback
    comment TEXT,
    suggested_improvement TEXT,
    
    -- Issue flags
    has_incorrect_info BOOLEAN DEFAULT FALSE,
    has_missing_info BOOLEAN DEFAULT FALSE,
    has_outdated_info BOOLEAN DEFAULT FALSE,
    has_citation_issue BOOLEAN DEFAULT FALSE,
    
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Constraints
    UNIQUE(query_id, user_id)
);

-- Indexes
CREATE INDEX idx_feedback_query ON feedback(query_id);
CREATE INDEX idx_feedback_user ON feedback(user_id);
CREATE INDEX idx_feedback_rating ON feedback(rating);
CREATE INDEX idx_feedback_issues ON feedback(has_incorrect_info, has_missing_info);

-- RLS
ALTER TABLE feedback ENABLE ROW LEVEL SECURITY;

CREATE POLICY "feedback_insert_own"
ON feedback FOR INSERT
TO authenticated
WITH CHECK (
    user_id IN (
        SELECT id FROM users WHERE auth_id = (SELECT auth.uid())
    )
);

CREATE POLICY "feedback_select_own"
ON feedback FOR SELECT
TO authenticated
USING (
    user_id IN (
        SELECT id FROM users WHERE auth_id = (SELECT auth.uid())
    )
);
```

---

### Migration 010: Tabulka api_logs

```sql
-- Migration: 010_create_api_logs.sql
-- Popis: Logy API volání pro audit a monitoring

CREATE TABLE api_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Request info
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    endpoint TEXT NOT NULL,
    method TEXT NOT NULL,
    
    -- Request details
    request_body JSONB,
    query_params JSONB,
    headers JSONB,
    
    -- Response
    status_code INTEGER NOT NULL,
    response_time_ms INTEGER,
    
    -- Client info
    client_ip INET,
    user_agent TEXT,
    
    -- Error info
    error_code TEXT,
    error_message TEXT,
    
    -- Timestamp
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_api_logs_user ON api_logs(user_id);
CREATE INDEX idx_api_logs_endpoint ON api_logs(endpoint);
CREATE INDEX idx_api_logs_created ON api_logs(created_at DESC);
CREATE INDEX idx_api_logs_status ON api_logs(status_code);
CREATE INDEX idx_api_logs_errors ON api_logs(error_code) WHERE error_code IS NOT NULL;

-- Partition by month for performance (optional)
-- CREATE TABLE api_logs_2025_12 PARTITION OF api_logs
-- FOR VALUES FROM ('2025-12-01') TO ('2026-01-01');

-- No RLS - accessed only by backend service

---

### Migration 011: Tabulka price_history
```sql
-- Migration: 011_create_price_history.sql
-- Popis: Historie cen a úhrad léků (LEK-13 archiv)

CREATE TABLE price_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Drug link
    sukl_code TEXT NOT NULL REFERENCES drugs(sukl_code) ON DELETE CASCADE,
    
    -- Pricing data
    price DECIMAL(10,2),          -- Koncová cena (MFC)
    max_price DECIMAL(10,2),      -- Maximální cena
    reimbursement_base DECIMAL(10,2), -- Úhrada
    patient_copay DECIMAL(10,2),  -- Doplatek
    dispensed_count INTEGER,      -- Počet vydaných balení (Volume)
    
    -- Date info
    valid_from DATE NOT NULL,
    valid_to DATE,
    
    -- Source info
    source_file TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_price_history_sukl ON price_history(sukl_code);
CREATE INDEX idx_price_history_valid_from ON price_history(valid_from DESC);
```
```

---

## 🔍 Funkce pro vyhledávání

### Sémantické vyhledávání dokumentů

```sql
-- Function: Semantic search in documents
CREATE OR REPLACE FUNCTION search_documents(
    query_embedding vector(1536),
    match_count INTEGER DEFAULT 10,
    source_filter source_type DEFAULT NULL,
    min_similarity FLOAT DEFAULT 0.7
)
RETURNS TABLE (
    id UUID,
    source_type source_type,
    title TEXT,
    content TEXT,
    abstract TEXT,
    url TEXT,
    pmid TEXT,
    doi TEXT,
    similarity FLOAT
)
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
    RETURN QUERY
    SELECT
        d.id,
        d.source_type,
        d.title,
        d.content,
        d.abstract,
        d.url,
        d.pmid,
        d.doi,
        1 - (d.embedding <=> query_embedding) AS similarity
    FROM documents d
    WHERE 
        d.is_indexed = TRUE
        AND (source_filter IS NULL OR d.source_type = source_filter)
        AND 1 - (d.embedding <=> query_embedding) >= min_similarity
    ORDER BY d.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;
```

---

### Vyhledávání léků

```sql
-- Function: Search drugs by name or active substance
CREATE OR REPLACE FUNCTION search_drugs(
    search_query TEXT,
    match_count INTEGER DEFAULT 20,
    only_available BOOLEAN DEFAULT TRUE,
    only_reimbursed BOOLEAN DEFAULT FALSE
)
RETURNS TABLE (
    id UUID,
    sukl_code TEXT,
    name TEXT,
    active_substance TEXT,
    atc_code TEXT,
    is_available BOOLEAN,
    is_reimbursed BOOLEAN,
    patient_copay DECIMAL,
    rank FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        d.id,
        d.sukl_code,
        d.name,
        d.active_substance,
        d.atc_code,
        d.is_available,
        d.is_reimbursed,
        d.patient_copay,
        ts_rank(
            to_tsvector('simple', d.name || ' ' || COALESCE(d.active_substance, '')),
            plainto_tsquery('simple', search_query)
        ) AS rank
    FROM drugs d
    WHERE 
        to_tsvector('simple', d.name || ' ' || COALESCE(d.active_substance, '')) 
        @@ plainto_tsquery('simple', search_query)
        AND (NOT only_available OR d.is_available = TRUE)
        AND (NOT only_reimbursed OR d.is_reimbursed = TRUE)
    ORDER BY rank DESC
    LIMIT match_count;
END;
$$;
```

---

### Vyhledávání guidelines

```sql
-- Function: Search guidelines
CREATE OR REPLACE FUNCTION search_guidelines(
    query_embedding vector(1536),
    search_text TEXT DEFAULT NULL,
    match_count INTEGER DEFAULT 10,
    only_czech BOOLEAN DEFAULT FALSE,
    only_current BOOLEAN DEFAULT TRUE,
    specialty_filter TEXT DEFAULT NULL
)
RETURNS TABLE (
    id UUID,
    title TEXT,
    organization TEXT,
    publication_year INTEGER,
    summary TEXT,
    url TEXT,
    is_czech BOOLEAN,
    similarity FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        g.id,
        g.title,
        g.organization,
        g.publication_year,
        g.summary,
        g.url,
        g.is_czech,
        CASE 
            WHEN query_embedding IS NOT NULL THEN 1 - (g.embedding <=> query_embedding)
            ELSE 0.0
        END AS similarity
    FROM guidelines g
    WHERE 
        (NOT only_current OR g.is_current = TRUE)
        AND (NOT only_czech OR g.is_czech = TRUE)
        AND (specialty_filter IS NULL OR g.specialty = specialty_filter)
        AND (
            search_text IS NULL 
            OR to_tsvector('simple', g.title || ' ' || COALESCE(g.summary, '')) 
               @@ plainto_tsquery('simple', search_text)
        )
    ORDER BY 
        CASE 
            WHEN query_embedding IS NOT NULL THEN g.embedding <=> query_embedding
            ELSE 0
        END
    LIMIT match_count;
END;
$$;
```

---

## 📊 Views

### View: Statistiky dotazů uživatele

```sql
-- View: User query statistics
CREATE OR REPLACE VIEW user_query_stats AS
SELECT 
    u.id AS user_id,
    u.email,
    COUNT(q.id) AS total_queries,
    COUNT(q.id) FILTER (WHERE q.created_at > NOW() - INTERVAL '30 days') AS queries_last_30_days,
    AVG(q.processing_time_ms) AS avg_processing_time_ms,
    AVG(q.confidence_score) AS avg_confidence_score,
    COUNT(DISTINCT DATE(q.created_at)) AS active_days,
    MAX(q.created_at) AS last_query_at
FROM users u
LEFT JOIN queries q ON u.id = q.user_id AND q.deleted_at IS NULL
GROUP BY u.id, u.email;
```

---

### View: Přehled feedback

```sql
-- View: Feedback summary
CREATE OR REPLACE VIEW feedback_summary AS
SELECT 
    DATE(f.created_at) AS date,
    COUNT(*) AS total_feedback,
    AVG(f.rating) AS avg_rating,
    AVG(f.accuracy_rating) AS avg_accuracy,
    AVG(f.relevance_rating) AS avg_relevance,
    COUNT(*) FILTER (WHERE f.is_helpful = TRUE) AS helpful_count,
    COUNT(*) FILTER (WHERE f.has_incorrect_info = TRUE) AS incorrect_info_count
FROM feedback f
GROUP BY DATE(f.created_at)
ORDER BY date DESC;
```

---

## 🔒 Bezpečnostní funkce

### Anonymizace pro audit

```sql
-- Function: Anonymize user data for audit
CREATE OR REPLACE FUNCTION anonymize_user_data(user_uuid UUID)
RETURNS VOID
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
    -- Anonymize user
    UPDATE users 
    SET 
        email = 'deleted_' || user_uuid || '@anonymized.local',
        first_name = 'Deleted',
        last_name = 'User',
        license_number = NULL,
        is_active = FALSE
    WHERE id = user_uuid;
    
    -- Soft delete queries
    UPDATE queries
    SET deleted_at = NOW()
    WHERE user_id = user_uuid;
END;
$$;
```

---

## 📈 Indexy pro produkci

```sql
-- Additional production indexes

-- Composite index for user query history
CREATE INDEX CONCURRENTLY idx_queries_user_history 
ON queries(user_id, created_at DESC, status) 
WHERE deleted_at IS NULL;

-- Index for monthly usage calculation
CREATE INDEX CONCURRENTLY idx_queries_monthly 
ON queries(user_id, created_at) 
WHERE created_at > NOW() - INTERVAL '31 days';

-- Index for feedback aggregation
CREATE INDEX CONCURRENTLY idx_feedback_aggregation 
ON feedback(query_id, rating, created_at);
```

---

## 🚀 Seed Data

```sql
-- Seed: Default admin user (update with real values)
INSERT INTO users (email, first_name, last_name, role, license_verified, subscription_plan, queries_limit)
VALUES ('admin@czechmedai.cz', 'Admin', 'Czech MedAI', 'admin', TRUE, 'enterprise', 999999);

-- Seed: Sample guidelines
INSERT INTO guidelines (title, organization, publication_year, specialty, is_czech, url)
VALUES 
('Doporučené postupy pro léčbu diabetes mellitus 2. typu', 'Česká diabetologická společnost', 2023, 'diabetology', TRUE, 'https://www.diab.cz/doporucene-postupy'),
('Doporučení pro diagnostiku a léčbu arteriální hypertenze', 'Česká kardiologická společnost', 2022, 'cardiology', TRUE, 'https://www.kardio-cz.cz');
```

---

## ✅ Checklist pro produkci

- [ ] Všechny migrace aplikovány
- [ ] RLS polícy aktivní na všech tabulkách s user data
- [ ] Indexy vytvořeny
- [ ] pgvector extension aktivní
- [ ] Backup strategie nastavena
- [ ] Connection pooling nakonfigurován
- [ ] Monitoring (pg_stat_statements) aktivní

---

*Dokument vytvořen: 15.12.2025*
