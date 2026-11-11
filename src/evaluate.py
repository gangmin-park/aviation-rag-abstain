"""Evaluation metrics.   (WEEK 3 and WEEK 5 — you implement)"""
from __future__ import annotations

def recall_at_k(retrieved: list[dict], gold_doc: str, gold_page: int, k: int) -> float:
    """1.0 if any of the first k retrieved chunks has (doc, page) == gold, else 0.0."""
    return 1.0 if any(c["doc"] == gold_doc and c["page"] == gold_page
                      for c in retrieved[:k]) else 0.0


def risk_coverage(confidences: list[float], correct: list[bool]) -> list[tuple[float, float]]:
    n_total = len(confidences)
    order = sorted(range(n_total), key=lambda i: confidences[i], reverse=True)

    curve = []
    wrong = 0
    for n, i in enumerate(order, start=1):
        if not correct[i]:
            wrong += 1
        curve.append((n / n_total, wrong / n))
    return curve


def aurc(curve: list[tuple[float, float]]) -> float:
    return sum(risk for _, risk in curve) / len(curve)

