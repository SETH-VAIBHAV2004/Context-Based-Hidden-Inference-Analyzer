# Milestones

| ID | Name | Done when | Status |
| --- | --- | --- | --- |
| 0 | Repository bootstrap | Git, docs, gitignore, CI stub, env example | in progress |
| 1 | Schemas and validation | Conversation/example schemas, fixture loader, split leakage tests | not started |
| 2 | FastAPI skeleton | Health, dataset metadata, honest model-unavailable inference | not started |
| 3 | Circa loader | Official file validation, group splits, distribution report | not started |
| 4 | TF-IDF baseline | Train/eval on fixture and on Circa if present; real metrics JSON | not started |
| 5 | Evidence diagnostics | Span alignment, sufficiency/necessity on the sklearn model | not started |
| 6 | Next.js workbench | Pages wired to the API; empty/error states; no fake charts | not started |
| 7 | Transformers + experiments UI | Optional encoder models, comparison page from saved runs | not started |
| 8 | Docker / deploy docs | Compose files; commands; Docker build tested if Docker exists | not started |

Environment observed on 2026-10-28 (this machine):

- Python 3.11.0 (`py -3.11`) and also 3.13 (avoid 3.13 for ML pins)
- Node v22.15.0, npm 10.9.2
- Git 2.47.0
- Docker CLI **not installed**
