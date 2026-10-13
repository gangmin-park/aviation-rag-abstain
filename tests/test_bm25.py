from src.bm25_retriever import BM25Retriever, tokenize

CHUNKS = [
    {"id": "a", "doc": "phak", "page": 1, "text": "Angle of attack is the angle between the chord line and the relative wind."},
    {"id": "b", "doc": "phak", "page": 2, "text": "Carburetor icing can occur at temperatures well above freezing."},
    {"id": "c", "doc": "afh", "page": 3, "text": "A stabilized approach keeps airspeed and descent rate constant."},
]


def test_tokenize():
    assert tokenize("Angle of Attack (AOA)!") == ["angle", "of", "attack", "aoa"]


def test_relevant_chunk_ranks_first():
    r = BM25Retriever(CHUNKS)
    results = r.search("what is carburetor icing", k=3)
    assert results[0][0]["id"] == "b"
    scores = [s for _, s in results]
    assert scores == sorted(scores, reverse=True)
