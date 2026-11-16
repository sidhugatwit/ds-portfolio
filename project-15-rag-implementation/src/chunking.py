"""Chunking strategies and the experiment: how chunk size and overlap change retrieval on labelled questions."""
from __future__ import annotations

import re
from typing import Callable

import numpy as np
import pandas as pd

SENTENCE = re.compile(r"(?<=[.!?])\s+")


def fixed_chunks(text: str, size: int, overlap: int) -> list[str]:
    """Windows of at most `size` characters that end and start on word boundaries, `overlap` characters shared."""
    if overlap >= size:
        raise ValueError("overlap must be smaller than size")
    text = " ".join(text.split())
    chunks, start, n = [], 0, len(text)
    while start < n:
        end = min(start + size, n)
        if end < n:
            cut = text.rfind(" ", start, end + 1)
            if cut > start:
                end = cut
        chunks.append(text[start:end].strip())
        if end >= n:
            break
        nxt = max(end - overlap, start + 1)
        if text[nxt - 1] != " ":  # landed mid-word: move to the next word
            space = text.find(" ", nxt)
            nxt = space + 1 if space != -1 and space < end else end
        start = nxt
    return [c for c in chunks if c]


def sentence_chunks(text: str, size: int, overlap: int) -> list[str]:
    """Whole sentences packed up to `size` characters; trailing sentences up to `overlap` characters carry over."""
    if overlap >= size:
        raise ValueError("overlap must be smaller than size")
    sentences = []
    for s in SENTENCE.split(" ".join(text.split())):
        if s:
            sentences.extend(fixed_chunks(s, size, 0) if len(s) > size else [s])

    def length(xs):
        return sum(map(len, xs)) + max(len(xs) - 1, 0)

    chunks, current = [], []
    for s in sentences:
        if current and length(current + [s]) > size:
            chunks.append(" ".join(current))
            carry = []
            for prev in reversed(current):
                if length([prev] + carry) > overlap:
                    break
                carry.insert(0, prev)
            while carry and length(carry + [s]) > size:
                carry.pop(0)
            current = carry
        current.append(s)
    if current:
        chunks.append(" ".join(current))
    return chunks


STRATEGIES: dict[str, Callable[[str, int, int], list[str]]] = {"fixed": fixed_chunks, "sentence": sentence_chunks}


def build_chunks(corpus: dict[int, str], strategy: str, size: int, overlap: int) -> pd.DataFrame:
    rows = [{"chapter": ch, "text": t} for ch, text in corpus.items() for t in STRATEGIES[strategy](text, size, overlap)]
    return pd.DataFrame(rows, columns=["chapter", "text"])


class EmbeddingCache:
    """Embeds each distinct text once, however many settings reuse it."""

    def __init__(self, embed: Callable[[list[str]], np.ndarray]):
        self.embed, self.cache = embed, {}

    def __call__(self, texts: list[str]) -> np.ndarray:
        missing = list(dict.fromkeys(t for t in texts if t not in self.cache))
        if missing:
            for t, v in zip(missing, self.embed(missing)):
                self.cache[t] = np.asarray(v, dtype=np.float32)
        return np.stack([self.cache[t] for t in texts])


def retrieve(vectors: np.ndarray, query_vec: np.ndarray, k: int) -> np.ndarray:
    """Indices of the k chunks most similar to the query (vectors are normalized, so dot product = cosine)."""
    return np.argsort(-(vectors @ query_vec), kind="stable")[:k]


def is_hit(row, chapter: int, keywords: list[str]) -> bool:
    text = row.text.lower()
    return row.chapter == chapter and any(k in text for k in keywords)


def keywords_of(value: str) -> list[str]:
    return [k.strip().lower() for k in str(value).split(";") if k.strip()]


def evaluate(chunks: pd.DataFrame, vectors: np.ndarray, questions: pd.DataFrame, query_vecs: np.ndarray,
             k: int = 5, with_ranks: bool = False) -> dict:
    """keyword_hit@k: share of questions with a chunk from the right chapter containing an answer keyword in the top k.
    MRR: mean of 1/rank of the first such chunk. context_chars@k: characters the LLM would have to read."""
    ranks, chars = [], []
    for q, qv in zip(questions.itertuples(), query_vecs):
        top = chunks.iloc[retrieve(vectors, qv, k)]
        chars.append(int(top.text.str.len().sum()))
        kws = keywords_of(q.keywords)
        ranks.append(next((i for i, r in enumerate(top.itertuples(), start=1) if is_hit(r, q.chapter, kws)), None))
    result = {"chunks": len(chunks), f"keyword_hit@{k}": float(np.mean([r is not None for r in ranks])),
              "MRR": float(np.mean([1 / r if r else 0 for r in ranks])), f"context_chars@{k}": float(np.mean(chars))}
    if with_ranks:
        result["ranks"] = ranks
    return result


def sweep(corpus: dict[int, str], questions: pd.DataFrame, embed: Callable, sizes, overlaps, strategies,
          k: int = 5, embed_query: Callable | None = None) -> pd.DataFrame:
    """Every strategy × size × overlap (as a fraction of size), scored on the same questions."""
    query_vecs = (embed_query or embed)(list(questions.question))
    rows = []
    for strategy in strategies:
        for size in sizes:
            for frac in overlaps:
                chunks = build_chunks(corpus, strategy, size, int(size * frac))
                vectors = embed(list(chunks.text))
                rows.append({"strategy": strategy, "size": size, "overlap": frac,
                             **evaluate(chunks, vectors, questions, query_vecs, k)})
    return pd.DataFrame(rows)


def best_setting(table: pd.DataFrame, k: int = 5) -> pd.Series:
    """Highest hit rate, then highest MRR, then the least text sent to the model."""
    return table.sort_values([f"keyword_hit@{k}", "MRR", f"context_chars@{k}"],
                             ascending=[False, False, True]).iloc[0]
