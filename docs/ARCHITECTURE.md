# Architecture

Status: design document. Implementation status is tracked in `docs/MILESTONES.md`.

## Goal

Build a research platform that:

1. Loads a verified pragmatic-inference dataset with attribution and license notes.
2. Trains and evaluates baselines under documented context windows.
3. Runs inference on user-entered multi-turn conversations when a trained model exists.
4. Attaches evidence to exact utterance IDs/spans.
5. Records experiment metadata without inventing results.

## Runtime topology

```
Browser (Next.js)
    -> HTTP JSON (versioned /api/v1)
Python FastAPI
    -> NLP library (dataset, models, evidence, evaluation)
    -> SQLite experiment store (local)
    -> optional files: Circa TSV, sklearn joblib, later transformers
```

Heavy models stay in the backend. The frontend never loads PyTorch or dataset dumps.

## Packages

| Path | Role |
| --- | --- |
| `backend/app` | FastAPI routes, settings, error model |
| `backend/nlp` | Dataset IO, splitting, models, evidence, metrics |
| `backend/tests` | pytest |
| `frontend` | Next.js research UI |
| `data/fixtures` | Tiny synthetic records for tests and labeled demo mode |
| `docs` | Research and operations notes |

## Inference contract (stable)

Request: conversation turns, target turn id, context window, model id.

Response always includes:

- `status`: `ok` | `model_unavailable` | `invalid_input`
- `literal_utterance`
- `predicted_label` (null if unavailable)
- `context_used` (exact turns fed to the model)
- `evidence` (structured, possibly empty)
- `limitations` (human-readable, always present when assumptions apply)

Confidence scores are returned only if the selected model actually produces them (for example, logistic regression probabilities). Calibration plots appear only after a calibration procedure has been run.

## Models (planned, not all implemented yet)

1. TF-IDF + Logistic Regression (first working path).
2. Transformer utterance baseline.
3. Context-aware transformer.
4. Context + linguistic features.
5. Optional LLM baseline only if a documented provider and credentials are configured.

## Persistence

SQLite is enough for local experiment metadata. PostgreSQL is documented as a production option and is not required for the student demo.

## Risks

| Risk | Mitigation |
| --- | --- |
| No large English multi-turn implicature corpus with evidence spans | Primary task is Circa pragmatic label prediction; evidence metrics stay diagnostic unless human spans exist |
| Circa is mostly two-turn | Context-window experiments still compare answer-only vs situation+question+answer; multi-turn is a documented generalization in the workbench |
| Transformers may not fit a free host | Demo mode uses the sklearn baseline; Docker documents CPU vs GPU |
| spaCy model download | Linguistic features are optional; tests use a lightweight fallback tokenizer when the model is absent |
| Docker not installed on this development machine | Compose files are provided; builds are verified later when Docker is available |
| Label leakage via repeated Circa questions | Group-aware splits by situation + question |
