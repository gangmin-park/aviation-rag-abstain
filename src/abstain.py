"""Deciding when NOT to answer.   (WEEK 5 — you implement; this is the research core)

Idea: a decision aid a pilot can trust must say "I don't know" when the
handbooks do not support an answer. Turn retrieval scores into a confidence
value, then answer only above a threshold.
"""
from __future__ import annotations

def confidence(scores: list[float], method: str = "margin") -> float:
    """Map a ranked score list (highest first) to a single confidence number.

    method="top1"   -> scores[0]
    method="margin" -> scores[0] - scores[1]   (0.0 if fewer than 2 scores)
    Empty list -> 0.0
    You may add your own methods later and compare them — that comparison
    is a result worth reporting.
    """
    raise NotImplementedError("TODO(week 5)")


def decide(conf: float, threshold: float) -> bool:
    """True = answer, False = abstain.  Answer when conf >= threshold."""
    raise NotImplementedError("TODO(week 5)")
