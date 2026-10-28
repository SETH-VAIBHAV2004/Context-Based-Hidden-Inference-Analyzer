"""Canonical data contracts for conversations, examples, and evidence."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, field_validator, model_validator


class DialogueTurn(BaseModel):
    turn_id: str = Field(min_length=1)
    speaker: str = Field(min_length=1)
    text: str = Field(min_length=1)


class EvidenceSpan(BaseModel):
    turn_id: str
    start_char: int = Field(ge=0)
    end_char: int = Field(ge=0)
    text: str
    role: Literal[
        "target_utterance",
        "prior_question",
        "situation",
        "cue",
        "human_annotation",
    ]
    source: Literal["conversation", "linguistic_feature", "model_attribution"]

    @model_validator(mode="after")
    def span_must_match_text(self) -> EvidenceSpan:
        if self.end_char < self.start_char:
            raise ValueError("end_char must be >= start_char")
        if len(self.text) != self.end_char - self.start_char:
            raise ValueError("text length must equal end_char - start_char")
        return self


class PragmaticExample(BaseModel):
    example_id: str
    dataset: str
    dataset_version: str
    conversation_id: str
    turns: list[DialogueTurn]
    target_turn_id: str
    label: str | None = None
    label_scheme: str
    context_situation: str | None = None
    implicature_text: str | None = None
    evidence_spans: list[EvidenceSpan] = Field(default_factory=list)
    group_key: str
    language: Literal["en", "zh", "synthetic"]
    is_synthetic: bool = False
    source_attribution: str

    @field_validator("turns")
    @classmethod
    def turns_not_empty(cls, value: list[DialogueTurn]) -> list[DialogueTurn]:
        if not value:
            raise ValueError("turns must be non-empty")
        ids = [turn.turn_id for turn in value]
        if len(ids) != len(set(ids)):
            raise ValueError("turn_id values must be unique")
        return value

    @model_validator(mode="after")
    def target_must_exist(self) -> PragmaticExample:
        ids = {turn.turn_id for turn in self.turns}
        if self.target_turn_id not in ids:
            raise ValueError("target_turn_id must refer to a turn in turns")
        return self


class ContextWindow(BaseModel):
    name: Literal["target_only", "prev_1", "situation_prev_1", "full"]
    include_situation: bool = False
    max_previous_turns: int | None = None
