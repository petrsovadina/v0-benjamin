# Benjamin - VZP Navigator Technical Specification

**Feature:** VZP Navigator - Automatická kontrola VZP úhrad léků

**Owner:** Backend Team + MCP Integration Team

**Priority:** MUST HAVE (Fáze 2, Q3 2026)

**Dependencies:** Supabase PostgreSQL, MCP Framework, SÚKL integration

---

## Executive Summary

VZP Navigator je MCP tool, který poskytuje real-time informace o VZP hrazení léků přímo v Benjamin Chat odpovědích. Technická implementace zahrnuje:
1. **Data ingestion pipeline** - Měsíční import VZP Seznam kategorizovaných LP
2. **MCP Tool API** - Query interface pro AI asistenta
3. **Caching layer** - Supabase database pro rychlý přístup
4. **Fallback mechanismy** - Handling stale data, missing drugs, API errors

**Estimated Effort:** 2 měsíce (1 senior backend dev + 1 MCP specialist)

---

## System Architecture

### High-Level Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│ ZDROJE DAT                                                    │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│ 1. VZP Seznam kategorizovaných LP (měsíční aktualizace)     │
│    • URL: https://www.vzp.cz/poskytovatele/               │
│           ciselniky/seznam-kategorizovanych-lecivych-pripravku│
│    • Format: Excel (.xlsx) nebo CSV                          │
│    • Velikost: ~50,000 záznamů                               │
│                                                               │
│ 2. SÚKL Databáze léků (týdenní aktualizace)                 │
│    • API: https://www.sukl.cz/sukl/data-api                 │
│    • Format: JSON API                                        │
│    • Propojení: SÚKL kód → VZP úhrada                       │
│                                                               │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ DATA INGESTION PIPELINE (Supabase Edge Function - Cron)     │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│ Měsíční job: parse_vzp_data()                                │
│ • Stáhne VZP Excel/CSV soubor                                │
│ • Parsuje jednotlivé řádky (název léku, ATC, kód, cena)     │
│ • Normalizuje názvy léků (empagliflozin vs Empagliflozin)   │
│ • Cross-reference s SÚKL API (validace)                     │
│ • Upsert do Supabase tabulky `vzp_reimbursement`            │
│                                                               │
│ Output: ~50,000 záznamů v PostgreSQL                         │
│                                                               │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ SUPABASE DATABASE (PostgreSQL + pgvector)                    │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│ Tabulky:                                                      │
│ • vzp_reimbursement (50K rows) - hlavní data                │
│ • vzp_update_log (audit trail) - kdy proběhla aktualizace   │
│ • vzp_query_cache (100K rows) - cached AI queries           │
│                                                               │
│ Indexy:                                                       │
│ • drug_name (B-tree) - rychlé vyhledávání                   │
│ • atc_code (B-tree) - group lookup                          │
│ • drug_name_vector (GiST) - fuzzy search                    │
│                                                               │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ MCP TOOL: VZP Navigator                                      │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│ Tool Name: get_vzp_reimbursement                             │
│                                                               │
│ Input Parameters:                                             │
│ • drug_name: string (required)                               │
│ • indication_icd10: string (optional) - "E11", "I50", etc.  │
│ • compare_alternatives: boolean (optional) - price compare   │
│                                                               │
│ Funkce:                                                       │
│ 1. Normalize drug_name (lowercase, remove diacritics)       │
│ 2. Query Supabase:                                           │
│    SELECT * FROM vzp_reimbursement WHERE drug_name ILIKE ... │
│ 3. Pokud indication_icd10 → filtruj podle indikací          │
│ 4. Pokud compare_alternatives → najdi ATC skupinu, srovnej  │
│ 5. Formátuj JSON response pro AI                            │
│                                                               │
│ Output: JSON structured data (viz API Contract níže)        │
│                                                               │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ CLAUDE AI (Sonnet 4.5)                                       │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│ • Přijme user query: "Je empagliflozin hrazený VZP?"        │
│ • Detekuje potřebu VZP dat (keyword: "hrazený", "VZP", "cena")│
│ • Zavolá MCP tool get_vzp_reimbursement()                    │
│ • Obdrží JSON response                                       │
│ • Syntetizuje natural language odpověď + strukturovanou card│
│                                                               │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ BENJAMIN FRONTEND (React)                                    │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│ • Renderuje Benjamin response s VZP Info Card               │
│ • Zobrazuje structured data (hrazení, doplatek, kódy)       │
│ • Interactive buttons (žádost o IU, price comparison)       │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## Database Schema (Supabase PostgreSQL)

### Tabulka: `vzp_reimbursement`

```sql
CREATE TABLE vzp_reimbursement (
  -- Primary Key
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

  -- Drug Identification
  drug_name TEXT NOT NULL,                  -- "Empagliflozin"
  drug_name_normalized TEXT NOT NULL,       -- "empagliflozin" (lowercase, no diacritics)
  brand_names TEXT[],                       -- ["Jardiance", "Empaglif"]
  atc_code TEXT,                            -- "A10BK03"
  sukl_code TEXT,                           -- "0123456" (SÚKL registrace)

  -- Reimbursement Status
  reimbursement_status TEXT NOT NULL,       -- 'reimbursed', 'not_reimbursed', 'conditional', 'off_label'
  copay_czk INTEGER,                        -- 30 (doplatek pacienta v Kč)
  full_price_czk INTEGER,                   -- 850 (plná cena léku měsíčně)
  reimbursement_percentage INTEGER,         -- 100 (procento úhrady VZP: 100%, 50%, 0%)

  -- Prescribing Information
  restriction_code TEXT,                    -- "H013" (Endokrinologie/Internista)
  restriction_description TEXT,             -- "Předepisuje endokrinolog nebo internista"
  indication_icd10 TEXT[],                  -- ["E11"] (diabetes 2. typu)
  indication_description TEXT,              -- "Diabetes mellitus 2. typu"

  -- Conditions for Reimbursement
  conditions TEXT,                          -- "HbA1c ≥ 53 mmol/mol po selhání metforminu"
  contraindications TEXT,                   -- "GFR < 30 ml/min"
  prior_authorization_required BOOLEAN DEFAULT FALSE,  -- Vyžaduje předchozí souhlas?

  -- Special Notes
  off_label_note TEXT,                      -- "Pro srdeční selhání nutná žádost o IU"
  iu_success_rate INTEGER,                  -- 60 (% úspěšnosti žádostí o IU)
  alternative_drugs TEXT[],                 -- ["dapagliflozin", "canagliflozin"]

  -- Data Provenance
  last_updated TIMESTAMP NOT NULL DEFAULT NOW(),  -- Poslední aktualizace VZP dat
  source_url TEXT,                          -- "https://www.vzp.cz/..."
  data_version TEXT,                        -- "2025-01" (měsíc/rok VZP publikace)

  -- Metadata
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),

  -- Full-text search vector
  drug_search_vector tsvector GENERATED ALWAYS AS (
    to_tsvector('czech', drug_name || ' ' || COALESCE(array_to_string(brand_names, ' '), ''))
  ) STORED
);

-- Indexes for fast lookups
CREATE INDEX idx_drug_name ON vzp_reimbursement (drug_name_normalized);
CREATE INDEX idx_atc_code ON vzp_reimbursement (atc_code);
CREATE INDEX idx_reimbursement_status ON vzp_reimbursement (reimbursement_status);
CREATE INDEX idx_drug_search_vector ON vzp_reimbursement USING GIN (drug_search_vector);

-- Row Level Security (RLS)
ALTER TABLE vzp_reimbursement ENABLE ROW LEVEL SECURITY;

-- Policy: VZP data jsou veřejně čitelná (read-only pro všechny uživatele)
CREATE POLICY "VZP data jsou veřejně čitelná"
ON vzp_reimbursement FOR SELECT
USING (true);
```

### Tabulka: `vzp_update_log`

```sql
CREATE TABLE vzp_update_log (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  update_started_at TIMESTAMP NOT NULL,
  update_completed_at TIMESTAMP,
  records_processed INTEGER,
  records_inserted INTEGER,
  records_updated INTEGER,
  errors_count INTEGER,
  error_log TEXT,
  data_version TEXT,                        -- "2025-01"
  source_file_url TEXT,
  status TEXT,                              -- 'in_progress', 'completed', 'failed'
  created_at TIMESTAMP DEFAULT NOW()
);
```

### Tabulka: `vzp_query_cache`

```sql
CREATE TABLE vzp_query_cache (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_query TEXT NOT NULL,                 -- "Je empagliflozin hrazený VZP?"
  normalized_query TEXT NOT NULL,           -- "empagliflozin hrazení"
  mcp_response JSONB NOT NULL,              -- Cached MCP tool response
  hit_count INTEGER DEFAULT 1,              -- Kolikrát byla tato query použita
  last_accessed_at TIMESTAMP DEFAULT NOW(),
  created_at TIMESTAMP DEFAULT NOW(),
  expires_at TIMESTAMP DEFAULT (NOW() + INTERVAL '30 days')
);

-- Index pro rychlé vyhledání cached queries
CREATE INDEX idx_normalized_query ON vzp_query_cache (normalized_query);
CREATE INDEX idx_expires_at ON vzp_query_cache (expires_at);
```

---

## MCP Tool API Contract

### Tool Definition

```json
{
  "name": "get_vzp_reimbursement",
  "description": "Získá informace o VZP úhradě léků pro České zdravotnictví. Vrací status hrazení, doplatek pacienta, prescribing codes, podmínky úhrady a alternativní léky.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "drug_name": {
        "type": "string",
        "description": "Název léku (generický nebo obchodní), např. 'empagliflozin' nebo 'Jardiance'"
      },
      "indication_icd10": {
        "type": "string",
        "description": "ICD-10 kód indikace (volitelný), např. 'E11' pro diabetes 2. typu. Pokud zadán, filtruje reimbursement podle indikace."
      },
      "compare_alternatives": {
        "type": "boolean",
        "description": "Pokud true, vrátí cenové srovnání s alternativními léky ve stejné ATC skupině",
        "default": false
      }
    },
    "required": ["drug_name"]
  }
}
```

### Request Example

```json
{
  "tool": "get_vzp_reimbursement",
  "arguments": {
    "drug_name": "empagliflozin",
    "indication_icd10": "E11",
    "compare_alternatives": true
  }
}
```

### Response Example (Success)

```json
{
  "status": "success",
  "drug": {
    "name": "Empagliflozin",
    "brand_names": ["Jardiance", "Empaglif"],
    "atc_code": "A10BK03",
    "sukl_code": "0123456"
  },
  "reimbursement": {
    "status": "reimbursed",
    "copay_czk": 30,
    "full_price_czk": 850,
    "reimbursement_percentage": 100,
    "conditions": "HbA1c ≥ 53 mmol/mol (7.0%) po selhání metforminu",
    "restriction_code": "H013",
    "restriction_description": "Předepisuje endokrinolog nebo internista"
  },
  "prescribing": {
    "indication_icd10": ["E11"],
    "indication_description": "Diabetes mellitus 2. typu",
    "contraindications": "GFR < 30 ml/min",
    "prior_authorization_required": false
  },
  "alternatives": [
    {
      "drug_name": "Dapagliflozin",
      "brand_names": ["Forxiga"],
      "copay_czk": 50,
      "atc_code": "A10BK01"
    },
    {
      "drug_name": "Canagliflozin",
      "brand_names": ["Invokana"],
      "copay_czk": 45,
      "atc_code": "A10BK02"
    }
  ],
  "metadata": {
    "last_updated": "2025-01-15T10:30:00Z",
    "data_version": "2025-01",
    "source_url": "https://www.vzp.cz/poskytovatele/ciselniky/..."
  }
}
```

### Response Example (Off-Label)

```json
{
  "status": "success",
  "drug": {
    "name": "Empagliflozin",
    "brand_names": ["Jardiance"],
    "atc_code": "A10BK03"
  },
  "reimbursement": {
    "status": "off_label",
    "copay_czk": 1200,
    "full_price_czk": 1200,
    "reimbursement_percentage": 0,
    "off_label_note": "Pro indikaci I50 (srdeční selhání) není empagliflozin hrazen VZP. Vyžaduje žádost o individuální úhradu (IU)."
  },
  "prescribing": {
    "indication_icd10": ["I50"],
    "indication_description": "Srdeční selhání",
    "prior_authorization_required": true,
    "iu_success_rate": 60
  },
  "alternatives": [
    {
      "drug_name": "Dapagliflozin",
      "brand_names": ["Forxiga"],
      "copay_czk": 50,
      "reimbursement_status": "reimbursed",
      "note": "Dapagliflozin je hrazen VZP pro srdeční selhání od 2023"
    }
  ],
  "metadata": {
    "last_updated": "2025-01-15T10:30:00Z",
    "data_version": "2025-01"
  }
}
```

### Response Example (Drug Not Found)

```json
{
  "status": "not_found",
  "error": {
    "code": "DRUG_NOT_FOUND",
    "message": "Lék 'tirzepatide' nebyl nalezen v VZP databázi. Možné důvody: (1) Lék není registrován v ČR, (2) Chyba v názvu, (3) VZP data nejsou aktuální.",
    "suggestions": [
      "Zkontrolujte název léku (možná překlep?)",
      "Lék může být registrován pod jiným názvem",
      "Ověřte SÚKL registraci: https://www.sukl.cz/"
    ]
  }
}
```

### Response Example (VZP API Error)

```json
{
  "status": "error",
  "error": {
    "code": "VZP_DATA_UNAVAILABLE",
    "message": "VZP databáze je dočasně nedostupná. Zobrazuji cached data (aktualizace: 10.1.2025).",
    "fallback_data": {
      "drug": { ... },
      "reimbursement": { ... },
      "metadata": {
        "last_updated": "2025-01-10T08:00:00Z",
        "data_age_days": 5,
        "cache_warning": "Data mohou být zastaralá"
      }
    }
  }
}
```

---

## Data Ingestion Pipeline

### Supabase Edge Function: `parse_vzp_data`

**Trigger:** Cron job (měsíčně 1. den v měsíci 02:00 CET)

**Steps:**

```typescript
// Supabase Edge Function: parse_vzp_data.ts

import { createClient } from '@supabase/supabase-js';
import * as XLSX from 'xlsx';

Deno.serve(async (req) => {
  const supabase = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
  );

  console.log('[VZP Parser] Starting monthly VZP data ingestion...');

  try {
    // Step 1: Download VZP Excel file
    const vzpUrl = 'https://www.vzp.cz/poskytovatele/ciselniky/seznam-kategorizovanych-lecivych-pripravku.xlsx';
    const response = await fetch(vzpUrl);
    const arrayBuffer = await response.arrayBuffer();
    const workbook = XLSX.read(arrayBuffer);
    const sheetName = workbook.SheetNames[0];
    const worksheet = workbook.Sheets[sheetName];
    const jsonData = XLSX.utils.sheet_to_json(worksheet);

    console.log(`[VZP Parser] Downloaded ${jsonData.length} rows from VZP`);

    // Step 2: Parse and normalize data
    const normalizedData = jsonData.map((row: any) => {
      const drugName = row['Název léčivého přípravku']?.trim();
      const atcCode = row['ATC kód']?.trim();
      const copay = parseInt(row['Doplatek pacienta (Kč)']) || 0;
      const reimbursementCode = row['Kód úhrady']?.trim();

      return {
        drug_name: drugName,
        drug_name_normalized: drugName.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, ''),
        atc_code: atcCode,
        copay_czk: copay,
        reimbursement_status: copay === 0 ? 'not_reimbursed' : 'reimbursed',
        restriction_code: reimbursementCode,
        data_version: new Date().toISOString().slice(0, 7), // "2025-01"
        source_url: vzpUrl,
        last_updated: new Date().toISOString()
      };
    });

    // Step 3: Upsert to Supabase (batch 1000 rows)
    let inserted = 0;
    let updated = 0;

    for (let i = 0; i < normalizedData.length; i += 1000) {
      const batch = normalizedData.slice(i, i + 1000);

      const { data, error } = await supabase
        .from('vzp_reimbursement')
        .upsert(batch, {
          onConflict: 'drug_name_normalized,atc_code',
          ignoreDuplicates: false
        });

      if (error) {
        console.error(`[VZP Parser] Error upserting batch ${i}:`, error);
      } else {
        inserted += batch.length;
      }
    }

    // Step 4: Log update
    await supabase.from('vzp_update_log').insert({
      update_started_at: new Date().toISOString(),
      update_completed_at: new Date().toISOString(),
      records_processed: jsonData.length,
      records_inserted: inserted,
      records_updated: updated,
      data_version: new Date().toISOString().slice(0, 7),
      source_file_url: vzpUrl,
      status: 'completed'
    });

    console.log(`[VZP Parser] ✅ Success: ${inserted} records inserted/updated`);

    return new Response(JSON.stringify({
      success: true,
      records_processed: jsonData.length,
      records_inserted: inserted
    }), {
      headers: { 'Content-Type': 'application/json' }
    });

  } catch (error) {
    console.error('[VZP Parser] ❌ Error:', error);

    // Log failed update
    await supabase.from('vzp_update_log').insert({
      update_started_at: new Date().toISOString(),
      status: 'failed',
      error_log: error.message
    });

    return new Response(JSON.stringify({
      success: false,
      error: error.message
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
});
```

### Cron Configuration (Supabase)

```sql
-- Create pg_cron extension (if not exists)
CREATE EXTENSION IF NOT EXISTS pg_cron;

-- Schedule monthly VZP data update (1st day of month at 2:00 AM)
SELECT cron.schedule(
  'vzp-monthly-update',
  '0 2 1 * *',
  $$
  SELECT net.http_post(
    url := 'https://[project-ref].supabase.co/functions/v1/parse_vzp_data',
    headers := jsonb_build_object('Authorization', 'Bearer [service-role-key]')
  );
  $$
);
```

---

## MCP Tool Implementation

### File: `mcp_tools/vzp_navigator.py`

```python
# MCP Tool: VZP Navigator
# Provides VZP reimbursement data for Czech drugs

import os
from typing import Optional, Dict, Any, List
from supabase import create_client, Client

supabase: Client = create_client(
    os.environ.get("SUPABASE_URL"),
    os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
)

def normalize_drug_name(drug_name: str) -> str:
    """Normalize drug name: lowercase, remove diacritics"""
    import unicodedata
    normalized = unicodedata.normalize('NFD', drug_name.lower())
    return ''.join(c for c in normalized if unicodedata.category(c) != 'Mn')

async def get_vzp_reimbursement(
    drug_name: str,
    indication_icd10: Optional[str] = None,
    compare_alternatives: bool = False
) -> Dict[str, Any]:
    """
    MCP Tool: get_vzp_reimbursement

    Fetches VZP reimbursement data for a given drug.

    Args:
        drug_name: Generic or brand name of the drug
        indication_icd10: Optional ICD-10 code to filter by indication
        compare_alternatives: If True, returns price comparison with alternatives

    Returns:
        JSON response with reimbursement data
    """

    # Step 1: Normalize drug name
    normalized_name = normalize_drug_name(drug_name)

    # Step 2: Query Supabase
    query = supabase.table('vzp_reimbursement').select('*')

    # Try exact match first
    result = query.eq('drug_name_normalized', normalized_name).execute()

    # Fallback: fuzzy search using full-text search
    if not result.data:
        result = query.textSearch('drug_search_vector', normalized_name).limit(5).execute()

    if not result.data:
        return {
            "status": "not_found",
            "error": {
                "code": "DRUG_NOT_FOUND",
                "message": f"Lék '{drug_name}' nebyl nalezen v VZP databázi.",
                "suggestions": [
                    "Zkontrolujte název léku (možná překlep?)",
                    "Lék může být registrován pod jiným názvem",
                    "Ověřte SÚKL registraci: https://www.sukl.cz/"
                ]
            }
        }

    drug_data = result.data[0]

    # Step 3: Filter by indication (if provided)
    if indication_icd10:
        if indication_icd10 not in (drug_data.get('indication_icd10') or []):
            # Off-label use case
            return build_off_label_response(drug_data, indication_icd10)

    # Step 4: Get alternatives (if requested)
    alternatives = []
    if compare_alternatives and drug_data.get('atc_code'):
        alt_result = supabase.table('vzp_reimbursement')\
            .select('drug_name, brand_names, copay_czk, atc_code, reimbursement_status')\
            .eq('atc_code', drug_data['atc_code'][:5])\ # Same ATC group (first 5 chars)
            .neq('drug_name_normalized', normalized_name)\
            .limit(5)\
            .execute()

        alternatives = alt_result.data if alt_result.data else []

    # Step 5: Build response
    return {
        "status": "success",
        "drug": {
            "name": drug_data['drug_name'],
            "brand_names": drug_data.get('brand_names', []),
            "atc_code": drug_data.get('atc_code'),
            "sukl_code": drug_data.get('sukl_code')
        },
        "reimbursement": {
            "status": drug_data['reimbursement_status'],
            "copay_czk": drug_data.get('copay_czk'),
            "full_price_czk": drug_data.get('full_price_czk'),
            "reimbursement_percentage": drug_data.get('reimbursement_percentage'),
            "conditions": drug_data.get('conditions'),
            "restriction_code": drug_data.get('restriction_code'),
            "restriction_description": drug_data.get('restriction_description')
        },
        "prescribing": {
            "indication_icd10": drug_data.get('indication_icd10', []),
            "indication_description": drug_data.get('indication_description'),
            "contraindications": drug_data.get('contraindications'),
            "prior_authorization_required": drug_data.get('prior_authorization_required', False)
        },
        "alternatives": alternatives,
        "metadata": {
            "last_updated": drug_data.get('last_updated'),
            "data_version": drug_data.get('data_version'),
            "source_url": drug_data.get('source_url')
        }
    }

def build_off_label_response(drug_data: Dict, indication_icd10: str) -> Dict[str, Any]:
    """Build response for off-label drug use"""
    return {
        "status": "success",
        "drug": {
            "name": drug_data['drug_name'],
            "brand_names": drug_data.get('brand_names', []),
            "atc_code": drug_data.get('atc_code')
        },
        "reimbursement": {
            "status": "off_label",
            "copay_czk": drug_data.get('full_price_czk'),  # Patient pays full price
            "full_price_czk": drug_data.get('full_price_czk'),
            "reimbursement_percentage": 0,
            "off_label_note": f"Pro indikaci {indication_icd10} není {drug_data['drug_name']} hrazen VZP. Vyžaduje žádost o individuální úhradu (IU)."
        },
        "prescribing": {
            "indication_icd10": [indication_icd10],
            "prior_authorization_required": True,
            "iu_success_rate": drug_data.get('iu_success_rate', 50)
        },
        "metadata": {
            "last_updated": drug_data.get('last_updated'),
            "data_version": drug_data.get('data_version')
        }
    }
```

---

## Error Handling & Fallbacks

### Scenario 1: VZP Data Stale (>90 days old)

```python
def check_data_freshness(last_updated: str) -> Dict[str, Any]:
    from datetime import datetime, timedelta

    last_update_date = datetime.fromisoformat(last_updated)
    age_days = (datetime.now() - last_update_date).days

    if age_days > 90:
        return {
            "warning": True,
            "message": f"⚠️ Upozornění: VZP data starší než {age_days} dní (poslední aktualizace: {last_update_date.strftime('%d.%m.%Y')}). Doporučujeme ověřit aktuální status na VZP web.",
            "fallback_url": "https://www.vzp.cz/poskytovatele/ciselniky/"
        }

    return {"warning": False}
```

### Scenario 2: Database Connection Failure

```python
async def get_vzp_reimbursement_with_fallback(drug_name: str) -> Dict[str, Any]:
    try:
        return await get_vzp_reimbursement(drug_name)
    except Exception as e:
        # Fallback: Try cache
        cached = await get_cached_query(drug_name)
        if cached:
            return {
                "status": "success",
                **cached,
                "metadata": {
                    **cached.get("metadata", {}),
                    "cache_warning": "⚠️ VZP databáze dočasně nedostupná. Zobrazuji cached data.",
                    "data_age_days": calculate_cache_age(cached)
                }
            }

        # Ultimate fallback: Manual VZP web link
        return {
            "status": "error",
            "error": {
                "code": "VZP_DATA_UNAVAILABLE",
                "message": "VZP databáze je dočasně nedostupná a cached data nejsou k dispozici.",
                "manual_check_url": f"https://www.vzp.cz/poskytovatele/ciselniky/?search={drug_name}"
            }
        }
```

---

## Performance Optimizations

### 1. Query Caching (Redis or Supabase)

```python
import hashlib

async def get_cached_query(normalized_query: str) -> Optional[Dict]:
    """Check if query result is cached (TTL: 30 days)"""
    result = supabase.table('vzp_query_cache')\
        .select('mcp_response')\
        .eq('normalized_query', normalized_query)\
        .gt('expires_at', datetime.now().isoformat())\
        .execute()

    if result.data:
        # Increment hit counter
        await supabase.table('vzp_query_cache')\
            .update({'hit_count': result.data[0]['hit_count'] + 1, 'last_accessed_at': datetime.now().isoformat()})\
            .eq('normalized_query', normalized_query)\
            .execute()

        return result.data[0]['mcp_response']

    return None

async def cache_query(user_query: str, normalized_query: str, response: Dict):
    """Cache MCP tool response for 30 days"""
    await supabase.table('vzp_query_cache').insert({
        'user_query': user_query,
        'normalized_query': normalized_query,
        'mcp_response': response,
        'hit_count': 1,
        'expires_at': (datetime.now() + timedelta(days=30)).isoformat()
    }).execute()
```

### 2. Pre-fetching Popular Drugs

```python
# Supabase Edge Function: prefetch_popular_drugs.ts
// Runs nightly: pre-fetch top 100 most queried drugs into cache

async function prefetchPopularDrugs() {
  const topDrugs = await supabase
    .from('vzp_query_cache')
    .select('normalized_query, hit_count')
    .order('hit_count', { ascending: false })
    .limit(100)
    .execute();

  // Warm cache by querying MCP tool for top 100 drugs
  for (const drug of topDrugs.data) {
    await get_vzp_reimbursement(drug.normalized_query);
  }
}
```

---

## Testing Strategy

### Unit Tests

```python
# tests/test_vzp_navigator.py

import pytest
from mcp_tools.vzp_navigator import get_vzp_reimbursement, normalize_drug_name

def test_normalize_drug_name():
    assert normalize_drug_name("Empagliflozin") == "empagliflozin"
    assert normalize_drug_name("Jardiance") == "jardiance"
    assert normalize_drug_name("Léčivo") == "lecivo"  # Remove diacritics

@pytest.mark.asyncio
async def test_get_vzp_reimbursement_success():
    result = await get_vzp_reimbursement("empagliflozin")
    assert result["status"] == "success"
    assert result["drug"]["name"] == "Empagliflozin"
    assert result["reimbursement"]["copay_czk"] == 30

@pytest.mark.asyncio
async def test_get_vzp_reimbursement_not_found():
    result = await get_vzp_reimbursement("nonexistent_drug_xyz")
    assert result["status"] == "not_found"
    assert result["error"]["code"] == "DRUG_NOT_FOUND"

@pytest.mark.asyncio
async def test_get_vzp_reimbursement_off_label():
    result = await get_vzp_reimbursement("empagliflozin", indication_icd10="I50")
    assert result["status"] == "success"
    assert result["reimbursement"]["status"] == "off_label"
    assert result["reimbursement"]["copay_czk"] > 1000  # Full price
```

### Integration Tests

```python
# tests/integration/test_vzp_mcp_tool.py

@pytest.mark.integration
async def test_mcp_tool_end_to_end():
    # Simulate Claude AI calling MCP tool
    user_query = "Je empagliflozin hrazený VZP?"

    # Step 1: Claude detects need for VZP data
    assert "hrazený" in user_query or "VZP" in user_query

    # Step 2: Call MCP tool
    result = await get_vzp_reimbursement("empagliflozin")

    # Step 3: Verify response structure
    assert result["status"] == "success"
    assert "reimbursement" in result
    assert "metadata" in result

    # Step 4: Verify frontend can render response
    assert result["reimbursement"]["copay_czk"] is not None
```

---

## Monitoring & Alerts

### Key Metrics

1. **MCP Tool Usage:**
   - Daily queries: Track via Supabase logs
   - Cache hit rate: `hit_count` in `vzp_query_cache`
   - Average response time: Log duration in MCP tool

2. **Data Freshness:**
   - Last VZP update timestamp
   - Alert if `last_updated` > 60 days old

3. **Error Rate:**
   - `DRUG_NOT_FOUND` errors per day
   - `VZP_DATA_UNAVAILABLE` errors per hour

### Supabase Alerts

```sql
-- Alert if VZP data not updated in 60 days
CREATE OR REPLACE FUNCTION check_vzp_data_freshness()
RETURNS void AS $$
DECLARE
  last_update TIMESTAMP;
BEGIN
  SELECT MAX(last_updated) INTO last_update FROM vzp_reimbursement;

  IF (NOW() - last_update) > INTERVAL '60 days' THEN
    -- Send alert (via Supabase webhook or email)
    PERFORM net.http_post(
      url := 'https://hooks.slack.com/services/[webhook]',
      body := jsonb_build_object('text', '⚠️ VZP data not updated in 60 days!')
    );
  END IF;
END;
$$ LANGUAGE plpgsql;

-- Run daily check
SELECT cron.schedule('check-vzp-freshness', '0 9 * * *', 'SELECT check_vzp_data_freshness()');
```

---

## Security & Compliance

### Data Privacy (GDPR)

- **No Personal Data:** VZP reimbursement data je veřejná (léky, ceny, kódy) → GDPR non-issue
- **User Queries Logging:** Store only anonymized queries (no patient names, diagnoses)
- **RLS Policy:** VZP data read-only, no PII storage

### API Rate Limiting

```python
# Rate limit: 100 VZP queries per user per day
@rate_limit(max_requests=100, period=86400)  # 24 hours
async def get_vzp_reimbursement(drug_name: str):
    # ... (implementation above)
```

---

## Deployment Plan

### Phase 1: Data Pipeline (Week 1-2)
- ✅ Supabase schema setup
- ✅ VZP data ingestion Edge Function
- ✅ Cron job configuration
- ✅ Initial data load (50K drugs)

### Phase 2: MCP Tool Development (Week 3-4)
- ✅ MCP tool Python implementation
- ✅ Unit tests + integration tests
- ✅ Query caching layer
- ✅ Error handling & fallbacks

### Phase 3: Frontend Integration (Week 5-6)
- ✅ React component for VZP Info Card
- ✅ Claude AI prompt engineering (detect VZP queries)
- ✅ Interactive buttons (žádost o IU, price comparison)

### Phase 4: Testing & Launch (Week 7-8)
- ✅ End-to-end testing with real user queries
- ✅ Performance testing (1000 concurrent queries)
- ✅ Soft launch to 10 beta users
- ✅ Full rollout to all users

---

## Success Metrics (Post-Launch)

**Month 1:**
- 50% lékařů používá VZP Navigator ≥1x týdně
- Cache hit rate: >40% (top drugs)
- Average response time: <2 seconds

**Month 3:**
- 70% lékařů používá VZP Navigator ≥5x týdně
- User satisfaction: "Pomohlo mi VZP Navigator?" → >80% ANO
- 15% lékařů upgraduje na Pro plan kvůli unlimited VZP queries

**Month 6:**
- VZP Navigator je #1 most-used feature (after Chat)
- 95%+ accuracy vs manual VZP web check
- <0.1% error rate (DRUG_NOT_FOUND, VZP_DATA_UNAVAILABLE)

---

## Závěr

VZP Navigator technical implementation je **feasible s 2-měsíčním vývojem**. Klíčové technické komponenty:
1. **Supabase PostgreSQL** - robust, scalable, GDPR-compliant
2. **MCP Tool API** - simple, fast, cacheable
3. **Edge Functions** - serverless, auto-scaling
4. **Cron Jobs** - reliable monthly updates

**Biggest Risk:** VZP data availability (pokud VZP nemá public API, nutný web scraping).
**Mitigation:** Partner s VZP (official data feed) nebo stable scraping pipeline s error handling.
