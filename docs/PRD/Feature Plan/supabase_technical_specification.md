# FONS Copilot - Supabase Technical Specification

## 📋 Přehled

Tento dokument definuje kompletní technickou architekturu FONS Copilot postavenou na Supabase platformě pro MVP i budoucí fáze.

---

## 🏗️ Architektura - Celkový Pohled

```
┌─────────────────────────────────────────────────────────────┐
│              FONS Enterprise (Frontend)                      │
│              Next.js 14 + TypeScript + Tailwind              │
│              @supabase/supabase-js client                    │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                  Supabase Platform                           │
│                  (Frankfurt, EU)                             │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Supabase Auth                                        │  │
│  │  - Azure AD SSO                                       │  │
│  │  - Session management                                 │  │
│  │  - JWT tokens                                         │  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Supabase Edge Functions (Deno)                      │  │
│  │  - benjamin-query (Q&A)                               │  │
│  │  - epicrisis-generate (Dokumentace)                   │  │
│  │  - translator (Překlad)                               │  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  PostgreSQL 15 + pgvector                             │  │
│  │  - profiles                                           │  │
│  │  - ai_queries                                         │  │
│  │  - epicrisis_generations                              │  │
│  │  - knowledge_base (vector embeddings)                 │  │
│  │  - audit_logs                                         │  │
│  │  Row Level Security (RLS) policies                    │  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Supabase Storage                                     │  │
│  │  - audit_exports/                                     │  │
│  │  - user_documents/                                    │  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Supabase Realtime (Fáze 2)                          │  │
│  │  - Live query updates                                 │  │
│  │  - Notifications                                      │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              Externí AI Services                             │
│  - Anthropic Claude API (LLM)                               │
│  - HuggingFace (Embeddings)                                 │
└─────────────────────────────────────────────────────────────┘
```

---

## 💾 Database Schema (Kompletní)

### **Tabulka: profiles**
Rozšíření Supabase auth.users o health-specific metadata

```sql
CREATE TABLE public.profiles (
  id UUID REFERENCES auth.users PRIMARY KEY,
  full_name TEXT NOT NULL,
  role TEXT NOT NULL CHECK (role IN ('doctor', 'nurse', 'admin')),
  hospital_id UUID REFERENCES hospitals(id),
  specialty TEXT, -- Specializace (kardiologie, internal, praktik)
  license_number TEXT, -- Číslo licence ČLK
  department TEXT, -- Oddělení
  consent_flags JSONB DEFAULT '{}', -- GDPR souhlasy
  preferences JSONB DEFAULT '{}', -- UI preferences, language, etc.
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_profiles_hospital ON profiles(hospital_id);
CREATE INDEX idx_profiles_role ON profiles(role);

-- Row Level Security
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own profile"
  ON profiles FOR SELECT
  USING (auth.uid() = id);

CREATE POLICY "Users can update own profile"
  ON profiles FOR UPDATE
  USING (auth.uid() = id);

-- Trigger pro updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_profiles_updated_at
  BEFORE UPDATE ON profiles
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

---

### **Tabulka: hospitals**
Enterprise klienti

```sql
CREATE TABLE public.hospitals (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name TEXT NOT NULL,
  ico TEXT UNIQUE, -- IČO nemocnice
  address TEXT,
  city TEXT,
  region TEXT,
  tier TEXT NOT NULL CHECK (tier IN ('pilot', 'professional', 'enterprise')) DEFAULT 'pilot',
  max_users INTEGER, -- Limit pro enterprise
  features JSONB DEFAULT '{}', -- Feature flags
  contact_email TEXT,
  contact_phone TEXT,
  contract_start DATE,
  contract_end DATE,
  is_active BOOLEAN DEFAULT true,
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_hospitals_tier ON hospitals(tier);
CREATE INDEX idx_hospitals_active ON hospitals(is_active);

-- RLS: Pouze admins vidí hospitals
ALTER TABLE hospitals ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Admins can view hospitals"
  ON hospitals FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = auth.uid()
      AND profiles.role = 'admin'
    )
  );
```

---

### **Tabulka: ai_queries**
Benjamin klinická podpora - historie dotazů a odpovědí

```sql
CREATE TABLE public.ai_queries (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users NOT NULL,
  module TEXT NOT NULL CHECK (module IN ('benjamin', 'epicrisis', 'translator')),
  query_text TEXT NOT NULL,
  response_text TEXT,
  sources JSONB, -- [{pmid: "12345", doi: "10.xxx", url: "...", title: "...", excerpt: "..."}]
  metadata JSONB DEFAULT '{}', -- {model: "claude-sonnet-4.5", tokens: 1500, latency_ms: 2300}
  rating INTEGER CHECK (rating >= 1 AND rating <= 5), -- User feedback
  status TEXT CHECK (status IN ('pending', 'completed', 'error')) DEFAULT 'pending',
  error_message TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_ai_queries_user ON ai_queries(user_id);
CREATE INDEX idx_ai_queries_module ON ai_queries(module);
CREATE INDEX idx_ai_queries_created ON ai_queries(created_at DESC);

-- Row Level Security
ALTER TABLE ai_queries ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users view own queries"
  ON ai_queries FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users insert own queries"
  ON ai_queries FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users update own queries rating"
  ON ai_queries FOR UPDATE
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);
```

---

### **Tabulka: epicrisis_generations**
Generované epikrízy

```sql
CREATE TABLE public.epicrisis_generations (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users NOT NULL,
  patient_id TEXT NOT NULL, -- ID z FONS Enterprise
  patient_name TEXT, -- Pro zobrazení (hashed/anonymized pro audit)
  hospitalization_id TEXT, -- ID hospitalizace z FONS
  input_data JSONB NOT NULL, -- {medical_reports: [...], lab_results: [...], medications: [...]}
  generated_text TEXT,
  version INTEGER DEFAULT 1, -- Pro "Generovat jinak"
  parent_id UUID REFERENCES epicrisis_generations(id), -- Link na původní verzi
  status TEXT CHECK (status IN ('pending', 'completed', 'error', 'edited')) DEFAULT 'pending',
  error_message TEXT,
  metadata JSONB DEFAULT '{}', -- {model, tokens, sources_count}
  is_final BOOLEAN DEFAULT false, -- Lékař potvrdil finální verzi
  finalized_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_epicrisis_user ON epicrisis_generations(user_id);
CREATE INDEX idx_epicrisis_patient ON epicrisis_generations(patient_id);
CREATE INDEX idx_epicrisis_created ON epicrisis_generations(created_at DESC);
CREATE INDEX idx_epicrisis_parent ON epicrisis_generations(parent_id) WHERE parent_id IS NOT NULL;

-- Row Level Security
ALTER TABLE epicrisis_generations ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users view own epicrisis"
  ON epicrisis_generations FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users insert own epicrisis"
  ON epicrisis_generations FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users update own epicrisis"
  ON epicrisis_generations FOR UPDATE
  USING (auth.uid() = user_id);
```

---

### **Tabulka: knowledge_base**
Vector embeddings pro RAG

```sql
-- Nejdříve enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE public.knowledge_base (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  source TEXT NOT NULL, -- 'pubmed', 'sukl', 'cls_jep', 'cochrane'
  source_id TEXT, -- PMID, DOI, SÚKL kód, etc.
  title TEXT NOT NULL,
  content TEXT NOT NULL,
  abstract TEXT, -- Kratší verze pro rychlé zobrazení
  metadata JSONB DEFAULT '{}',
  -- {
  --   authors: [...],
  --   publication_date: "2024-01-15",
  --   journal: "...",
  --   language: "cs/en",
  --   medical_specialty: "cardiology"
  -- }
  embedding vector(1024), -- Embedding dimension (depends on model)
  is_active BOOLEAN DEFAULT true, -- Pro soft delete
  version INTEGER DEFAULT 1,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_knowledge_source ON knowledge_base(source);
CREATE INDEX idx_knowledge_source_id ON knowledge_base(source_id);
CREATE INDEX idx_knowledge_active ON knowledge_base(is_active) WHERE is_active = true;

-- Vector similarity search index (IVFFlat)
CREATE INDEX ON knowledge_base
  USING ivfflat (embedding vector_cosine_ops)
  WITH (lists = 100);

-- Full-text search index (pro hybrid search)
CREATE INDEX idx_knowledge_content_fts ON knowledge_base
  USING gin(to_tsvector('simple', content));

-- RLS: Všichni authenticated users mohou číst
ALTER TABLE knowledge_base ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Authenticated users can read knowledge"
  ON knowledge_base FOR SELECT
  USING (auth.role() = 'authenticated' AND is_active = true);

-- Pouze admins mohou upravovat
CREATE POLICY "Admins can manage knowledge"
  ON knowledge_base FOR ALL
  USING (
    EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = auth.uid()
      AND profiles.role = 'admin'
    )
  );
```

---

### **Tabulka: audit_logs**
Kompletní audit trail

```sql
CREATE TABLE public.audit_logs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users NOT NULL,
  action TEXT NOT NULL, -- 'query', 'epicrisis_generate', 'translate', 'login', 'export'
  module TEXT, -- 'benjamin', 'epicrisis', 'translator'
  resource_type TEXT, -- 'ai_query', 'epicrisis', 'profile'
  resource_id UUID, -- ID dotčeného záznamu
  details JSONB DEFAULT '{}', -- Další metadata specifická pro akci
  ip_address INET,
  user_agent TEXT,
  success BOOLEAN DEFAULT true,
  error_message TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_audit_user ON audit_logs(user_id);
CREATE INDEX idx_audit_action ON audit_logs(action);
CREATE INDEX idx_audit_created ON audit_logs(created_at DESC);
CREATE INDEX idx_audit_resource ON audit_logs(resource_type, resource_id);

-- RLS: Pouze admins vidí vše, users vidí svoje
ALTER TABLE audit_logs ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users view own audit logs"
  ON audit_logs FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Admins view all audit logs"
  ON audit_logs FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM profiles
      WHERE profiles.id = auth.uid()
      AND profiles.role = 'admin'
    )
  );

-- Pouze system může vkládat
CREATE POLICY "Service role can insert audit logs"
  ON audit_logs FOR INSERT
  WITH CHECK (auth.jwt()->>'role' = 'service_role');
```

---

### **Postgres Functions: Vector Search**

```sql
-- Function pro similarity search
CREATE OR REPLACE FUNCTION match_documents(
  query_embedding vector(1024),
  match_threshold float DEFAULT 0.7,
  match_count int DEFAULT 10
)
RETURNS TABLE (
  id uuid,
  source text,
  source_id text,
  title text,
  content text,
  abstract text,
  metadata jsonb,
  similarity float
)
LANGUAGE sql STABLE
AS $$
  SELECT
    knowledge_base.id,
    knowledge_base.source,
    knowledge_base.source_id,
    knowledge_base.title,
    knowledge_base.content,
    knowledge_base.abstract,
    knowledge_base.metadata,
    1 - (knowledge_base.embedding <=> query_embedding) AS similarity
  FROM knowledge_base
  WHERE
    knowledge_base.is_active = true
    AND 1 - (knowledge_base.embedding <=> query_embedding) > match_threshold
  ORDER BY knowledge_base.embedding <=> query_embedding
  LIMIT match_count;
$$;

-- Function pro hybrid search (vector + full-text)
CREATE OR REPLACE FUNCTION hybrid_search(
  query_text text,
  query_embedding vector(1024),
  match_count int DEFAULT 10
)
RETURNS TABLE (
  id uuid,
  source text,
  title text,
  content text,
  similarity float,
  rank float
)
LANGUAGE sql STABLE
AS $$
  WITH vector_search AS (
    SELECT
      id,
      source,
      title,
      content,
      1 - (embedding <=> query_embedding) AS similarity
    FROM knowledge_base
    WHERE is_active = true
    ORDER BY embedding <=> query_embedding
    LIMIT match_count * 2
  ),
  text_search AS (
    SELECT
      id,
      ts_rank(to_tsvector('simple', content), plainto_tsquery('simple', query_text)) AS rank
    FROM knowledge_base
    WHERE
      is_active = true
      AND to_tsvector('simple', content) @@ plainto_tsquery('simple', query_text)
  )
  SELECT
    v.id,
    v.source,
    v.title,
    v.content,
    v.similarity,
    COALESCE(t.rank, 0) AS rank
  FROM vector_search v
  LEFT JOIN text_search t ON v.id = t.id
  ORDER BY (v.similarity * 0.7 + COALESCE(t.rank, 0) * 0.3) DESC
  LIMIT match_count;
$$;
```

---

## ⚡ Supabase Edge Functions

### **Struktura Projektu**

```
supabase/
├── config.toml
├── migrations/
│   └── 20250120000000_initial_schema.sql
└── functions/
    ├── _shared/
    │   ├── anthropic-client.ts
    │   ├── supabase-client.ts
    │   ├── embeddings.ts
    │   ├── rag.ts
    │   └── types.ts
    ├── benjamin-query/
    │   └── index.ts
    ├── epicrisis-generate/
    │   └── index.ts
    └── translator/
        └── index.ts
```

### **1. Benjamin Query Edge Function**

```typescript
// supabase/functions/benjamin-query/index.ts

import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { createClient } from "https://esm.sh/@supabase/supabase-js@2"
import Anthropic from "https://esm.sh/@anthropic-ai/sdk@0.20.0"
import { corsHeaders } from "../_shared/cors.ts"
import { getEmbedding } from "../_shared/embeddings.ts"

interface BenjaminRequest {
  query: string
}

serve(async (req) => {
  // Handle CORS
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  try {
    const startTime = Date.now()

    // 1. Ověření autentizace
    const authHeader = req.headers.get('Authorization')
    if (!authHeader) {
      throw new Error('Missing authorization header')
    }

    const supabase = createClient(
      Deno.env.get('SUPABASE_URL')!,
      Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!,
      {
        global: { headers: { Authorization: authHeader } }
      }
    )

    const { data: { user }, error: authError } = await supabase.auth.getUser()
    if (authError || !user) {
      throw new Error('Unauthorized')
    }

    // 2. Parse request
    const { query }: BenjaminRequest = await req.json()
    if (!query || query.trim().length === 0) {
      throw new Error('Query is required')
    }

    // 3. Získat embedding pro dotaz
    const queryEmbedding = await getEmbedding(query)

    // 4. Vector search v knowledge base
    const { data: relevantDocs, error: searchError } = await supabase
      .rpc('match_documents', {
        query_embedding: queryEmbedding,
        match_threshold: 0.75,
        match_count: 10
      })

    if (searchError) {
      console.error('Search error:', searchError)
      throw new Error('Failed to search knowledge base')
    }

    // 5. Sestavit prompt s kontextem
    const context = relevantDocs
      .map((doc: any, idx: number) =>
        `[${idx + 1}] ${doc.title}\nZdroj: ${doc.source} (${doc.source_id || 'N/A'})\n${doc.abstract || doc.content.substring(0, 500)}...\n`
      )
      .join('\n---\n')

    const systemPrompt = `Jsi zkušený lékař a klinický asistent pro české lékaře.
Tvým úkolem je poskytnout přesnou, evidence-based odpověď na klinický dotaz lékaře.

PRAVIDLA:
1. Odpověz POUZE na základě poskytnutých zdrojů níže
2. Každé tvrzení MUSÍ mít inline citaci ve formátu [číslo]
3. Odpověď musí být stručná (3-5 vět)
4. Pokud informace není v zdrojích, řekni "Nenašel jsem relevantní informaci v databázi"
5. Neposkytuj diagnostiku ani terapeutická doporučení, pouze informace
6. Odpovídej v češtině

DOSTUPNÉ ZDROJE:
${context}`

    // 6. Zavolat Claude API
    const anthropic = new Anthropic({
      apiKey: Deno.env.get('ANTHROPIC_API_KEY')!
    })

    const message = await anthropic.messages.create({
      model: 'claude-sonnet-4-20250514',
      max_tokens: 2000,
      temperature: 0.3,
      system: systemPrompt,
      messages: [{
        role: 'user',
        content: query
      }]
    })

    const responseText = message.content[0].type === 'text'
      ? message.content[0].text
      : ''

    // 7. Extrahovat citace a mapovat na zdroje
    const citationRegex = /\[(\d+)\]/g
    const citations = new Set<number>()
    let match
    while ((match = citationRegex.exec(responseText)) !== null) {
      citations.add(parseInt(match[1]))
    }

    const sources = Array.from(citations)
      .map(idx => relevantDocs[idx - 1])
      .filter(Boolean)
      .map(doc => ({
        pmid: doc.source_id,
        doi: doc.metadata?.doi,
        url: doc.metadata?.url,
        title: doc.title,
        source: doc.source,
        excerpt: doc.abstract || doc.content.substring(0, 200)
      }))

    const latencyMs = Date.now() - startTime

    // 8. Uložit do ai_queries
    const { error: insertError } = await supabase
      .from('ai_queries')
      .insert({
        user_id: user.id,
        module: 'benjamin',
        query_text: query,
        response_text: responseText,
        sources: sources,
        status: 'completed',
        metadata: {
          model: 'claude-sonnet-4.5',
          input_tokens: message.usage.input_tokens,
          output_tokens: message.usage.output_tokens,
          latency_ms: latencyMs
        }
      })

    if (insertError) {
      console.error('Insert error:', insertError)
    }

    // 9. Audit log
    await supabase.from('audit_logs').insert({
      user_id: user.id,
      action: 'query',
      module: 'benjamin',
      details: {
        query_length: query.length,
        sources_count: sources.length,
        latency_ms: latencyMs
      },
      ip_address: req.headers.get('x-forwarded-for'),
      user_agent: req.headers.get('user-agent')
    })

    // 10. Vrátit odpověď
    return new Response(
      JSON.stringify({
        answer: responseText,
        sources: sources,
        metadata: {
          latency_ms: latencyMs,
          tokens: message.usage.input_tokens + message.usage.output_tokens
        }
      }),
      {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        status: 200
      }
    )

  } catch (error) {
    console.error('Benjamin query error:', error)

    return new Response(
      JSON.stringify({
        error: error.message || 'Internal server error'
      }),
      {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        status: 500
      }
    )
  }
})
```

---

### **2. Epicrisis Generate Edge Function**

```typescript
// supabase/functions/epicrisis-generate/index.ts

import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { createClient } from "https://esm.sh/@supabase/supabase-js@2"
import Anthropic from "https://esm.sh/@anthropic-ai/sdk@0.20.0"
import { corsHeaders } from "../_shared/cors.ts"

interface EpicrisisRequest {
  patientId: string
  patientName?: string
  hospitalizationId?: string
  inputData: {
    medicalReports: Array<{
      date: string
      type: string
      content: string
      author: string
    }>
    labResults: Array<{
      date: string
      testName: string
      value: string
      unit: string
      isAbnormal: boolean
    }>
    medications: Array<{
      drugName: string
      dosage: string
      frequency: string
      startDate: string
    }>
  }
}

serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  try {
    const startTime = Date.now()

    // 1. Auth
    const authHeader = req.headers.get('Authorization')
    const supabase = createClient(
      Deno.env.get('SUPABASE_URL')!,
      Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!,
      { global: { headers: { Authorization: authHeader! } } }
    )

    const { data: { user }, error: authError } = await supabase.auth.getUser()
    if (authError || !user) {
      throw new Error('Unauthorized')
    }

    // 2. Parse request
    const requestData: EpicrisisRequest = await req.json()
    const { patientId, inputData } = requestData

    // 3. Vytvořit záznam (pending)
    const { data: epicrisisRecord, error: createError } = await supabase
      .from('epicrisis_generations')
      .insert({
        user_id: user.id,
        patient_id: patientId,
        patient_name: requestData.patientName,
        hospitalization_id: requestData.hospitalizationId,
        input_data: inputData,
        status: 'pending'
      })
      .select()
      .single()

    if (createError) {
      throw new Error(`Failed to create epicrisis record: ${createError.message}`)
    }

    // 4. Připravit prompt
    const systemPrompt = `Jsi zkušený lékař, specialista na tvorbu zdravotnické dokumentace.
Tvým úkolem je vytvořit strukturovanou epikrízu na základě poskytnutých informací o pacientovi.

STRUKTURA EPIKRÍZY (MVP - Epikríza 0.1):
1. Klinický přehled pacienta
2. Hlavní klinické nálezy
3. Významné laboratorní výsledky (zejména patologické)
4. Aplikovaná medikace
5. Doporučení pro další péči

PRAVIDLA:
- Buď stručný ale kompletní
- Zdůrazni abnormální hodnoty
- Používej odbornou terminologii
- Odpovídej POUZE v češtině
- Dodržuj strukturu výše`

    const userPrompt = `LÉKAŘSKÉ ZPRÁVY:
${inputData.medicalReports.map(r =>
  `${r.date} (${r.type}) - ${r.author}:\n${r.content}`
).join('\n\n')}

LABORATORNÍ VÝSLEDKY:
${inputData.labResults.map(l =>
  `${l.date}: ${l.testName} = ${l.value} ${l.unit} ${l.isAbnormal ? '⚠️ ABNORMÁLNÍ' : ''}`
).join('\n')}

MEDIKACE:
${inputData.medications.map(m =>
  `${m.drugName} ${m.dosage} ${m.frequency} (od ${m.startDate})`
).join('\n')}

Vytvoř strukturovanou epikrízu podle výše uvedených pravidel.`

    // 5. Claude API call
    const anthropic = new Anthropic({
      apiKey: Deno.env.get('ANTHROPIC_API_KEY')!
    })

    const message = await anthropic.messages.create({
      model: 'claude-sonnet-4-20250514',
      max_tokens: 4000,
      temperature: 0.5,
      system: systemPrompt,
      messages: [{ role: 'user', content: userPrompt }]
    })

    const generatedText = message.content[0].type === 'text'
      ? message.content[0].text
      : ''

    const latencyMs = Date.now() - startTime

    // 6. Update record
    const { error: updateError } = await supabase
      .from('epicrisis_generations')
      .update({
        generated_text: generatedText,
        status: 'completed',
        metadata: {
          model: 'claude-sonnet-4.5',
          input_tokens: message.usage.input_tokens,
          output_tokens: message.usage.output_tokens,
          latency_ms: latencyMs,
          sources_count: {
            medical_reports: inputData.medicalReports.length,
            lab_results: inputData.labResults.length,
            medications: inputData.medications.length
          }
        }
      })
      .eq('id', epicrisisRecord.id)

    if (updateError) {
      console.error('Update error:', updateError)
    }

    // 7. Audit log
    await supabase.from('audit_logs').insert({
      user_id: user.id,
      action: 'epicrisis_generate',
      module: 'epicrisis',
      resource_type: 'epicrisis',
      resource_id: epicrisisRecord.id,
      details: {
        patient_id: patientId,
        latency_ms: latencyMs
      },
      ip_address: req.headers.get('x-forwarded-for'),
      user_agent: req.headers.get('user-agent')
    })

    // 8. Response
    return new Response(
      JSON.stringify({
        id: epicrisisRecord.id,
        text: generatedText,
        metadata: {
          latency_ms: latencyMs,
          tokens: message.usage.input_tokens + message.usage.output_tokens
        }
      }),
      {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        status: 200
      }
    )

  } catch (error) {
    console.error('Epicrisis generation error:', error)

    return new Response(
      JSON.stringify({ error: error.message }),
      {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        status: 500
      }
    )
  }
})
```

---

## 🔐 Supabase Auth Configuration

### **config.toml**

```toml
[auth]
site_url = "https://fons-copilot.yourdomain.com"
additional_redirect_urls = ["http://localhost:3000"]
jwt_expiry = 3600 # 1 hour
enable_signup = false # Only admins can create users
enable_confirmations = true

[auth.email]
enable_signup = false
double_confirm_changes = true
enable_confirmations = true

[auth.external.azure]
enabled = true
client_id = "env(AZURE_CLIENT_ID)"
secret = "env(AZURE_CLIENT_SECRET)"
tenant = "env(AZURE_TENANT_ID)"
redirect_uri = "https://your-project.supabase.co/auth/v1/callback"

[auth.security]
session_timeout = 3600 # 1 hour
refresh_token_rotation_enabled = true
```

### **Frontend Auth Example (Next.js)**

```typescript
// lib/supabase-client.ts
import { createClientComponentClient } from '@supabase/auth-helpers-nextjs'

export const supabase = createClientComponentClient()

// Login with Azure AD
export async function loginWithAzure() {
  const { data, error } = await supabase.auth.signInWithOAuth({
    provider: 'azure',
    options: {
      scopes: 'email openid profile',
      redirectTo: `${window.location.origin}/auth/callback`
    }
  })

  if (error) {
    console.error('Login error:', error)
    return { error }
  }

  return { data }
}

// Get current session
export async function getSession() {
  const { data: { session }, error } = await supabase.auth.getSession()
  return { session, error }
}

// Logout
export async function logout() {
  const { error } = await supabase.auth.signOut()
  return { error }
}
```

---

## 📊 Monitoring & Observability

### **Supabase Dashboard Metrics**

**Built-in Metrics:**
- Database performance
- API requests/sec
- Edge Function invocations
- Storage usage
- Auth active users

### **Custom Metrics (Fáze 2)**

```sql
-- Views pro analytics

CREATE VIEW analytics_daily_usage AS
SELECT
  DATE(created_at) AS date,
  module,
  COUNT(*) AS query_count,
  AVG((metadata->>'latency_ms')::float) AS avg_latency_ms,
  AVG((metadata->>'tokens')::integer) AS avg_tokens
FROM ai_queries
WHERE status = 'completed'
GROUP BY DATE(created_at), module
ORDER BY date DESC;

CREATE VIEW analytics_user_retention AS
WITH first_usage AS (
  SELECT
    user_id,
    MIN(DATE(created_at)) AS first_date
  FROM ai_queries
  GROUP BY user_id
),
cohorts AS (
  SELECT
    f.first_date AS cohort_date,
    DATE(q.created_at) AS activity_date,
    COUNT(DISTINCT q.user_id) AS active_users
  FROM first_usage f
  JOIN ai_queries q ON f.user_id = q.user_id
  GROUP BY f.first_date, DATE(q.created_at)
)
SELECT
  cohort_date,
  activity_date,
  active_users,
  EXTRACT(DAY FROM activity_date - cohort_date) AS days_since_first
FROM cohorts
ORDER BY cohort_date DESC, activity_date DESC;
```

---

## 💰 Cost Optimization

### **Supabase Pricing Tiers**

| Tier | Price/month | Database | Bandwidth | Edge Functions | Auth MAU |
|------|-------------|----------|-----------|----------------|----------|
| **Free** | $0 | 500 MB | 5 GB | 500K | 50K |
| **Pro** | $25 | 8 GB | 250 GB | 2M | 100K |
| **Team** | $99 | 50 GB | 500 GB | 5M | 250K |
| **Enterprise** | Custom | Custom | Custom | Custom | Custom |

### **MVP Recommendation: Pro ($25/měsíc)**

**Odhadované Náklady MVP (50 users):**
- Supabase Pro: $25/měsíc
- Anthropic Claude API: ~$500-1000/měsíc (50 users × 10 queries/day × $0.03/1K tokens)
- **Total: ~$525-1025/měsíc**

### **Scaling (500 users):**
- Supabase Team: $99/měsíc
- Anthropic API: ~$5000/měsíc
- **Total: ~$5099/měsíc**

---

## 🚀 Deployment Strategy

### **MVP Deployment Checklist**

1. ✅ Supabase projekt setup (Frankfurt region)
2. ✅ Database migrations (`supabase db push`)
3. ✅ RLS policies testování
4. ✅ Edge Functions deployment
5. ✅ Azure AD SSO konfigurace
6. ✅ Environment variables (ANTHROPIC_API_KEY)
7. ✅ Frontend deployment (Vercel/Netlify)
8. ✅ DNS + SSL certifikáty
9. ✅ Monitoring alerts setup
10. ✅ Backup schedule verification

### **Deployment Commands**

```bash
# 1. Initialize Supabase project
supabase init

# 2. Link to remote project
supabase link --project-ref your-project-ref

# 3. Push database migrations
supabase db push

# 4. Deploy Edge Functions
supabase functions deploy benjamin-query
supabase functions deploy epicrisis-generate
supabase functions deploy translator

# 5. Set secrets
supabase secrets set ANTHROPIC_API_KEY=sk-ant-...
supabase secrets set AZURE_CLIENT_ID=...
supabase secrets set AZURE_CLIENT_SECRET=...
supabase secrets set AZURE_TENANT_ID=...
```

---

## 📝 Shrnutí Výhod Supabase Pro FONS Copilot

### **Technické Výhody**

✅ **PostgreSQL + pgvector** - Žádná extra služba pro vector search
✅ **Row Level Security** - GDPR compliance out-of-the-box
✅ **Edge Functions** - Serverless AI processing bez vendor lock-in
✅ **Built-in Auth** - Azure AD SSO, 2FA ready
✅ **Real-time** - Live updates zdarma (Fáze 2)
✅ **EU Hosting** - Frankfurt datacenter (GDPR)

### **Business Výhody**

💰 **Úspora ~$500/měsíc** (Pinecone + Auth0 + Redis)
⚡ **Rychlejší vývoj** - 4-5 týdnů úspory (auth, RLS, API)
🔐 **Bezpečnost** - Security by default (RLS, encryption)
📊 **Observability** - Dashboard + metrics built-in
🚀 **Scalabilita** - Automatic scaling edge functions

---

**Konec Technické Specifikace**
