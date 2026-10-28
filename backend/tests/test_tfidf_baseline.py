from pathlib import Path

from nlp.context import ContextWindow
from nlp.datasets.validation import group_aware_split, load_jsonl_examples
from nlp.experiments import run_tfidf_ablations
from nlp.models.tfidf_lr import evaluate, train, vectorizer_was_fit_on, texts_and_labels

FIXTURE = Path(__file__).resolve().parents[2] / "data" / "fixtures" / "synthetic_pragmatics.jsonl"


def test_tfidf_vocabulary_is_subset_of_training_documents():
    examples = load_jsonl_examples(FIXTURE)
    splits = group_aware_split(examples, seed=3)
    window = ContextWindow(name="prev_1")
    model = train(splits["train"], window, seed=3)
    train_texts, _ = texts_and_labels(splits["train"], window)
    test_texts, _ = texts_and_labels(splits["test"], window)
    assert vectorizer_was_fit_on(model.pipeline, train_texts)
    vocab = set(model.pipeline.named_steps["tfidf"].vocabulary_)
    nonce = "xyzzynonceleakage"
    leaked_docs = [text + " " + nonce for text in test_texts]
    leaked_vectorizer = __import__(
        "sklearn.feature_extraction.text", fromlist=["TfidfVectorizer"]
    ).TfidfVectorizer
    from nlp.models.tfidf_lr import VECTORIZER_PARAMS

    extra = leaked_vectorizer(**VECTORIZER_PARAMS)
    extra.fit(train_texts + leaked_docs)
    assert nonce in extra.vocabulary_
    assert nonce not in vocab


def test_evaluation_metrics_are_computed_from_predictions(tmp_path: Path):
    payload = run_tfidf_ablations(FIXTURE, seed=13, artifact_dir=tmp_path)
    assert payload["status"] == "completed"
    assert len(payload["runs"]) == 3
    for run in payload["runs"]:
        test = run["test"]
        assert test["n_examples"] > 0
        assert 0.0 <= test["accuracy"] <= 1.0
        assert 0.0 <= test["macro_f1"] <= 1.0
        assert test["is_synthetic_data"] is True
        assert Path(run["artifact"]).is_file()
    assert (tmp_path / "last_tfidf_eval.json").is_file()


def test_evaluate_empty_labeled_set_is_safe():
    examples = load_jsonl_examples(FIXTURE)
    model = train(examples[:8], ContextWindow(name="target_only"), seed=1)
    unlabeled = [ex.model_copy(update={"label": None}) for ex in examples[:2]]
    metrics = evaluate(model, unlabeled)
    assert metrics["n_examples"] == 0
    assert metrics["accuracy"] is None
