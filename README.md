# Inferring the Unsaid

Explainable, context-aware pragmatic reasoning for multi-turn conversations.

This repository is a Computational Linguistics research platform: dataset tooling, models, evaluation, and a professional web workbench. It is **not** a chatbot product.

**Implementation status:** repository initialized with research documentation. Runtime application, trained models, and evaluation metrics are **not** available until later milestones complete.

## Research hypothesis

Combining conversational context, explicit linguistic features, and evidence-based explanations can improve pragmatic inference and make predictions more interpretable.

That statement is a hypothesis. It has not been confirmed by experiments in this repository.

## What is implemented now

- Project documentation, license for **code**, contribution rules, and GitHub Actions stub.
- Dataset policy: Circa as the intended English classification corpus; SwordsmanImp documented as Chinese-only related work.

See `docs/MILESTONES.md` for the live checklist.

## Setup (Python 3.11)

```
py -3.11 -m venv backend/.venv
backend\.venv\Scripts\activate
cd backend
pip install -e ".[dev]"
pytest
```

Frontend and Docker commands will be added when those milestones exist.

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
