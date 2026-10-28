"""Circa normalization helpers. Official files are not bundled."""

from __future__ import annotations

from nlp.schemas import DialogueTurn, PragmaticExample

# Names taken from the Circa dataset card (goldstandard2 mapping described there).
# Rows whose gold label is NA are excluded from supervised training.
CIRCA_LABEL_MAP = {
    "Yes": "yes",
    "No": "no",
    "Yes, subject to some conditions": "yes_conditional",
    "In the middle, neither yes nor no": "middle",
    "Other": "other",
    "Probably yes / sometimes yes": "yes",
    "Probably no": "no",
    "I am not sure how X will interpret Y's answer": "middle",
}

CIRCA_DROP_LABELS = {"NA", "na", ""}


def normalize_circa_label(raw: str | None) -> str | None:
    if raw is None:
        return None
    text = raw.strip()
    if text in CIRCA_DROP_LABELS:
        return None
    if text in CIRCA_LABEL_MAP:
        return CIRCA_LABEL_MAP[text]
    return None


def circa_row_to_example(row: dict, *, version: str) -> PragmaticExample | None:
    label = normalize_circa_label(row.get("goldstandard2") or row.get("goldstandard1"))
    question = (row.get("question-X") or "").strip()
    answer = (row.get("answer-Y") or "").strip()
    situation = (row.get("context") or "").strip()
    if not question or not answer:
        return None
    example_id = str(row.get("id") or f"circa-{hash((situation, question, answer))}")
    turns = [
        DialogueTurn(turn_id="t0", speaker="X", text=question),
        DialogueTurn(turn_id="t1", speaker="Y", text=answer),
    ]
    return PragmaticExample(
        example_id=f"circa-{example_id}",
        dataset="circa",
        dataset_version=version,
        conversation_id=f"circa-q-{hash((situation, question))}",
        turns=turns,
        target_turn_id="t1",
        label=label,
        label_scheme="circa_goldstandard2",
        context_situation=situation or None,
        group_key=f"{situation}||{question}",
        language="en",
        is_synthetic=False,
        source_attribution=(
            "Louis, Roth, and Radlinski, EMNLP 2020. "
            "https://github.com/google-research-datasets/circa"
        ),
    )
