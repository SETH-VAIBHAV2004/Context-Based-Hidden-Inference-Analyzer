# Inferring the Unsaid

Explainable, context-aware pragmatic reasoning for multi-turn conversations.

This repository is a Computational Linguistics research platform: dataset tooling, models, evaluation, and a professional web workbench. It is **not** a chatbot product.

**Implementation status:** repository initialized with research documentation. Runtime application, trained models, and evaluation metrics are **not** available until later milestones complete.

## Research hypothesis

Combining conversational context, explicit linguistic features, and evidence-based explanations can improve pragmatic inference and make predictions more interpretable.

That statement is a hypothesis. It has not been confirmed by experiments in this repository.

## What is implemented now

- ✅ Project documentation, license for **code**, contribution rules, and GitHub Actions stub
- ✅ Dataset schemas and validation with group-aware splits
- ✅ FastAPI backend with health, dataset, model, training, and inference endpoints
- ✅ TF-IDF + Logistic Regression baseline with context window experiments
- ✅ Model training and evaluation pipeline
- ✅ Next.js frontend with professional research UI
- ✅ Analysis Workbench for interactive pragmatic inference
- ✅ Experiments page for model training and metrics visualization
- ✅ Dataset explorer with Circa integration

See `docs/MILESTONES.md` for the live checklist.

## Setup

### Backend (Python 3.11)

```powershell
py -3.11 -m venv backend/.venv
backend\.venv\Scripts\activate
cd backend
pip install -e ".[dev]"
pytest
```

### Frontend (Node.js)

```powershell
cd frontend
npm install
npm run dev
```

The frontend will be available at http://localhost:3000

### Run Backend API

In a separate terminal:

```powershell
cd backend
.\.venv\Scripts\activate
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

## Quick Start

1. Start the backend API (see above)
2. Start the frontend dev server (see above)
3. Navigate to http://localhost:3000
4. Go to Experiments page and train the TF-IDF model on synthetic data
5. Go to Workbench and run pragmatic inference on sample conversations

## Using Circa Dataset

1. Download the official Circa TSV from https://github.com/google-research-datasets/circa
2. Set the environment variable: `CIRCA_PATH=path/to/circa.tsv`
3. Restart the backend
4. Train models using the Circa dataset option

## Connecting GitHub (you run this)

This repo has not been pushed. After you create an empty GitHub repository you own:

```
git remote add origin https://github.com/<your-user>/<your-repo>.git
git branch -M main
git push -u origin main
```

Use SSH if you prefer (`git@github.com:...`). Do not put tokens in the remote URL.

## Integrity

- No fabricated metrics in the UI.
- Fixtures are labeled synthetic.
- Dataset files and checkpoints are gitignored.

## License

MIT for original code (`LICENSE`). Datasets keep their own licenses (`docs/DATASETS.md`).
