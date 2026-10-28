"""Observable faithfulness diagnostics. Prediction change is not causal proof."""

from __future__ import annotations

from nlp.context import format_model_text
from nlp.evidence import collect_evidence, remove_spans_from_example
from nlp.models.tfidf_lr import TrainedBaseline
from nlp.schemas import EvidenceSpan, PragmaticExample


def _predict_label(model: TrainedBaseline, example: PragmaticExample) -> str:
    text = format_model_text(example, model.window)
    return str(model.pipeline.predict([text])[0])


def sufficiency(
    model: TrainedBaseline,
    example: PragmaticExample,
    evidence: list[EvidenceSpan],
) -> dict:
    """Keep only evidenced turns (others blanked) and see if the label is preserved."""
    original = _predict_label(model, example)
    keep_ids = {span.turn_id for span in evidence if span.source == "conversation"}
    blanked_turns = []
    for turn in example.turns:
        if turn.turn_id in keep_ids:
            blanked_turns.append(turn)
        else:
            blanked_turns.append(turn.model_copy(update={"text": " "}))
    reduced = example.model_copy(update={"turns": blanked_turns, "context_situation": None})
    reduced_label = _predict_label(model, reduced)
    return {
        "original_label": original,
        "reduced_label": reduced_label,
        "label_preserved": original == reduced_label,
        "limitation": (
            "Sufficiency here means the sklearn model produced the same class "
            "after non-evidence turns were blanked. It does not prove that the "
            "spans caused the original decision."
        ),
    }


def necessity(
    model: TrainedBaseline,
    example: PragmaticExample,
    evidence: list[EvidenceSpan],
) -> dict:
    original = _predict_label(model, example)
    removed = remove_spans_from_example(example, evidence)
    new_label = _predict_label(model, removed)
    return {
        "original_label": original,
        "label_after_removal": new_label,
        "label_changed": original != new_label,
        "limitation": (
            "A label change after deletion is a diagnostic, not a causal explanation "
            "of the classifier."
        ),
    }


def diagnose(model: TrainedBaseline, example: PragmaticExample) -> dict:
    evidence = collect_evidence(example)
    conversational = [span for span in evidence if span.source == "conversation"]
    return {
        "evidence": [span.model_dump() for span in evidence],
        "sufficiency": sufficiency(model, example, conversational),
        "necessity": necessity(model, example, conversational),
        "human_gold_spans": False,
        "note": "No human evidence annotations are available for this example.",
    }
