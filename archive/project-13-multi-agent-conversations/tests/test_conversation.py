"""Offline tests with a scripted model: no LLM needed."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import conversation as cv  # noqa: E402

AGENTS = [cv.Agent("SON", "Wants a motorcycle."), cv.Agent("MOTHER", "Worried about safety."), cv.Agent("FATHER", "Wants rules.")]


def test_each_agent_sees_its_own_lines_as_assistant():
    conv = cv.Conversation("A family talk.", AGENTS, turns=[("SON", "Can I buy one?"), ("MOTHER", "It's risky.")])
    son = conv.view(AGENTS[0])
    mother = conv.view(AGENTS[1])
    assert son[1] == {"role": "assistant", "content": "Can I buy one?"}
    assert son[2] == {"role": "user", "content": "MOTHER: It's risky."}
    assert mother[1] == {"role": "user", "content": "SON: Can I buy one?"}
    assert mother[2] == {"role": "assistant", "content": "It's risky."}
    assert "You are SON" in son[0]["content"] and "MOTHER, FATHER" in son[0]["content"]


def test_clean_reply_strips_thinking_and_own_prefix():
    assert cv.clean_reply("<think>hmm</think>\n**SON:** Fine, I'll take a course.", "SON", ["SON"]) == "Fine, I'll take a course."


def test_detects_speaking_for_others():
    text = "I'll take the course.\nMOTHER: Good.\nFATHER: Agreed."
    assert cv.speaks_for_others(text, "SON", ["SON", "MOTHER", "FATHER"]) == ["MOTHER", "FATHER"]
    assert cv.speaks_for_others("Mother: is right, I think.", "SON", ["SON", "MOTHER"]) == ["MOTHER"]
    assert cv.speaks_for_others("I agree with mother.", "SON", ["SON", "MOTHER"]) == []


def test_run_follows_turn_order_and_logs_checks():
    replies = iter(["MOTHER: Too risky.", "Rules first.", "OK, a course first.\nFATHER: Deal."])
    conv = cv.Conversation("A family talk.", AGENTS)
    log = cv.run(conv, lambda msgs: next(replies), ("SON", "Can I buy one?"), ["MOTHER", "FATHER", "SON"], rounds=1)
    assert [t["speaker"] for t in log] == ["SON", "MOTHER", "FATHER", "SON"]
    assert log[1]["text"] == "Too risky."
    assert log[3]["speaks_for_others"] == ["FATHER"]


def test_summary_parses_fenced_json():
    conv = cv.Conversation("A family talk.", AGENTS, turns=[("SON", "Deal.")])
    out = cv.summarize(conv, lambda m: '<think>x</think>```json\n{"agreed": true, "terms": ["course"], "open_issues": []}\n```')
    assert out == {"agreed": True, "terms": ["course"], "open_issues": []}
    out = cv.summarize(conv, lambda m: '{"agreed": true, "terms": ["course"], "open_issues": ["None"]}')
    assert out["open_issues"] == []
