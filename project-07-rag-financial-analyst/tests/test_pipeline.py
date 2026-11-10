"""Offline tests: section extraction, chunking, retrieval and answer checks (no network, no models)."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import answer as an  # noqa: E402
import edgar  # noqa: E402
import rag  # noqa: E402

BODY = "We face risks. " * 300

DOC = f"""Table of Contents
Item 1A. Risk Factors 12
Item 1B. Unresolved Staff Comments 30
Item 7. Management's Discussion and Analysis 40
Item 7A. Quantitative and Qualitative Disclosures 60
PART I
Item 1A. Risk Factors
{BODY}
Item 1B. Unresolved Staff Comments
None.
Item 7. Management’s Discussion and Analysis of Financial Condition
Revenue grew. {"Data center revenue increased. " * 200}
Item 7A. Quantitative and Qualitative Disclosures About Market Risk
"""


def test_extract_skips_table_of_contents():
    start, end = edgar.SECTIONS["Risk Factors"]
    section = edgar.extract_section(DOC, start, end)
    assert section.startswith("Item 1A. Risk Factors\nWe face risks.")
    assert "Unresolved" not in section


def test_extract_mdna_with_curly_apostrophe():
    start, end = edgar.SECTIONS["MD&A"]
    section = edgar.extract_section(DOC, start, end)
    assert section is not None and "Data center revenue" in section and "7A" not in section


def test_cross_reference_mid_sentence_is_not_a_heading():
    doc = ("Results should be read with Item 1A. Risk Factors, our statements " + "and more. " * 400 + "\n"
           "Item 1B. Unresolved Staff Comments\n")
    start, end = edgar.SECTIONS["Risk Factors"]
    assert edgar.extract_section(doc, start, end) is None


def test_heading_split_across_spans_is_joined():
    html = '<div><span>ITEM 1A. RIS</span><span>K FACTORS</span></div><p>Body</p>'
    assert edgar.html_to_text(html).splitlines()[0] == "ITEM 1A. RISK FACTORS"


def test_total_revenue_takes_largest_concept_for_latest_year():
    def entry(v):
        return {"form": "10-K", "start": "2025-07-01", "end": "2026-06-30", "val": v, "filed": "2026-07-30"}
    facts = {"facts": {"us-gaap": {"Revenues": {"units": {"USD": [entry(62)]}},
                                   "RevenueFromContractWithCustomerExcludingAssessedTax": {"units": {"USD": [entry(300)]}}}}}
    concept, e = edgar._total_revenue(facts)
    assert e["val"] == 300


def test_missing_section_returns_none():
    start, end = edgar.SECTIONS["MD&A"]
    assert edgar.extract_section("Item 7. Management's Discussion: see Exhibit 13.", start, end) is None


def test_html_to_text_drops_hidden_xbrl():
    html = '<html><body><div style="display:none">hidden facts</div><p>Visible&nbsp;text</p></body></html>'
    assert edgar.html_to_text(html) == "Visible text"


def test_chunks_respect_size_and_overlap():
    text = "\n".join(f"Paragraph {i} " + "word " * 40 for i in range(30))
    chunks = edgar.chunk_text(text, size=600, overlap=300)
    assert all(len(c) <= 600 for c in chunks)
    assert chunks[1].split(" word")[0] in chunks[0]  # last paragraph of one chunk starts the next


def test_annual_values_takes_latest_full_year():
    facts = {"facts": {"us-gaap": {"Revenues": {"units": {"USD": [
        {"form": "10-K", "start": "2023-01-01", "end": "2023-12-31", "val": 1, "filed": "2024-02-01"},
        {"form": "10-K", "start": "2024-10-01", "end": "2024-12-31", "val": 9, "filed": "2025-02-01"},
        {"form": "10-K", "start": "2024-01-01", "end": "2024-12-31", "val": 2, "filed": "2025-02-01"},
    ]}}}}}
    concept, entry = edgar._annual_values(facts, ["Revenues"])
    assert concept == "Revenues" and entry["val"] == 2


CHUNKS = pd.DataFrame([
    {"chunk_id": "NVIDIA-RF-000", "company": "NVIDIA", "section": "Risk Factors", "period": "2025", "text": "Export controls restrict sales of chips to China."},
    {"chunk_id": "Tesla-MDA-000", "company": "Tesla", "section": "MD&A", "period": "2025", "text": "We delivered 1.8 million vehicles."},
    {"chunk_id": "Tesla-RF-000", "company": "Tesla", "section": "Risk Factors", "period": "2025", "text": "Export rules and suppliers affect cells."},
])
VOCAB = ["export", "chip", "deliver", "vehicle", "supplier"]


def fake_embed(texts):
    v = np.array([[t.lower().count(w) for w in VOCAB] for t in texts], dtype=np.float32) + 1e-3
    return v / np.linalg.norm(v, axis=1, keepdims=True)


@pytest.fixture(scope="module")
def retriever():
    return rag.Retriever(CHUNKS, embed=fake_embed)


def test_company_filter(retriever):
    out = retriever.search("What export risks does Tesla see?", k=2, mode="hybrid+filter")
    assert set(out["company"]) == {"Tesla"}


def test_all_modes_return_ranked_results(retriever):
    for mode in rag.MODES:
        out = retriever.search("How many vehicles did Tesla deliver?", k=2, mode=mode)
        assert list(out["rank"]) == [1, 2] and out.iloc[0]["chunk_id"] == "Tesla-MDA-000"


def test_evaluate_scores_perfect_on_easy_questions(retriever):
    qs = pd.DataFrame([{"question": "Tesla vehicles delivered", "company": "Tesla", "section": "MD&A", "keywords": "deliver"}])
    scores = rag.evaluate(retriever, qs, k=2, modes=["bm25"])
    assert scores.loc[0, "hit@2"] == 1 and scores.loc[0, "MRR"] == 1


def test_check_answer_flags_invented_numbers():
    sources = {"S1": "We delivered 1.8 million vehicles.", "F": "Tesla: revenue $97.7 billion"}
    good = an.check_answer("Tesla delivered 1.8 million vehicles [S1] on $97.7 billion revenue [F].", sources)
    bad = an.check_answer("Tesla delivered 2.1 million vehicles [S1] and more [S9].", sources)
    assert good["grounded"]
    assert not bad["grounded"] and bad["numbers_not_in_sources"] == ["2.1"] and bad["unknown_citations"] == ["S9"]


def test_abstentions_are_not_counted_as_grounded():
    sources = {"S1": "AWS costs rose."}
    full = an.check_answer("The sources do not provide AWS growth figures [S1].", sources)
    none = an.check_answer("There is no information about AWS growth in the sources.", sources)
    assert full["verdict"] == "partial" and not full["grounded"]
    assert none["verdict"] == "abstained"


def test_ask_adds_facts_only_for_figure_questions(retriever):
    facts = pd.DataFrame([{"company": "Tesla", "fiscal_year_end": "2024-12-31", "revenue": 97.7e9, "net_income": 7.1e9}])
    r1 = an.ask("Which company had the highest revenue?", retriever, facts, chat=lambda p: "Tesla, $97.7 billion [F].")
    r2 = an.ask("What export risks does Tesla see?", retriever, facts, chat=lambda p: "Export rules [S1].")
    assert "F" in r1["sources"] and r1["grounded"]
    assert "F" not in r2["sources"]
