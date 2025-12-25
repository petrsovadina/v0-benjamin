# Testing Guide

## Backend Testing

The backend uses `pytest` for unit and integration testing.

### Prerequisites
Ensure you have the backend development dependencies installed:
```bash
pip install -r backend/requirements.txt
```

### Running Tests
To run all tests:
```bash
pytest backend/tests/
```

### Writing Tests
- Place new tests in `backend/tests/`.
- File names should start with `test_`.
- Use `pytest` fixtures for setup (e.g., database connections, API clients).

## CI/CD Integration

We use **GitHub Actions** for continuous integration. The pipeline is defined in `.github/workflows/ci.yml`.

### Workflow Steps
1.  **Backend Test**:
    - Sets up Python 3.11.
    - Installs dependencies.
    - Runs `pytest` with dummy environment variables to ensure logic correctness without needing live API keys.
2.  **Frontend Build**:
    - Sets up Node.js.
    - Installs npm dependencies.
    - Runs `npm run build` to verify TypeScript types and build success.

### Triggering
The pipeline runs automatically on:
- Pushes to `main` and `dev` branches.
- Pull Requests targeting `main` and `dev`.
