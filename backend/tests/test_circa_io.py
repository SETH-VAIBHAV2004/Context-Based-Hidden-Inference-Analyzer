from pathlib import Path

import pytest

from nlp.datasets.circa_io import load_circa_table
from nlp.datasets.validation import DatasetError


def test_circa_loader_rejects_executables(tmp_path: Path):
    bad = tmp_path / "payload.exe"
    bad.write_bytes(b"MZ")
    with pytest.raises(DatasetError):
        load_circa_table(bad)


def test_circa_loader_reads_minimal_tsv(tmp_path: Path):
    path = tmp_path / "circa.tsv"
    path.write_text(
        "id\tcontext\tquestion-X\tanswer-Y\tgoldstandard2\n"
        "1\tfood talk\tDo you like spicy food?\tI put hot sauce on everything.\tYes\n"
        "2\tfood talk\tDo you like spicy food?\tEven pepper is too much.\tNo\n"
        "3\tfood talk\tDo you eat meat?\tIf it is local.\tYes, subject to some conditions\n"
        "4\tfood talk\tAre you vegan?\tMaybe.\tNA\n",
        encoding="utf-8",
    )
    examples = load_circa_table(path)
    assert len(examples) == 3
    assert {ex.label for ex in examples} == {"yes", "no", "yes_conditional"}
    assert all(not ex.is_synthetic for ex in examples)
    assert examples[0].group_key.endswith("Do you like spicy food?")
