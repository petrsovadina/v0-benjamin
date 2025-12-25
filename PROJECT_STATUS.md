# Analýza stavu projektu: Czech MedAI (Benjamin)

## 1. Souhrn projektu
Jedná se o moderní webovou aplikaci **Czech MedAI** postavenou na **Next.js 16 (App Router)**, která slouží jako AI asistent pro lékařské dotazy a vyhledávání informací o úhradách léků (VZP Navigator). Projekt je ve fázi **pokročilého prototypu / MVP**, kde je dokončena infrastruktura a autentizace, ale aplikační logika zatím běží na mock datech.

## 2. Technologický Stack
- **Frontend**: Next.js 16, React 19, Tailwind CSS 4, Shadcn UI (`radix-ui`), Lucide React.
- **Backend / BaaS**: **Supabase** (PostgreSQL, Auth, Storage).
- **Jazyk**: TypeScript.
- **State Management**: React Hooks (`useState`, `useContext` pro Auth).

## 3. Detailní analýza funkcionalit

### ✅ A. Autentizace a Uživatelé (DOKONČENO)
- **Implementace**: Plně funkční přes Supabase Auth.
- **Flows**: Registrace, Přihlášení, Zapomenuté heslo, Reset hesla.
- **Infrastruktura**:
  - `lib/auth-actions.ts`: Server Actions pro auth operace.
  - `lib/auth-context.tsx`: Klientský kontext pro správu session.
  - `middleware.ts`: Ochrana `/dashboard` rout a přesměrování.
  - **Databáze**: Automatický trigger (`scripts/02-auth-trigger.sql`) vytváří profil v `user_profiles` při registraci.

### 🟡 B. Dashboard a UI (ČÁSTEČNĚ DOKONČENO)
- **Struktura**: Existuje layout s navigací (`sidebar`, `header`).
- **Komponenty**: Vytvořeny vizuální komponenty pro Chat, Historii a VZP Navigator.
- **Stav**: UI je hotové, ale komponenty (`ChatInterface`, `VzpSearchInterface`) zatím používají **mock data** (natvrdo napsaná v kódu) a simulují API volání pomocí `setTimeout`. **Nejsou napojeny na databázi.**

### ❌ C. Datová vrstva a Logika (ČEKÁ NA IMPLEMENTACI)
- **Schéma**: Databáze je připravena (`scripts/01-init-supabase.sql`).
  - Tabulky: `queries`, `answers` (pro chat), `vzp_medicines` (pro léky).
  - RLS Policies: Nastaveny pro bezpečný přístup uživatelů k vlastním datům.
- **Integrace**: V kódu aplikace (frontend komponenty) chybí volání `supabase.from(...)`.
  - Chat ukládá zprávy pouze do lokálního state (zmizí po refresh).
  - Vyhledávání léků filtruje pouze lokální pole testovacích dat.

## 4. Aktuální stav a "Zdraví" projektu
- **Build**: ✅ Projekt se úspěšně kompiluje (`npm run build` prochází).
- **Konfigurace**: ✅ Správně nastaveny `.env.local`, Supabase Client/Server utility i TypeScript definice (`database.types.ts`).
- **Kvalita kódu**: Kód je čistý, moderní (Server Components), ale vyžaduje dokončení napojení na backend.

## 5. Doporučený další postup (Roadmap)
1.  **Migrace Chatu na DB**:
    - Nahradit `useState` v `ChatInterface` voláním API/Server Actions, které ukládají dotazy do tabulek `queries` a `answers`.
    - Implementovat načítání historie chatu (`RecentQueries`).
2.  **VZP Data**:
    - Naplnit tabulku `vzp_medicines` reálnými daty (import CSV/JSON).
    - Přepsat `VzpSearchInterface` aby vyhledával v Supabase pomocí `.ilike()` filtrů.
3.  **AI Integrace**:
    - Napojit backend na AI model (např. OpenAI nebo Anthropic), který bude generovat odpovědi místo simulovaného textu.

## Závěr
Projekt má **solidní základy**. "Lešení" aplikace (Auth, DB schéma, UI komponenty) stojí pevně. Nyní je potřeba "oživit" aplikaci napojením existujícího UI na připravenou databázi.
