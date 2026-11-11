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

1. **Chunks stop at page boundaries.** Every chunk is confined to one page so that a
   retrieved passage maps to exactly one citable page. The cost is that evidence split
   across a page break is never available intact: 213 of 868 body pages (24.5%) end
   mid-sentence.

2. **The dense model silently truncates long chunks.** `all-MiniLM-L6-v2` accepts 256
   tokens, but a 200-word chunk of handbook prose runs to a median of 247 tokens and 30%
   of chunks exceed the limit. The overflow is dropped with no warning, so for those
   chunks the dense retriever never sees the tail.

3. **The labels were verified by machine, not by reading.** Each answerable row was
   checked by confirming that a distinctive phrase from the cited passage appears on the
   cited page. No one has read the 60 rows back against the PDFs, so the labels carry the
   accuracy of a phrase-level check.

4. **Difficulty is mixed on purpose, so subsets of the question set are not comparable.**
   Some questions reuse the handbook's own term; others paraphrase it away entirely.
   Recall@1 is 0.227 on the first 22 answerable questions and 0.500 on the next 22 — a
   difference in the questions, not in the retriever.

5. **This is retrieval, not answer generation.** The system returns passages; it never
   writes an answer. "Correct" means the gold page was retrieved, not that a correct
   answer was produced.

6. **Answers are bounded by the two handbooks.** Because every answer must rest on the
   corpus, questions whose evidence lives elsewhere cannot be answered at all, however
   reasonable they are to ask.

7. **Low-coverage numbers rest on very few questions, and coverage trades one failure
   against another.** At 25% coverage only 15 questions are answered, so a single question
   moves risk by 0.067. More importantly, coverage trades two kinds of failure against
   each other: raise it and the system answers more questions it has no support for; lower
   it and the system stays silent on questions the handbooks do answer. In this data the
   two meet at about 50% coverage, where unsupported answers reach zero while 19 of 44
   answerable questions are still answered correctly. Pushing coverage below that point
   buys no further safety. Improving on this crossover would require judging the intent of
   the question and the content of the supporting passage more finely than a retrieval
   score can.

8. **Risk does not count the cost of abstaining.** Risk is the error rate among answered
   questions only, so a system that answers nothing scores a perfect 0. The four-outcome
   table is reported alongside it for that reason.

9. **Compound (multi-hop) questions are out of scope.** `gold_page` holds a single page,
   so a question whose evidence spans two pages can be neither labelled nor scored. The
   question set was built from single-page evidence throughout.

10. **What counts as "unanswerable" is a function of the corpus.** Of the 16 unanswerable
    questions, only 2 — both asking for real-time information — could not be answered by
    any fixed document. The other 14 are covered by other FAA publications or by
    manufacturer documentation.

This project tests a measuring instrument rather than a finished system. It was built on a
deliberately limited corpus and question set, and its aim was to locate the boundary where
the evidence runs out and to see whether that boundary can be detected. Every corpus has
such a boundary, and a system meant to be trusted has to recognise it and act on it. From
here I intend to work on analysing compound questions and on what a system should do with
the questions it cannot answer.

## How to run

Chunking, BM25, evaluation and the plots run in the main environment:

```bash
# macOS:   bash setup_mac.command      Windows: double-click setup_windows.bat
# (or manually)
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m src.download
pytest -q
```

Dense retrieval needs a second environment. The last PyTorch release with Intel-macOS
wheels is 2.2.2, which supports Python 3.8-3.12 only, while the main environment runs
3.13 — so on an Intel Mac the two cannot be merged. On Apple Silicon or Linux, install
`requirements-dense.txt` into the main environment and ignore this step.

```bash
conda create -n dense python=3.12 -y
conda run -n dense pip install -r requirements-dense.txt
```

PyMuPDF has no Python 3.12 x86-macOS wheel, so the dense environment cannot read the
PDFs: export the chunks from the main environment as JSON and load them there.

## Authorship and AI assistance

I used an AI assistant (Claude) as a tutor throughout this project, and I want to be precise about who did what.

**The assistant** proposed the project structure, wrote the setup utility (`src/download.py`) and the unit-test specifications in `tests/`, drafted the seed questions and located their supporting pages in the PDFs, explained the design decisions behind each module, **showed me a reference implementation of each core function**, and reviewed my code.

**I** wrote every core module (chunking, retrieval, abstention, evaluation) myself: for each function I studied the reference implementation and the reasoning behind it, closed it, and wrote my own version against the tests. I ran the experiments and wrote the analysis. All implementation commits are my own.

**The evaluation set is the exception, and I want to be explicit about it.** Its questions were drafted by the assistant and its labels were checked programmatically, as described under *Data*. I set the design constraints — which chapters to draw from, that each question must have one unambiguous source page, and which question types belong in the unanswerable half — but I have not yet read every row back against the PDFs. Until I do, treat the retrieval numbers as resting on machine-checked labels.
