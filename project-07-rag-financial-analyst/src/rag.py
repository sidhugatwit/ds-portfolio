"""Retrieval over 10-K chunks: dense (embeddings + FAISS), keyword (BM25), and hybrid (reciprocal rank fusion),
with optional company filtering taken from the question."""
from __future__ import annotations

import re
from typing import Callable

import numpy as np
import pandas as pd
from rank_bm25 import BM25Okapi

COMPANY_ALIASES = {
    "NVIDIA": ["nvidia", "nvda"],
    "Microsoft": ["microsoft", "msft", "azure"],
    "JPMorgan": ["jpmorgan", "jp morgan", "jpm", "chase"],
    "Amazon": ["amazon", "amzn", "aws"],
    "Tesla": ["tesla", "tsla"],
}
MODES = ("dense", "bm25", "hybrid", "hybrid+filter")


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def companies_in(question: str) -> list[str]:
    q = question.lower()
    return [name for name, aliases in COMPANY_ALIASES.items() if any(re.search(rf"\b{re.escape(a)}\b", q) for a in aliases)]


def default_embedder(model_name: str = "BAAI/bge-small-en-v1.5") -> Callable[[list[str]], np.ndarray]:
    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer(model_name)
    return lambda texts: model.encode(texts, normalize_embeddings=True, batch_size=32, show_progress_bar=False)


class Retriever:
    def __init__(self, chunks: pd.DataFrame, embed: Callable[[list[str]], np.ndarray] | None = None):
        import faiss

        self.chunks = chunks.reset_index(drop=True)
        self.embed = embed or default_embedder()
        texts = self.chunks["text"].tolist()
        vectors = np.asarray(self.embed(texts), dtype=np.float32)
        self.index = faiss.IndexFlatIP(vectors.shape[1])  # inner product on normalized vectors = cosine
        self.index.add(vectors)
        self.bm25 = BM25Okapi([tokenize(t) for t in texts])

    def _dense(self, question: str, n: int) -> list[int]:
        q = np.asarray(self.embed([question]), dtype=np.float32)
        _, idx = self.index.search(q, min(n, len(self.chunks)))
        return [int(i) for i in idx[0] if i >= 0]

    def _bm25(self, question: str, n: int) -> list[int]:
        scores = self.bm25.get_scores(tokenize(question))
        return [int(i) for i in np.argsort(-scores)[:n]]

    def search(self, question: str, k: int = 5, mode: str = "hybrid+filter") -> pd.DataFrame:
        if mode not in MODES:
            raise ValueError(f"mode must be one of {MODES}")
        pool = max(50, k * 10)
        if mode == "dense":
            ranked = self._dense(question, pool)
        elif mode == "bm25":
            ranked = self._bm25(question, pool)
        else:  # reciprocal rank fusion: score = sum of 1 / (60 + rank) over both lists
            fused: dict[int, float] = {}
            for ranking in (self._dense(question, pool), self._bm25(question, pool)):
                for rank, i in enumerate(ranking):
                    fused[i] = fused.get(i, 0.0) + 1.0 / (60 + rank + 1)
            ranked = sorted(fused, key=fused.get, reverse=True)
        if mode == "hybrid+filter":
            wanted = companies_in(question)
            if wanted:
                ranked = [i for i in ranked if self.chunks.at[i, "company"] in wanted]
        out = self.chunks.iloc[ranked[:k]].copy()
        out.insert(0, "rank", range(1, len(out) + 1))
        return out


def evaluate(retriever: Retriever, questions: pd.DataFrame, k: int = 5, modes=MODES) -> pd.DataFrame:
    """Per mode: share of questions with a chunk from the right company and section in the top k (hit@k),
    the same with one of the expected keywords in that chunk (keyword hit@k), and mean reciprocal rank."""
    rows = []
    for mode in modes:
        hits, kw_hits, rr = [], [], []
        for q in questions.itertuples():
            results = retriever.search(q.question, k=k, mode=mode)
            gold = (results["company"] == q.company) & (results["section"] == q.section)
            keywords = [w.strip().lower() for w in str(q.keywords).split(";") if w.strip()]
            has_kw = results["text"].str.lower().apply(lambda t: any(w in t for w in keywords))
            hits.append(bool(gold.any()))
            kw_hits.append(bool((gold & has_kw).any()))
            first = results.loc[gold, "rank"]
            rr.append(1.0 / first.iloc[0] if len(first) else 0.0)
        rows.append({"mode": mode, f"hit@{k}": np.mean(hits), f"keyword_hit@{k}": np.mean(kw_hits), "MRR": np.mean(rr)})
    return pd.DataFrame(rows).round(3)
