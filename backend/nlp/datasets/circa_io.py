"""Load an official Circa TSV/CSV from a local path. Does not download data."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from nlp.datasets.circa import circa_row_to_example
from nlp.datasets.validation import DatasetError, file_sha256
from nlp.schemas import PragmaticExample

MAX_CIRCA_BYTES = 50_000_000
ALLOWED = {".tsv", ".csv"}


def load_circa_table(path: Path) -> list[PragmaticExample]:
    if path.suffix.lower() not in ALLOWED:
        raise DatasetError(f"Circa loader accepts TSV/CSV only, not {path.suffix}")
    if not path.is_file():
        raise DatasetError(f"Circa file not found: {path}")
    if path.stat().st_size > MAX_CIRCA_BYTES:
        raise DatasetError("Circa file exceeds size limit")
    sep = "\t" if path.suffix.lower() == ".tsv" else ","
    frame = pd.read_csv(path, sep=sep, dtype=str).fillna("")
    required = {"id", "context", "question-X", "answer-Y"}
    missing = required - set(frame.columns)
    if missing:
        raise DatasetError(f"Circa file missing columns: {sorted(missing)}")
    version = f"sha256:{file_sha256(path)[:12]}"
    examples: list[PragmaticExample] = []
    for row in frame.to_dict(orient="records"):
        example = circa_row_to_example(row, version=version)
        if example and example.label:
            examples.append(example)
    if not examples:
        raise DatasetError("no labeled Circa rows after NA filtering")
    return examples
