from pathlib import Path

import pytest

from nlp.datasets.circa import normalize_circa_label
from nlp.datasets.validation import (
    DatasetError,
    duplicate_keys,
    group_aware_split,
    label_distribution,
    load_jsonl_examples,
    overlapping_groups,
    random_split_for_leakage_contrast,
)
from nlp.context import ContextWindow, format_model_text, select_turns

FIXTURE = Path(__file__).resolve().parents[2] / "data" / "fixtures" / "synthetic_pragmatics.jsonl"


def test_fixture_loads_and_is_marked_synthetic():
    examples = load_jsonl_examples(FIXTURE)
    assert len(examples) == 12
    assert all(ex.is_synthetic for ex in examples)
    assert set(label_distribution(examples)) == {"yes", "no", "yes_conditional"}


def test_rejects_unknown_extension(tmp_path: Path):
    bad = tmp_path / "data.exe"
    bad.write_bytes(b"not a dataset")
    with pytest.raises(DatasetError):
        load_jsonl_examples(bad)


def test_circa_label_map_drops_na():
    assert normalize_circa_label("NA") is None
    assert normalize_circa_label("Yes") == "yes"
    assert normalize_circa_label("Yes, subject to some conditions") == "yes_conditional"


def test_group_aware_split_has_no_group_leakage():
    examples = load_jsonl_examples(FIXTURE)
    splits = group_aware_split(examples, seed=7, train_ratio=0.5, val_ratio=0.25)
    assert overlapping_groups(splits["train"], splits["test"]) == set()
    assert overlapping_groups(splits["train"], splits["validation"]) == set()
    assert overlapping_groups(splits["validation"], splits["test"]) == set()
    total = sum(len(v) for v in splits.values())
    assert total == len(examples)


def test_random_split_can_leak_groups():
    examples = load_jsonl_examples(FIXTURE)
    train, test = random_split_for_leakage_contrast(examples, seed=0, test_ratio=0.4)
    # The fixture reuses questions, so a naive split is expected to leak for some seeds.
    leaked = overlapping_groups(train, test)
    assert leaked  # documents why group-aware splitting is required


def test_duplicate_detection():
    examples = load_jsonl_examples(FIXTURE)
    assert duplicate_keys(examples) == []


def test_context_windows():
    examples = load_jsonl_examples(FIXTURE)
    example = examples[0]
    target_only = ContextWindow(name="target_only")
    prev = ContextWindow(name="prev_1")
    situ = ContextWindow(name="situation_prev_1", include_situation=True)
    assert [t.turn_id for t in select_turns(example, target_only)] == ["t1"]
    assert [t.turn_id for t in select_turns(example, prev)] == ["t0", "t1"]
    text = format_model_text(example, situ)
    assert "[SITUATION]" in text
    assert "[TARGET]" in text
    assert example.turns[0].text in format_model_text(example, prev)
    assert example.turns[0].text not in format_model_text(example, target_only)
