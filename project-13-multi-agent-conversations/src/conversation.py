"""Turn-based multi-agent conversations with per-agent perspective, plus checks on the result.

Each agent sees the conversation from its own point of view: its own past lines as "assistant",
everyone else's as "user" with the speaker's name. (Sharing one history where every line is
"assistant" makes agents lose track of who said what, and start speaking for each other.)
"""
from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from typing import Callable

Chat = Callable[[list[dict]], str]  # messages -> reply text


@dataclass
class Agent:
    name: str
    persona: str


@dataclass
class Conversation:
    scene: str
    agents: list[Agent]
    turns: list[tuple[str, str]] = field(default_factory=list)  # (speaker, text)

    def view(self, agent: Agent) -> list[dict]:
        """The messages one agent sends to the model."""
        others = ", ".join(a.name for a in self.agents if a.name != agent.name)
        system = (f"{self.scene}\nYou are {agent.name}. {agent.persona}\n"
                  f"The others are: {others}. Speak only as {agent.name}, in 1-4 sentences, "
                  f"with no name prefix and no lines for anyone else.")
        messages = [{"role": "system", "content": system}]
        for speaker, text in self.turns:
            if speaker == agent.name:
                messages.append({"role": "assistant", "content": text})
            else:
                messages.append({"role": "user", "content": f"{speaker}: {text}"})
        return messages


def clean_reply(text: str, speaker: str, names: list[str]) -> str:
    """Remove reasoning blocks and a leading 'NAME:' the model added despite instructions."""
    text = re.sub(r"<think>.*?</think>", "", text or "", flags=re.S).strip()
    text = re.sub(rf"^\**\s*{re.escape(speaker)}\s*:?\s*\**\s*:?\s*", "", text, flags=re.I) if re.match(
        rf"^\**\s*{re.escape(speaker)}\s*\**\s*:", text, flags=re.I) else text
    return text.strip()


def speaks_for_others(text: str, speaker: str, names: list[str]) -> list[str]:
    """Names of other agents this reply writes lines for ('MOTHER: ...' inside the son's turn)."""
    return [n for n in names if n != speaker and re.search(rf"(^|\n)\s*\**\s*{re.escape(n)}\s*\**\s*:", text, re.I)]


def run(conv: Conversation, chat: Chat, opening: tuple[str, str], order: list[str], rounds: int) -> list[dict]:
    """Play `rounds` rounds in `order` after the opening line. Returns a log with a check per turn."""
    by_name = {a.name: a for a in conv.agents}
    names = list(by_name)
    conv.turns.append(opening)
    log = [{"speaker": opening[0], "text": opening[1], "speaks_for_others": []}]
    for _ in range(rounds):
        for name in order:
            reply = clean_reply(chat(conv.view(by_name[name])), name, names)
            conv.turns.append((name, reply))
            log.append({"speaker": name, "text": reply, "speaks_for_others": speaks_for_others(reply, name, names)})
    return log


SUMMARY_PROMPT = """Here is a conversation:

{transcript}

Did they reach an agreement? Reply with JSON only, in this form:
{{"agreed": true, "terms": ["each condition they agreed on"], "open_issues": ["anything still unresolved"]}}"""


def parse_json(text: str) -> dict:
    text = re.sub(r"<think>.*?</think>", "", text or "", flags=re.S)
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip())
    match = re.search(r"\{.*\}", text, flags=re.S)
    if not match:
        raise ValueError(f"No JSON in reply: {text[:200]}")
    return json.loads(match.group(0))


def summarize(conv: Conversation, chat: Chat) -> dict:
    """A neutral moderator states what was agreed, as structured data."""
    transcript = "\n".join(f"{s}: {t}" for s, t in conv.turns)
    reply = chat([{"role": "user", "content": SUMMARY_PROMPT.format(transcript=transcript)}])
    summary = parse_json(reply)
    # Models sometimes write "None" as an item instead of an empty list.
    for key in ("terms", "open_issues"):
        summary[key] = [x for x in summary.get(key, []) if str(x).strip().lower() not in ("", "none", "n/a")]
    return summary


def openai_chat(temperature: float = 0.4, max_tokens: int = 300) -> Chat:
    """A chat function for any OpenAI-compatible endpoint in .env (LM Studio by default)."""
    from openai import OpenAI

    client = OpenAI()
    model = os.getenv("LLM_MODEL", "gpt-4o-mini")
    budget = max_tokens + int(os.getenv("LLM_REASONING_TOKENS", "0"))

    def chat(messages: list[dict]) -> str:
        import time
        from openai import APIError

        for attempt in (1, 2):  # local servers occasionally reject a request while busy; retry once
            try:
                r = client.chat.completions.create(model=model, temperature=temperature, max_tokens=budget,
                                                   messages=messages)
                return r.choices[0].message.content or ""
            except APIError as e:
                if attempt == 2:
                    raise RuntimeError(f"LLM request failed twice: {e}. Check LM Studio's server log, and that its "
                                       "context length fits the conversation plus LLM_REASONING_TOKENS.") from e
                time.sleep(3)
    return chat
