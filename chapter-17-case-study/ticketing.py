"""Stub of the client to the ticketing MCP server: the in-memory client
from chapter 13. It delegates to the pure logic in ticket.py, so the key
idempotency is exercised in the test as well.
"""

import ticket


def open_ticket(category: str, summary: str, description: str,
                requester: str, key: str) -> dict:
    id_ = ticket.create(category, summary, description,
                        requester, key)
    return {"opened": True, "id": id_}
