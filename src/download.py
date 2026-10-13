"""Download FAA handbooks (U.S. government works) into data/raw/.

Setup utility (scaffolded with AI assistance).

The URLs in HANDBOOKS point to the "Full Version" PDF on each FAA page:
  - Pilot's Handbook of Aeronautical Knowledge (FAA-H-8083-25C):
    https://www.faa.gov/regulations_policies/handbooks_manuals/aviation/phak
  - Airplane Flying Handbook (FAA-H-8083-3C):
    https://www.faa.gov/regulations_policies/handbooks_manuals/aviation/airplane_handbook

Usage:  python -m src.download
"""
from pathlib import Path

import requests

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"

# doc_id -> full-PDF URL
HANDBOOKS = {
    "phak": "https://www.faa.gov/regulations_policies/handbooks_manuals/aviation/faa-h-8083-25c.pdf",
    "afh": "https://www.faa.gov/sites/faa.gov/files/regulations_policies/handbooks_manuals/aviation/airplane_handbook/00_afh_full.pdf",
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
