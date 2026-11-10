"""Evaluation metrics.   (WEEK 3 and WEEK 5 — you implement)"""
from __future__ import annotations

def recall_at_k(retrieved: list[dict], gold_doc: str, gold_page: int, k: int) -> float:
    """1.0 if any of the first k retrieved chunks has (doc, page) == gold, else 0.0."""
    return 1.0 if any(c["doc"] == gold_doc and c["page"] == gold_page
                      for c in retrieved[:k]) else 0.0


def risk_coverage(confidences: list[float], correct: list[bool]) -> list[tuple[float, float]]:
    """Risk-coverage curve for selective answering.

    Sort questions by confidence (highest first). For n = 1..N, answering only
    the top-n questions gives:
        coverage = n / N
        risk     = (number of wrong answers among those n) / n
    Return the list of (coverage, risk) for n = 1..N.
    An unanswerable question that the system answers counts as wrong.
    """
    raise NotImplementedError("TODO(week 5)")


def aurc(curve: list[tuple[float, float]]) -> float:
    """Area under the risk-coverage curve = mean of the risk values. Lower is better."""
    raise NotImplementedError("TODO(week 5)")
