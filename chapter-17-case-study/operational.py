"""Stub of the chapter 12 operational agent: no model, scripted results.
If the request mentions a ticket it produces a structured proposal (that
the graph submits for human confirmation); otherwise it answers read-only
about the status of an order.

In the real system this module is the chapter 12 loop
(code/chapter-12-agents/agent_from_scratch.py) equipped with the tools
of the two MCP servers.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Result:
    text: str = ""
    ticket_proposal: Optional[dict] = None


def run(request: str, user: str) -> Result:
    if "ticket" in request.lower():
        return Result(ticket_proposal={
            "category": "IT",
            "summary": "Broken monitor",
            "description": request,
            "requester": user,
            "key": f"{user}-demo-1",   # idempotency (ch. 15)
        })
    return Result(text="Order ORD-1042 shows as shipped, "
                       "updated 2026-08-02. (stub)")
