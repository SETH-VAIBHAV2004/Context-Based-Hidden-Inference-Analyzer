"""Train and evaluate context-window ablations; persist metrics JSON."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from nlp.context import ContextWindow
from nlp.datasets.validation import group_aware_split, load_jsonl_examples, split_report
from nlp.models.tfidf_lr import evaluate, save_model, train, vectorizer_was_fit_on, texts_and_labels

ARTIFACT_DIR = Path(__file__).resolve().parents[2] / "artifacts"
DEFAULT_FIXTURE = Path(__file__).resolve().parents[2] / "data" / "fixtures" / "synthetic_pragmatics.jsonl"

WINDOWS = [
    ContextWindow(name="target_only"),
    ContextWindow(name="prev_1"),
    ContextWindow(name="situation_prev_1", include_situation=True),
]


def run_tfidf_ablations(
    data_path: Path = DEFAULT_FIXTURE,
    *,
    seed: int = 13,
    artifact_dir: Path = ARTIFACT_DIR,
) -> dict:
    examples = load_jsonl_examples(data_path)
    splits = group_aware_split(examples, seed=seed)
    train_texts, _ = texts_and_labels(splits["train"], ContextWindow(name="full"))
    started = datetime.now(timezone.utc).isoformat()
    runs = []
    for window in WINDOWS:
        model = train(splits["train"], window, seed=seed)
        train_window_texts, _ = texts_and_labels(splits["train"], window)
        assert vectorizer_was_fit_on(model.pipeline, train_window_texts)
        val_metrics = evaluate(model, splits["validation"])
        test_metrics = evaluate(model, splits["test"])
        artifact = artifact_dir / f"tfidf_lr_{window.name}.joblib"
        save_model(model, artifact)
        runs.append(
            {
                "model_id": "tfidf_lr",
                "window": window.model_dump(),
                "artifact": str(artifact),
                "validation": val_metrics,
                "test": test_metrics,
            }
        )
    payload = {
        "started_at": started,
        "finished_at": datetime.now(timezone.utc).isoformat(),
        "status": "completed",
        "seed": seed,
        "data_path": str(data_path),
        "split_report": split_report(splits),
        "n_train_documents_for_tfidf_check": len(train_texts),
        "runs": runs,
        "disclaimer": (
            "Metrics are computed from this run's predictions. "
            "If the data file is the synthetic fixture, do not report them as Circa results."
        ),
    }
    artifact_dir.mkdir(parents=True, exist_ok=True)
    metrics_path = artifact_dir / "last_tfidf_eval.json"
    metrics_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


if __name__ == "__main__":
    result = run_tfidf_ablations()
    print(json.dumps({"status": result["status"], "runs": len(result["runs"])}, indent=2))
