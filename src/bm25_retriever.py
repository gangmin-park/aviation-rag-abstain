"""Lexical baseline retriever.   (WEEK 3 — you implement)"""
from __future__ import annotations

import re


def tokenize(text: str) -> list[str]:
    """Lowercase and split into alphanumeric tokens.
    "Angle of Attack (AOA)!" -> ["angle", "of", "attack", "aoa"]
    """
    raise NotImplementedError("TODO(week 3)")


class BM25Retriever:
    def __init__(self, chunks: list[dict]):
        """Build a BM25 index over chunk["text"].  Hint: rank_bm25.BM25Okapi"""
        raise NotImplementedError("TODO(week 3)")

    def search(self, query: str, k: int = 5) -> list[tuple[dict, float]]:
        """Return the top-k (chunk, score) pairs, highest score first."""
        raise NotImplementedError("TODO(week 3)")
