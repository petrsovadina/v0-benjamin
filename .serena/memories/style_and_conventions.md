# Style and Conventions

## Frontend
*   **Language**: TypeScript. Use strict typing.
*   **Framework**: Next.js App Router. Use Server Components where possible.
*   **Styling**: Tailwind CSS. Utility-first approach.
*   **Components**: Use shadcn/ui components as a base.
*   **State Management**: Use React Hooks.
*   **Validation**: Use Zod for schema validation.

## Backend
*   **Language**: Python 3.x.
*   **Framework**: FastAPI.
*   **Type Hints**: Use Python type hints extensively.
*   **AI Orchestration**: Use LangGraph for complex AI flows.

## Security
*   **API Keys**: Store all API keys in `.env` files. NEVER commit them to Git.
*   **Environment Variables**: Use `.env.example` files as templates.
*   **Authentication**: Use Supabase Auth. Backend endpoints should verify Bearer tokens.

## Documentation
*   **Language**: Czech (primary for user-facing content), English (code comments/docs).
*   **CLAUDE.md**: Follow instructions in `CLAUDE.md` for AI agent interactions.
