# Czech MedAI — API Specification

**Projekt:** Czech MedAI (kódové označení: Benjamin)  
**Verze API:** v1.0.0  
**Base URL:** `https://api.czechmedai.cz/api/v1`  
**Datum:** 15.12.2025  
**Formát:** OpenAPI 3.1 kompatibilní

---

## 📋 Přehled API

Czech MedAI API poskytuje programový přístup ke klinickému AI asistentovi. Všechny odpovědi jsou v JSON formátu, autentizace probíhá přes Bearer token.

### Base URLs

| Prostředí | URL |
|-----------|-----|
| Production | `https://api.czechmedai.cz/api/v1` |
| Staging | `https://staging-api.czechmedai.cz/api/v1` |
| Development | `http://localhost:8000/api/v1` |

---

## 🔐 Autentizace

### Bearer Token (JWT)

Všechny endpointy (kromě `/auth/*`) vyžadují autentizaci.

```http
Authorization: Bearer <access_token>
```

### Získání tokenu

```http
POST /auth/login
Content-Type: application/json

{
  "email": "doktor@nemocnice.cz",
  "password": "securepassword123"
}
```

**Response 200:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "doktor@nemocnice.cz",
    "license_verified": true,
    "role": "physician"
  }
}
```

---

## 📡 Endpointy

### 1. Klinické dotazy

#### POST /query — Hlavní endpoint pro dotazy

Zpracuje klinický dotaz a vrátí odpověď s citacemi.

**Request:**
```http
POST /query
Authorization: Bearer <token>
Content-Type: application/json

{
  "query": "Jaká je první linie léčby hypertenze u pacienta s diabetem 2. typu?",
  "query_type": "quick",
  "language": "cs",
  "sources": ["pubmed", "sukl", "guidelines"],
  "max_citations": 5
}
```

| Parametr | Typ | Povinný | Popis |
|----------|-----|---------|-------|
| `query` | string | ✅ | Klinický dotaz (3-2000 znaků) |
| `query_type` | enum | ❌ | `quick` (default) nebo `deep` |
| `language` | enum | ❌ | `cs` (default) nebo `en` |
| `sources` | array | ❌ | Zdroje k prohledání |
| `max_citations` | int | ❌ | Max počet citací (1-10, default 5) |

**Response 200:**
```json
{
  "id": "q_abc123def456",
  "answer": "U pacientů s diabetem 2. typu a hypertenzí jsou léky první volby ACE inhibitory nebo sartany [1][2], které kromě antihypertenzního účinku poskytují renoprotekci [3]. Dle českých guidelines ČDS je cílový TK < 130/80 mmHg [4].",
  "citations": [
    {
      "id": 1,
      "source": "pubmed",
      "title": "2023 ESC Guidelines for the management of cardiovascular disease in patients with diabetes",
      "authors": ["Marx N", "Federici M", "Schütt K"],
      "journal": "European Heart Journal",
      "year": 2023,
      "pmid": "37622657",
      "doi": "10.1093/eurheartj/ehad192",
      "url": "https://pubmed.ncbi.nlm.nih.gov/37622657/",
      "relevance_score": 0.94
    },
    {
      "id": 2,
      "source": "guidelines",
      "title": "Doporučené postupy ČDS pro léčbu diabetes mellitus 2. typu",
      "authors": ["Česká diabetologická společnost"],
      "year": 2023,
      "url": "https://www.diab.cz/doporucene-postupy",
      "relevance_score": 0.91
    },
    {
      "id": 3,
      "source": "pubmed",
      "title": "ADVANCE Collaborative Group - Effects of blood pressure lowering",
      "pmid": "17868116",
      "doi": "10.1016/S0140-6736(07)61303-8",
      "url": "https://pubmed.ncbi.nlm.nih.gov/17868116/",
      "relevance_score": 0.87
    },
    {
      "id": 4,
      "source": "guidelines",
      "title": "Doporučení ČKS pro diagnostiku a léčbu arteriální hypertenze",
      "year": 2022,
      "url": "https://www.kardio-cz.cz",
      "relevance_score": 0.85
    }
  ],
  "metadata": {
    "query_type": "quick",
    "language": "cs",
    "sources_searched": ["pubmed", "sukl", "guidelines"],
    "processing_time_ms": 3420,
    "model": "claude-sonnet-4-5",
    "confidence_score": 0.92
  },
  "created_at": "2025-12-15T10:30:00Z"
}
```

**Response 400 — Nevalidní dotaz:**
```json
{
  "error": {
    "code": "INVALID_QUERY",
    "message": "Dotaz musí mít minimálně 3 znaky",
    "details": {
      "field": "query",
      "min_length": 3,
      "actual_length": 2
    }
  }
}
```

**Response 429 — Rate limit:**
```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Překročen limit dotazů. Zkuste to znovu za 60 sekund.",
    "retry_after": 60
  }
}
```

---

#### GET /query/{query_id} — Získání uloženého dotazu

```http
GET /query/q_abc123def456
Authorization: Bearer <token>
```

**Response 200:** Stejný formát jako POST /query

---

#### GET /query/history — Historie dotazů

```http
GET /query/history?limit=20&offset=0&from=2025-01-01&to=2025-12-31
Authorization: Bearer <token>
```

| Parametr | Typ | Popis |
|----------|-----|-------|
| `limit` | int | Max počet výsledků (1-100, default 20) |
| `offset` | int | Offset pro stránkování |
| `from` | date | Filtr od data (ISO 8601) |
| `to` | date | Filtr do data (ISO 8601) |
| `query_type` | enum | Filtr podle typu dotazu |

**Response 200:**
```json
{
  "queries": [
    {
      "id": "q_abc123def456",
      "query": "Jaká je první linie léčby hypertenze...",
      "query_type": "quick",
      "created_at": "2025-12-15T10:30:00Z"
    }
  ],
  "pagination": {
    "total": 156,
    "limit": 20,
    "offset": 0,
    "has_more": true
  }
}
```

---

### 2. Informace o lécích

#### GET /api/v1/drugs/search — Vyhledání léku

```http
GET /api/v1/drugs/search?q=aspirin&limit=20
Authorization: Bearer <token>
```

| Parametr | Typ | Popis |
|----------|-----|-------|
| `q` | string | Název léku nebo účinná látka |
| `limit` | int | Max počet výsledků (default 20) |

**Response 200:**
```json
{
  "drugs": [
    {
      "sukl_code": "0000001",
      "name": "METFORMIN TEVA 500 MG",
      "active_substance": "Metformini hydrochloridum",
      "atc_code": "A10BA02",
      "form": "Potahovaná tableta",
      "strength": "500 mg",
      "manufacturer": "Teva Pharmaceuticals CR",
      "registration_holder": "Teva B.V.",
      "registration_number": "18/123/05-C",
      "is_available": true,
      "requires_prescription": true,
      "reimbursement": {
        "is_reimbursed": true,
        "reimbursement_group": "A/1",
        "max_price": 89.50,
        "patient_copay": 0.00,
        "conditions": "Bez omezení"
      }
    }
  ],
  "total": 24
}
```

---

#### GET /drugs/{sukl_code} — Detail léku

```http
GET /drugs/0000001
Authorization: Bearer <token>
```

**Response 200:**
```json
{
  "sukl_code": "0000001",
  "name": "METFORMIN TEVA 500 MG",
  "active_substance": "Metformini hydrochloridum",
  "atc_code": "A10BA02",
  "form": "Potahovaná tableta",
  "strength": "500 mg",
  "package_size": "120 tablet",
  "manufacturer": "Teva Pharmaceuticals CR",
  "registration_holder": "Teva B.V.",
  "registration_number": "18/123/05-C",
  "first_registration": "2005-03-15",
  "is_available": true,
  "requires_prescription": true,
  "spc": {
    "indications": "Léčba diabetes mellitus 2. typu, zejména u pacientů s nadváhou...",
    "contraindications": "Hypersenzitivita na léčivou látku, diabetická ketoacidóza...",
    "dosage": "Dospělí: Obvyklá počáteční dávka je 500 mg nebo 850 mg 2-3x denně...",
    "interactions": "Alkohol, jodované kontrastní látky, léčiva ovlivňující renální funkce...",
    "side_effects": "Velmi časté: gastrointestinální obtíže (nauzea, zvracení, průjem)...",
    "pregnancy": "Kategorie B - metformin není doporučen v těhotenství...",
    "storage": "Uchovávejte při teplotě do 25°C...",
    "full_spc_url": "https://www.sukl.cz/modules/medication/detail.php?code=0000001"
  },
  "reimbursement": {
    "is_reimbursed": true,
    "reimbursement_group": "A/1",
    "max_price": 89.50,
    "patient_copay": 0.00,
    "conditions": "Bez omezení",
    "valid_from": "2025-01-01",
    "valid_to": "2025-12-31"
  },
  "alternatives": [
    {
      "sukl_code": "0000002",
      "name": "SIOFOR 500",
      "patient_copay": 12.00
    }
  ]
}
```

---

#### GET /drugs/{sukl_code}/interactions — Lékové interakce

```http
GET /drugs/0000001/interactions?with=0000100,0000200
Authorization: Bearer <token>
```

**Response 200:**
```json
{
  "drug": {
    "sukl_code": "0000001",
    "name": "METFORMIN TEVA 500 MG"
  },
  "interactions": [
    {
      "interacting_drug": {
        "sukl_code": "0000100",
        "name": "WARFARIN ORION 5 MG"
      },
      "severity": "moderate",
      "description": "Metformin může mírně zvyšovat účinek warfarinu. Doporučena kontrola INR.",
      "recommendation": "Monitorovat INR při zahájení nebo ukončení léčby metforminem.",
      "source": "SÚKL"
    }
  ]
}
```

---

### 3. Guidelines

#### GET /guidelines/search — Vyhledání guidelines

```http
GET /guidelines/search?q=diabetes&source=czech&specialty=diabetology
Authorization: Bearer <token>
```

| Parametr | Typ | Popis |
|----------|-----|-------|
| `q` | string | Hledaný výraz |
| `source` | enum | `czech`, `international`, `all` |
| `specialty` | string | Lékařská specializace |

**Response 200:**
```json
{
  "guidelines": [
    {
      "id": "gl_cds_dm2_2023",
      "title": "Doporučené postupy ČDS pro léčbu diabetes mellitus 2. typu",
      "organization": "Česká diabetologická společnost",
      "year": 2023,
      "version": "2.0",
      "source": "czech",
      "specialty": "diabetology",
      "summary": "Komplexní doporučení pro diagnostiku a léčbu DM2 včetně farmakoterapie, dietních opatření a prevence komplikací.",
      "url": "https://www.diab.cz/doporucene-postupy",
      "pdf_url": "https://www.diab.cz/dokumenty/dp_dm2_2023.pdf",
      "keywords": ["diabetes", "metformin", "GLP-1", "SGLT2"]
    }
  ],
  "total": 5
}
```

---

#### GET /guidelines/{guideline_id} — Detail guidelines

```http
GET /guidelines/gl_cds_dm2_2023
Authorization: Bearer <token>
```

**Response 200:**
```json
{
  "id": "gl_cds_dm2_2023",
  "title": "Doporučené postupy ČDS pro léčbu diabetes mellitus 2. typu",
  "organization": "Česká diabetologická společnost",
  "authors": ["Prof. MUDr. Milan Kvapil, CSc.", "Prof. MUDr. Terezie Pelikánová, DrSc."],
  "year": 2023,
  "version": "2.0",
  "source": "czech",
  "specialty": "diabetology",
  "content": {
    "sections": [
      {
        "title": "1. Diagnostika DM2",
        "content": "Diagnóza DM2 je stanovena na základě..."
      },
      {
        "title": "2. Cíle léčby",
        "content": "Cílová hodnota HbA1c < 53 mmol/mol..."
      },
      {
        "title": "3. Farmakoterapie",
        "content": "Metformin je lékem první volby..."
      }
    ]
  },
  "key_recommendations": [
    "Metformin je lékem první volby u všech pacientů s DM2",
    "U pacientů s KV onemocněním preferovat GLP-1 RA nebo SGLT2i",
    "Cílový HbA1c individualizovat dle věku a komorbidit"
  ],
  "url": "https://www.diab.cz/doporucene-postupy",
  "pdf_url": "https://www.diab.cz/dokumenty/dp_dm2_2023.pdf",
  "last_updated": "2023-06-15"
}
```

---

---

### 4. AI Nástroje

#### POST /api/v1/ai/epicrisis — Generování epikrízy

Generuje lékařskou zprávu z neformálních poznámek.

```http
POST /api/v1/ai/epicrisis
Authorization: Bearer <token>
Content-Type: application/json

{
  "items": "- Pacient muž, 45 let\n- Přichází pro bolest v krku, 3 dny\n- Teplota 38.5C\n- Objektivně: zarudlé hrdlo, čepy na mandlích\n- Dg: Angína\n- Th: Penicilin 1.5 MIU po 8h, 10 dní"
}
```

**Response 200:**
```json
{
  "response": "LÉKAŘSKÁ ZPRÁVA\n\nPacient: Muž, 45 let\nDůvod návštěvy: Bolest v krku trvající 3 dny, febrilie (38.5°C).\n\nObjektivní nález:\n- Hrdlo zarudlé\n- Přítomny čepy na tonzilách\n\nDiagnóza:\n- Akutní tonzilitida (Angína)\n\nTerapie:\n- Penicilin 1.5 MIU á 8 hod po dobu 10 dnů\n\nDoporučení:\n- Klidový režim, dostatek tekutin.",
  "source": "claude-3-haiku"
}
```

#### POST /api/v1/ai/translate — Překlad

Překládá lékařské texty (defaultně do češtiny).

```http
POST /api/v1/ai/translate
Authorization: Bearer <token>
Content-Type: application/json

{
  "text": "Patient presents with acute abdominal pain localized in the right lower quadrant.",
  "language": "Czech"
}
```

**Response 200:**
```json
{
  "response": "Pacient přichází s akutní bolestí břicha lokalizovanou v pravém dolním kvadrantu.",
  "source": "claude-3-haiku"
}
```

#### POST /api/v1/ai/transcribe — Přepis audia

Přepisuje audio záznam (např. diktát, vizita).

```http
POST /api/v1/ai/transcribe
Authorization: Bearer <token>
Content-Type: multipart/form-data

file: <audio_file.mp3>
```

**Response 200:**
```json
{
  "transcript": "Pacient Jan Novák, ročník 1980, kontrola po měsíci. Tlak 120 na 80...",
  "source": "gemini-1.5-pro"
}
```

---

### 5. Uživatelé a autentizace

#### POST /auth/register — Registrace

```http
POST /auth/register
Content-Type: application/json

{
  "email": "doktor@nemocnice.cz",
  "password": "SecurePassword123!",
  "first_name": "Jan",
  "last_name": "Novák",
  "license_number": "12345",
  "license_type": "CLK",
  "specialty": "internal_medicine"
}
```

**Response 201:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "doktor@nemocnice.cz",
  "first_name": "Jan",
  "last_name": "Novák",
  "license_verified": false,
  "verification_pending": true,
  "message": "Registrace úspěšná. Ověření licence probíhá, budete informováni emailem."
}
```

---

#### POST /auth/refresh — Obnovení tokenu

```http
POST /auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

---

#### GET /users/me — Profil přihlášeného uživatele

```http
GET /users/me
Authorization: Bearer <token>
```

**Response 200:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "doktor@nemocnice.cz",
  "first_name": "Jan",
  "last_name": "Novák",
  "license_number": "12345",
  "license_type": "CLK",
  "license_verified": true,
  "specialty": "internal_medicine",
  "role": "physician",
  "subscription": {
    "plan": "professional",
    "queries_remaining": 450,
    "queries_limit": 500,
    "valid_until": "2026-01-15"
  },
  "created_at": "2025-01-15T08:00:00Z"
}
```

---

### 5. Zdraví systému

#### GET /health — Health check

```http
GET /health
```

**Response 200:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2025-12-15T10:30:00Z",
  "services": {
    "database": "healthy",
    "redis": "healthy",
    "llm": "healthy",
    "pubmed_mcp": "healthy",
    "sukl_mcp": "healthy"
  }
}
```

---

## ❌ Chybové kódy

| HTTP Status | Kód | Popis |
|-------------|-----|-------|
| 400 | `INVALID_REQUEST` | Nevalidní požadavek |
| 400 | `INVALID_QUERY` | Nevalidní klinický dotaz |
| 401 | `UNAUTHORIZED` | Chybí nebo neplatný token |
| 401 | `TOKEN_EXPIRED` | Vypršel access token |
| 403 | `FORBIDDEN` | Nedostatečná oprávnění |
| 403 | `LICENSE_NOT_VERIFIED` | Lékařská licence není ověřena |
| 404 | `NOT_FOUND` | Zdroj nenalezen |
| 429 | `RATE_LIMIT_EXCEEDED` | Překročen limit požadavků |
| 500 | `INTERNAL_ERROR` | Interní chyba serveru |
| 503 | `SERVICE_UNAVAILABLE` | Služba dočasně nedostupná |

**Standardní error response:**
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Lidsky čitelný popis chyby",
    "details": {},
    "request_id": "req_abc123"
  }
}
```

---

## ⏱️ Rate Limiting

| Plán | Limit dotazů | Okno |
|------|--------------|------|
| Free | 10 dotazů | hodina |
| Professional | 500 dotazů | měsíc |
| Enterprise | neomezeno | — |

**Headers v odpovědi:**
```http
X-RateLimit-Limit: 500
X-RateLimit-Remaining: 450
X-RateLimit-Reset: 1735689600
```

---

## 📊 Webhooks (Enterprise)

Pro Enterprise zákazníky je k dispozici webhook notifikace:

```json
{
  "event": "query.completed",
  "data": {
    "query_id": "q_abc123def456",
    "user_id": "550e8400-e29b-41d4-a716-446655440000"
  },
  "timestamp": "2025-12-15T10:30:00Z"
}
```

---

*Dokument vytvořen: 15.12.2025*
