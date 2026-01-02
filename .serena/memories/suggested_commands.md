# Suggested Commands

## Frontend (Next.js)
Run these commands from the project root.

*   **Install Dependencies**: `pnpm install`
*   **Start Development Server**: `pnpm dev` (Runs on http://localhost:3000)
*   **Build for Production**: `pnpm build`
*   **Start Production Server**: `pnpm start`
*   **Lint Code**: `pnpm lint`

## Backend (FastAPI)
Run these commands from the project root, ensuring the virtual environment is activated.

*   **Create Virtual Environment**: `python -m venv backend/venv`
*   **Activate Virtual Environment**: `source backend/venv/bin/activate` (macOS/Linux)
*   **Install Dependencies**: `pip install -r backend/requirements.txt`
*   **Start Development Server**: `uvicorn backend.main:app --reload --port 8000` (Runs on http://localhost:8000)
*   **Run Tests**: `pytest backend/` (Assumed based on presence of `pytest.ini`)

## Database (Supabase)
*   **Start Local Supabase**: `npx supabase start` (If using local dev)
*   **Generate Types**: `npx supabase gen types typescript --project-id <project-id> > lib/database.types.ts` (Check if this is the correct path)

## General
*   **Git Ignore Check**: Ensure `.env` files are not committed.
