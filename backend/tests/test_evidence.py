from pathlib import Path

from nlp.context import ContextWindow
from nlp.datasets.validation import load_jsonl_examples
from nlp.evidence import collect_evidence, extract_cues
from nlp.faithfulness import diagnose
from nlp.models.tfidf_lr import train
from nlp.schemas import EvidenceSpan

FIXTURE = Path(__file__).resolve().parents[2] / "data" / "fixtures" / "synthetic_pragmatics.jsonl"


def test_evidence_spans_align_to_utterance_text():
    example = load_jsonl_examples(FIXTURE)[2]
    evidence = collect_evidence(example)
    target = next(span for span in evidence if span.role == "target_utterance")
    turn = next(t for t in example.turns if t.turn_id == example.target_turn_id)
    assert turn.text[target.start_char : target.end_char] == target.text
    cues = extract_cues(turn.text, turn.turn_id)
    for cue in cues:
        assert turn.text[cue.start_char : cue.end_char] == cue.text


def test_invalid_span_rejected():
    try:
        EvidenceSpan(
            turn_id="t1",
            start_char=0,
            end_char=3,
            text="if",
            role="cue",
            source="conversation",
        )
        raised = False
    except ValueError:
        raised = True
    assert raised


def test_faithfulness_diagnostics_are_labeled_as_limitations():
    examples = load_jsonl_examples(FIXTURE)
    model = train(examples, ContextWindow(name="prev_1"), seed=2)
    report = diagnose(model, examples[2])
    assert report["human_gold_spans"] is False
    assert "limitation" in report["sufficiency"]
    assert "limitation" in report["necessity"]
    assert report["sufficiency"]["original_label"] in model.labels
