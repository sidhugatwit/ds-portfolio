"""Email triage as a LangGraph graph: classify (ignore / notify / respond), using past corrections from long-term memory."""
from __future__ import annotations

import json
import os
import re
from typing import Callable, TypedDict

from langgraph.graph import END, START, StateGraph

LABELS = ("ignore", "notify", "respond")

PROFILE = {
    "name": "Gurveer",
    "background": "Data Science student at Wentworth Institute of Technology, private pilot, "
                  "building an AI/ML portfolio and looking for a 2027 co-op.",
    "ignore": "Marketing, promotions, spam, mass newsletters, and automated notifications.",
    "notify": "Important information Gurveer should know about but that needs no reply.",
    "respond": "Direct questions, requests, and meeting scheduling addressed to Gurveer personally.",
}

PROMPT = """You are an email triage assistant for {name}. {background}

Classify the email into exactly one category:
- ignore: {ignore}
- notify: {notify}
- respond: {respond}
{examples}
Reply with JSON only, no other text:
{{"reasoning": "<one or two sentences>", "classification": "ignore" or "notify" or "respond"}}

Email to triage:
{email}"""

EXAMPLES_HEADER = """
{name} corrected these past triage decisions. When the new email is similar, follow his preference:
"""


def email_text(email: dict, max_body: int = 600) -> str:
    return f"From: {email['author']}\nSubject: {email['subject']}\n\n{email['body'][:max_body]}"


def examples_block(memories: list[dict], name: str) -> str:
    if not memories:
        return ""
    parts = [EXAMPLES_HEADER.format(name=name)]
    for i, m in enumerate(memories, start=1):
        parts.append(f"Past email {i}:\n{email_text(m['email'], 300)}\nCorrect: {m['label']}. Why: {m['reason']}\n")
    return "\n".join(parts)


def strip_thinking(text: str) -> str:
    text = re.sub(r"<think>.*?</think>", "", text or "", flags=re.S)
    return text.split("<think>")[0].strip()


def parse_triage(text: str) -> dict:
    """The model's JSON verdict; falls back to the first label it names. classification is None if there's none."""
    text = strip_thinking(text)
    for block in reversed(re.findall(r"\{.*?\}", text, flags=re.S)):
        try:
            data = json.loads(block)
        except json.JSONDecodeError:
            continue
        label = str(data.get("classification", "")).strip().lower()
        if label in LABELS:
            return {"classification": label, "reasoning": str(data.get("reasoning", "")).strip()}
    m = re.search(r'classification"?\s*[:=]\s*"?(ignore|notify|respond)', text, flags=re.I)
    return {"classification": m.group(1).lower() if m else None, "reasoning": text[:300]}


class TriageState(TypedDict, total=False):
    email: dict
    classification: str | None
    reasoning: str
    memories_used: list[str]
    reply: dict


def build_graph(chat: Callable[[str], str], memory=None, responder: Callable[[dict], dict] | None = None,
                k: int = 3, profile: dict = PROFILE):
    """START -> triage -> (respond -> END | END). `memory` is a TriageMemory or None; `responder` drafts replies."""

    def triage(state: TriageState) -> TriageState:
        email = state["email"]
        memories = memory.search(email, k) if memory is not None else []
        prompt = PROMPT.format(**profile, examples=examples_block(memories, profile["name"]), email=email_text(email))
        verdict = parse_triage(chat(prompt))
        return {**verdict, "memories_used": [m["key"] for m in memories]}

    def route(state: TriageState) -> str:
        return "respond" if state.get("classification") == "respond" and responder is not None else END

    def respond(state: TriageState) -> TriageState:
        return {"reply": responder(state["email"])}

    g = StateGraph(TriageState)
    g.add_node("triage", triage)
    g.add_node("respond", respond)
    g.add_edge(START, "triage")
    g.add_conditional_edges("triage", route, ["respond", END])
    g.add_edge("respond", END)
    return g.compile()


def openai_chat(max_tokens: int = 300):
    """A chat function for any OpenAI-compatible endpoint set in .env (LM Studio by default)."""
    from openai import OpenAI

    client = OpenAI()
    model = os.getenv("LLM_MODEL", "gpt-4o-mini")
    budget = max_tokens + int(os.getenv("LLM_REASONING_TOKENS", "0"))

    def chat(prompt: str) -> str:
        r = client.chat.completions.create(model=model, temperature=0, max_tokens=budget,
                                           messages=[{"role": "user", "content": prompt}])
        return r.choices[0].message.content or ""
    return chat
