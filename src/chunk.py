"""Turn handbook PDFs into page-tagged text chunks.   (WEEK 2 — you implement)

Every chunk must remember WHERE it came from (doc_id + page number), because
the whole project depends on citing the source of every answer.
"""
from __future__ import annotations

from pathlib import Path


def extract_pages(pdf_path: str | Path, doc_id: str) -> list[dict]:
    """Return one dict per PDF page: {"doc": doc_id, "page": int, "text": str}.

    - page numbers are 1-based PDF page indices
    - skip pages whose stripped text is empty
    Hint: `import fitz` (PyMuPDF) -> fitz.open(path); page.get_text()
    """
    raise NotImplementedError("TODO(week 2)")


def chunk_pages(pages: list[dict], max_words: int = 200, overlap: int = 50) -> list[dict]:
    """Split each page's text into overlapping word windows.

    Returns a list of {"id": str, "doc": str, "page": int, "text": str}.
    - windows never cross a page boundary (keeps citations exact)
    - consecutive windows on the same page share `overlap` words
    - id format: f"{doc}-p{page}-c{k}" with k = 0, 1, 2, ... within the page
    - a page with <= max_words words becomes exactly one chunk
    """
    raise NotImplementedError("TODO(week 2)")
