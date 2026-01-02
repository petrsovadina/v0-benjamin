# Project Summary: Czech MedAI (Benjamin)

## Purpose
Czech MedAI (Benjamin) is an AI assistant designed for Czech healthcare professionals. It provides evidence-based answers to clinical questions using citations from PubMed, SÚKL (State Institute for Drug Control), and Czech guidelines. It also features VZP reimbursement verification, EHR integration, and deep clinical case analysis.

## Tech Stack
### Frontend
- **Framework**: Next.js 16 (App Router)
- **Language**: TypeScript 5.9
- **UI Library**: React 19
- **Styling**: Tailwind CSS 4.1.9
- **Components**: Radix UI / shadcn/ui
- **State/Data**: React Hook Form, Zod
- **Package Manager**: pnpm

### Backend
- **Framework**: FastAPI (Python 3.x)
- **Server**: Uvicorn
- **AI/LLM**: LangGraph, LangChain, Anthropic (Claude 3), OpenAI (Embeddings), Google (Transcription)
- **Database**: Supabase (PostgreSQL)
- **Package Manager**: pip

## Project Structure
- `app/`: Next.js App Router source code (Frontend)
- `backend/`: Python FastAPI backend service
  - `app/`: Backend application logic
  - `data/`: Data files (CSV, PDFs)
  - `mcp_servers/`: MCP server implementations
  - `tests/`: Backend tests
- `components/`: Shared React components
- `lib/`: Utility functions and shared logic
- `public/`: Static assets
- `scripts/`: Database initialization and migration scripts
- `supabase/`: Supabase configuration and migrations
- `docs/`: Project documentation
