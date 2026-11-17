"""Score triage against the labels."""
from __future__ import annotations

import pandas as pd


def run_triage(graph, emails: list[dict]) -> pd.DataFrame:
    rows = []
    for e in emails:
        out = graph.invoke({"email": e})
        rows.append({"id": e["id"], "group": e["group"], "label": e["label"], "predicted": out.get("classification"),
                     "reasoning": out.get("reasoning", ""), "memories_used": out.get("memories_used", [])})
    df = pd.DataFrame(rows)
    df["correct"] = df["label"] == df["predicted"]
    return df


def accuracy_table(runs: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Accuracy overall and by group (preference: rules only Gurveer's corrections state; general: the base rules)."""
    table = {}
    for name, df in runs.items():
        table[name] = {"all": f"{df.correct.sum()}/{len(df)}",
                       **{g: f"{d.correct.sum()}/{len(d)}" for g, d in df.groupby("group")},
                       "unparsed": int(df.predicted.isna().sum())}
    return pd.DataFrame(table)
