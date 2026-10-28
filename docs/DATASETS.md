# Dataset selection

Status: literature and resource review as of 2026-10-28. **No dataset has been downloaded into this repository yet.** Split sizes and label distributions for Circa will be computed from the official file after download, not copied from memory.

## Decision (provisional)

| Role | Resource | Why |
| --- | --- | --- |
| **Primary training/evaluation (English classification)** | Circa (Louis, Roth, and Radlinski, EMNLP 2020) | Licensed for research reuse, English, discrete pragmatic labels, large enough for TF-IDF and transformer experiments |
| **Related English implicature text** | George and Mamidi (2020) conversational implicature triples | English context / utterance / implicated meaning; better as explanation or retrieval data than as a closed label set |
| **Related Chinese multi-turn implicature** | SwordsmanImp (Yue et al., CCL 2024) | True multi-turn sitcom dialogues with Gricean maxim annotations; **not an English dataset** |
| **Not selected as primary** | CICERO | Dialogue commonsense (cause, motivation, emotion), not conversational implicature labels |
| **Not selected as primary** | ImplicatureX | Small cancellation-focused resource; useful later as a diagnostic, not a training set |

This choice is a research design decision, not a claim that Circa covers every pragmatic phenomenon named in the project title.

## What Circa supports

Official description (GitHub `google-research-datasets/circa`, Hugging Face `google-research-datasets/circa`):

- English polar questions with **indirect answers**.
- About **34,268** question–answer pairs collected in **10 social situations**.
- Annotator interpretations of how X would understand Y's answer.
- Gold labels including yes / no / middle-ground / conditional interpretations, plus `NA` when annotators did not form a majority.

Fields used by this project after normalization:

- situation text → `context_situation`
- `question-X` → dialogue turn (speaker X)
- `answer-Y` → target turn (speaker Y)
- `goldstandard2` as the default label column (less strict majority; documented in the Circa card)
- examples with `NA` labels are dropped for supervised training

Circa is **not**:

- long multi-turn sitcom dialogue
- an irony / sarcasm / criticism corpus
- a span-annotated evidence dataset

## License and source (Circa)

- Paper: Louis, Roth, and Radlinski. “I'd rather just go to bed”: Understanding Indirect Answers. EMNLP 2020. https://aclanthology.org/2020.emnlp-main.601/
- Code/data: https://github.com/google-research-datasets/circa
- Hugging Face card: https://huggingface.co/datasets/google-research-datasets/circa
- GitHub README states Creative Commons Attribution 4.0. The Hugging Face card text also mentions the BY-SA 4.0 deed URL. **Treat redistribution conservatively: keep the official files out of git, cite the authors, and link the source.** Do not re-license Circa as MIT.

## SwordsmanImp (do not misuse)

- Paper: Yue, Song, Cheng, and Hu. Do Large Language Models Understand Conversational Implicature – A Case Study with a Chinese Sitcom. CCL 2024. https://aclanthology.org/2024.ccl-1.98/
- About **200** handcrafted Chinese items from *My Own Swordsman*.
- Tasks: multiple-choice implicature and free-form explanation; Gricean maxim violation flags.
- Code: https://github.com/sjtu-compling/llm-pragmatics
- Hugging Face listing observed: `Junrui1202/Swordsman` (verify the dataset card license before any download).
- **Do not translate and train as if it were English Circa.** A future optional Chinese evaluation module may load it with language tags.

## George and Mamidi (2020)

- English dialogue snippets: context, utterance, implicated meaning.
- Sources include TOEFL-style listening items and movie-script dialogue.
- Hugging Face redistribution: `tasksource/implicatures` (about 1k examples). Original paper: Procedia Computer Science 171.
- Labels are free-text implicatures, not Circa-style yes/no interpretations.
- **Do not merge these labels with Circa classes.**

## Leakage and splitting policy (Circa)

Questions are reused with different answers. A random row split can put the same question in train and test.

Required procedure once the official file is present:

1. Drop unlabeled (`NA`) rows for the chosen gold column.
2. Normalize labels with an explicit map (see `nlp/datasets/circa.py` once implemented).
3. Detect duplicate (situation, question, answer) triples.
4. Split **groups** defined by `(context_situation, question-X)` with stratification on the group's majority label where possible.
5. Record dataset version as a content hash of the source file plus the split seed.

## Fixtures in this repository

`data/fixtures/synthetic_pragmatics.jsonl` is **synthetic**. It exists so schema, split, and API tests can run without downloading Circa. The UI must label it as a fixture, never as Circa evaluation.

## Human evidence annotations

None of the selected public resources provide gold evidence spans aligned to our pipeline. Faithfulness tests will therefore be:

- **diagnostic** (sufficiency / necessity / counterfactual prediction change) on model behavior, and
- **human evaluation** if we later annotate a subset.

Automated diagnostics are not a substitute for human faithfulness judgments.
