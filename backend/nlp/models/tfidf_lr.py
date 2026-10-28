"""TF-IDF + Logistic Regression baseline with train-only vectorizer fitting."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
)
from sklearn.pipeline import Pipeline

from nlp.context import ContextWindow, format_model_text
from nlp.schemas import PragmaticExample

VECTORIZER_PARAMS = {
    "ngram_range": (1, 2),
    "min_df": 1,
    "sublinear_tf": True,
    "smooth_idf": True,
    "norm": "l2",
    "lowercase": True,
}


@dataclass
class TrainedBaseline:
    pipeline: Pipeline
    labels: list[str]
    window: ContextWindow
    dataset: str
    dataset_version: str
    seed: int


def build_pipeline(seed: int = 13) -> Pipeline:
    return Pipeline(
        [
            ("tfidf", TfidfVectorizer(**VECTORIZER_PARAMS)),
            (
                "clf",
                LogisticRegression(
                    max_iter=500,
                    class_weight="balanced",
                    random_state=seed,
                    solver="lbfgs",
                ),
            ),
        ]
    )


def format_texts(examples: list[PragmaticExample], window: ContextWindow) -> list[str]:
    return [format_model_text(ex, window) for ex in examples]


def texts_and_labels(
    examples: list[PragmaticExample], window: ContextWindow
) -> tuple[list[str], list[str]]:
    labeled = [ex for ex in examples if ex.label]
    return format_texts(labeled, window), [ex.label for ex in labeled]


def predict_one(model: TrainedBaseline, example: PragmaticExample) -> tuple[str, dict[str, float]]:
    text = format_model_text(example, model.window)
    label = str(model.pipeline.predict([text])[0])
    proba = model.pipeline.predict_proba([text])[0]
    return label, {cls: float(score) for cls, score in zip(model.labels, proba, strict=True)}


def vectorizer_was_fit_on(pipeline: Pipeline, documents: list[str]) -> bool:
    """True if every vocabulary item occurs in the provided documents (training set)."""
    vocab = pipeline.named_steps["tfidf"].vocabulary_
    vectorizer = TfidfVectorizer(**VECTORIZER_PARAMS)
    vectorizer.fit(documents)
    train_vocab = set(vectorizer.vocabulary_)
    return set(vocab).issubset(train_vocab)


def train(
    train_examples: list[PragmaticExample],
    window: ContextWindow,
    *,
    seed: int = 13,
) -> TrainedBaseline:
    X, y = texts_and_labels(train_examples, window)
    if len(set(y)) < 2:
        raise ValueError("training data must contain at least two labels")
    pipeline = build_pipeline(seed)
    pipeline.fit(X, y)
    return TrainedBaseline(
        pipeline=pipeline,
        labels=list(pipeline.named_steps["clf"].classes_),
        window=window,
        dataset=train_examples[0].dataset,
        dataset_version=train_examples[0].dataset_version,
        seed=seed,
    )


def predict_proba(model: TrainedBaseline, examples: list[PragmaticExample]) -> np.ndarray:
    X, _ = texts_and_labels(examples, model.window)
    return model.pipeline.predict_proba(X)


def evaluate(model: TrainedBaseline, examples: list[PragmaticExample]) -> dict:
    labeled = [ex for ex in examples if ex.label]
    labels = model.labels
    if not labeled:
        return {
            "n_examples": 0,
            "accuracy": None,
            "macro_f1": None,
            "per_class": {},
            "confusion_matrix": {"labels": labels, "matrix": []},
            "window": model.window.model_dump(),
            "dataset": model.dataset,
            "dataset_version": model.dataset_version,
            "seed": model.seed,
            "is_synthetic_data": True,
            "note": "No labeled examples were provided to evaluate().",
        }
    X, y_true = texts_and_labels(labeled, model.window)
    y_pred = model.pipeline.predict(X)
    labels = model.labels
    report = classification_report(
        y_true, y_pred, labels=labels, output_dict=True, zero_division=0
    )
    matrix = confusion_matrix(y_true, y_pred, labels=labels)
    return {
        "n_examples": len(labeled),
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "macro_f1": float(f1_score(y_true, y_pred, average="macro", zero_division=0)),
        "per_class": {
            label: {
                "precision": report[label]["precision"],
                "recall": report[label]["recall"],
                "f1": report[label]["f1-score"],
                "support": report[label]["support"],
            }
            for label in labels
            if label in report
        },
        "confusion_matrix": {
            "labels": labels,
            "matrix": matrix.tolist(),
        },
        "window": model.window.model_dump(),
        "dataset": model.dataset,
        "dataset_version": model.dataset_version,
        "seed": model.seed,
        "is_synthetic_data": all(ex.is_synthetic for ex in labeled),
    }


def save_model(model: TrainedBaseline, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, path)


def load_model(path: Path) -> TrainedBaseline:
    loaded = joblib.load(path)
    if not isinstance(loaded, TrainedBaseline):
        raise TypeError("artifact is not a TrainedBaseline")
    return loaded
