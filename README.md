# Knowing When Not to Answer: Abstaining Retrieval over FAA Flight-Training Handbooks

> Status: **work in progress** (started October 2026). Sections marked _TBD_ are filled in as results come in.

## Motivation

A decision aid for pilots is only useful if pilots can calibrate how much to trust it. A system that answers every question with the same confidence, including questions its sources cannot support, invites over-trust. This project asks a small, measurable version of that problem:

**Research question.** Given a question and a fixed body of authoritative documents, can a retrieval system decide *when not to answer*, and how much does abstaining reduce the error rate of the answers it does give?

## Data

- *Pilot's Handbook of Aeronautical Knowledge* (FAA-H-8083-25C) and *Airplane Flying Handbook* (FAA-H-8083-3C), published by the U.S. Federal Aviation Administration (U.S. government works). Download with `python -m src.download`.
- `data/questions.csv`: the evaluation set (60 questions: 44 answerable, 16 unanswerable). Questions were drafted with AI assistance against the two PDFs. Every cited page is a 1-based PDF page, and `source_note` records the chapter, the printed handbook page, and the phrase the label rests on.
  - **How the labels were checked.** Each answerable row was verified programmatically: a distinctive phrase from the cited passage must appear on the cited page. Rows whose supporting passage also appears elsewhere in either handbook were narrowed or dropped, so that each question has one unambiguous source page. For the **unanswerable** rows, the absence was verified by searching both PDFs for the terms the answer would have to use; `source_note` records what was searched. These rows have not yet been read back against the PDFs by a human, so the labels carry the accuracy of a phrase-level check, not of a careful reading.
  - **Difficulty is mixed on purpose.** Some questions reuse the handbook's own term; others paraphrase it away entirely. This spread is what separates a lexical retriever from a dense one, but it also means the aggregate numbers depend on the mix, and subsets of this set are not comparable with each other.
- Only public civil-aviation material is used. No military or non-public data is involved.

## Method

1. **Chunking** (`src/chunk.py`): split PDF pages into overlapping word windows that never cross a page, so every answer can cite an exact page.
2. **Retrieval**: compare a lexical baseline, BM25 (`src/bm25_retriever.py`), with dense sentence embeddings (`src/dense_retriever.py`).
3. **Abstention** (`src/abstain.py`): turn the ranked retrieval scores into a confidence value (top-1 score, top-1 − top-2 margin, ...), then answer only when it is above a threshold.
4. **Evaluation** (`src/evaluate.py`): Recall@k for retrieval; the risk–coverage curve and its area (AURC) for selective answering.

## Results

_TBD_: Recall@k table (BM25 vs. dense), the risk–coverage plot, and AURC for each confidence method.

## Limitations

_TBD_

## How to run

```bash
# macOS:   bash setup_mac.command      Windows: double-click setup_windows.bat
# (or manually)
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt            # core
pip install -r requirements-dense.txt      # Week 4: dense retrieval (PyTorch)
python -m src.download
pytest -q
```

## Authorship and AI assistance

I used an AI assistant (Claude) as a tutor throughout this project, and I want to be precise about who did what.

**The assistant** proposed the project structure, wrote the setup utility (`src/download.py`) and the unit-test specifications in `tests/`, drafted the seed questions and located their supporting pages in the PDFs, explained the design decisions behind each module, **showed me a reference implementation of each core function**, and reviewed my code.

**I** wrote every core module (chunking, retrieval, abstention, evaluation) myself: for each function I studied the reference implementation and the reasoning behind it, closed it, and wrote my own version against the tests. I ran the experiments and wrote the analysis. All implementation commits are my own.

**The evaluation set is the exception, and I want to be explicit about it.** Its questions were drafted by the assistant and its labels were checked programmatically, as described under *Data*. I set the design constraints — which chapters to draw from, that each question must have one unambiguous source page, and which question types belong in the unanswerable half — but I have not yet read every row back against the PDFs. Until I do, treat the retrieval numbers as resting on machine-checked labels.
