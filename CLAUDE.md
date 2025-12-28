# CLAUDE.md

Tento soubor poskytuje pokyny pro Claude Code (claude.ai/code) při práci s kódem v tomto úložišti.



## Přehled projektu

**Czech MedAI (Benjamin)** je AI asistent pro české zdravotníky, který poskytuje klinické odpovědi založené na důkazech s citacemi z PubMed, SÚKL (Státní ústav pro kontrolu léčiv) a českých lékařských pokynů. Aplikace zahrnuje ověření VZP (zdravotní pojištění) a integraci EHR.

Jedná se o **full-stack projekt** s:
- **Frontendem**: aplikace Next.js 16 App Router (TypeScript, React 19, Tailwind CSS)
- **Backendem**: služba Python FastAPI se zpracováním klinických dotazů na základě LangGraph
- **Databází**: Supabase (PostgreSQL s Row Level Security)

## Konfigurace prostředí

### 🔒 Bezpečnost API klíčů

**DŮLEŽITÉ**: Tento projekt používá citlivé API klíče, které **NESMÍ být commitovány do gitu**.

#### Nastavení pro nové vývojáře:

1. **Zkopírujte example soubory**:
```bash
# Frontend
cp .env.example .env.local

# Backend
cp backend/.env.example backend/.env

# Claude Code (pokud používáte)
cp .auto-claude/.env.example .auto-claude/.env
```

2. **Vyplňte skutečné API klíče** v `.env` souborech:
   - `ANTHROPIC_API_KEY` - z https://console.anthropic.com/settings/keys
   - `NEXT_PUBLIC_SUPABASE_URL` - z Supabase Dashboard
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY` - z Supabase Dashboard
   - `SUPABASE_KEY` (service role) - z Supabase Dashboard
   - Další klíče dle potřeby

3. **Ověřte .gitignore**:
```bash
# Tyto soubory by NIKDY neměly být v gitu:
.env
.env.local
backend/.env
.auto-claude/.env
```

#### ⚠️ Co NIKDY nedělat:
- ❌ Nepushujte soubory `.env` do gitu
- ❌ Nepublikujte API klíče v issue/PR
- ❌ Nesdílejte klíče přes veřejné kanály
- ✅ Používejte pouze `.env.example` s placeholdery

## Vývojové příkazy

### Frontend (Next.js)

```bash
# Instalace závislostí
pnpm install

# Vývojový server (http://localhost:3000)
pnpm dev

# Produkční sestavení
pnpm build

# Spuštění produkčního serveru
pnpm start

# Linting
pnpm lint
```

**Poznámka**: Tento projekt používá jako správce balíčků **pnpm**, nikoli npm nebo yarn.

### Backend (Python FastAPI)

```bash
# Přejít do adresáře backend
cd backend/

# Instalace závislostí Pythonu
pip install -r requirements.txt

# Spusťte vývojový server (http://localhost:8000)
uvicorn main:app --reload

# Spusťte s konkrétním hostitelem/portem
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Architektura

### Architektura frontendu (Next.js App Router)

Frontend používá Next.js 16 App Router s jasným rozdělením mezi:

1. **Veřejné trasy** (`app/`):
   - Úvodní stránka (`app/page.tsx`)
   - Ověřovací toky (`app/auth/login/`, `app/auth/register/` atd.)
   - Dokumentace (`app/docs/`)

2. **Chráněné trasy** (`app/dashboard/`):
   - Rozhraní chatu (`app/dashboard/chat/`)
   - VZP Navigator (`app/dashboard/vzp-navigator/`)
   - Historie (`app/dashboard/history/`)
   - Nastavení (`app/dashboard/settings/`)

3. **Organizace komponent**:
   - `components/auth/` – Ověřovací formuláře a toky
   - `components/dashboard/` – Komponenty specifické pro dashboard (chat, vyhledávání VZP atd.)
   - `components/landing/` – Komponenty marketingové/vstupní stránky
   - `components/ui/` – Opakovaně použitelné komponenty uživatelského rozhraní z Radix UI/shadcn

4. **Struktura knihovny** (`lib/`):
   - `lib/supabase/` – Konfigurace klienta Supabase (strana klienta, strana serveru, middleware)
   - `lib/auth-actions.ts` – Akce serveru pro ověřování
   - `lib/auth-context.tsx` – Kontext ověřování na straně klienta
   - `lib/utils.ts` – Pomocné funkce (cn pro slučování className atd.)

**Aliasy cest**: Použijte `@/` pro import z kořenového adresáře projektu (např. `import { Button } from „@/components/ui/button“`)

**Proces ověřování**:
- Middleware (`middleware.ts`) zachycuje všechny požadavky a aktualizuje relaci Supabase
- Chráněné trasy kontrolují ověření v serverových komponentách pomocí `lib/supabase/server.ts`
- Stav ověření na straně klienta je spravován prostřednictvím `AuthProvider` v `lib/auth-context.tsx`

### Architektura backendu (Python FastAPI)

Backend je aplikace FastAPI s LangGraph pro zpracování klinických dotazů:

1. **Základní struktura** (`backend/`):
   - `main.py` - vstupní bod aplikace FastAPI
   - `agent_graph.py` - stavový stroj LangGraph pro klinické dotazy
   - `epicrisis_graph.py` - specializovaný graf pro generování epikrisis (lékařského shrnutí)

2. **Organizace API** (`backend/app/`):
   - `app/api/` – obslužné rutiny API
   - `app/core/` – základní konfigurace a nástroje
   - `app/models/` – modely Pydantic pro ověřování požadavků/odpovědí

3. **Zpracování dat** (`backend/data_processing/`):
   - Pipeline pro zpracování zdrojů lékařských dat (SÚKL, PubMed, české směrnice)
   - Transformace a indexování dat pro RAG (Retrieval-Augmented Generation)

4. **MCP servery** (`backend/mcp_servers/`):
   - Servery Model Context Protocol pro externí integrace

**LangGraph State Machine**:
Zpracování klinických dotazů využívá architekturu stavového stroje (`agent_graph.py`), která:
- směruje dotazy podle typu (klinická otázka, informace o léku, ověření VZP)
- načítá relevantní kontext z lékařských databází
- generuje odpovědi založené na důkazech s citacemi
- formátuje výstup s příslušnými lékařskými odkazy

### Databáze (Supabase)

Klíčové tabulky databáze (úplné schéma viz README.md):

- `profiles` – Rozšířené informace o uživateli nad rámec auth.users
- `chat_messages` – Historie chatu s citacemi (JSONB)
- `vzp_searches` – Historie vyhledávání VZP

**Row Level Security (RLS)**: Všechny tabulky používají zásady RLS, aby bylo zajištěno, že uživatelé mají přístup pouze ke svým vlastním datům.

### Komunikace mezi frontendem a backendem

Frontend komunikuje s backendem prostřednictvím:
1. **Přímých volání API** do koncových bodů FastAPI (např. `/api/chat`, `/api/vzp-search`)
2. **Supabase** pro autentizaci, uživatelské profily a trvalé uchovávání dat
3. **Předplatného v reálném čase** prostřednictvím Supabase pro živé aktualizace (pokud je implementováno)

## Klíčové technické podrobnosti

### Konfigurace TypeScript

- **Povolení přísného režimu** – všechny typy musí být správně definovány
- **Aliasy cest**: `@/*` mapuje na kořen projektu
- **JSX**: Používá `react-jsx` (není třeba importovat React do souborů)
- **Rozlišení modulů**: režim `bundler` pro kompatibilitu s Next.js

**Důležité**: Projekt má v souboru `next.config.mjs` nastaveno `ignoreBuildErrors: true` – jedná se o dočasnou konfiguraci, která by měla být odstraněna, jakmile budou vyřešeny všechny chyby TypeScriptu.

### Stylování

- **Tailwind CSS 4.1.9** s vlastní konfigurací
- **CSS proměnné** pro témata (definované v `app/globals.css`)
- **Tmavý/světlý režim** prostřednictvím balíčku `next-themes`
- **Stylování komponent**: Použijte nástroj `cn()` z `lib/utils.ts` ke sloučení tříd Tailwind

Příklad:
```tsx
import { cn } from „@/lib/utils“

<div className={cn(„base-classes“, conditional && „conditional-classes“, className)} />
```

### Integrace Supabase

**Tři klienti Supabase** v závislosti na kontextu:

1. **Na straně klienta** (`lib/supabase/client.ts`):
```tsx
   import { createClient } from „@/lib/supabase/client“
   const supabase = createClient()
   ```

2. **Komponenty serveru** (`lib/supabase/server.ts`):
   ```tsx
   import { createClient } from „@/lib/supabase/server“
   const supabase = await createClient()
   ```

3. **Middleware** (`lib/supabase/middleware.ts`):
   Automaticky používáno `middleware.ts` k obnovení relací

### Zpracování formulářů

Formuláře používají **React Hook Form** s validací **Zod**:

```tsx
import { useForm } from „react-hook-form“
import { zodResolver } from „@hookform/resolvers/zod“
import { z } from „zod“

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
})

const form = useForm({
  resolver: zodResolver(schema),
})
```

### Přidání komponent uživatelského rozhraní

Tento projekt používá komponenty **shadcn/ui**. Chcete-li přidat novou komponentu:

```bash
npx shadcn@latest add [název komponenty]
```

Komponenty se přidávají do `components/ui/` a lze je přizpůsobit.

## Důležité vzory

### Akce serveru vs. trasy API

- **Akce serveru** (`lib/auth-actions.ts`) – preferované pro jednoduché mutace a autentizační toky
- **Trasy API** (`app/api/`) – používané pro složitou logiku nebo když potřebujete větší kontrolu nad požadavky/odpověďmi

### Chráněné trasy

Chráněné trasy by měly:
1. Kontrolovat ověření v serverových komponentách pomocí `lib/supabase/server.ts`
2. Přesměrovat na `/auth/login`, pokud nejsou ověřeny
3. Používat `AuthProvider` v `layout.tsx` pro stav ověření na straně klienta

Příklad:
```tsx
// app/dashboard/page.tsx
import { createClient } from „@/lib/supabase/server“
import { redirect } from „next/navigation“

export default async function DashboardPage() {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    redirect(„/auth/login“)
  }

  // Renderovat chráněný obsah
}
```

### Zpracování chyb

Projekt obsahuje hranici chyb (`components/error-boundary.tsx`) pro elegantní zpracování chyb v uživatelském rozhraní.

## Proměnné prostředí

Požadované proměnné prostředí (viz `.env.local` nebo backend `.env`):

**Frontend**:
- `NEXT_PUBLIC_SUPABASE_URL` - URL projektu Supabase
- `NEXT_PUBLIC_SUPABASE_PUBLISHABLE_DEFAULT_KEY` - Anonymní klíč Supabase

**Backend**:
- `OPENAI_API_KEY` - Klíč API OpenAI pro LLM
- `ANTHROPIC_API_KEY` - klíč API Anthropic (volitelné)
- Řetězce připojení k databázi pro SÚKL a další zdroje dat

## Časté problémy

### Chyby při kompilaci

Pokud během kompilace narazíte na chyby TypeScriptu:
1. Zkontrolujte, zda všechny importy používají správné aliasy cest (`@/`)
2. Ověřte, zda jsou generovány typy Supabase: `supabase gen types typescript`
3. Spusťte `pnpm build`, abyste viděli všechny chyby typu najednou

### Problémy se seancí Supabase

Pokud se zdá, že ověřování nefunguje:
1. Ověřte, zda middleware běží na všech trasách (zkontrolujte konfiguraci matcheru `middleware.ts`)
2. Ujistěte se, že používáte správného klienta Supabase pro daný kontext (klient vs. server)
3. Zkontrolujte konzoli prohlížeče, zda neobsahuje chyby CORS nebo problémy s cookies.

## Testování

**Poznámka**: Testovací framework ještě není nakonfigurován. Projekt je nastaven pro testování pomocí Vitest nebo Jest + React Testing Library, ale v současné době nejsou napsány žádné testy.

## Nasazení

Projekt je nakonfigurován pro nasazení **Vercel** s `output: „standalone“` v `next.config.mjs`.

**Nasazení backendu**: Pythonový backend lze nasadit na jakoukoli platformu podporující FastAPI (např. Railway, Render, Docker container).

## Komunikační jazyk

**Český jazyk**: Tento projekt je určen pro české zdravotnické pracovníky. Obsah určený pro uživatele, chybové zprávy a dokumentace by měly být v češtině. Komentáře kódu a technická dokumentace mohou být v angličtině nebo češtině.