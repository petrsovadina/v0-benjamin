-- Create pricing table linked to SÚKL codes
CREATE TABLE IF NOT EXISTS public.drug_pricing (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    sukl_code TEXT NOT NULL REFERENCES public.drugs(sukl_code) ON DELETE CASCADE,
    max_price_manufacturer NUMERIC,
    reimbursement_amount NUMERIC,
    max_copayment NUMERIC,
    coverage_type TEXT, -- 'plná', 'částečná', etc.
    valid_from DATE,
    valid_to DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Ensure one pricing record per drug per validity period (optional, simplified for MVP)
    UNIQUE(sukl_code, valid_from)
);

ALTER TABLE public.drug_pricing ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow public read access pricing" ON public.drug_pricing
    FOR SELECT USING (auth.role() = 'authenticated');
