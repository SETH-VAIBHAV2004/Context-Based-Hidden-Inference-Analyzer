"""Load, validate, and split pragmatic examples without leaking groups."""

from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

from sklearn.model_selection import GroupShuffleSplit, train_test_split

from nlp.schemas import PragmaticExample

ALLOWED_FIXTURE_SUFFIXES = {".jsonl"}
MAX_UPLOAD_BYTES = 2_000_000


class DatasetError(ValueError):
    pass


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_jsonl_examples(path: Path) -> list[PragmaticExample]:
    if path.suffix.lower() not in ALLOWED_FIXTURE_SUFFIXES:
        raise DatasetError(f"unsupported file type: {path.suffix}")
    size = path.stat().st_size
    if size > MAX_UPLOAD_BYTES:
        raise DatasetError("file exceeds size limit")
    examples: list[PragmaticExample] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                payload = json.loads(line)
            except json.JSONDecodeError as exc:
                raise DatasetError(f"invalid JSON on line {line_number}") from exc
            examples.append(PragmaticExample.model_validate(payload))
    if not examples:
        raise DatasetError("no records found")
    return examples


def duplicate_keys(examples: list[PragmaticExample]) -> list[str]:
    seen: dict[tuple[str, str, str], str] = {}
    duplicates: list[str] = []
    for example in examples:
        target = next(t for t in example.turns if t.turn_id == example.target_turn_id)
        key = (example.context_situation or "", target.text, example.label or "")
        previous = seen.get(key)
        if previous:
            duplicates.append(example.example_id)
        else:
            seen[key] = example.example_id
    return duplicates


def label_distribution(examples: list[PragmaticExample]) -> dict[str, int]:
    counts = Counter(example.label or "<unlabeled>" for example in examples)
    return dict(sorted(counts.items()))


def group_aware_split(
    examples: list[PragmaticExample],
    *,
    seed: int = 13,
    train_ratio: float = 0.7,
    val_ratio: float = 0.15,
) -> dict[str, list[PragmaticExample]]:
    if not 0 < train_ratio < 1 or not 0 < val_ratio < 1 or train_ratio + val_ratio >= 1:
        raise DatasetError("split ratios must be positive and leave a test remainder")
    labeled = [ex for ex in examples if ex.label]
    if len(labeled) < 6:
        raise DatasetError("need at least 6 labeled examples to split")

    groups = [ex.group_key for ex in labeled]
    unique_groups = sorted(set(groups))
    if len(unique_groups) < 3:
        raise DatasetError("need at least 3 groups for a group-aware split")

    labels = [ex.label for ex in labeled]
    test_ratio = 1.0 - train_ratio - val_ratio

    splitter = GroupShuffleSplit(n_splits=1, test_size=test_ratio, random_state=seed)
    train_val_idx, test_idx = next(splitter.split(labeled, labels, groups))
    train_val = [labeled[i] for i in train_val_idx]
    test = [labeled[i] for i in test_idx]

    tv_groups = [ex.group_key for ex in train_val]
    relative_val = val_ratio / (train_ratio + val_ratio)
    if len(set(tv_groups)) < 2:
        raise DatasetError("not enough groups remaining for validation")
    tv_splitter = GroupShuffleSplit(n_splits=1, test_size=relative_val, random_state=seed)
    tv_labels = [ex.label for ex in train_val]
    train_idx, val_idx = next(tv_splitter.split(train_val, tv_labels, tv_groups))
    train = [train_val[i] for i in train_idx]
    val = [train_val[i] for i in val_idx]

    _assert_no_group_overlap(train, val, test)
    return {"train": train, "validation": val, "test": test}


def random_split_for_leakage_contrast(
    examples: list[PragmaticExample],
    *,
    seed: int = 13,
    test_ratio: float = 0.2,
) -> tuple[list[PragmaticExample], list[PragmaticExample]]:
    """Naive split used only to demonstrate leakage checks in tests."""
    labeled = [ex for ex in examples if ex.label]
    train, test = train_test_split(
        labeled, test_size=test_ratio, random_state=seed, shuffle=True
    )
    return train, test


def overlapping_groups(
    left: list[PragmaticExample], right: list[PragmaticExample]
) -> set[str]:
    return {ex.group_key for ex in left} & {ex.group_key for ex in right}


def split_report(splits: dict[str, list[PragmaticExample]]) -> dict:
    report: dict = {"splits": {}, "group_overlap": {}}
    names = list(splits)
    for name, items in splits.items():
        report["splits"][name] = {
            "n": len(items),
            "n_groups": len({ex.group_key for ex in items}),
            "labels": label_distribution(items),
        }
    for i, a in enumerate(names):
        for b in names[i + 1 :]:
            overlap = sorted(overlapping_groups(splits[a], splits[b]))
            report["group_overlap"][f"{a}|{b}"] = overlap
    return report


def _assert_no_group_overlap(
    train: list[PragmaticExample],
    val: list[PragmaticExample],
    test: list[PragmaticExample],
) -> None:
    pairs = [("train", train), ("validation", val), ("test", test)]
    for i, (na, a) in enumerate(pairs):
        for nb, b in pairs[i + 1 :]:
            overlap = overlapping_groups(a, b)
            if overlap:
                raise DatasetError(f"group leakage between {na} and {nb}: {sorted(overlap)}")


def examples_by_group(examples: list[PragmaticExample]) -> dict[str, list[str]]:
    grouped: dict[str, list[str]] = defaultdict(list)
    for example in examples:
        grouped[example.group_key].append(example.example_id)
    return dict(grouped)
