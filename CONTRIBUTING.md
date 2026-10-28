# Contributing

This is a student Computational Linguistics research codebase. Changes should be small, testable, and scientifically conservative.

## Ground rules

1. Do not invent metrics, citations, dataset properties, or deployment status.
2. Distinguish planned work from completed experiments in the UI and docs.
3. Do not commit secrets, dataset dumps, or model checkpoints.
4. Fit vectorizers and other learned preprocessors on training data only.
5. Do not mix incompatible label schemes without an explicit mapping document.
6. SwordsmanImp is a Chinese resource. Do not treat translations as equivalent English data.

## Local workflow

1. Create a Python 3.11 virtual environment in `backend/.venv`.
2. Install backend dependencies from `backend/pyproject.toml`.
3. Run `pytest` from `backend/`.
4. After the frontend exists, run lint, typecheck, and Vitest from `frontend/`.
5. Open a focused pull request or commit with a conventional message.

## Commit messages

Use prefixes such as `chore:`, `docs:`, `feat:`, `test:`, `fix:`, `ci:`, and `deploy:`.

## Review checklist

- Tests cover the changed behavior.
- Empty/error states are honest when models or data are missing.
- New dependencies are pinned and justified.
