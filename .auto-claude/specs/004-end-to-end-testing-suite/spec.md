# Specification: End-to-End Testing Suite

## Overview

Implement a comprehensive End-to-End (E2E) testing suite for Czech MedAI, a medical application built with Next.js and Supabase. The testing suite will cover four critical user flows: authentication (login/logout/sessions), AI chat with response validation, drug search with SUKL data, and VZP (Czech health insurance) verification. This is a high-priority feature as medical applications require high reliability - automated E2E testing prevents regressions and ensures consistent user experience in this healthcare context.

## Workflow Type

**Type**: feature

**Rationale**: This task involves implementing a new comprehensive E2E testing infrastructure from scratch. It includes creating new test files, configuration, CI pipeline integration, and coverage reporting - all new functionality that doesn't exist in the current codebase.

## Task Scope

### Services Involved
- **main** (primary) - Next.js frontend application with all user-facing components
- **backend** (integration) - FastAPI backend providing API endpoints for chat, drug search, and VZP

### This Task Will:
- [ ] Install and configure Playwright Test framework with TypeScript support
- [ ] Create authentication E2E tests covering login, logout, and session management
- [ ] Create AI chat E2E tests with response validation
- [ ] Create drug search E2E tests with SUKL data verification
- [ ] Create VZP verification E2E tests
- [ ] Set up CI pipeline integration to run tests on every PR
- [ ] Configure test coverage reporting with v8-to-istanbul

### Out of Scope:
- Backend unit tests (already exist in `backend/tests/`)
- Performance testing and load testing
- Visual regression testing
- Mobile-specific testing
- Backend API modifications

## Service Context

### Main (Next.js Frontend)

**Tech Stack:**
- Language: TypeScript
- Framework: Next.js 16
- Styling: Tailwind CSS
- Auth: Supabase (@supabase/supabase-js)
- Key directories: `app/`, `components/`, `lib/`

**Entry Point:** `app/page.tsx`

**How to Run:**
```bash
npm run dev
```

**Port:** 3000

**Key Routes:**
- `/auth/login` - Login page
- `/auth/register` - Registration page
- `/auth/logout` - Logout
- `/dashboard` - Main dashboard (requires auth)
- `/dashboard/chat` - AI chat interface
- `/dashboard/vzp-navigator` - VZP verification interface

### Backend (FastAPI)

**Tech Stack:**
- Language: Python 3.11
- Framework: FastAPI

**Key API Endpoints:**
- `GET /api/v1/drugs/search` - Drug search
- `POST /api/v1/drugs/vzp-search` - VZP search
- `GET /api/v1/drugs/{sukl_code}` - Drug by SUKL code
- `POST /api/v1/query` - AI chat query
- `POST /api/v1/query/stream` - AI chat streaming

**Port:** 8000

## Files to Modify

| File | Service | What to Change |
|------|---------|---------------|
| `package.json` | main | Add @playwright/test and v8-to-istanbul dev dependencies |
| `.gitignore` | main | Add playwright/.auth/, playwright-report/, test-results/ |
| `.github/workflows/ci.yml` | main | Add E2E test job with Playwright |

## Files to Create

| File | Service | Purpose |
|------|---------|---------|
| `playwright.config.ts` | main | Playwright configuration with auth setup project |
| `tests/auth.setup.ts` | main | Authentication setup for storing session state |
| `tests/auth.spec.ts` | main | Authentication flow E2E tests |
| `tests/chat.spec.ts` | main | AI chat E2E tests |
| `tests/drug-search.spec.ts` | main | Drug search with SUKL data E2E tests |
| `tests/vzp-verification.spec.ts` | main | VZP verification E2E tests |
| `.github/workflows/playwright.yml` | main | Dedicated Playwright CI workflow |

## Files to Reference

These files show patterns to follow:

| File | Pattern to Copy |
|------|----------------|
| `components/auth/login-form.tsx` | Login form structure, field IDs, button labels (Czech) |
| `components/dashboard/chat-interface.tsx` | Chat input/output structure, message format |
| `components/dashboard/vzp-search-interface.tsx` | VZP search form structure, result display |
| `lib/auth-actions.ts` | Authentication flow with Supabase (signIn, signOut) |
| `.github/workflows/ci.yml` | Existing CI structure and environment variables |

## Patterns to Follow

### Playwright Configuration Pattern

From research - standard Next.js + Playwright setup:

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['html'],
    ['github'],
  ],
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
});
```

**Key Points:**
- Setup project runs first to authenticate
- StorageState persists auth between tests
- WebServer auto-starts Next.js in CI

### Authentication Setup Pattern

```typescript
// tests/auth.setup.ts
import { test as setup, expect } from '@playwright/test';

const authFile = 'playwright/.auth/user.json';

setup('authenticate', async ({ page }) => {
  await page.goto('/auth/login');
  await page.getByLabel('Email').fill(process.env.TEST_USER_EMAIL!);
  await page.getByLabel('Heslo').fill(process.env.TEST_USER_PASSWORD!);
  await page.getByRole('button', { name: 'Přihlásit se' }).click();
  await page.waitForURL('/dashboard');
  await page.context().storageState({ path: authFile });
});
```

**Key Points:**
- Uses Czech labels as found in login-form.tsx
- Saves auth state for reuse
- Redirects to /dashboard on success

### Login Form Structure

From `components/auth/login-form.tsx`:

```typescript
// Form uses these identifiers:
<label htmlFor="email">Email</label>
<Input id="email" type="email" placeholder="vas@email.cz" />

<label htmlFor="password">Heslo</label>
<Input id="password" type="password" placeholder="Vaše heslo" />

<Button type="submit">Přihlásit se</Button>
// Loading state: "Přihlašování..."
```

**Key Points:**
- Email field: id="email", label="Email"
- Password field: id="password", label="Heslo"
- Submit button text: "Přihlásit se"
- Error displayed in destructive div

### Chat Interface Pattern

From `components/dashboard/chat-interface.tsx`:

```typescript
// Initial message pattern
{
  role: "assistant",
  content: "Ahoj! Jsem Czech MedAI (v2.0)..."
}

// Input/output
<Input placeholder="Zadejte svůj klinický dotaz..." />
<Button>Odeslat</Button>

// API call
fetch(`${apiUrl}/api/v1/query`, {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${token}`
  },
  body: JSON.stringify({ message, history })
})
```

**Key Points:**
- Chat starts with AI greeting message
- Input placeholder: "Zadejte svůj klinický dotaz..."
- Send button: "Odeslat"
- Requires auth token for API

### VZP Search Pattern

From `components/dashboard/vzp-search-interface.tsx`:

```typescript
// Search structure
<Input placeholder="Vyhledejte lék (např. 'Bisoprolol', 'warfarin', 'C07AB07')..." />
<Button>Vyhledat</Button>

// Loading: "Hledám..."
// API: POST /api/v1/drugs/vzp-search
// Body: { query: searchQuery }
```

**Key Points:**
- Search placeholder includes examples
- Button text: "Vyhledat"
- Shows result count: "Nalezeno X výsledků"
- Empty state: "Žádné výsledky pro..."

## Requirements

### Functional Requirements

1. **Authentication E2E Tests**
   - Description: Test login, logout, and session persistence flows
   - Acceptance:
     - Login with valid credentials redirects to /dashboard
     - Invalid credentials show error message
     - Logout redirects to /auth/login
     - Protected routes redirect unauthenticated users

2. **AI Chat E2E Tests**
   - Description: Test chat query and response flow
   - Acceptance:
     - Chat page loads with initial AI greeting
     - User can send message and receive response
     - Response includes citations when available
     - Error handling displays user-friendly message

3. **Drug Search E2E Tests**
   - Description: Test drug search with SUKL data
   - Acceptance:
     - Search by drug name returns results
     - Search by ATC code returns results
     - Empty search shows appropriate message
     - Result cards display drug information

4. **VZP Verification E2E Tests**
   - Description: Test VZP insurance verification search
   - Acceptance:
     - Search page loads correctly
     - Search with valid drug returns coverage info
     - Result shows coverage status (full/partial/limited)
     - Empty results handled gracefully

5. **CI Pipeline Integration**
   - Description: Tests run automatically on PRs
   - Acceptance:
     - GitHub Actions workflow triggers on PR
     - Tests run in headless Chromium
     - Results reported in PR checks
     - Artifacts uploaded on failure

6. **Coverage Reporting**
   - Description: Generate test coverage reports
   - Acceptance:
     - HTML coverage report generated
     - Coverage includes all tested pages
     - Report accessible in CI artifacts

### Edge Cases

1. **Network Failures** - Mock API responses for offline/error scenarios
2. **Session Expiry** - Test behavior when auth token expires mid-session
3. **Empty States** - Verify all empty/no-result states display correctly
4. **Loading States** - Verify loading indicators appear during async operations
5. **Form Validation** - Test required field validation (email format, empty password)
6. **Rate Limiting** - Handle potential API rate limiting gracefully

## Implementation Notes

### DO
- Follow the existing Czech language patterns for all selectors (use "Heslo", "Přihlásit se", etc.)
- Use data-testid attributes for stable selectors where ID/label is unreliable
- Create fixtures for common test data (test user credentials, drug names)
- Use environment variables for sensitive test data (TEST_USER_EMAIL, TEST_USER_PASSWORD)
- Implement proper teardown to avoid test pollution
- Use Playwright's built-in waiting mechanisms (waitForURL, waitForSelector)
- Mock external API responses when testing edge cases

### DON'T
- Hardcode credentials in test files
- Create tests that depend on production data
- Skip the setup project - all authenticated tests need session state
- Use arbitrary sleep/delays - rely on Playwright's auto-waiting
- Run tests in parallel against real API without mocking
- Commit playwright/.auth/ directory (contains session data)

## Development Environment

### Start Services

```bash
# Install Playwright dependencies
npm install -D @playwright/test v8-to-istanbul
npx playwright install --with-deps

# Start development server
npm run dev

# Run tests locally
npx playwright test

# Run tests with UI mode
npx playwright test --ui

# Run specific test file
npx playwright test tests/auth.spec.ts

# Generate HTML report
npx playwright show-report
```

### Service URLs
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

### Required Environment Variables
- `NEXT_PUBLIC_SUPABASE_URL`: Supabase project URL
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`: Supabase anonymous key
- `NEXT_PUBLIC_API_URL`: Backend API URL (http://localhost:8000)
- `TEST_USER_EMAIL`: E2E test user email (CI secret)
- `TEST_USER_PASSWORD`: E2E test user password (CI secret)

## Success Criteria

The task is complete when:

1. [x] Playwright is installed and configured with Next.js webserver
2. [ ] E2E tests cover authentication flow (login, logout, session)
3. [ ] E2E tests cover AI chat with response verification
4. [ ] E2E tests cover drug search with SUKL data
5. [ ] E2E tests cover VZP verification process
6. [ ] Tests run in CI pipeline on every PR
7. [ ] Test coverage report is generated
8. [ ] No console errors in test output
9. [ ] All existing CI tests still pass
10. [ ] Tests pass in headless Chromium mode

## QA Acceptance Criteria

**CRITICAL**: These criteria must be verified by the QA Agent before sign-off.

### Unit Tests
| Test | File | What to Verify |
|------|------|----------------|
| Playwright Config | `playwright.config.ts` | Config loads without errors, projects defined correctly |

### Integration Tests
| Test | Services | What to Verify |
|------|----------|----------------|
| Auth Setup | Frontend ↔ Supabase | Login saves session state to JSON file |
| Chat API | Frontend ↔ Backend | Chat queries reach backend and return responses |
| VZP Search | Frontend ↔ Backend | VZP search queries return properly formatted data |
| Drug Search | Frontend ↔ Backend | Drug search queries return SUKL data |

### End-to-End Tests
| Flow | Steps | Expected Outcome |
|------|-------|------------------|
| Login Flow | 1. Navigate to /auth/login 2. Fill email 3. Fill password 4. Click submit | User redirected to /dashboard |
| Logout Flow | 1. Be logged in 2. Click logout | User redirected to /auth/login |
| Chat Query | 1. Navigate to /dashboard/chat 2. Enter query 3. Submit | AI response displayed with citations |
| VZP Search | 1. Navigate to /dashboard/vzp-navigator 2. Enter drug name 3. Search | Coverage results displayed |
| Drug Search | 1. Search by drug name | Drug info card displayed |

### Browser Verification (Frontend)
| Page/Component | URL | Checks |
|----------------|-----|--------|
| Login Page | `http://localhost:3000/auth/login` | Form renders, submit works |
| Dashboard | `http://localhost:3000/dashboard` | Protected, requires auth |
| Chat Interface | `http://localhost:3000/dashboard/chat` | Input, messages, send button work |
| VZP Navigator | `http://localhost:3000/dashboard/vzp-navigator` | Search form, results display |

### CI/CD Verification
| Check | Command | Expected |
|-------|---------|----------|
| Playwright Install | `npx playwright install --with-deps` | Browsers installed |
| Test Run | `npx playwright test` | All tests pass |
| Coverage Report | Check `playwright-report/` | HTML report generated |
| CI Workflow | Push to PR | GitHub Actions job runs |

### QA Sign-off Requirements
- [ ] All E2E tests pass locally
- [ ] All E2E tests pass in CI
- [ ] Coverage report generated and accessible
- [ ] No regressions in existing frontend build
- [ ] No regressions in existing backend tests
- [ ] Auth session properly isolated between test runs
- [ ] CI workflow correctly configured with secrets
- [ ] No security vulnerabilities (no hardcoded credentials)
- [ ] Tests use Czech language selectors correctly

## Test File Structure

```
tests/
├── auth.setup.ts          # Authentication setup (runs first)
├── auth.spec.ts           # Login, logout, session tests
├── chat.spec.ts           # AI chat query/response tests
├── drug-search.spec.ts    # SUKL drug search tests
└── vzp-verification.spec.ts  # VZP insurance verification tests

playwright/
└── .auth/
    └── user.json          # Stored auth state (gitignored)

playwright-report/         # HTML test reports (gitignored)
test-results/              # Test artifacts (gitignored)
```

## API Mocking Strategy

For reliable E2E tests, especially edge cases, mock the backend API:

```typescript
// Example: Mock VZP search response
await page.route('**/api/v1/drugs/vzp-search', async route => {
  await route.fulfill({
    status: 200,
    contentType: 'application/json',
    body: JSON.stringify({
      results: [{
        id: '1',
        name: 'Bisoprolol',
        inn: 'Bisoprololum',
        atc: 'C07AB07',
        form: 'tablety',
        coverage: 'full',
        conditions: [],
        alternatives: []
      }]
    })
  });
});
```

This ensures tests are:
- Fast (no real API calls)
- Reliable (consistent responses)
- Isolated (no external dependencies)
