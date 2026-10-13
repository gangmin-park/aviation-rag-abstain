"""Download FAA handbooks (U.S. government works) into data/raw/.

Setup utility (scaffolded with AI assistance).

WEEK 0 TASK: open the FAA handbook pages below in a browser, find the link
labelled "Full Version" (full PDF), and paste the URLs into HANDBOOKS.
  - Pilot's Handbook of Aeronautical Knowledge (FAA-H-8083-25C):
    https://www.faa.gov/regulations_policies/handbooks_manuals/aviation/phak
  - Airplane Flying Handbook (FAA-H-8083-3C):
    https://www.faa.gov/regulations_policies/handbooks_manuals/aviation/airplane_handbook

Usage:  python -m src.download
"""
from pathlib import Path

import requests

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"

# doc_id -> full-PDF URL  (fill these in yourself)
HANDBOOKS = {
    "phak": "",  # TODO(week 0)
    "afh": "",   # TODO(week 0)
}


def download(doc_id: str, url: str) -> Path:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    out = RAW_DIR / f"{doc_id}.pdf"
    if out.exists():
        print(f"[skip] {out.name} already exists")
        return out
    print(f"[get ] {url}")
    resp = requests.get(url, timeout=120)
    resp.raise_for_status()
    out.write_bytes(resp.content)
    print(f"[ok  ] {out.name}  ({len(resp.content) / 1e6:.1f} MB)")
    return out


if __name__ == "__main__":
    for doc_id, url in HANDBOOKS.items():
        if not url:
            raise SystemExit(f"Fill in the URL for '{doc_id}' in HANDBOOKS first.")
        download(doc_id, url)
