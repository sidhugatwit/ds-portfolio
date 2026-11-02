"""Recompute v1 benchmark scores from the saved model responses.

The original v1 notebook was lost, but every model response and reference
answer was saved in outputs/llm_responses.csv. This script re-derives the
published scores from that file, so the v1 results stay verifiable.

ROUGE reproduces eval_scores.csv exactly (Google's rouge-score, Porter stemmer on).
BERTScore downloads roberta-large (~1.4 GB) on first run; pass --skip-bert to skip it.

Usage (from the project folder):
    python src/rescore.py
    python src/rescore.py --skip-bert
"""

import argparse
from pathlib import Path

import pandas as pd
from rouge_score import rouge_scorer

OUTPUTS = Path(__file__).resolve().parent.parent / "outputs"
METRICS = ["rouge1", "rouge2", "rougeL"]


def rouge_scores(responses: pd.DataFrame) -> pd.DataFrame:
    scorer = rouge_scorer.RougeScorer(METRICS, use_stemmer=True)
    rows = [
        {m: s.fmeasure for m, s in scorer.score(ref, resp).items()}
        for ref, resp in zip(responses["reference"], responses["response"])
    ]
    return pd.concat([responses[["id", "domain", "model"]], pd.DataFrame(rows)], axis=1)


def add_bertscore(scores: pd.DataFrame, responses: pd.DataFrame) -> pd.DataFrame:
    from bert_score import score as bert_score

    _, _, f1 = bert_score(
        responses["response"].tolist(), responses["reference"].tolist(), lang="en"
    )
    return scores.assign(bert_f1=f1.numpy())


def compare(recomputed: pd.DataFrame, published: pd.DataFrame, metrics: list) -> None:
    merged = recomputed.merge(published, on=["id", "model"], suffixes=("", "_published"))
    print(f"Compared {len(merged)} rows against eval_scores.csv")
    for m in metrics:
        diff = (merged[m] - merged[f"{m}_published"]).abs().max()
        verdict = "matches" if diff < 1e-3 else "DIFFERS"
        print(f"  {m:8s} max abs difference {diff:.4f}  -> {verdict}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--skip-bert", action="store_true", help="Skip BERTScore")
    args = parser.parse_args()

    responses = pd.read_csv(OUTPUTS / "llm_responses.csv")
    published = pd.read_csv(OUTPUTS / "eval_scores.csv")

    scores = rouge_scores(responses)
    metrics = list(METRICS)
    if not args.skip_bert:
        scores = add_bertscore(scores, responses)
        metrics.append("bert_f1")

    compare(scores, published, metrics)
    print("\nLeaderboard (mean per model):")
    print(scores.groupby("model")[metrics].mean().round(4).to_string())


if __name__ == "__main__":
    main()
