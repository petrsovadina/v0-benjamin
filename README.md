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

### Frontend
- **Framework**: [Next.js](https://nextjs.org/) 16.0.7 (App Router)
- **React**: 19.2.0
- **TypeScript**: 5.x
- **Styling**: [Tailwind CSS](https://tailwindcss.com/) 4.1.9
- **UI Components**: [Radix UI](https://www.radix-ui.com/)
- **Form Handling**: React Hook Form + Zod validation
- **Charts**: Recharts 2.15.4
- **Icons**: Lucide React
- **Theme**: next-themes (dark/light mode)
- **Analytics**: Vercel Analytics

### Backend & Database
- **BaaS**: [Supabase](https://supabase.com/)
  - Authentication
  - PostgreSQL Database
  - Real-time subscriptions
  - Row Level Security (RLS)

### Package Manager
- **pnpm** - Fast, disk space efficient package manager

## 📁 Struktura projektu

```
v0-benjamin/
├── app/                          # Next.js App Router
│   ├── auth/                     # Autentizační stránky
│   │   ├── login/               # Přihlášení
│   │   ├── register/            # Registrace
│   │   ├── forgot-password/     # Obnovení hesla
│   │   └── reset-password/      # Reset hesla
│   ├── dashboard/               # Hlavní aplikace (chráněno)
│   │   ├── chat/                # AI Chat interface
│   │   ├── vzp-navigator/       # VZP vyhledávač
│   │   ├── history/             # Historie dotazů
│   │   └── settings/            # Uživatelská nastavení
│   ├── theme-test/              # Testovací stránka témat
│   ├── layout.tsx               # Root layout
│   ├── page.tsx                 # Landing page
│   └── globals.css              # Globální styly
├── components/                   # React komponenty
│   ├── auth/                    # Autentizační komponenty
│   ├── dashboard/               # Dashboard komponenty
│   │   ├── chat-interface.tsx
│   │   ├── chat-message.tsx
│   │   ├── chat-citations.tsx
│   │   ├── vzp-search-interface.tsx
│   │   ├── vzp-result-card.tsx
│   │   ├── history-interface.tsx
│   │   ├── settings-interface.tsx
│   │   ├── header.tsx
│   │   └── sidebar.tsx
│   ├── landing/                 # Landing page komponenty
│   │   ├── landing-header.tsx
│   │   ├── hero-section.tsx
│   │   ├── features-section.tsx
│   │   ├── pricing-section.tsx
│   │   ├── testimonials-section.tsx
│   │   └── landing-footer.tsx
│   ├── ui/                      # Reusable UI komponenty (Radix)
│   └── theme-provider.tsx       # Theme context provider
├── lib/                         # Utility funkce
│   ├── supabase/               # Supabase konfigurace
│   │   ├── client.ts           # Client-side Supabase client
│   │   ├── server.ts           # Server-side Supabase client
│   │   └── middleware.ts       # Session middleware
│   ├── auth-actions.ts         # Server actions pro auth
│   ├── auth-context.tsx        # Auth context provider
│   └── utils.ts                # Pomocné funkce
├── public/                      # Statické soubory
├── styles/                      # Dodatečné styly
├── scripts/                     # Build a utility skripty
├── middleware.ts                # Next.js middleware
├── next.config.mjs             # Next.js konfigurace
├── tailwind.config.ts          # Tailwind konfigurace
├── components.json             # shadcn/ui konfigurace
├── tsconfig.json               # TypeScript konfigurace
├── package.json                # NPM dependencies
└── pnpm-lock.yaml              # pnpm lock file
```

## 🚀 Začínáme

### Požadavky

- **Node.js** 18.x nebo vyšší
- **pnpm** 8.x nebo vyšší
- **Supabase účet** (zdarma na [supabase.com](https://supabase.com))

### Instalace

1. **Klonujte repozitář**
```bash
git clone <repository-url>
cd v0-benjamin
```

2. **Nainstalujte závislosti**
```bash
pnpm install
```

3. **Nastavte prostředí**

Vytvořte soubor `.env.local` v kořenovém adresáři:

```env
# Supabase
NEXT_PUBLIC_SUPABASE_URL=your_supabase_project_url
NEXT_PUBLIC_SUPABASE_PUBLISHABLE_DEFAULT_KEY=your_supabase_anon_key

# Optional: API keys pro backend služby
# OPENAI_API_KEY=your_openai_api_key
# ANTHROPIC_API_KEY=your_anthropic_api_key
```

**Jak získat Supabase credentials:**
1. Vytvořte projekt na [supabase.com](https://supabase.com)
2. Jděte do Settings → API
3. Zkopírujte `Project URL` a `anon/public` klíč

4. **Spusťte vývojový server**
```bash
pnpm dev
```

Aplikace bude dostupná na [http://localhost:3000](http://localhost:3000)

## 🗄️ Supabase Setup

### Database Schema (příklad)

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

-- Enable Row Level Security
alter table public.profiles enable row level security;
alter table public.chat_messages enable row level security;
alter table public.vzp_searches enable row level security;

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
```

### Authentication Setup

1. V Supabase Dashboard jděte do **Authentication → Providers**
2. Povolte **Email** provider
3. (Volitelně) Nakonfigurujte další providery (Google, GitHub, atd.)

## 🛠️ Vývoj

### Dostupné skripty

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

### Přidání nových komponent

Projekt používá shadcn/ui komponenty. Pro přidání nové komponenty:

```bash
npx shadcn-ui@latest add [component-name]
```

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

### Vercel (doporučeno)

1. **Pushněte kód na GitHub**

2. **Importujte projekt do Vercel**
   - Jděte na [vercel.com](https://vercel.com)
   - Klikněte na "Import Project"
   - Vyberte váš GitHub repozitář

3. **Nastavte environment variables**
   - Přidejte všechny proměnné z `.env.local`
   - Zkontrolujte, že `NEXT_PUBLIC_*` proměnné jsou správně nastaveny

4. **Deploy**
   - Vercel automaticky buildne a nasadí aplikaci
   - Každý push do main větve spustí nový deployment

### Jiné platformy

Projekt je kompatibilní s jakoukoliv platformou podporující Next.js:
- **Netlify**: Použijte Next.js runtime
- **Cloudflare Pages**: Podporuje Next.js
- **Railway**: One-click deploy
- **Docker**: Vytvořte vlastní Dockerfile

## 🧪 Testing

> **Poznámka**: Testing framework zatím není nakonfigurován. Doporučené setup:

```bash
# Instalace testing dependencies
pnpm add -D jest @testing-library/react @testing-library/jest-dom
pnpm add -D @testing-library/user-event vitest
```

## 📄 Licence

Tento projekt je proprietární software. Všechna práva vyhrazena.

## 🤝 Kontakt a podpora

- **Web**: [czechmedai.cz](https://czechmedai.cz) (placeholder)
- **Email**: podpora@czechmedai.cz (placeholder)
- **Dokumentace**: [docs.czechmedai.cz](https://docs.czechmedai.cz) (placeholder)

## 🙏 Acknowledgments

- Postaveno s [Next.js](https://nextjs.org/)
- UI komponenty od [Radix UI](https://www.radix-ui.com/)
- Backend powered by [Supabase](https://supabase.com/)
- Ikony od [Lucide](https://lucide.dev/)

---

**Vytvořeno s ❤️ pro české lékaře**
