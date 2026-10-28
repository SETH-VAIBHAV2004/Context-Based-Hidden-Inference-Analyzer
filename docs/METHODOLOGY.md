# Methodology

Status: **draft for human review**. Experiments have not been run. Do not quote this file as containing results.

## Problem

Speakers often mean more than they literally say. A computational system that only classifies a single isolated sentence can miss the question under discussion, prior turns, and linguistic cues that make an indirect answer interpretable.

## Research questions

1. Does adding conversational context (situation + prior turn, or more turns when available) improve pragmatic label prediction relative to the target utterance alone?
2. Do explicit linguistic features add anything beyond a text encoder or TF-IDF representation?
3. Can we attach evidence spans that are faithful to the model's observable behavior, even when human evidence annotations are absent?

## Hypothesis (to be tested)

Combining multi-turn (or at least question+answer) context with linguistic features and structured evidence will improve pragmatic inference and interpretability compared with classification-only, target-only baselines.

This is a **hypothesis**, not a finding.

## Label task (primary)

Circa gold interpretations of indirect answers to polar questions. Exact class set is computed from data after download. Paper-reported BERT numbers (82–88% for 4-class, 74–85% for 6-class) are **prior-work results**, not this project's results.

## Context windows

| Condition | Input |
| --- | --- |
| `target_only` | Answer turn |
| `prev_1` | Question + answer |
| `situation_prev_1` | Situation text + question + answer |
| `full` | All available turns in the example |
| `features_only` | Linguistic features without lexical text (ablation) |

## TF-IDF + logistic regression (first model)

Documented sklearn convention for this project:

- Term frequency: sublinear (`1 + log(tf)` when tf > 0), via `TfidfVectorizer(sublinear_tf=True)`.
- IDF: smoothed `log((1 + n) / (1 + df(t))) + 1` (`smooth_idf=True`).
- L2 row normalization (`norm='l2'`).
- Word n-grams fitted **only on training documents**.
- Classifier: `sklearn.linear_model.LogisticRegression` with `class_weight='balanced'` unless a later validation sweep selects otherwise.

Hyperparameters may be tuned on train/validation only.

## Evidence (planned)

Initial evidence is **source-grounded and extractive**:

- Highlight the target span.
- Optionally highlight question tokens and a small set of cue patterns (negation, conditionals, contrast).
- Record utterance ids.

Natural-language explanations, if added, are a separate field and must be evaluated for faithfulness rather than treated as the model's inner reasoning.

## Evaluation

- Accuracy and macro-F1 on the held-out test groups.
- Per-class precision, recall, F1.
- Confusion matrix.
- Context-window ablations with the same split.
- Evidence sufficiency/necessity as **prediction-change diagnostics**.

## Limitations (current)

- Circa is not full multi-turn implicature.
- No gold evidence spans.
- Phenomena such as irony are not claimed.
- Transformer and LLM baselines are unimplemented until later milestones.
