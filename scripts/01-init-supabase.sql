-- Vytvoř users profil tabulku (rozšíření Supabase auth.users)
CREATE TABLE IF NOT EXISTS public.user_profiles (
  id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL PRIMARY KEY,
  email TEXT NOT NULL,
  full_name TEXT,
  specialty TEXT,
  organization TEXT,
  profile_picture_url TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- RLS polítics pro user_profiles
ALTER TABLE public.user_profiles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own profile" ON public.user_profiles
  FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own profile" ON public.user_profiles
  FOR UPDATE USING (auth.uid() = id);

CREATE POLICY "Users can insert own profile" ON public.user_profiles
  FOR INSERT WITH CHECK (auth.uid() = id);

-- Vytvoř tabulku pro dotazy a odpovědi
CREATE TABLE IF NOT EXISTS public.queries (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
  query_text TEXT NOT NULL,
  category TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- RLS polítics pro queries
ALTER TABLE public.queries ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own queries" ON public.queries
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own queries" ON public.queries
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own queries" ON public.queries
  FOR UPDATE USING (auth.uid() = user_id);

-- Vytvoř tabulku pro odpovědi
CREATE TABLE IF NOT EXISTS public.answers (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  query_id UUID REFERENCES public.queries(id) ON DELETE CASCADE NOT NULL,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
  answer_text TEXT NOT NULL,
  citations JSONB,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- RLS polítics pro answers
ALTER TABLE public.answers ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view answers to their queries" ON public.answers
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert answers to their queries" ON public.answers
  FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Vytvoř tabulku pro VZP navigátor data
CREATE TABLE IF NOT EXISTS public.vzp_medicines (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  name TEXT NOT NULL,
  inn TEXT,
  atc_code TEXT,
  coverage_type TEXT,
  coverage_percentage NUMERIC,
  indications JSONB,
  alternatives JSONB,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Vytvoř tabulku pro uživatelské preference
CREATE TABLE IF NOT EXISTS public.user_preferences (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL UNIQUE,
  theme TEXT DEFAULT 'light',
  language TEXT DEFAULT 'cs',
  notifications_enabled BOOLEAN DEFAULT TRUE,
  email_digest BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- RLS polítics pro user_preferences
ALTER TABLE public.user_preferences ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own preferences" ON public.user_preferences
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can update own preferences" ON public.user_preferences
  FOR UPDATE USING (auth.uid() = user_id);
