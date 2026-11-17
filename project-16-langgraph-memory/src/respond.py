"""The respond branch: a tool-calling agent that drafts a reply and books meetings. Nothing is actually sent."""
from __future__ import annotations

import os
import re

from langchain_core.tools import tool

SLOTS = {"monday": ["10:00 AM", "2:00 PM"], "tuesday": ["9:00 AM", "1:00 PM"], "wednesday": ["11:00 AM", "3:00 PM"],
         "thursday": ["10:00 AM", "4:00 PM"], "friday": ["9:30 AM", "1:30 PM"]}


def make_tools(log: list):
    @tool
    def check_calendar_availability(day: str) -> str:
        """List Gurveer's free time slots on a weekday (monday to friday)."""
        slots = SLOTS.get(day.strip().lower(), [])
        log.append({"tool": "check_calendar_availability", "day": day, "result": slots})
        return f"Free on {day}: {', '.join(slots)}" if slots else f"No free slots found for {day}."

    @tool
    def schedule_meeting(attendees: list[str], subject: str, duration_minutes: int, day: str, time: str) -> str:
        """Put a meeting on Gurveer's calendar."""
        log.append({"tool": "schedule_meeting", "attendees": attendees, "subject": subject,
                    "duration_minutes": duration_minutes, "day": day, "time": time})
        return f"Scheduled '{subject}' on {day} at {time} for {duration_minutes} minutes."

    @tool
    def write_email(to: str, subject: str, content: str) -> str:
        """Save a draft reply for Gurveer to review. Drafts are not sent automatically."""
        log.append({"tool": "write_email", "to": to, "subject": subject, "content": content})
        return "Draft saved for review."

    return [check_calendar_availability, schedule_meeting, write_email]


SYSTEM = ("You are Gurveer's email assistant. Draft a short, polite reply to the email with write_email. "
          "If it asks to meet or pick a time, check his calendar first and propose real free slots; book a meeting only "
          "if a specific time is already agreed. Never invent facts about Gurveer.")


def make_responder(llm):
    """Returns email -> {"tool_calls": [...], "final": str}. `llm` is a LangChain chat model with tool calling."""
    from langgraph.prebuilt import create_react_agent

    def respond(email: dict) -> dict:
        log: list = []
        agent = create_react_agent(llm, make_tools(log), prompt=SYSTEM)
        text = f"From: {email['author']}\nSubject: {email['subject']}\n\n{email['body']}"
        result = agent.invoke({"messages": [{"role": "user", "content": text}]}, {"recursion_limit": 12})
        final = re.sub(r"<think>.*?</think>", "", result["messages"][-1].content or "", flags=re.S).strip()
        return {"tool_calls": log, "final": final}
    return respond


def lmstudio_llm(max_tokens: int = 800):
    from langchain_openai import ChatOpenAI

    return ChatOpenAI(model=os.getenv("LLM_MODEL", "gpt-4o-mini"), temperature=0,
                      max_tokens=max_tokens + int(os.getenv("LLM_REASONING_TOKENS", "0")))
