from nlp.schemas import DialogueTurn, EvidenceSpan, PragmaticExample
import pytest


def test_evidence_span_requires_matching_offsets():
    with pytest.raises(ValueError):
        EvidenceSpan(
            turn_id="t1",
            start_char=0,
            end_char=4,
            text="no",
            role="cue",
            source="conversation",
        )


def test_target_turn_must_exist():
    with pytest.raises(ValueError):
        PragmaticExample(
            example_id="x",
            dataset="synthetic_pragmatics",
            dataset_version="v1",
            conversation_id="c",
            turns=[DialogueTurn(turn_id="t0", speaker="X", text="Hi")],
            target_turn_id="missing",
            label_scheme="x",
            group_key="g",
            language="synthetic",
            source_attribution="test",
        )
