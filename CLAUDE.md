# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.



## Project Overview

**Czech MedAI (Benjamin)** is an AI assistant for Czech medical professionals, providing evidence-based clinical answers with citations from PubMed, SÚKL (State Institute for Drug Control), and Czech medical guidelines. The application includes VZP (health insurance) verification and EHR integration capabilities.

This is a **full-stack project** with:
- **Frontend**: Next.js 16 App Router application (TypeScript, React 19, Tailwind CSS)
- **Backend**: Python FastAPI service with LangGraph-based clinical query processing
- **Database**: Supabase (PostgreSQL with Row Level Security)

## Development Commands

### Frontend (Next.js)

```bash
# Install dependencies
pnpm install

# Development server (http://localhost:3000)
pnpm dev

# Production build
pnpm build

# Start production server
pnpm start

# Linting
pnpm lint
```

**Note**: This project uses **pnpm** as the package manager, not npm or yarn.

### Backend (Python FastAPI)

```bash
# Navigate to backend directory
cd backend/

# Install Python dependencies
pip install -r requirements.txt

# Run development server (http://localhost:8000)
uvicorn main:app --reload

# Run with specific host/port
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Architecture

### Frontend Architecture (Next.js App Router)

The frontend uses Next.js 16 App Router with a clear separation between:

1. **Public Routes** (`app/`):
   - Landing page (`app/page.tsx`)
   - Authentication flows (`app/auth/login/`, `app/auth/register/`, etc.)
   - Documentation (`app/docs/`)

2. **Protected Routes** (`app/dashboard/`):
   - Chat interface (`app/dashboard/chat/`)
   - VZP Navigator (`app/dashboard/vzp-navigator/`)
   - History (`app/dashboard/history/`)
   - Settings (`app/dashboard/settings/`)

3. **Component Organization**:
   - `components/auth/` - Authentication forms and flows
   - `components/dashboard/` - Dashboard-specific components (chat, VZP search, etc.)
   - `components/landing/` - Marketing/landing page components
   - `components/ui/` - Reusable UI components from Radix UI/shadcn

4. **Library Structure** (`lib/`):
   - `lib/supabase/` - Supabase client configuration (client-side, server-side, middleware)
   - `lib/auth-actions.ts` - Server Actions for authentication
   - `lib/auth-context.tsx` - Client-side authentication context
   - `lib/utils.ts` - Utility functions (cn for className merging, etc.)

**Path Aliases**: Use `@/` to import from the project root (e.g., `import { Button } from "@/components/ui/button"`)

**Authentication Flow**:
- Middleware (`middleware.ts`) intercepts all requests and updates Supabase session
- Protected routes check authentication in Server Components using `lib/supabase/server.ts`
- Client-side auth state managed via `AuthProvider` in `lib/auth-context.tsx`

### Backend Architecture (Python FastAPI)

The backend is a FastAPI application with LangGraph for clinical query processing:

1. **Core Structure** (`backend/`):
   - `main.py` - FastAPI application entry point
   - `agent_graph.py` - LangGraph state machine for clinical queries
   - `epicrisis_graph.py` - Specialized graph for epicrisis (medical summary) generation

2. **API Organization** (`backend/app/`):
   - `app/api/` - API route handlers
   - `app/core/` - Core configuration and utilities
   - `app/models/` - Pydantic models for request/response validation

3. **Data Processing** (`backend/data_processing/`):
   - Pipeline for processing medical data sources (SÚKL, PubMed, Czech guidelines)
   - Data transformation and indexing for RAG (Retrieval-Augmented Generation)

4. **MCP Servers** (`backend/mcp_servers/`):
   - Model Context Protocol servers for external integrations

**LangGraph State Machine**:
The clinical query processing uses a state machine architecture (`agent_graph.py`) that:
- Routes queries based on type (clinical question, drug information, VZP verification)
- Retrieves relevant context from medical databases
- Generates evidence-based responses with citations
- Formats output with proper medical references

### Database (Supabase)

Key database tables (see README.md for full schema):

- `profiles` - Extended user information beyond auth.users
- `chat_messages` - Chat history with citations (JSONB)
- `vzp_searches` - VZP search history

**Row Level Security (RLS)**: All tables use RLS policies to ensure users can only access their own data.

### Frontend-Backend Communication

The frontend communicates with the backend via:
1. **Direct API calls** to FastAPI endpoints (e.g., `/api/chat`, `/api/vzp-search`)
2. **Supabase** for authentication, user profiles, and data persistence
3. **Real-time subscriptions** via Supabase for live updates (if implemented)

## Key Technical Details

### TypeScript Configuration

- **Strict mode enabled** - All types must be properly defined
- **Path aliases**: `@/*` maps to project root
- **JSX**: Uses `react-jsx` (no need to import React in files)
- **Module resolution**: `bundler` mode for Next.js compatibility

**Important**: The project has `ignoreBuildErrors: true` in `next.config.mjs` - this is a temporary configuration and should be removed once all TypeScript errors are resolved.

### Styling

- **Tailwind CSS 4.1.9** with custom configuration
- **CSS Variables** for theming (defined in `app/globals.css`)
- **Dark/Light Mode** via `next-themes` package
- **Component Styling**: Use `cn()` utility from `lib/utils.ts` to merge Tailwind classes

Example:
```tsx
import { cn } from "@/lib/utils"

<div className={cn("base-classes", conditional && "conditional-classes", className)} />
```

### Supabase Integration

**Three Supabase clients** depending on context:

1. **Client-side** (`lib/supabase/client.ts`):
   ```tsx
   import { createClient } from "@/lib/supabase/client"
   const supabase = createClient()
   ```

2. **Server Components** (`lib/supabase/server.ts`):
   ```tsx
   import { createClient } from "@/lib/supabase/server"
   const supabase = await createClient()
   ```

3. **Middleware** (`lib/supabase/middleware.ts`):
   Used automatically by `middleware.ts` to refresh sessions

### Form Handling

Forms use **React Hook Form** with **Zod** validation:

```tsx
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
})

const form = useForm({
  resolver: zodResolver(schema),
})
```

### Adding UI Components

This project uses **shadcn/ui** components. To add a new component:

```bash
npx shadcn@latest add [component-name]
```

Components are added to `components/ui/` and can be customized.

## Important Patterns

### Server Actions vs. API Routes

- **Server Actions** (`lib/auth-actions.ts`) - Preferred for simple mutations and authentication flows
- **API Routes** (`app/api/`) - Used for complex logic or when you need more control over request/response

### Protected Routes

Protected routes should:
1. Check authentication in Server Components using `lib/supabase/server.ts`
2. Redirect to `/auth/login` if not authenticated
3. Use `AuthProvider` in `layout.tsx` for client-side auth state

Example:
```tsx
// app/dashboard/page.tsx
import { createClient } from "@/lib/supabase/server"
import { redirect } from "next/navigation"

export default async function DashboardPage() {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    redirect("/auth/login")
  }

  // Render protected content
}
```

### Error Handling

The project includes an error boundary (`components/error-boundary.tsx`) for graceful error handling in the UI.

## Environment Variables

Required environment variables (see `.env.local` or backend `.env`):

**Frontend**:
- `NEXT_PUBLIC_SUPABASE_URL` - Supabase project URL
- `NEXT_PUBLIC_SUPABASE_PUBLISHABLE_DEFAULT_KEY` - Supabase anon key

**Backend**:
- `OPENAI_API_KEY` - OpenAI API key for LLM
- `ANTHROPIC_API_KEY` - Anthropic API key (optional)
- Database connection strings for SÚKL and other data sources

## Common Issues

### Build Errors

If you encounter TypeScript errors during build:
1. Check that all imports use the correct path aliases (`@/`)
2. Verify Supabase types are generated: `supabase gen types typescript`
3. Run `pnpm build` to see all type errors at once

### Supabase Session Issues

If authentication seems broken:
1. Verify middleware is running on all routes (check `middleware.ts` matcher config)
2. Ensure you're using the correct Supabase client for the context (client vs. server)
3. Check browser console for CORS errors or cookie issues

## Testing

**Note**: Testing framework is not yet configured. The project is set up for testing with Vitest or Jest + React Testing Library, but no tests are currently written.

## Deployment

The project is configured for **Vercel** deployment with `output: "standalone"` in `next.config.mjs`.

**Backend deployment**: The Python backend can be deployed to any platform supporting FastAPI (e.g., Railway, Render, Docker container).

## Communication Language

**Czech Language**: This project is for Czech medical professionals. User-facing content, error messages, and documentation should be in Czech. Code comments and technical documentation can be in English or Czech.
