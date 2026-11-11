"""Deciding when NOT to answer.   (WEEK 5 — you implement; this is the research core)

Idea: a decision aid a pilot can trust must say "I don't know" when the
handbooks do not support an answer. Turn retrieval scores into a confidence
value, then answer only above a threshold.
"""
from __future__ import annotations

def confidence(scores: list[float], method: str = "margin") -> float:
    if not scores:
        return 0.0
    if method == "top1":
        return float(scores[0])
    if method == "margin":
        return float(scores[0] - scores[1]) if len(scores) > 1 else 0.0
    raise ValueError(f"unknown method: {method}")


def decide(conf: float, threshold: float) -> bool:
    return bool(conf >= threshold)


