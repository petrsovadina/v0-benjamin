# Czech MedAI 🏥

> AI asistent nové generace pro české lékaře

**Czech MedAI** je pokročilý AI asistent speciálně navržený pro české zdravotníky. Poskytuje evidence-based odpovědi na klinické otázky s citacemi z PubMed, SÚKL a českých guidelines. Umožňuje rychlé ověření úhrad VZP a integraci s českými EHR systémy.

## ✨ Klíčové vlastnosti

### 🤖 AI Chat v češtině
- Přirozený dialog v českém jazyce
- Evidence-based odpovědi do 5 sekund
- Citace z 29M+ vědeckých článků
- Podpora odborné české terminologie

### 📚 Evidence-based citace
- **PubMed** - odkazy na vědecké články s PMID
- **SÚKL** - referenční data ze Státního ústavu pro kontrolu léčiv
- **České guidelines** - národní doporučené postupy
- Každá odpověď s ověřitelnými zdroji

### 💳 VZP Navigator
- Okamžité ověření úhrad z veřejného zdravotního pojištění
- Aktuální data z VZP
- Rychlé vyhledávání léčivých přípravků a výkonů
- Přehledný výpis výsledků s detaily

### 📊 DeepConsult
- Hloubková analýza komplexních klinických případů
- Podrobný rozbor s literární rešerší
- Dostupné v Premium plánu (20×/měsíc)

### 🔔 SÚKL Alerts
- Automatické notifikace o změnách v SPC
- Upozornění na stažení šarží
- Nová varování a bezpečnostní informace

### 🌐 EHR Integrace
- REST API pro integraci s českými EHR systémy
- Podpora pro ICZ, CGM, Medisoft a další
- API přístup v Premium plánu

### 🔒 Bezpečnost a compliance
- **GDPR compliant** - data hostována v EU
- **MDR ready** - připraveno pro certifikaci zdravotnického prostředku
- Šifrovaná komunikace
- Bezpečné uložení dat

## 🏗️ Technologie

Toto je **full-stack aplikace** s odděleným frontendem a backendem.

### Frontend
- **Framework**: [Next.js](https://nextjs.org/) 16.0.7 (App Router)
- **React**: 19.2.0
- **TypeScript**: 5.9
- **Styling**: [Tailwind CSS](https://tailwindcss.com/) 4.1.9
- **UI Components**: [Radix UI](https://www.radix-ui.com/) / shadcn/ui
- **Form Handling**: React Hook Form + Zod validation
- **Charts**: Recharts 2.15.4
- **Icons**: Lucide React
- **Theme**: next-themes (dark/light mode)
- **Analytics**: Vercel Analytics

### Backend
- **Language**: Python 3.x
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Server**: Uvicorn (ASGI)
- **AI Orchestration**: [LangGraph](https://github.com/langchain-ai/langgraph) + [LangChain](https://www.langchain.com/)
- **LLM Providers**:
  - Anthropic (Claude 3) - Hlavní AI model
  - OpenAI - Embeddings pro sémantické vyhledávání
  - Google - Audio transkripce
- **Data Processing**: Pandas, openpyxl
- **Database Client**: Supabase Python SDK

### Database
- **BaaS**: [Supabase](https://supabase.com/)
  - Authentication
  - PostgreSQL Database
  - Real-time subscriptions
  - Row Level Security (RLS)

### Package Managers
- **Frontend**: pnpm - Fast, disk space efficient package manager
- **Backend**: pip - Python package installer

## 📁 Struktura projektu

```
v0-benjamin/
├── app/                          # Next.js App Router (Frontend)
│   ├── _components/              # Shared app components
│   ├── api/                      # Next.js API routes
│   │   ├── chat/                 # Chat proxy endpoint
│   │   ├── epicrisis/            # Epicrisis generation endpoint
│   │   ├── transcribe/           # Audio transcription endpoint
│   │   └── translate/            # Translation endpoint
│   ├── auth/                     # Autentizační stránky
│   │   ├── login/                # Přihlášení
│   │   ├── register/             # Registrace
│   │   ├── forgot-password/      # Obnovení hesla
│   │   └── reset-password/       # Reset hesla
│   ├── dashboard/                # Hlavní aplikace (chráněno)
│   │   ├── chat/                 # AI Chat interface
│   │   ├── epikriza/             # Generátor epikrizy
│   │   ├── guidelines/           # České guidelines
│   │   ├── translator/           # Překladač lékařských textů
│   │   ├── vzp-navigator/        # VZP vyhledávač
│   │   ├── history/              # Historie dotazů
│   │   └── settings/             # Uživatelská nastavení
│   ├── docs/                     # Dokumentace (Nextra)
│   │   ├── developer/            # Vývojářská dokumentace
│   │   └── user/                 # Uživatelská dokumentace
│   ├── theme-test/               # Testovací stránka témat
│   ├── layout.tsx                # Root layout
│   ├── page.tsx                  # Landing page
│   └── globals.css               # Globální styly
├── backend/                      # Python FastAPI Backend
│   ├── app/                      # FastAPI aplikace
│   │   ├── api/                  # API route handlers
│   │   ├── core/                 # Core configuration
│   │   └── models/               # Pydantic models
│   ├── data_processing/          # ETL pipeline pro lékařská data
│   ├── pipeline/                 # SÚKL data pipeline
│   ├── mcp_servers/              # Model Context Protocol servers
│   ├── main.py                   # FastAPI entry point
│   ├── agent_graph.py            # LangGraph state machine (klinické dotazy)
│   ├── epicrisis_graph.py        # LangGraph pro epikrizy
│   ├── requirements.txt          # Python dependencies
│   ├── .env.example              # Backend environment variables template
│   └── README.md                 # Backend dokumentace
├── components/                   # React komponenty (Frontend)
│   ├── auth/                     # Autentizační komponenty
│   ├── dashboard/                # Dashboard komponenty
│   │   ├── chat-interface.tsx
│   │   ├── chat-message.tsx
│   │   ├── chat-citations.tsx
│   │   ├── vzp-search-interface.tsx
│   │   └── ...
│   ├── landing/                  # Landing page komponenty
│   │   ├── landing-header.tsx
│   │   ├── hero-section.tsx
│   │   ├── features-section.tsx
│   │   └── ...
│   ├── ui/                       # Reusable UI komponenty (shadcn/ui)
│   ├── error-boundary.tsx        # Error boundary
│   └── theme-provider.tsx        # Theme context provider
├── lib/                          # Utility funkce (Frontend)
│   ├── supabase/                 # Supabase konfigurace
│   │   ├── client.ts             # Client-side Supabase client
│   │   ├── server.ts             # Server-side Supabase client
│   │   ├── middleware.ts         # Session middleware
│   │   └── database.types.ts     # Generated DB types
│   ├── auth-actions.ts           # Server actions pro auth
│   ├── auth-context.tsx          # Auth context provider
│   └── utils.ts                  # Pomocné funkce (cn, atd.)
├── public/                       # Statické soubory
├── middleware.ts                 # Next.js middleware (auth)
├── next.config.mjs               # Next.js konfigurace
├── tailwind.config.ts            # Tailwind konfigurace
├── components.json               # shadcn/ui konfigurace
├── tsconfig.json                 # TypeScript konfigurace
├── package.json                  # NPM dependencies
├── pnpm-lock.yaml                # pnpm lock file
├── CLAUDE.md                     # Dokumentace pro Claude Code
└── README.md                     # Tento soubor
```

## 🚀 Začínáme

### Požadavky

- **Node.js** 18.x nebo vyšší
- **pnpm** 8.x nebo vyšší
- **Python** 3.10 nebo vyšší
- **Supabase účet** (zdarma na [supabase.com](https://supabase.com))
- **API klíče**:
  - Anthropic API key (Claude 3)
  - OpenAI API key (pro embeddings)
  - Google API key (pro audio transkripci)

### Instalace

#### 1. Klonujte repozitář

```bash
git clone <repository-url>
cd v0-benjamin
```

#### 2. Frontend Setup

**Nainstalujte závislosti:**
```bash
pnpm install
```

**Nastavte environment variables:**

Vytvořte soubor `.env.local` v kořenovém adresáři:

```env
# Supabase
NEXT_PUBLIC_SUPABASE_URL=your_supabase_project_url
NEXT_PUBLIC_SUPABASE_PUBLISHABLE_DEFAULT_KEY=your_supabase_anon_key
```

**Jak získat Supabase credentials:**
1. Vytvořte projekt na [supabase.com](https://supabase.com)
2. Jděte do Settings → API
3. Zkopírujte `Project URL` a `anon/public` klíč

**Spusťte vývojový server:**
```bash
pnpm dev
```

Frontend bude dostupný na [http://localhost:3000](http://localhost:3000)

#### 3. Backend Setup

**Vytvořte Python virtual environment:**
```bash
python -m venv backend/venv
source backend/venv/bin/activate  # macOS/Linux
# .\backend\venv\Scripts\activate  # Windows
```

**Nainstalujte Python závislosti:**
```bash
pip install -r backend/requirements.txt
```

**Nastavte backend environment variables:**

Vytvořte soubor `.env` v adresáři `backend/` (zkopírujte z `backend/.env.example`):

```env
# AI Provider Keys
ANTHROPIC_API_KEY=your_anthropic_api_key       # POVINNÉ - Claude 3
OPENAI_API_KEY=your_openai_api_key             # POVINNÉ - Embeddings
GOOGLE_API_KEY=your_google_api_key             # POVINNÉ - Audio transkripce

# Database
SUPABASE_URL=your_supabase_url                 # Stejné jako frontend
SUPABASE_KEY=your_supabase_service_role_key   # Service role key pro pipeline

# Optional
ENVIRONMENT=development
LOG_LEVEL=INFO
```

**Spusťte backend server:**

**DŮLEŽITÉ**: Spouštějte z kořenového adresáře projektu (ne z `backend/`):

```bash
# Z v0-benjamin/ (kořenový adresář)
uvicorn backend.main:app --reload --port 8000
```

Backend bude dostupný na:
- **API**: `http://localhost:8000`
- **Dokumentace**: `http://localhost:8000/docs` (Swagger UI)
- **Health check**: `http://localhost:8000/health`

## 🗄️ Supabase Setup

### Database Schema

Pro plnou funkčnost aplikace budete potřebovat vytvořit následující tabulky v Supabase:

```sql
-- Users table (rozšíření Supabase auth.users)
create table public.profiles (
  id uuid references auth.users on delete cascade primary key,
  email text,
  full_name text,
  avatar_url text,
  subscription_tier text default 'free',
  created_at timestamp with time zone default now(),
  updated_at timestamp with time zone default now()
);

-- Chat history
create table public.chat_messages (
  id uuid default gen_random_uuid() primary key,
  user_id uuid references public.profiles(id) on delete cascade,
  role text not null,
  content text not null,
  citations jsonb,
  created_at timestamp with time zone default now()
);

-- VZP searches
create table public.vzp_searches (
  id uuid default gen_random_uuid() primary key,
  user_id uuid references public.profiles(id) on delete cascade,
  query text not null,
  results jsonb,
  created_at timestamp with time zone default now()
);

-- SÚKL drugs database
create table public.sukl_drugs (
  id uuid default gen_random_uuid() primary key,
  sukl_code text unique not null,
  name text not null,
  atc_code text,
  atc_name text,
  form text,
  strength text,
  package_size text,
  registration_holder text,
  price numeric,
  reimbursement_category text,
  embedding vector(1536),  -- OpenAI embeddings pro sémantické vyhledávání
  created_at timestamp with time zone default now(),
  updated_at timestamp with time zone default now()
);

-- Enable Row Level Security
alter table public.profiles enable row level security;
alter table public.chat_messages enable row level security;
alter table public.vzp_searches enable row level security;
alter table public.sukl_drugs enable row level security;

-- RLS Policies
create policy "Users can view own profile"
  on public.profiles for select
  using (auth.uid() = id);

create policy "Users can update own profile"
  on public.profiles for update
  using (auth.uid() = id);

create policy "Users can view own messages"
  on public.chat_messages for select
  using (auth.uid() = user_id);

create policy "Users can insert own messages"
  on public.chat_messages for insert
  with check (auth.uid() = user_id);

create policy "Users can view own searches"
  on public.vzp_searches for select
  using (auth.uid() = user_id);

create policy "Users can insert own searches"
  on public.vzp_searches for insert
  with check (auth.uid() = user_id);

create policy "Public read access to SÚKL drugs"
  on public.sukl_drugs for select
  using (true);

-- Indexes pro výkon
create index idx_sukl_drugs_code on public.sukl_drugs(sukl_code);
create index idx_sukl_drugs_name on public.sukl_drugs using gin(to_tsvector('czech', name));
create index idx_chat_messages_user on public.chat_messages(user_id);
```

### Vector Extension (pro sémantické vyhledávání)

V Supabase SQL editoru povolte pgvector extension:

```sql
create extension if not exists vector;
```

### Authentication Setup

1. V Supabase Dashboard jděte do **Authentication → Providers**
2. Povolte **Email** provider
3. (Volitelně) Nakonfigurujte další providery (Google, GitHub, atd.)

## 🛠️ Vývoj

### Frontend Příkazy

```bash
# Vývojový server s hot reload
pnpm dev

# Production build
pnpm build

# Spuštění production serveru
pnpm start

# Linting
pnpm lint
```

### Backend Příkazy

**DŮLEŽITÉ**: Všechny backend příkazy spouštějte z **kořenového adresáře** projektu (`v0-benjamin/`), ne z `backend/`.

```bash
# Spuštění API serveru (development)
uvicorn backend.main:app --reload --port 8000

# Spuštění API serveru (production)
uvicorn backend.main:app --host 0.0.0.0 --port 8000

# Testování
cd backend && pytest

# Spuštění SÚKL data pipeline (viz níže)
python -m backend.pipeline.run_pipeline --drugs --pricing --documents
```

### SÚKL Data Pipeline

Backend obsahuje robustní ETL pipeline pro zpracování dat ze SÚKL (Státní ústav pro kontrolu léčiv).

**Pipeline zpracovává:**
1. **DLP (Léčiva)** - měsíční aktualizace a eRecept data
2. **Pricing (Ceny)** - aktuální ceny a historické archivy
3. **Documents** - odkazy na SPC/PIL dokumenty
4. **Vectors** - sémantické embeddings pro vyhledávání (OpenAI)

**Spuštění celého pipeline:**

```bash
# Z v0-benjamin/ (kořenový adresář)
python -m backend.pipeline.run_pipeline --drugs --pricing --documents --with-embeddings
```

**Jednotlivé kroky:**

```bash
# 1. Stáhnout raw CSV ze SÚKL
python -m backend.pipeline.run_pipeline --download

# 2. Zpracovat léčiva + generovat embeddings
python -m backend.pipeline.run_pipeline --drugs --with-embeddings

# 3. Zpracovat ceny (current + historical)
python -m backend.pipeline.run_pipeline --pricing

# 4. Zpracovat SPC/PIL dokumenty
python -m backend.pipeline.run_pipeline --documents
```

**Parametry:**
- `--limit <číslo>`: Zpracovat pouze N položek (pro testování)
- `--with-embeddings`: Generovat OpenAI vektory (stojí peníze!)
- `--dry-run`: Spustit bez zápisu do databáze

**⚠️ Upozornění**: Generování embeddings (`--with-embeddings`) stojí peníze (OpenAI API). Pro ~20,000 léků je to přibližně $5-10.

## 🔌 Backend API

Backend poskytuje RESTful API pro všechny AI funkce.

### Autentizace

Všechny endpointy (kromě `/docs`, `/health`) vyžadují Bearer token z Supabase Auth:

```http
Authorization: Bearer <jwt_token_from_supabase>
```

### Hlavní Endpointy

#### Chat & Query
- `POST /api/v1/query` - Standardní chat (non-streaming)
- `POST /api/v1/query/stream` - Streaming chat (NDJSON)

```json
{
  "message": "Jaké je dávkování aspirinu?",
  "history": [],
  "session_id": "optional-uuid"
}
```

#### Drugs (SÚKL databáze)
- `GET /api/v1/drugs/search?q=aspirin&limit=20` - Sémantické vyhledávání
- `GET /api/v1/drugs/{sukl_code}` - Detail léku

#### AI Tools
- `POST /api/v1/ai/epicrisis` - Generování epikrizy z poznámek
- `POST /api/v1/ai/translate` - Překlad lékařského textu
- `POST /api/v1/ai/transcribe` - Transkripce audio souboru

**Kompletní API dokumentace**: `http://localhost:8000/docs`

## 🧩 Přidání nových komponent

### Frontend (shadcn/ui)

Projekt používá shadcn/ui komponenty. Pro přidání nové komponenty:

```bash
npx shadcn@latest add [component-name]
```

Komponenty jsou přidány do `components/ui/` a lze je plně přizpůsobit.

### Theme Customization

Upravte CSS proměnné v `app/globals.css` pro změnu barev a stylů:

```css
@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --primary: 221.2 83.2% 53.3%;
    /* ... další proměnné */
  }
}
```

## 💰 Cenové plány

### Free - 0 Kč/měsíc
- ✅ 50 dotazů měsíčně
- ✅ Základní AI odpovědi
- ✅ PubMed citace
- ✅ Webové rozhraní

### Professional - 990 Kč/měsíc
- ✅ Neomezené dotazy
- ✅ VZP Navigator
- ✅ SÚKL databáze
- ✅ Historie dotazů
- ✅ Prioritní podpora
- ✅ CME kredity

### Premium - 1 990 Kč/měsíc
- ✅ Vše z Professional plánu
- ✅ DeepConsult (20×/měsíc)
- ✅ API přístup
- ✅ Týmový účet (5 uživatelů)
- ✅ Personalizace
- ✅ Offline přístup

### Enterprise
Kontaktujte nás pro řešení pro celou nemocnici nebo síť ordinací.

## 📦 Deployment

### Frontend Deployment (Vercel - doporučeno)

1. **Pushněte kód na GitHub**

2. **Importujte projekt do Vercel**
   - Jděte na [vercel.com](https://vercel.com)
   - Klikněte na "Import Project"
   - Vyberte váš GitHub repozitář

3. **Nastavte environment variables**
   - Přidejte `NEXT_PUBLIC_SUPABASE_URL`
   - Přidejte `NEXT_PUBLIC_SUPABASE_PUBLISHABLE_DEFAULT_KEY`

4. **Deploy**
   - Vercel automaticky buildne a nasadí aplikaci
   - Každý push do main větve spustí nový deployment

**Jiné platformy**: Projekt je kompatibilní s Netlify, Cloudflare Pages, Railway.

### Backend Deployment

Backend lze nasadit několika způsoby:

#### Option 1: Docker (doporučeno)

Backend obsahuje `Dockerfile`:

```bash
# Build image
docker build -t czech-medai-backend ./backend

# Run container
docker run -p 8000:8000 \
  -e ANTHROPIC_API_KEY=your_key \
  -e OPENAI_API_KEY=your_key \
  -e SUPABASE_URL=your_url \
  -e SUPABASE_KEY=your_key \
  czech-medai-backend
```

#### Option 2: Railway / Render / Fly.io

1. Vytvořte nový Python service
2. Nastavte build command: `pip install -r backend/requirements.txt`
3. Nastavte start command: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
4. Přidejte environment variables (ANTHROPIC_API_KEY, atd.)

#### Option 3: VPS (Manuální)

```bash
# Na serveru
git clone <repo>
cd v0-benjamin/backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Spusťte s gunicorn + uvicorn workers
gunicorn backend.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

**⚠️ Důležité pro production:**
- Nastavte HTTPS/SSL certifikáty
- Použijte process manager (systemd, supervisor)
- Nastavte CORS správně v `backend/app/core/config.py`
- Zvažte rate limiting a monitoring

## 🧪 Testing

### Frontend Testing

Testing framework zatím není nakonfigurován. Doporučené setup:

```bash
# Instalace testing dependencies
pnpm add -D jest @testing-library/react @testing-library/jest-dom
pnpm add -D @testing-library/user-event vitest
```

### Backend Testing

Backend používá pytest:

```bash
cd backend
pytest                      # Všechny testy
pytest tests/test_api.py   # Specifický soubor
pytest -v                   # Verbose mode
pytest --cov               # S coverage reportem
```

## 📚 Dokumentace

- **CLAUDE.md** - Pokyny pro Claude Code při vývoji
- **backend/README.md** - Detailní backend dokumentace
- **app/docs/** - Nextra dokumentace (developer + user docs)
- **API Docs** - `http://localhost:8000/docs` (když běží backend)

## 📄 Licence

Tento projekt je proprietární software. Všechna práva vyhrazena.

## 🤝 Kontakt a podpora

- **Web**: czechmedai.cz *(připravujeme)*
- **Email**: podpora@czechmedai.cz *(připravujeme)*
- **Dokumentace**: docs.czechmedai.cz *(připravujeme)*
- **GitHub**: Tento repozitář

## 🙏 Acknowledgments

- Postaveno s [Next.js](https://nextjs.org/) a [FastAPI](https://fastapi.tiangolo.com/)
- UI komponenty od [Radix UI](https://www.radix-ui.com/)
- Database powered by [Supabase](https://supabase.com/)
- AI orchestration by [LangGraph](https://github.com/langchain-ai/langgraph)
- Ikony od [Lucide](https://lucide.dev/)

---

**Vytvořeno s ❤️ pro české lékaře**

*Poslední aktualizace: leden 2025*
