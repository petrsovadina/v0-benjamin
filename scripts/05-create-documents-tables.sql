-- Create tables for SPC (Summary of Product Characteristics) and PIL (Patient Information Leaflet)
-- Using separate tables as per README architecture, though they share structure.

CREATE TABLE IF NOT EXISTS public.spc_documents (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    sukl_code TEXT NOT NULL REFERENCES public.drugs(sukl_code) ON DELETE CASCADE,
    document_url TEXT NOT NULL,
    title TEXT,
    revision_date DATE,
    extracted_text TEXT, -- For full text search / rag
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS public.pil_documents (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    sukl_code TEXT NOT NULL REFERENCES public.drugs(sukl_code) ON DELETE CASCADE,
    document_url TEXT NOT NULL,
    title TEXT,
    revision_date DATE,
    extracted_text TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- RLS
ALTER TABLE public.spc_documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.pil_documents ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow public read access spc" ON public.spc_documents
    FOR SELECT USING (auth.role() = 'authenticated');

CREATE POLICY "Allow public read access pil" ON public.pil_documents
    FOR SELECT USING (auth.role() = 'authenticated');
