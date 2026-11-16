"""Offline tests: chunking, the experiment and answer checks, with a toy embedding (no network, no model)."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import answer as an  # noqa: E402
import chunking as ck  # noqa: E402
import phak  # noqa: E402

TEXT = " ".join(f"Sentence number {i} talks about density altitude and takeoff." for i in range(60))
WORDS = set(TEXT.split())


def test_fixed_chunks_respect_size_overlap_and_cover_the_text():
    chunks = ck.fixed_chunks(TEXT, 200, 50)
    assert all(len(c) <= 200 for c in chunks)
    assert chunks[0][-10:] in chunks[1]  # overlap carries the end of one chunk into the next
    assert chunks[0].startswith("Sentence number 0") and chunks[-1].endswith("number 59 talks about density altitude and takeoff.")
    with pytest.raises(ValueError):
        ck.fixed_chunks(TEXT, 100, 100)


def test_fixed_chunks_never_cut_a_word():
    for size, overlap in [(97, 0), (150, 40), (61, 30)]:
        for c in ck.fixed_chunks(TEXT, size, overlap):
            assert set(c.split()) <= WORDS


def test_no_overlap_means_no_repeated_text():
    chunks = ck.fixed_chunks(TEXT, 120, 0)
    assert " ".join(chunks) == TEXT


def test_sentence_chunks_keep_whole_sentences_and_carry_overlap():
    chunks = ck.sentence_chunks(TEXT, 250, 70)
    assert all(c.startswith("Sentence") and c.endswith(".") and len(c) <= 250 for c in chunks)
    last_sentence = "Sentence" + chunks[0].split("Sentence")[-1]
    assert chunks[1].startswith(last_sentence)


def test_clean_joins_wrapped_lines_and_drops_page_numbers():
    raw = "Density alti-\ntude is pressure altitude\ncorrected for temperature.\n11-14\nNext paragraph."
    assert phak.clean(raw) == "Density altitude is pressure altitude corrected for temperature.\nNext paragraph."


VOCAB = ["density", "takeoff", "inversion", "clearance", "heaps"]


def toy_embed(texts):
    v = np.array([[t.lower().count(w) for w in VOCAB] for t in texts], dtype=np.float32) + 1e-3
    return v / np.linalg.norm(v, axis=1, keepdims=True)


CORPUS = {11: "Density altitude raises takeoff distance. " * 20, 12: "An inversion traps haze. " * 20,
          15: "Class B needs a clearance. " * 20}
QUESTIONS = pd.DataFrame([{"question": "density takeoff", "chapter": 11, "keywords": "takeoff"},
                          {"question": "inversion", "chapter": 12, "keywords": "inversion"},
                          {"question": "clearance", "chapter": 11, "keywords": "clearance"}])  # wrong chapter: a miss


def test_sweep_scores_each_setting_and_embeds_each_text_once():
    calls = []
    embed = ck.EmbeddingCache(lambda t: (calls.append(len(t)), toy_embed(t))[1])
    table = ck.sweep(CORPUS, QUESTIONS, embed, sizes=[100, 300], overlaps=[0, 0.2], strategies=["fixed", "sentence"], k=2)
    assert len(table) == 8
    assert np.allclose(table["keyword_hit@2"], 2 / 3) and np.allclose(table["MRR"], 2 / 3)
    small, large = table[table["size"] == 100], table[table["size"] == 300]
    assert (large["context_chars@2"].values > small["context_chars@2"].values).all()
    assert sum(calls) == len(embed.cache)
    best = ck.best_setting(table, k=2)
    assert best["size"] == 100  # same accuracy, less text


def test_evaluate_reports_rank_of_first_hit():
    chunks = pd.DataFrame({"chapter": [11, 11, 12], "text": ["nothing here", "takeoff roll", "inversion"]})
    vecs = np.eye(3, dtype=np.float32)
    q = pd.DataFrame([{"question": "x", "chapter": 11, "keywords": "takeoff"}])
    result = ck.evaluate(chunks, vecs, q, np.array([[0.9, 0.5, 0.1]], dtype=np.float32), k=3, with_ranks=True)
    assert result["ranks"] == [2] and result["MRR"] == 0.5


def test_answers_cite_abstain_and_flag_bad_citations():
    good = an.ask("q", ["Density altitude is..."], lambda p: "Pressure altitude corrected for temperature [P1].")
    none = an.ask("q", ["Density altitude is..."], lambda p: "<think>hmm</think>Not in the handbook passages.")
    cut_off = an.ask("q", ["a"], lambda p: "<think>still thinking when the tokens ran out")
    bad = an.ask("q", ["a"], lambda p: "Answer [P1, P3].")
    assert good["citations"] == ["1"] and good["verdict"] == "answered"
    assert none["abstained"] and none["verdict"] == "abstained"
    assert cut_off["verdict"] == "empty"
    assert bad["unknown_citations"] == ["3"] and bad["verdict"] == "check"
