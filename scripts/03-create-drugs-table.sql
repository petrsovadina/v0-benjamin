-- Create drugs table to match SÚKL DLP data structure
CREATE TABLE IF NOT EXISTS public.drugs (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    sukl_code TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    name_normalized TEXT,
    active_substance TEXT,
    atc_code TEXT,
    strength TEXT,
    pharmaceutical_form TEXT,
    package_size TEXT,
    registration_holder TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE public.drugs ENABLE ROW LEVEL SECURITY;

-- Allow read access to authenticated users
CREATE POLICY "Allow public read access" ON public.drugs
    FOR SELECT USING (auth.role() = 'authenticated');

-- Allow write access only to service role (backend pipeline)
-- Note: Service role bypasses RLS, so no specific policy needed for insert/update if using service key.
