"""Fetch 10-K filings and financial facts from SEC EDGAR, extract sections, and chunk them.

SEC asks every client to identify itself: set SEC_USER_AGENT in the repo's .env, for example
    SEC_USER_AGENT=Your Name your.email@example.com
EDGAR is free and needs no key. Keep to a few requests per second (this module sleeps between calls).
"""
from __future__ import annotations

import os
import re
import time
from datetime import date
from pathlib import Path

import warnings

import pandas as pd
import requests
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning

# Modern 10-Ks are inline XBRL (XHTML). Parsing them as HTML is intended here, so silence bs4's warning.
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

COMPANIES = {  # name -> SEC CIK
    "NVIDIA": 1045810,
    "Microsoft": 789019,
    "JPMorgan": 19617,
    "Amazon": 1018724,
    "Tesla": 1318605,
}

# Bump when extraction changes, so saved corpora are rebuilt from the cached filings.
CORPUS_VERSION = "2"

# Headings must start a line: mid-sentence cross-references ("see Item 1A. Risk Factors") don't count.
SECTIONS = {
    "Risk Factors": (
        r"(?im)^[ \t]*item\s*1a\.?\s*[-–—:.]?\s*risk\s+factors",
        r"(?im)^[ \t]*(?:item\s*1b\b|item\s*1c\b|item\s*2\.?\s*[-–—:.]?\s*properties)",
    ),
    "MD&A": (
        r"(?im)^[ \t]*item\s*7\.?\s*[-–—:.]?\s*management['’`]?s\s+discussion",
        r"(?im)^[ \t]*(?:item\s*7a\b|item\s*8\b)",
    ),
}
MIN_SECTION_CHARS = 3000  # anything shorter is a table-of-contents line or a cross-reference

REVENUE_CONCEPTS = ["Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax", "RevenuesNetOfInterestExpense"]
NET_INCOME_CONCEPTS = ["NetIncomeLoss"]


def _headers() -> dict:
    agent = os.getenv("SEC_USER_AGENT")
    if not agent:
        raise RuntimeError("Set SEC_USER_AGENT in the repo's .env, e.g. 'Your Name your.email@example.com' (SEC requires it)")
    return {"User-Agent": agent, "Accept-Encoding": "gzip, deflate"}


def _get(url: str) -> requests.Response:
    time.sleep(0.3)  # stay well under SEC's 10 requests per second
    r = requests.get(url, headers=_headers(), timeout=60)
    r.raise_for_status()
    return r


def latest_10k(cik: int, cache_dir: Path | None = None) -> dict:
    """Accession number, document name and dates of the company's most recent 10-K."""
    import json
    path = cache_dir / f"{cik}_submissions.json" if cache_dir else None
    if path and path.exists():
        recent = json.loads(path.read_text())["filings"]["recent"]
    else:
        response = _get(f"https://data.sec.gov/submissions/CIK{cik:010d}.json")
        recent = response.json()["filings"]["recent"]
        if path:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(response.content)
    for i, form in enumerate(recent["form"]):
        if form == "10-K":
            return {"accession": recent["accessionNumber"][i], "document": recent["primaryDocument"][i],
                    "filed": recent["filingDate"][i], "period": recent["reportDate"][i]}
    raise ValueError(f"No 10-K found for CIK {cik}")


def fetch_filing_html(cik: int, filing: dict, cache_dir: Path) -> str:
    cache_dir.mkdir(parents=True, exist_ok=True)
    path = cache_dir / f"{cik}_{filing['accession']}.htm"
    if not path.exists():
        acc = filing["accession"].replace("-", "")
        path.write_bytes(_get(f"https://www.sec.gov/Archives/edgar/data/{cik}/{acc}/{filing['document']}").content)
    return path.read_text(encoding="utf-8", errors="ignore")


BLOCK_TAGS = ["p", "div", "br", "tr", "li", "table", "h1", "h2", "h3", "h4", "h5", "h6"]


def html_to_text(html: str) -> str:
    """Text with a line break after each block element. Inline spans are joined without breaks, so a heading
    split across styled spans ("RIS" + "K FACTORS") stays one word."""
    soup = BeautifulSoup(html, "lxml")
    for tag in soup(["script", "style", "ix:header"]):
        tag.decompose()
    for tag in soup.select('[style*="display:none"], [style*="display: none"]'):
        tag.decompose()
    for tag in soup.find_all(BLOCK_TAGS):
        tag.insert_after("\n")
    for cell in soup.find_all(["td", "th"]):
        cell.insert_after(" ")
    text = soup.get_text("")
    text = text.replace("\xa0", " ")
    lines = [re.sub(r"[ \t]+", " ", line).strip() for line in text.splitlines()]
    text = "\n".join(line for line in lines if line)
    return re.sub(r"\n{3,}", "\n\n", text)


def extract_section(text: str, start_pattern: str, end_pattern: str) -> str | None:
    """Longest span from a heading to the next end heading. Table-of-contents entries are short, so the
    longest span is the real section; a start with no end heading after it is ignored."""
    best = ""
    end_re = re.compile(end_pattern)
    for start in re.finditer(start_pattern, text):
        end = end_re.search(text, start.end())
        if not end:
            continue
        span = text[start.start(): end.start()]
        if len(span) > len(best):
            best = span
    return best.strip() if len(best) >= MIN_SECTION_CHARS else None


def chunk_text(text: str, size: int = 1200, overlap: int = 200) -> list[str]:
    """Paragraph-aware chunks of about `size` characters; the last paragraph carries over when it fits `overlap`."""
    paragraphs = [p.strip() for p in re.split(r"\n+", text) if len(p.strip()) > 40]
    chunks, current = [], []
    for p in paragraphs:
        while len(p) > size:  # split very long paragraphs on sentence boundaries
            cut = p.rfind(". ", 0, size)
            cut = cut + 1 if cut > size // 2 else size
            paragraphs_piece, p = p[:cut].strip(), p[cut:].strip()
            if current:
                chunks.append(" ".join(current))
                current = []
            chunks.append(paragraphs_piece)
        if current and len(" ".join(current + [p])) > size:
            chunks.append(" ".join(current))
            current = [current[-1]] if len(current[-1]) <= overlap else []
        current.append(p)
    if current:
        chunks.append(" ".join(current))
    return chunks


def _annual_values(facts: dict, concepts: list[str]) -> tuple[str, dict] | None:
    """Latest fiscal-year value reported in a 10-K for the first concept the company uses."""
    gaap = facts.get("facts", {}).get("us-gaap", {})
    for concept in concepts:
        entries = gaap.get(concept, {}).get("units", {}).get("USD", [])
        annual = [e for e in entries if e.get("form") == "10-K" and e.get("start") and
                  330 <= (date.fromisoformat(e["end"]) - date.fromisoformat(e["start"])).days <= 400]
        if annual:
            return concept, max(annual, key=lambda e: (e["end"], e.get("filed", "")))
    return None


def _total_revenue(facts: dict) -> tuple[str, dict] | None:
    """Companies tag revenue under different concepts, and some use one concept for a sub-total.
    Take the latest fiscal year across all revenue concepts, then the largest value for that year."""
    found = [f for c in REVENUE_CONCEPTS if (f := _annual_values(facts, [c]))]
    if not found:
        return None
    latest = max(entry["end"] for _, entry in found)
    return max((f for f in found if f[1]["end"] == latest), key=lambda f: f[1]["val"])


def company_facts(cik: int, cache_dir: Path | None = None) -> dict:
    path = cache_dir / f"{cik}_companyfacts.json" if cache_dir else None
    if path and path.exists():
        import json
        facts = json.loads(path.read_text())
    else:
        response = _get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json")
        facts = response.json()
        if path:
            path.write_bytes(response.content)
    row = {}
    for label, found in (("revenue", _total_revenue(facts)), ("net_income", _annual_values(facts, NET_INCOME_CONCEPTS))):
        if found:
            concept, entry = found
            row.update({label: entry["val"], f"{label}_concept": concept, f"{label}_period_end": entry["end"]})
    row["fiscal_year_end"] = row.get("revenue_period_end")
    if row.get("revenue") and row.get("net_income") and row["net_income"] > row["revenue"]:
        row["check"] = "net income above revenue: concept mismatch"
    return row


def build_corpus(out_dir: Path, cache_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Fetch, extract and chunk every company's latest 10-K. Returns (chunks, facts, coverage)."""
    chunks, facts, coverage = [], [], []
    for company, cik in COMPANIES.items():
        filing = latest_10k(cik, cache_dir)
        text = html_to_text(fetch_filing_html(cik, filing, cache_dir))
        for section, (start, end) in SECTIONS.items():
            body = extract_section(text, start, end)
            pieces = chunk_text(body) if body else []
            coverage.append({"company": company, "section": section, "found": bool(body),
                             "characters": len(body or ""), "chunks": len(pieces), "accession": filing["accession"],
                             "period": filing["period"]})
            for i, piece in enumerate(pieces):
                chunks.append({"chunk_id": f"{company}-{'RF' if section == 'Risk Factors' else 'MDA'}-{i:03d}",
                               "company": company, "section": section, "period": filing["period"],
                               "accession": filing["accession"], "text": piece})
        facts.append({"company": company, "cik": cik, **company_facts(cik, cache_dir)})
    out_dir.mkdir(parents=True, exist_ok=True)
    chunks_df, facts_df, coverage_df = pd.DataFrame(chunks), pd.DataFrame(facts), pd.DataFrame(coverage)
    chunks_df.to_csv(out_dir / "chunks.csv", index=False)
    facts_df.to_csv(out_dir / "facts.csv", index=False)
    coverage_df.to_csv(out_dir / "coverage.csv", index=False)
    (out_dir / "version.txt").write_text(CORPUS_VERSION)
    return chunks_df, facts_df, coverage_df
