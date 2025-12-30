# Gotchas & Pitfalls

Things to watch out for in this codebase.

## [2025-12-30 16:14]
Installed versions are much newer than spec targets: langchain 1.2.0 (vs 0.3.x target), langgraph 1.0.5 (vs 0.2.x target). This is expected since requirements use >= constraints.

_Context: Dependency upgrade task 1.2 - pip install verification_
