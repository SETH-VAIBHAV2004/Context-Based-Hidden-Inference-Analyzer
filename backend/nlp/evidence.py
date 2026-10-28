"""Extractive, source-grounded evidence. Not a claim about internal reasoning."""

from __future__ import annotations

import re

from nlp.context import get_target_turn
from nlp.schemas import EvidenceSpan, PragmaticExample

CUE_PATTERNS = [
    (r"\bif\b", "condition"),
    (r"\bonly if\b", "condition"),
    (r"\bdepends\b", "condition"),
    (r"\bnot\b|\bn't\b|\bnever\b|\bno\b", "negation"),
    (r"\bbut\b|\bhowever\b", "contrast"),
]


def span_from_turn(turn_id: str, text: str, role: str, source: str = "conversation") -> EvidenceSpan:
    return EvidenceSpan(
        turn_id=turn_id,
        start_char=0,
        end_char=len(text),
        text=text,
        role=role,  # type: ignore[arg-type]
        source=source,  # type: ignore[arg-type]
    )


def extract_cues(text: str, turn_id: str) -> list[EvidenceSpan]:
    spans: list[EvidenceSpan] = []
    lowered = text
    for pattern, _name in CUE_PATTERNS:
        for match in re.finditer(pattern, lowered, flags=re.IGNORECASE):
            spans.append(
                EvidenceSpan(
                    turn_id=turn_id,
                    start_char=match.start(),
                    end_char=match.end(),
                    text=text[match.start() : match.end()],
                    role="cue",
                    source="linguistic_feature",
                )
            )
    return spans


def collect_evidence(example: PragmaticExample) -> list[EvidenceSpan]:
    target = get_target_turn(example)
    evidence = [span_from_turn(target.turn_id, target.text, "target_utterance")]
    prior = None
    for turn in example.turns:
        if turn.turn_id == target.turn_id:
            break
        prior = turn
    if prior:
        evidence.append(span_from_turn(prior.turn_id, prior.text, "prior_question"))
    if example.context_situation:
        evidence.append(
            span_from_turn("situation", example.context_situation, "situation")
        )
    evidence.extend(extract_cues(target.text, target.turn_id))
    return evidence


def remove_spans_from_example(
    example: PragmaticExample, spans: list[EvidenceSpan]
) -> PragmaticExample:
    """Replace selected character spans with spaces (length-preserving)."""
    by_turn: dict[str, list[EvidenceSpan]] = {}
    for span in spans:
        by_turn.setdefault(span.turn_id, []).append(span)
    new_turns = []
    for turn in example.turns:
        text = turn.text
        chars = list(text)
        for span in by_turn.get(turn.turn_id, []):
            for i in range(span.start_char, min(span.end_char, len(chars))):
                chars[i] = " "
        new_turns.append(turn.model_copy(update={"text": "".join(chars)}))
    return example.model_copy(update={"turns": new_turns})
