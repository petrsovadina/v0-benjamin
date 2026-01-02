# Task Completion Workflow

When a task is completed, follow these steps:

1.  **Verify Changes**: Ensure the changes meet the requirements.
2.  **Linting**:
    *   Frontend: Run `pnpm lint` to check for linting errors.
    *   Backend: Ensure code follows Python standards (e.g., PEP 8).
3.  **Testing**:
    *   Backend: Run `pytest backend/` to ensure no regressions.
    *   Frontend: Run any available tests (check `package.json` for test scripts if added later).
4.  **Cleanup**: Remove any temporary files or debug prints.
5.  **Documentation**: Update documentation if necessary (e.g., `README.md`, `CLAUDE.md`).
6.  **Commit**: Prepare a clear commit message describing the changes.
