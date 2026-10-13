"""Embedding-based retriever.   (WEEK 4 — you implement)

Model suggestion: sentence-transformers "all-MiniLM-L6-v2" (runs on CPU).
Same interface as BM25Retriever so evaluate.py can compare them directly.
"""
from __future__ import annotations

class DenseRetriever:
    def __init__(self, chunks: list[dict], model_name: str = "all-MiniLM-L6-v2"):
        raise NotImplementedError("TODO(week 4)")

    def search(self, query: str, k: int = 5) -> list[tuple[dict, float]]:
        """Return top-k (chunk, cosine_similarity) pairs, highest first."""
        raise NotImplementedError("TODO(week 4)")
