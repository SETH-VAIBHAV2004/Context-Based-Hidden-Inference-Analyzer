"""Build model inputs from a documented context-window policy."""

from __future__ import annotations

from nlp.schemas import ContextWindow, DialogueTurn, PragmaticExample


def get_target_turn(example: PragmaticExample) -> DialogueTurn:
    for turn in example.turns:
        if turn.turn_id == example.target_turn_id:
            return turn
    raise ValueError("target turn missing")


def select_turns(example: PragmaticExample, window: ContextWindow) -> list[DialogueTurn]:
    target_index = next(
        i for i, turn in enumerate(example.turns) if turn.turn_id == example.target_turn_id
    )
    if window.name == "target_only":
        start = target_index
    elif window.name == "prev_1":
        start = max(0, target_index - 1)
    elif window.name in {"situation_prev_1", "full"}:
        if window.max_previous_turns is None:
            start = 0 if window.name == "full" else max(0, target_index - 1)
        else:
            start = max(0, target_index - window.max_previous_turns)
    else:
        raise ValueError(f"unsupported window {window.name}")
    return example.turns[start : target_index + 1]


def format_model_text(example: PragmaticExample, window: ContextWindow) -> str:
    parts: list[str] = []
    if window.include_situation or window.name == "situation_prev_1":
        if example.context_situation:
            parts.append(f"[SITUATION] {example.context_situation}")
    selected = select_turns(example, window)
    target_id = example.target_turn_id
    for turn in selected:
        marker = "[TARGET]" if turn.turn_id == target_id else "[CONTEXT]"
        parts.append(f"{marker} {turn.speaker}: {turn.text}")
    return "\n".join(parts)
