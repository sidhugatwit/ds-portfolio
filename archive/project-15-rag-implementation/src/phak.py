"""Build a text corpus from three chapters of the FAA Pilot's Handbook of Aeronautical Knowledge (public domain)."""
from __future__ import annotations

import re
from pathlib import Path

BASE_URL = "https://www.faa.gov/sites/faa.gov/files/"
CHAPTERS = {
    11: ("Aircraft Performance", "13_phak_ch11.pdf"),
    12: ("Weather Theory", "14_phak_ch12.pdf"),
    15: ("Airspace", "17_phak_ch15.pdf"),
}
PAGE_NUMBER = re.compile(r"^\d{1,2}-\d{1,3}$")  # running page numbers like "11-14"
SENTENCE_END = re.compile(r"[.!?:]$")


def download(chapter: int, raw_dir: Path) -> Path:
    """Download one chapter PDF from faa.gov unless it's already in raw_dir."""
    import requests

    raw_dir = Path(raw_dir)
    raw_dir.mkdir(parents=True, exist_ok=True)
    path = raw_dir / CHAPTERS[chapter][1]
    if not path.exists():
        r = requests.get(BASE_URL + CHAPTERS[chapter][1], timeout=120,
                         headers={"User-Agent": "Mozilla/5.0 (portfolio research)"})
        r.raise_for_status()
        if not r.content.startswith(b"%PDF"):
            raise RuntimeError(f"faa.gov did not return a PDF for chapter {chapter}. Download "
                               f"{BASE_URL + CHAPTERS[chapter][1]} in a browser and save it to {path}.")
        path.write_bytes(r.content)
    return path


def clean(text: str) -> str:
    """Rejoin hyphenated and wrapped lines, drop page numbers; keep one paragraph per line."""
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)
    paragraphs, current = [], []
    for line in (l.strip() for l in text.splitlines()):
        if not line or PAGE_NUMBER.match(line):
            continue
        current.append(line)
        if SENTENCE_END.search(line):
            paragraphs.append(" ".join(current))
            current = []
    if current:
        paragraphs.append(" ".join(current))
    return "\n".join(re.sub(r"\s+", " ", p) for p in paragraphs)


def extract(pdf: Path) -> str:
    from pypdf import PdfReader

    return "\n".join(page.extract_text() or "" for page in PdfReader(str(pdf)).pages)


def build_corpus(raw_dir: Path, out_dir: Path) -> dict[int, str]:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    corpus = {}
    for chapter in CHAPTERS:
        corpus[chapter] = clean(extract(download(chapter, raw_dir)))
        (out_dir / f"phak_ch{chapter}.txt").write_text(corpus[chapter], encoding="utf-8")
    return corpus


def load_corpus(out_dir: Path) -> dict[int, str]:
    return {ch: (Path(out_dir) / f"phak_ch{ch}.txt").read_text(encoding="utf-8") for ch in CHAPTERS
            if (Path(out_dir) / f"phak_ch{ch}.txt").exists()}
