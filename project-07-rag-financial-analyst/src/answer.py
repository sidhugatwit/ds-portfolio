"""Answer questions from retrieved 10-K passages and XBRL facts, then check the answer against its sources."""
from __future__ import annotations

import os
import re

import pandas as pd

FACT_WORDS = re.compile(r"\b(revenue|revenues|sales|net income|profit|earnings|largest|highest|biggest)\b", re.I)


def billions(value) -> str:
    return "n/a" if pd.isna(value) else f"${value / 1e9:,.1f} billion"


def facts_source(facts: pd.DataFrame) -> str:
    lines = [f"{r.company}: fiscal year ended {r.fiscal_year_end}, revenue {billions(r.revenue)}, "
             f"net income {billions(r.net_income)}" for r in facts.itertuples()]
    return "Reported annual figures from SEC XBRL company facts (latest 10-K):\n" + "\n".join(lines)


def build_sources(passages: pd.DataFrame, facts: pd.DataFrame | None, question: str) -> dict[str, str]:
    sources = {f"S{i}": f"{r.company} 10-K ({r.section}, period {r.period}, {r.chunk_id}):\n{r.text}"
               for i, r in enumerate(passages.itertuples(), start=1)}
    if facts is not None and FACT_WORDS.search(question):
        sources["F"] = facts_source(facts)
    return sources


PROMPT = """You are a careful financial analyst. Answer the question using only the sources below.
Cite every claim with its source tag, like [S1] or [F]. If the sources don't answer it, say so.
Quote numbers exactly as the sources state them.

{sources}

Question: {question}
Answer:"""


def numbers_in(text: str) -> set[str]:
    found = set()
    text = re.sub(r"\[(S\d+|F)\]", " ", text)  # citation tags aren't figures
    for n in re.findall(r"\d[\d,]*\.?\d*", text):
        n = n.replace(",", "").rstrip(".")
        if n and not (len(n) == 4 and n.isdigit() and 1990 <= int(n) <= 2035):  # skip years
            found.add(n)
    return found


NO_ANSWER = re.compile(r"\b(no information|not (?:state|provide|contain|include|mention|address)\w*|"
                       r"cannot answer|can't answer|unable to answer|don't (?:state|provide|contain))\b", re.I)


def check_answer(answer: str, sources: dict[str, str]) -> dict:
    """Citations must point at real sources, and every number in the answer must appear in a cited source.
    An answer that says the sources don't cover the question is an abstention, not a grounded answer."""
    cited = set(re.findall(r"\[(S\d+|F)\]", answer))
    unknown = sorted(c for c in cited if c not in sources)
    cited_text = " ".join(sources[c] for c in cited if c in sources)
    missing = sorted(numbers_in(answer) - numbers_in(cited_text))
    abstained = bool(NO_ANSWER.search(answer))
    grounded = bool(cited) and not unknown and not missing
    if unknown or missing:
        verdict = "check"
    elif abstained:
        verdict = "partial" if cited else "abstained"
    else:
        verdict = "grounded" if cited else "uncited"
    return {"citations": sorted(cited), "unknown_citations": unknown, "numbers_not_in_sources": missing,
            "abstained": abstained, "grounded": grounded and not abstained, "verdict": verdict}


def ask(question: str, retriever, facts: pd.DataFrame | None, chat, k: int = 8) -> dict:
    """`chat` takes a prompt and returns the model's text (see `openai_chat`)."""
    passages = retriever.search(question, k=k)
    sources = build_sources(passages, facts, question)
    prompt = PROMPT.format(sources="\n\n".join(f"[{tag}] {text}" for tag, text in sources.items()), question=question)
    answer = re.sub(r"<think>.*?</think>", "", chat(prompt) or "", flags=re.S).strip()
    return {"question": question, "answer": answer, "sources": list(sources), **check_answer(answer, sources)}


def openai_chat(max_tokens: int = 700):
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
