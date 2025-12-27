# Specification: Comprehensive Testing (Komplexni Testovani)

## Overview

This task implements a comprehensive testing infrastructure for the Czech MedAI application - a medical AI assistant with a Next.js frontend and FastAPI backend. The goal is to establish robust testing coverage across both services, including setting up Vitest for frontend testing (currently non-existent), enhancing backend pytest infrastructure with proper configuration and fixtures, and achieving 80% code coverage targets. This enables reliable development, catches regressions early, and ensures production quality.

## Workflow Type

**Type**: feature

**Rationale**: This is a substantial new capability (frontend testing infrastructure) combined with enhancement of existing infrastructure (backend tests). It requires multi-file changes across both services, configuration setup, and new code creation.

## Task Scope

### Services Involved
- **main** (primary) - Next.js frontend - needs complete test infrastructure setup
- **backend** (integration) - FastAPI Python - needs test infrastructure enhancement

### This Task Will:
- [ ] Set up Vitest testing framework for React/Next.js frontend
- [ ] Create testing library configuration for React components
- [ ] Add conftest.py with shared fixtures for backend pytest
- [ ] Create pyproject.toml with pytest and coverage configuration
- [ ] Write unit tests for key frontend components
- [ ] Write unit tests for frontend lib utilities
- [ ] Enhance backend tests with proper fixtures
- [ ] Add coverage reporting to both services
- [ ] Add npm scripts for test execution

### Out of Scope:
- End-to-end browser testing (Playwright/Cypress)
- Performance testing
- Security penetration testing
- API contract testing between services
- CI/CD pipeline modifications (beyond running tests)

## Service Context

### Main (Frontend)

**Tech Stack:**
- Language: TypeScript
- Framework: Next.js 16 with React 19
- Styling: Tailwind CSS
- UI Library: Radix UI components
- Form handling: React Hook Form + Zod

**Key directories:**
- `components/` - UI components (42+ files)
- `lib/` - Utility modules (6 files)
- `app/` - Next.js app router pages

**Entry Point:** `app/page.tsx`

**How to Run:**
```bash
pnpm dev
```

**Port:** 3000

### Backend

**Tech Stack:**
- Language: Python
- Framework: FastAPI
- Testing: pytest, pytest-asyncio (installed)
- Database: Supabase

**Key directories:**
- `backend/app/` - Main application code
- `backend/tests/` - Existing test files (10 files)
- `backend/services/` - Business logic
- `backend/pipeline/` - Data processing

**Entry Point:** `backend/main.py`

**How to Run:**
```bash
cd backend && uvicorn main:app --reload
```

**Port:** 8000

## Files to Modify

| File | Service | What to Change |
|------|---------|---------------|
| `package.json` | main | Add test scripts and devDependencies: vitest, @vitest/coverage-v8, @vitejs/plugin-react, @testing-library/react, @testing-library/jest-dom, @testing-library/user-event, jsdom |
| `vitest.config.ts` | main | Create - Vitest configuration with jsdom |
| `vitest.setup.ts` | main | Create - Testing library setup file |
| `backend/pyproject.toml` | backend | Create - pytest and coverage configuration |
| `backend/tests/conftest.py` | backend | Create - Shared pytest fixtures |
| `components/__tests__/button.test.tsx` | main | Create - Button component tests |
| `components/__tests__/input.test.tsx` | main | Create - Input component tests |
| `components/__tests__/chat-interface.test.tsx` | main | Create - Chat interface tests |
| `lib/__tests__/utils.test.ts` | main | Create - Utils tests |
| `lib/__tests__/auth-actions.test.ts` | main | Create - Auth actions tests |
| `.gitignore` | main | Add coverage artifacts |

## Files to Reference

These files show patterns to follow:

| File | Pattern to Copy |
|------|----------------|
| `backend/tests/test_api_integration.py` | TestClient usage, mocking pattern, fixture structure |
| `components/ui/button.tsx` | Component structure for test targeting |
| `components/ui/input.tsx` | Form component pattern |
| `lib/utils.ts` | Utility function patterns |
| `lib/auth-actions.ts` | Async server action patterns |

## Patterns to Follow

### Backend Test Pattern

From `backend/tests/test_api_integration.py`:

```python
import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch, AsyncMock
from backend.main import app

client = TestClient(app)

@pytest.fixture
def mock_supabase():
    mock_client = MagicMock()
    mock_table = MagicMock()
    mock_client.table.return_value = mock_table
    return mock_client

def test_health_check():
    """Clear docstring explaining test purpose."""
    response = client.get("/health")
    assert response.status_code == 200
```

**Key Points:**
- Use TestClient for synchronous tests
- Define fixtures for mocked dependencies
- Clear dependency override cleanup after tests
- Czech comments acceptable for domain context

### Backend pyproject.toml Configuration Pattern

Create `backend/pyproject.toml` with pytest and coverage configuration:

```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
asyncio_default_fixture_loop_scope = "function"
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
addopts = [
    "-v",
    "--tb=short"
]

[tool.coverage.run]
branch = true
source = ["backend"]
omit = ["*/tests/*", "*/migrations/*"]

[tool.coverage.report]
show_missing = true
exclude_lines = [
    "pragma: no cover",
    "raise NotImplementedError"
]
```

### Frontend Component Test Pattern

Standard React Testing Library pattern to implement:

```typescript
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { Button } from '../ui/button'

describe('Button', () => {
  it('renders with text', () => {
    render(<Button>Click me</Button>)
    expect(screen.getByRole('button', { name: /click me/i })).toBeInTheDocument()
  })

  it('calls onClick when clicked', async () => {
    const user = userEvent.setup()
    const handleClick = vi.fn()
    render(<Button onClick={handleClick}>Click</Button>)

    await user.click(screen.getByRole('button'))
    expect(handleClick).toHaveBeenCalledTimes(1)
  })
})
```

**Key Points:**
- Use role-based queries (accessibility-first)
- Use userEvent over fireEvent
- vi.fn() for mock functions in Vitest
- Async/await for user interactions

### Utility Test Pattern

```typescript
import { describe, it, expect } from 'vitest'
import { cn } from '../utils'

describe('cn utility', () => {
  it('merges class names', () => {
    expect(cn('px-2', 'py-4')).toBe('px-2 py-4')
  })

  it('handles conditional classes', () => {
    expect(cn('base', false && 'hidden')).toBe('base')
  })
})
```

### Vitest Configuration Pattern

Create `vitest.config.ts` with React plugin and jsdom environment:

```typescript
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./vitest.setup.ts'],
    include: ['**/*.{test,spec}.{ts,tsx}'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html'],
      exclude: ['node_modules/', '**/*.d.ts']
    }
  }
})
```

### Vitest Setup File Pattern

Create `vitest.setup.ts` to configure jest-dom matchers:

```typescript
import '@testing-library/jest-dom'
```

**CRITICAL**: This file MUST be created - without it, matchers like `toBeInTheDocument()` will not work.

## Requirements

### Functional Requirements

1. **Frontend Test Infrastructure**
   - Description: Set up Vitest with React Testing Library for component testing
   - Acceptance: `pnpm test` runs all frontend tests successfully

2. **Frontend Component Coverage**
   - Description: Write tests for core UI components (Button, Input, Card) and key features (ChatInterface)
   - Acceptance: At least 5 component test files created with passing tests

3. **Frontend Utility Coverage**
   - Description: Write tests for lib utilities (utils.ts, auth-actions.ts)
   - Acceptance: All exported utility functions have test coverage

4. **Backend Test Enhancement**
   - Description: Add conftest.py with reusable fixtures, pyproject.toml with configuration
   - Acceptance: `pytest` runs with proper configuration and fixtures available

5. **Coverage Reporting**
   - Description: Configure and enable coverage reporting for both services
   - Acceptance: `pnpm test:coverage` and `pytest --cov` produce coverage reports

### Edge Cases

1. **Async Server Actions** - Mock server-side functions properly in tests
2. **React 19 Compatibility** - Ensure testing library versions are compatible
3. **Supabase Mocking** - Backend tests mock Supabase client to avoid real API calls
4. **Environment Variables** - Tests run without requiring real env vars

## Implementation Notes

### DO
- Follow the pattern in `backend/tests/test_api_integration.py` for mocking FastAPI dependencies
- Reuse Radix UI accessibility patterns (components have proper ARIA)
- Use `screen.getByRole()` for React component queries (accessibility-first)
- Use `vi.mock()` at top of test files before imports
- Clear FastAPI `dependency_overrides` after each test
- Add `.coverage` and `htmlcov/` to .gitignore

### DON'T
- Create tests that require real API keys or Supabase connections
- Use `getByTestId()` - prefer semantic queries
- Commit coverage artifacts to git
- Skip the vitest.setup.ts file - it's required for jest-dom matchers
- Forget to handle React 19's strict mode in tests

## Development Environment

### Start Services

```bash
# Frontend
pnpm dev

# Backend
cd backend && uvicorn main:app --reload --port 8000
```

### Service URLs
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

### Required Environment Variables
- `NEXT_PUBLIC_API_URL`: http://localhost:8000
- `NEXT_PUBLIC_SUPABASE_URL`: Required for frontend
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`: Required for frontend (mocked in tests)

## Success Criteria

The task is complete when:

1. [ ] `pnpm test` executes and passes all frontend tests
2. [ ] `pnpm test:coverage` generates coverage report for frontend
3. [ ] `pytest backend/tests/` passes all backend tests
4. [ ] `pytest --cov=backend backend/tests/` generates coverage report
5. [ ] At least 5 frontend component test files exist
6. [ ] At least 2 frontend lib test files exist
7. [ ] conftest.py with shared fixtures exists in backend/tests/
8. [ ] pyproject.toml with pytest config exists in backend/
9. [ ] No console errors in test output
10. [ ] Existing backend tests still pass

## QA Acceptance Criteria

**CRITICAL**: These criteria must be verified by the QA Agent before sign-off.

### Unit Tests
| Test | File | What to Verify |
|------|------|----------------|
| Button renders | `components/__tests__/button.test.tsx` | Button displays correctly, handles clicks |
| Input renders | `components/__tests__/input.test.tsx` | Input accepts text, shows placeholder |
| cn utility | `lib/__tests__/utils.test.ts` | Class name merging works correctly |
| Auth actions | `lib/__tests__/auth-actions.test.ts` | Async functions return expected results |
| Backend health | `backend/tests/test_api_integration.py` | Health check returns 200 |

### Integration Tests
| Test | Services | What to Verify |
|------|----------|----------------|
| API endpoints | backend | All existing backend integration tests pass |
| Query endpoint | backend | Request/response structure correct |

### End-to-End Tests
| Flow | Steps | Expected Outcome |
|------|-------|------------------|
| Run all tests | 1. `pnpm test` 2. Check output | All tests pass, no failures |
| Run backend tests | 1. `pytest backend/tests/` | All tests pass |
| Coverage check | 1. Run coverage commands | Reports generated |

### Browser Verification (if frontend)
| Page/Component | URL | Checks |
|----------------|-----|--------|
| N/A - Unit tests only | - | Tests run in jsdom, not real browser |

### Database Verification (if applicable)
| Check | Query/Command | Expected |
|-------|---------------|----------|
| N/A - Tests use mocks | - | All DB operations mocked |

### Configuration Verification
| File | Check | Expected |
|------|-------|----------|
| `vitest.config.ts` | Exists and valid | Configures jsdom, coverage |
| `vitest.setup.ts` | Exists and valid | Imports @testing-library/jest-dom |
| `backend/pyproject.toml` | Exists and valid | Configures pytest, coverage |
| `backend/tests/conftest.py` | Exists and valid | Exports shared fixtures |
| `package.json` | Has test scripts | "test", "test:coverage" present |

### QA Sign-off Requirements
- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] Frontend tests execute without errors
- [ ] Backend tests execute without errors
- [ ] Coverage reports generated for both services
- [ ] No regressions in existing functionality
- [ ] Code follows established patterns
- [ ] No security vulnerabilities introduced
