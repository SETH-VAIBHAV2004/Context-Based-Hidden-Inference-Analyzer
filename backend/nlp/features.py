"""Lightweight linguistic cues used when spaCy is not installed.

These are surface features, not a full syntactic analysis. POS and dependency
counts are omitted unless a spaCy model is explicitly loaded elsewhere.
"""

from __future__ import annotations

import re

from nlp.schemas import PragmaticExample

FEATURE_NAMES = [
    "char_len",
    "token_count",
    "question_marks",
    "negation_cues",
    "conditional_cues",
    "contrast_cues",
    "modality_cues",
]


def extract_feature_vector(text: str) -> list[float]:
    tokens = re.findall(r"\w+", text.lower())
    joined = " ".join(tokens)
    return [
        float(len(text)),
        float(len(tokens)),
        float(text.count("?")),
        float(len(re.findall(r"\b(not|never|no|cannot|can't|n't)\b", joined))),
        float(len(re.findall(r"\b(if|unless|provided|depends)\b", joined))),
        float(len(re.findall(r"\b(but|however|although)\b", joined))),
        float(len(re.findall(r"\b(would|could|might|should|may)\b", joined))),
    ]


def example_feature_vector(example: PragmaticExample) -> list[float]:
    target = next(t for t in example.turns if t.turn_id == example.target_turn_id)
    prior = ""
    for turn in example.turns:
        if turn.turn_id == example.target_turn_id:
            break
        prior = turn.text
    situation = example.context_situation or ""
    return extract_feature_vector(f"{situation} {prior} {target.text}")
