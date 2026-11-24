"""Answer from retrieved handbook passages with citations, and abstain when the passages don't cover the question."""
from __future__ import annotations

import os
import re

PROMPT = """You answer a student pilot's question using only the passages below, from the FAA Pilot's Handbook of
Aeronautical Knowledge. Cite every claim with its passage tag, like [P1]. If the passages don't contain the answer,
reply exactly: Not in the handbook passages.

{passages}

Question: {question}
Answer:"""

ABSTAIN = re.compile(r"not in the handbook passages", re.I)


def strip_thinking(text: str) -> str:
    text = re.sub(r"<think>.*?</think>", "", text or "", flags=re.S)
    return text.split("<think>")[0].strip()  # an unclosed block means the model ran out of tokens


def ask(question: str, passages: list[str], chat) -> dict:
    """`chat` takes a prompt and returns the model's text (see `openai_chat`)."""
    numbered = "\n\n".join(f"[P{i}] {p}" for i, p in enumerate(passages, start=1))
    answer = strip_thinking(chat(PROMPT.format(passages=numbered, question=question)))
    cited = sorted({n for group in re.findall(r"\[([^\]]*)\]", answer) for n in re.findall(r"P(\d+)", group)}, key=int)
    unknown = [c for c in cited if not 1 <= int(c) <= len(passages)]
    abstained = bool(ABSTAIN.search(answer))
    citations = [c for c in cited if c not in unknown]
    verdict = ("check" if unknown else "abstained" if abstained else "answered" if citations
               else "empty" if not answer else "uncited")
    return {"question": question, "answer": answer, "abstained": abstained, "citations": citations,
            "unknown_citations": unknown, "verdict": verdict}


def openai_chat(max_tokens: int = 500):
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
