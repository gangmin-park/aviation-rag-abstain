"""Embedding-based retriever.   (WEEK 4 — you implement)

Model suggestion: sentence-transformers "all-MiniLM-L6-v2" (runs on CPU).
Same interface as BM25Retriever so evaluate.py can compare them directly.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np


class DenseRetriever:
    def __init__(self, chunks: list[dict], model_name: str = "all-MiniLM-L6-v2",
                 cache_dir: str | Path = "data/cache"):
        from sentence_transformers import SentenceTransformer  # lazy: torch only lives in the dense env

        self.chunks = chunks
        self.model = SentenceTransformer(model_name)

        cache = Path(cache_dir) / f"{model_name.replace('/', '_')}-{len(chunks)}.npy"
        if cache.exists():
            self.emb = np.load(cache)
        else:
            self.emb = self.model.encode(
                [c["text"] for c in chunks],
                batch_size=64,
                normalize_embeddings=True,
            )
            cache.parent.mkdir(parents=True, exist_ok=True)
            np.save(cache, self.emb)

    def search(self, query: str, k: int = 5) -> list[tuple[dict, float]]:
        q = self.model.encode([query], normalize_embeddings=True)[0]
        scores = self.emb @ q
        order = np.argsort(-scores, kind="stable")[:k]
        return [(self.chunks[i], float(scores[i])) for i in order]