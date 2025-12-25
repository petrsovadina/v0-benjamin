-- Create table for Active Substances (Léčivé látky) from SÚKL OpenData
CREATE TABLE IF NOT EXISTS active_substances (
    kod_latky VARCHAR PRIMARY KEY,
    nazev_inn VARCHAR,
    nazev_en VARCHAR,
    nazev_cs VARCHAR,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Add index on nazev_cs for faster search
CREATE INDEX IF NOT EXISTS idx_active_substances_nazev_cs ON active_substances (nazev_cs);
