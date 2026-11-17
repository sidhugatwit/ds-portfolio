"""Offline tests: parsing, memory search and persistence, graph routing, scoring, data. No model, no network."""
import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import evaluate as ev  # noqa: E402
import respond  # noqa: E402
import triage as tr  # noqa: E402
from memory import TriageMemory  # noqa: E402

EMAILS = [json.loads(l) for l in (ROOT / "eval" / "emails.jsonl").read_text(encoding="utf-8").splitlines()]
BY_ID = {e["id"]: e for e in EMAILS}
VOCAB = ["github", "run failed", "recruit", "sales", "faa", "receipt", "club", "fair", "lesson", "notebook"]


def toy_embed(texts):
    out = []
    for t in texts:
        v = [float(t.lower().count(w)) for w in VOCAB] + [0.01]
        n = sum(x * x for x in v) ** 0.5
        out.append([x / n for x in v])
    return out


def test_parse_triage_handles_thinking_json_and_fallbacks():
    assert tr.parse_triage('<think>hmm</think>{"reasoning": "CI failure", "classification": "Notify"}') == \
        {"classification": "notify", "reasoning": "CI failure"}
    assert tr.parse_triage('Sure. classification: respond')["classification"] == "respond"
    assert tr.parse_triage("<think>ran out of tokens")["classification"] is None
    assert tr.parse_triage('{"classification": "archive"}')["classification"] is None


def test_memory_finds_the_relevant_correction_and_survives_a_restart(tmp_path):
    memory = TriageMemory(toy_embed, len(VOCAB) + 1)
    for e in EMAILS:
        if e["split"] == "teach":
            memory.add(e["id"], e, e["label"], e["reason"])
    assert len(memory) == 8
    assert memory.search(BY_ID["X1"], k=1)[0]["key"] == "T1"  # a CI failure recalls the CI correction
    memory.save(tmp_path / "memory.json")
    reloaded = TriageMemory.load(tmp_path / "memory.json", toy_embed, len(VOCAB) + 1)
    assert [m["key"] for m in reloaded.search(BY_ID["X1"], k=2)] == [m["key"] for m in memory.search(BY_ID["X1"], k=2)]


def test_graph_puts_memories_in_the_prompt_and_routes_only_respond_to_the_responder():
    prompts, replies = [], []
    memory = TriageMemory(toy_embed, len(VOCAB) + 1)
    memory.add("T1", BY_ID["T1"], "notify", BY_ID["T1"]["reason"])

    def chat(prompt):
        prompts.append(prompt)
        return '{"reasoning": "x", "classification": "respond"}' if "Capstone" in prompt else \
            '{"reasoning": "x", "classification": "notify"}'

    graph = tr.build_graph(chat, memory, responder=lambda e: replies.append(e["id"]) or {"final": "ok"}, k=1)
    ci = graph.invoke({"email": BY_ID["X1"]})
    prof = graph.invoke({"email": BY_ID["X14"]})
    assert ci["classification"] == "notify" and ci["memories_used"] == ["T1"] and "reply" not in ci
    assert "corrected these past triage decisions" in prompts[0] and "Correct: notify" in prompts[0]
    assert prof["reply"] == {"final": "ok"} and replies == ["X14"]
    plain = tr.build_graph(chat).invoke({"email": BY_ID["X1"]})
    assert plain["memories_used"] == [] and "corrected these past" not in prompts[-1]


def test_accuracy_table_counts_by_group():
    df = pd.DataFrame({"group": ["general", "preference", "preference"], "label": ["ignore", "notify", "respond"],
                       "predicted": ["ignore", "ignore", None]})
    df["correct"] = df.label == df.predicted
    table = ev.accuracy_table({"run": df})
    assert table.loc["all", "run"] == "1/3" and table.loc["preference", "run"] == "0/2" and table.loc["unparsed", "run"] == 1


def test_tools_log_what_they_did():
    log = []
    check, schedule, write = respond.make_tools(log)
    assert "10:00 AM" in check.invoke({"day": "Monday"})
    write.invoke({"to": "a@b.example", "subject": "Re: hi", "content": "Thanks"})
    assert [c["tool"] for c in log] == ["check_calendar_availability", "write_email"]


def test_dataset_is_labelled_and_has_no_real_address():
    assert len(EMAILS) == 30 and {e["label"] for e in EMAILS} == set(tr.LABELS)
    assert sum(e["split"] == "teach" for e in EMAILS) == 8
    assert all(e.get("reason") for e in EMAILS if e["split"] == "teach")
    for path in [ROOT / "eval" / "emails.jsonl", *ROOT.glob("notebooks/*.ipynb")]:
        assert "gmail.com" not in path.read_text(encoding="utf-8")
