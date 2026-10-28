# Deployment

Status: **not deployed**. This file is a plan plus local commands. No hosting account has been configured from this repository.

## Local development (intended)

Backend:

```
py -3.11 -m venv backend/.venv
backend\.venv\Scripts\activate
pip install -e ".[dev]"
uvicorn app.main:app --app-dir backend --reload --port 8000
```

Frontend (after Milestone 6):

```
cd frontend
npm install
npm run dev
```

## Suggested hosting (not provisioned)

| Piece | Candidate | Notes |
| --- | --- | --- |
| Next.js UI | Vercel or Cloudflare Pages | Free tiers typically enough for the static/SSR UI |
| FastAPI + sklearn demo | Render, Fly.io, or a campus VM | Keep the demo on Logistic Regression so cold starts stay small |
| Transformer training | Local GPU or a short-lived cloud VM | Do not assume a free web host can fine-tune or serve large encoders |

Costs depend on the provider plan you choose. This project has **not** incurred hosting costs yet.

## Environment variables

See `.env.example`. Secrets belong only on the backend host. `NEXT_PUBLIC_*` must not contain API keys.

## Docker

Compose files will live at the repo root. They have not been built on this machine because Docker is not installed.

## HTTPS

When a public domain is added, terminate TLS at the host/proxy. If authentication is added later, use secure cookies (`Secure`, `HttpOnly`, `SameSite`). Authentication is **not** in scope until private user data exists.
