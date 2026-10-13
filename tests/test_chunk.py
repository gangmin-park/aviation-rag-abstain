from src.chunk import chunk_pages


def _page(n_words, page=1, doc="phak"):
    return {"doc": doc, "page": page, "text": " ".join(f"w{i}" for i in range(n_words))}


def test_short_page_is_one_chunk():
    chunks = chunk_pages([_page(30)], max_words=200, overlap=50)
    assert len(chunks) == 1
    assert chunks[0]["id"] == "phak-p1-c0"
    assert chunks[0]["page"] == 1


def test_overlap_between_windows():
    chunks = chunk_pages([_page(350)], max_words=200, overlap=50)
    first, second = chunks[0]["text"].split(), chunks[1]["text"].split()
    assert len(first) == 200
    assert first[-50:] == second[:50]


def test_windows_never_cross_pages():
    chunks = chunk_pages([_page(10, page=1), _page(10, page=2)])
    assert [c["page"] for c in chunks] == [1, 2]
    assert chunks[1]["id"] == "phak-p2-c0"


def test_every_word_is_covered():
    words = _page(500)["text"].split()
    chunks = chunk_pages([_page(500)], max_words=200, overlap=50)
    covered = set(w for c in chunks for w in c["text"].split())
    assert covered == set(words)
