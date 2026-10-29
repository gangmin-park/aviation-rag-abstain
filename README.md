# Knowing When Not to Answer: Abstaining Retrieval over FAA Flight-Training Handbooks

> Status: **work in progress** (started October 2026). Sections marked _TBD_ are filled in as results come in.

## Motivation

A decision aid for pilots is only useful if pilots can calibrate how much to trust it. A system that answers every question with the same confidence, including questions its sources cannot support, invites over-trust. This project asks a small, measurable version of that problem:

**Research question.** Given a question and a fixed body of authoritative documents, can a retrieval system decide *when not to answer*, and how much does abstaining reduce the error rate of the answers it does give?

## Data

- *Pilot's Handbook of Aeronautical Knowledge* (FAA-H-8083-25C) and *Airplane Flying Handbook* (FAA-H-8083-3C), published by the U.S. Federal Aviation Administration (U.S. government works). Download with `python -m src.download`.
- `data/questions.csv`: the evaluation set (30 questions: 22 answerable, 8 unanswerable). Questions were drafted with AI assistance against the two PDFs and then verified and revised by the author; every cited page is a 1-based PDF page located by searching the handbook text, and `source_note` records the chapter and the passage it rests on. The **unanswerable** half are plausible aviation questions the handbooks do not cover, each with a note on what was searched to confirm the absence.
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

**I** reviewed and revised the evaluation set, then wrote every core module (chunking, retrieval, abstention, evaluation) myself: for each function I studied the reference implementation and the reasoning behind it, closed it, and wrote my own version against the tests. I ran the experiments and wrote the analysis. All implementation commits are my own.
