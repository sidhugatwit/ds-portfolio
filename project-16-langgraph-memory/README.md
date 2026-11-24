# Email Triage

I built an email triage agent that recalls previous corrections and evaluated it with and without that memory.

## Architecture

Incoming email → retrieve user corrections → LangGraph triage → compare labels with and without memory.

## Run locally

From this folder, run `uv sync --frozen` and `uv run --frozen jupyter lab`. Open [the notebook](./notebooks/triage_memory.ipynb). Review the existing run notes below for any data or service requirements.

## Results

**Held-out triage, with vs without memory** · 22/22 vs 17/22. [Saved evidence](./outputs/triage_run.json).

## Demo and deployment

TODO · Record a demo and verify any deployment.

## Next steps

Test more inboxes and document what happens when preferences conflict.

## Implementation notes

An assistant sorts email into **ignore / notify / respond**. General rules get it most of the way, but every person
has preferences no rulebook states: *CI failures on my repos: tell me. Recruiters for sales roles: ignore. FAA Safety
Team notices: tell me.* This project tests whether a LangGraph agent **learns those preferences from a handful of
corrections, keeps them across sessions, and gets measurably better** without getting worse at everything else.

## How it works

```
START → triage ──respond──→ reply agent (calendar + draft tools) → END
            └──ignore / notify──→ END
```

- **Triage** (`src/triage.py`): a LangGraph node that asks the LLM for a JSON verdict. Before asking, it searches
  long-term memory for the 3 most similar past corrections and puts them in the prompt with Gurveer's reason for each.
- **Long-term memory** (`src/memory.py`): corrections live in a LangGraph `InMemoryStore` with semantic search
  (BGE-small embeddings), saved to `outputs/memory_store.json` and reloaded into a fresh store, as a new session would.
- **Reply agent** (`src/respond.py`): a tool-calling ReAct agent with `check_calendar_availability`,
  `schedule_meeting` and `write_email`. It drafts; nothing is sent.

## The test

`eval/emails.jsonl` holds 30 labelled emails from fictional senders:

- **8 corrections** Gurveer gives the assistant, each with a one-line reason (the preferences are illustrative).
- **22 held-out test emails.** 11 fall under a preference that only the corrections state (CI failures, recruiters,
  campus announcements, FAA Safety Team notices, receipts); 11 are covered by the general rules (spam, newsletters,
  direct questions, meeting requests, FYIs).

The notebook triages the 22 test emails twice, without memory and with it, and reports accuracy on each group. The
general group is the check that memory doesn't make things worse.

## Results

Recorded run: 17 November 2026, Qwen3.6-35B-A3B in LM Studio, BGE-small embeddings, 3 recalled corrections per email
(`outputs/triage_run.json`, `outputs/memory_store.json`).

| 22 held-out emails | No memory | With memory |
|---|---|---|
| Covered by a preference (11) | 6 / 11 | **11 / 11** |
| Covered by the general rules (11) | 11 / 11 | 11 / 11 |
| All | 17 / 22 | **22 / 22** |

- **Memory fixed all five preference mistakes, and broke nothing.** Without memory, Qwen ignored both CI-failure emails
  and the FAA Safety Team webinar as "automated notifications", wanted to reply to a retail-store recruiter because he
  asked a question, and flagged a shipping notice as worth knowing. With memory, each of these recalled the matching
  correction first, and the model's reasoning cites it ("matches the past example", "following the past correction
  rule for unrelated recruiters").
- **The general emails stayed at 11 / 11**, so three recalled corrections in the prompt didn't pull unrelated emails
  off course.
- **Memory survives a restart.** The with-memory run used a store rebuilt from `outputs/memory_store.json`, not the
  one the corrections were written to.

**How far this goes.** 22 emails is a small test, and I wrote the test emails alongside the corrections, so many of
them resemble a correction closely (another GitHub failure, another FAA Safety Team notice); others share only the rule
(a different store's receipt, a different company's recruiter). This shows the agent applies a preference to similar
emails. It doesn't show it can generalise a correction to a different kind of email,
which would need a larger set written by someone else.

**Replies.** For the three emails routed to the reply agent, Qwen called the calendar tool before writing, and booked
nothing, since no time had been agreed:

- **Interview request:** checked the week and proposed exactly the two times the recruiter asked for.
- **Advisor meeting:** checked every weekday and listed all ten free slots. Correct, but more than a person would send.
- **Flight lesson moved to Saturday: wrong.** The sample calendar only covers weekdays, so the tool answered "No free
  slots found for Saturday", and the agent drafted a reply declining the lesson. It's the right reading of the tool's
  words and the wrong outcome. The fix is in the tool, not the model: say "no calendar data for weekends" so the agent
  asks rather than declines. Drafts are never sent, which is why a human review step matters.

## Run it

```bash
uv sync
uv run pytest -q tests          # offline: parsing, memory search and reload, graph routing, scoring, data checks
uv run jupyter lab notebooks/triage_memory.ipynb
```

The notebook needs LM Studio's server running with the model named in `LLM_MODEL` (see the repo's `.env.example`).
Any OpenAI-compatible endpoint with tool calling works.

## Files

- `notebooks/triage_memory.ipynb` — baseline, teaching, reload, re-test, replies
- `src/triage.py`, `src/memory.py`, `src/respond.py`, `src/evaluate.py` — the code the notebook calls
- `eval/emails.jsonl` — the 30 labelled emails
- `outputs/memory_store.json`, `outputs/triage_run.json` — recorded run

## Earlier version

The first version was a course notebook titled "Long-Term Agentic Memory" that had no memory: a triage router and
ReAct agent on GPT-4o-mini, tried on 3 emails with no check of whether its labels were right. This rebuild adds the
memory, a labelled test set, and a before/after measurement.
