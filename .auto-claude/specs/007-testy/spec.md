# Specification: E2E Test Suite for MedAI

## Overview

Implement a comprehensive End-to-End (E2E) test suite using Playwright for MedAI, a Czech medical application built with Next.js and Supabase. The test suite will cover four critical user flows: authentication (login/logout/session), AI chat with response validation, drug search with SUKL data, and VZP (Czech health insurance) verification. This is a high-priority feature as medical applications require exceptional reliability - automated E2E testing prevents regressions and ensures consistent user experience in a healthcare context.

## Workflow Type

**Type**: feature

**Rationale**: This is a new feature implementation that adds comprehensive testing infrastructure to the project. No existing E2E tests or Playwright configuration exists, requiring setup from scratch plus test creation for all four critical user flows.

## Task Scope

### Services Involved
- **main** (primary) - Next.js frontend application containing all UI components and pages to be tested
- **backend** (integration) - FastAPI Python backend providing API endpoints for chat, drugs, and VZP search

### This Task Will:
- [ ] Install and configure Playwright for Next.js E2E testing
- [ ] Create authentication test suite (login, logout, session persistence)
- [ ] Create AI chat interface test suite with response validation
- [ ] Create drug search test suite with SUKL data verification
- [ ] Create VZP Navigator test suite for insurance verification flow
- [ ] Set up API mocking for external integrations (SUKL, VZP)
- [ ] Configure CI workflow for automated E2E testing

### Out of Scope:
- Unit tests for individual functions
- Backend Python API tests
- Performance/load testing
- Visual regression testing
- Mobile responsiveness testing

## Service Context

### Main Frontend Service

**Tech Stack:**
- Language: TypeScript
- Framework: Next.js 15+
- Styling: Tailwind CSS
- Auth: Supabase SSR
- Package Manager: pnpm
- Key directories: `app/`, `components/`, `lib/`

**Entry Point:** `app/layout.tsx`

**How to Run:**
```bash
npm run dev
```

**Port:** 3000

### Backend API Service

**Tech Stack:**
- Language: Python
- Framework: FastAPI
- Key directories: `backend/app/api/`, `backend/services/`

**How to Run:**
```bash
cd backend && uvicorn app.main:app --reload
```

**Port:** 8000

## Files to Modify

| File | Service | What to Change |
|------|---------|---------------|
| `package.json` | main | Add Playwright dev dependency and test scripts |
| `playwright.config.ts` | main | Create new Playwright configuration file |
| `.gitignore` | main | Add Playwright auth state and test results directories |

## Files to Create

| File | Service | Purpose |
|------|---------|---------|
| `e2e/auth.setup.ts` | main | Authentication setup project for session persistence |
| `e2e/auth.spec.ts` | main | Authentication flow tests (login/logout) |
| `e2e/chat.spec.ts` | main | AI chat interface tests |
| `e2e/drug-search.spec.ts` | main | Drug search with SUKL data tests |
| `e2e/vzp-navigator.spec.ts` | main | VZP insurance verification tests |
| `e2e/fixtures/test-data.ts` | main | Shared test data and constants |
| `.github/workflows/e2e.yml` | main | CI workflow for E2E tests |

## Files to Reference

These files show patterns to follow:

| File | Pattern to Copy |
|------|----------------|
| `lib/auth-actions.ts` | Authentication flow (signIn/signOut with redirect) |
| `components/auth/login-form.tsx` | Login form selectors and interactions |
| `components/dashboard/chat-interface.tsx` | Chat message flow and API calls |
| `components/dashboard/vzp-search-interface.tsx` | VZP search form and result handling |
| `lib/supabase/client.ts` | Supabase client configuration for browser |

## Patterns to Follow

### Authentication Flow Pattern

From `lib/auth-actions.ts`:

```typescript
// Login redirects to /dashboard on success
export async function signIn(email: string, password: string) {
  const supabase = await createClient()
  const { error } = await supabase.auth.signInWithPassword({ email, password })
  if (error) return { error: error.message }
  redirect("/dashboard")
}

// Logout redirects to /auth/login
export async function signOut() {
  const supabase = await createClient()
  await supabase.auth.signOut()
  redirect("/auth/login")
}
```

**Key Points:**
- Test must wait for redirect after login: `/auth/login` → `/dashboard`
- Test must verify redirect after logout: `/dashboard` → `/auth/login`
- Use `page.waitForURL()` to handle server action redirects

### Login Form Selectors Pattern

From `components/auth/login-form.tsx`:

```typescript
<Input id="email" type="email" placeholder="vas@email.cz" />
<Input id="password" type="password" placeholder="Vaše heslo" />
<Button type="submit">Přihlásit se</Button>
```

**Key Points:**
- Email input: `#email` or `[placeholder="vas@email.cz"]`
- Password input: `#password` or `[placeholder="Vaše heslo"]`
- Submit button: `button[type="submit"]` or text "Přihlásit se"
- Error message: `.bg-destructive/10` container

### Chat Interface Pattern

From `components/dashboard/chat-interface.tsx`:

```typescript
// API call pattern
const response = await fetch(`${apiUrl}/api/v1/query`, {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${token}`
  },
  body: JSON.stringify({
    message: textToSend,
    history: messages.map(m => ({ role: m.role, content: m.content }))
  }),
})
```

**Key Points:**
- Input placeholder: "Zadejte svůj klinický dotaz..."
- Submit button text: "Odeslat"
- Initial greeting contains: "Ahoj! Jsem Czech MedAI"
- Loading indicator: `ThinkingIndicator` component
- Must mock `/api/v1/query` endpoint for reliable tests

### VZP Search Pattern

From `components/dashboard/vzp-search-interface.tsx`:

```typescript
// API endpoint
const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/drugs/vzp-search`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ query: searchQuery }),
})
```

**Key Points:**
- Search placeholder: "Vyhledejte lék..."
- Button text: "Vyhledat" (loading: "Hledám...")
- Quick search chips: "Bisoprolol", "C07AB", "Warfarin"
- Results count: "Nalezeno X výsledků"
- No results message: "Žádné výsledky pro..."

## Requirements

### Functional Requirements

1. **Playwright Installation & Configuration**
   - Description: Set up Playwright with proper configuration for Next.js
   - Acceptance: `npx playwright test` runs successfully with webServer config

2. **Authentication Test Suite**
   - Description: Test login, logout, and session persistence flows
   - Acceptance: Tests cover valid login, invalid credentials error, logout redirect

3. **AI Chat Test Suite**
   - Description: Test chat interface message sending and response rendering
   - Acceptance: Tests verify message appears, API is called, response is displayed

4. **Drug Search Test Suite**
   - Description: Test drug search functionality with mocked SUKL data
   - Acceptance: Tests verify search input, API call, results display

5. **VZP Navigator Test Suite**
   - Description: Test VZP insurance verification search flow
   - Acceptance: Tests verify search, quick filters, results, no-results state

6. **Session Persistence (storageState)**
   - Description: Use Playwright's storageState for auth between tests
   - Acceptance: Auth setup runs once, other tests reuse session

### Edge Cases

1. **Invalid Login Credentials** - Verify error message "Přihlášení se nezdařilo" displays
2. **Empty Search Query** - Search button should be disabled, no API call made
3. **API Timeout/Error** - Verify graceful error handling in chat and search
4. **Session Expiry** - Handle redirect to login when session expires
5. **No Search Results** - Verify "Žádné výsledky" message appears correctly

## Implementation Notes

### DO
- Follow the `storageState` pattern for auth persistence across tests
- Use `page.route()` to mock external API calls (backend endpoints)
- Create reusable fixtures for common test data (drugs, VZP results)
- Use Czech text in assertions (app is in Czech locale)
- Configure `webServer` in playwright.config.ts for auto-start
- Add `test.describe` blocks for logical test grouping

### DON'T
- Don't test against live SUKL/VZP APIs (use mocks)
- Don't hardcode absolute URLs (use baseURL config)
- Don't skip waiting for navigation after actions
- Don't create separate test databases (mock at API layer)
- Don't commit auth state files (add to .gitignore)

## Development Environment

### Start Services

```bash
# Start Next.js frontend
npm run dev

# Start Python backend (in separate terminal)
cd backend && uvicorn app.main:app --reload --port 8000
```

### Service URLs
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Login Page: http://localhost:3000/auth/login
- Dashboard: http://localhost:3000/dashboard
- Chat: http://localhost:3000/dashboard/chat
- VZP Navigator: http://localhost:3000/dashboard/vzp-navigator

### Required Environment Variables
- `NEXT_PUBLIC_API_URL`: Backend API URL (default: http://localhost:8000)
- `NEXT_PUBLIC_SUPABASE_URL`: Supabase project URL
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`: Supabase anonymous key
- `TEST_USER_EMAIL`: Test user email for E2E authentication
- `TEST_USER_PASSWORD`: Test user password for E2E authentication

## Success Criteria

The task is complete when:

1. [ ] Playwright is installed and configured with working webServer setup
2. [ ] Auth tests pass: login, logout, session persistence
3. [ ] Chat tests pass: message send, response display with mocked API
4. [ ] Drug search tests pass: search flow with mocked SUKL data
5. [ ] VZP Navigator tests pass: search flow with mocked results
6. [ ] All tests can run in CI (`npx playwright test` succeeds)
7. [ ] No console errors during test execution
8. [ ] Test results are reproducible (no flaky tests)

## QA Acceptance Criteria

**CRITICAL**: These criteria must be verified by the QA Agent before sign-off.

### Unit Tests
| Test | File | What to Verify |
|------|------|----------------|
| Auth setup | `e2e/auth.setup.ts` | Login succeeds and saves storageState |
| Login validation | `e2e/auth.spec.ts` | Invalid credentials show error |
| Logout flow | `e2e/auth.spec.ts` | Logout redirects to login page |

### Integration Tests
| Test | Services | What to Verify |
|------|----------|----------------|
| Chat API | Frontend ↔ Backend | Message sent to `/api/v1/query`, response rendered |
| VZP Search | Frontend ↔ Backend | Search query POSTed, results rendered |
| Drug Search | Frontend ↔ Backend | SUKL code lookup returns drug info |

### End-to-End Tests
| Flow | Steps | Expected Outcome |
|------|-------|------------------|
| Login Flow | 1. Navigate to /auth/login 2. Enter credentials 3. Submit | Redirected to /dashboard |
| Chat Flow | 1. Navigate to /dashboard/chat 2. Enter query 3. Submit | AI response appears |
| VZP Search | 1. Navigate to /dashboard/vzp-navigator 2. Enter drug name 3. Search | Results displayed |
| Logout Flow | 1. Click logout 2. Confirm | Redirected to /auth/login |

### Browser Verification
| Page/Component | URL | Checks |
|----------------|-----|--------|
| Login Form | `http://localhost:3000/auth/login` | Email/password inputs visible, submit button works |
| Dashboard | `http://localhost:3000/dashboard` | Loads after login, sidebar visible |
| Chat Interface | `http://localhost:3000/dashboard/chat` | Initial greeting visible, input enabled |
| VZP Navigator | `http://localhost:3000/dashboard/vzp-navigator` | Search input visible, quick filters work |

### Test Execution Verification
| Check | Command | Expected |
|-------|---------|----------|
| All tests pass | `npx playwright test` | Exit code 0, all tests green |
| HTML report generated | `npx playwright show-report` | Report opens in browser |
| CI workflow runs | GitHub Actions | E2E workflow passes |

### QA Sign-off Requirements
- [ ] All E2E tests pass locally
- [ ] All E2E tests pass in CI environment
- [ ] Tests are not flaky (run 3x with consistent results)
- [ ] Auth persistence works correctly between tests
- [ ] API mocking is comprehensive (no real external calls)
- [ ] Czech language assertions match actual UI text
- [ ] Error cases are properly tested
- [ ] No hardcoded credentials in test files
- [ ] Test execution time is reasonable (<5 minutes)

## Technical Implementation Details

### Playwright Configuration

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
  },
  projects: [
    { name: 'setup', testMatch: /.*\.setup\.ts/ },
    {
      name: 'chromium',
      use: {
        ...devices['Desktop Chrome'],
        storageState: 'playwright/.auth/user.json',
      },
      dependencies: ['setup'],
    },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
})
```

### Mock Data Structure

```typescript
// VZP Result mock
interface VzpResult {
  id: string
  name: string
  inn: string  // International nonproprietary name
  atc: string  // ATC code
  form: string // Pharmaceutical form
  coverage: "full" | "partial" | "limited"
  conditions: string[]
  alternatives: string[]
}

// Chat Response mock
interface ChatResponse {
  response: string
  citations: Array<{
    source: string
    title: string
    url: string
    metadata?: Record<string, any>
  }>
}
```

### Required npm Scripts

```json
{
  "scripts": {
    "test:e2e": "playwright test",
    "test:e2e:ui": "playwright test --ui",
    "test:e2e:headed": "playwright test --headed",
    "test:e2e:report": "playwright show-report"
  }
}
```
