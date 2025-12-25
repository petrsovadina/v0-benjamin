-- Create table for Price History (Historie cen) from LEK-13
CREATE TABLE IF NOT EXISTS price_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sukl_code VARCHAR NOT NULL,
    max_price_manufacturer NUMERIC, -- Nákupní cena bez DPH
    max_copayment NUMERIC, -- Doplatek
    reimbursement_amount NUMERIC, -- Úhrada
    coverage_type VARCHAR, -- Typ úhrady (Hrazeno/Nehrazeno)
    is_reimbursed BOOLEAN,
    valid_from DATE, -- Období (např. 2024-01-01)
    source_file VARCHAR,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index for fast lookup by drug and date
CREATE INDEX IF NOT EXISTS idx_price_history_sukl_code ON price_history (sukl_code);
CREATE INDEX IF NOT EXISTS idx_price_history_valid_from ON price_history (valid_from);
