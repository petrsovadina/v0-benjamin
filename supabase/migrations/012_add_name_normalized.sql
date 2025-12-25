-- Migration: 012_add_name_normalized.sql
-- Description: Adds name_normalized column to drugs table for case-insensitive search

ALTER TABLE drugs
ADD COLUMN IF NOT EXISTS name_normalized TEXT;

CREATE INDEX IF NOT EXISTS idx_drugs_name_normalized ON drugs(name_normalized);

-- Backfill from name if possible (simple lowercase)
UPDATE drugs SET name_normalized = LOWER(trim(name)) WHERE name_normalized IS NULL;
