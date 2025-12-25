# Frontend Documentation

## Architecture

The frontend is built with **Next.js 16 (App Router)** and **TypeScript**.

### Directory Structure
- `app/`: Contains the application routes and layouts.
  - `dashboard/`: The main authenticated application area.
  - `api/`: Route handlers acting as a proxy to the backend.
- `components/`: React components.
  - `ui/`: Reusable primitive components (Shadcn/UI).
  - `dashboard/`: Feature-specific components for the dashboard.
- `lib/`: Shared utilities, including authentication and Supabase client.

## Components (Shadcn/UI)

We use [Shadcn/UI](https://ui.shadcn.com/) for our component library. These components are located in `components/ui` and are built on top of Radix UI primitives and styled with Tailwind CSS.

### Adding New Components
To add a new Shadcn component, run:
```bash
npx shadcn-ui@latest add [component-name]
```
This will copy the component code into `components/ui`, allowing for full customization.

## Styling

Styling is handled via **Tailwind CSS**.
- Configuration: `tailwind.config.ts` (or mapped in `app/globals.css` via CSS variables).
- Theming: We support dark/light mode using `next-themes`.

## State Management

The application currently uses **React Context** and **Hooks** for state management.
- **AuthContext**: Manages user session and authentication state (`lib/auth-context.tsx`).
- **Local State**: Component-level state is managed with `useState` and `useReducer`.

## Data Fetching

Data fetching is currently performed using standard `fetch` calls to our API endpoints.
- **Chat Interface**: Uses `fetch` to backend via proxy `app/api/chat/route.ts` which forwards to `/api/v1/query`.
