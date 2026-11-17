"""Long-term triage memory: corrections Gurveer gives, kept in a LangGraph store with semantic search, saved to disk."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Callable

from langgraph.store.memory import InMemoryStore

NAMESPACE = ("gurveer", "triage_corrections")


class TriageMemory:
    def __init__(self, embed: Callable[[list[str]], list[list[float]]], dims: int):
        self.embed, self.dims = embed, dims
        self.store = InMemoryStore(index={"dims": dims, "embed": embed, "fields": ["text"]})
        self.records: dict[str, dict] = {}

    def add(self, key: str, email: dict, label: str, reason: str) -> None:
        from triage import email_text

        record = {"text": email_text(email), "email": email, "label": label, "reason": reason}
        self.store.put(NAMESPACE, key, record)
        self.records[key] = record

    def search(self, email: dict, k: int = 3) -> list[dict]:
        from triage import email_text

        hits = self.store.search(NAMESPACE, query=email_text(email), limit=k)
        return [{"key": h.key, "score": h.score, **h.value} for h in hits]

    def __len__(self) -> int:
        return len(self.records)

    def save(self, path: Path) -> None:
        Path(path).write_text(json.dumps(self.records, indent=2, ensure_ascii=False), encoding="utf-8")

    @classmethod
    def load(cls, path: Path, embed, dims: int) -> "TriageMemory":
        memory = cls(embed, dims)
        for key, r in json.loads(Path(path).read_text(encoding="utf-8")).items():
            memory.add(key, r["email"], r["label"], r["reason"])
        return memory
