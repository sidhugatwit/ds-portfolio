"""Leakage rules and a minimal agent for the speed-dating data.

Usage: uv run python src/agents.py "Check these features for leakage: attr_o, int_corr, dec"
"""
import json
import os
import re
import sys

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(usecwd=True))
os.environ.setdefault("OPENAI_API_KEY", "lm-studio")  # local servers accept any key

OUTCOME = re.compile(r"^(match|dec|dec_o)$")
AFTER_DATE = re.compile(
    r"^(attr|sinc|intel|fun|amb|shar|like|prob|met)(_o)?$"
    r"|^match_es$|_s$"
    r"|_2$|_3$|^(you_call|them_cal|date_3|numdat_3|num_in_3|satis_2|length|numdat_2)$"
)


def is_leakage(col: str) -> bool:
    """True for outcome columns and anything recorded during or after the date."""
    return bool(OUTCOME.search(col) or AFTER_DATE.search(col))


def build_agent():
    from langchain_core.tools import tool
    from langchain_openai import ChatOpenAI
    from langgraph.prebuilt import create_react_agent

    @tool
    def check_leakage(features: str) -> str:
        """Check a comma-separated list of column names for leakage."""
        names = [f.strip() for f in features.split(",") if f.strip()]
        flagged = [f for f in names if is_leakage(f)]
        return json.dumps({"flagged_leakage": flagged, "safe_features": [f for f in names if f not in flagged]})

    budget = 1000 + int(os.getenv("LLM_REASONING_TOKENS", "0"))
    llm = ChatOpenAI(model=os.getenv("LLM_MODEL", "gpt-4o-mini"), temperature=0, max_tokens=budget)
    return create_react_agent(llm, tools=[check_leakage])


if __name__ == "__main__":
    question = " ".join(sys.argv[1:]) or "Check these features for leakage: attr_o, like, int_corr, age_o, dec"
    result = build_agent().invoke({"messages": [{"role": "user", "content": question}]})
    print(re.sub(r"<think>.*?</think>", "", result["messages"][-1].content, flags=re.S).strip())
