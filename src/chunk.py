"""Turn handbook PDFs into page-tagged text chunks.   (WEEK 2 — you implement)

Every chunk must remember WHERE it came from (doc_id + page number), because
the whole project depends on citing the source of every answer.
"""
from __future__ import annotations

import fitz

def extract_pages(pdf_path, doc_id):
    pages = []
    with fitz.open(str(pdf_path)) as doc:
        for i, page in enumerate(doc, start=1):
            text = page.get_text().strip()
            if not text:
                continue
            pages.append({"doc": doc_id, "page": i, "text": text})
    return pages

def chunk_pages(pages, max_words=200, overlap=50):
    if overlap >= max_words:
        raise ValueError("overlap must be smaller than max_words")
    step = max_words - overlap

    chunks = []
    for page in pages:
        words = page["text"].split()
        start = 0
        k = 0
        while start < len(words):
            window = words[start:start + max_words]
            chunks.append({
                "id": f"{page['doc']}-p{page['page']}-c{k}",
                "doc": page["doc"],
                "page": page["page"],
                "text": " ".join(window),
            })
            if start + max_words >= len(words):
                break
            start += step
            k += 1
    return chunks