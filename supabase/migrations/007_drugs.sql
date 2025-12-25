-- Migration: 007_create_drugs.sql
-- Popis: Cache SÚKL databáze léčiv

CREATE TABLE IF NOT EXISTS drugs (
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
    
    -- Metadata
    raw_data JSONB,
    
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    sukl_updated_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_drugs_sukl_code ON drugs(sukl_code);
CREATE INDEX IF NOT EXISTS idx_drugs_name ON drugs(name);
CREATE INDEX IF NOT EXISTS idx_drugs_active_substance ON drugs(active_substance);
CREATE INDEX IF NOT EXISTS idx_drugs_atc ON drugs(atc_code);
CREATE INDEX IF NOT EXISTS idx_drugs_available ON drugs(is_available) WHERE is_available = TRUE;
CREATE INDEX IF NOT EXISTS idx_drugs_reimbursed ON drugs(is_reimbursed) WHERE is_reimbursed = TRUE;

CREATE INDEX IF NOT EXISTS idx_drugs_embedding ON drugs 
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

CREATE INDEX IF NOT EXISTS idx_drugs_fts ON drugs 
USING gin(to_tsvector('simple', name || ' ' || COALESCE(active_substance, '')));

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'drugs_updated_at') THEN
        CREATE TRIGGER drugs_updated_at
            BEFORE UPDATE ON drugs
            FOR EACH ROW
            EXECUTE FUNCTION update_updated_at();
    END IF;
END $$;
