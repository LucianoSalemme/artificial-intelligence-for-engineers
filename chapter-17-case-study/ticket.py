"""Pure ticketing logic, without protocol: create() and status(),
testable with ordinary unit tests (the chapter 13 method).

The idempotency key does what chapter 17 describes: if a gateway retry
or a graph resume delivers the call twice, create() recognizes the key
already seen and returns the existing ticket instead of duplicating it.
"""

_tickets: dict[str, dict] = {}    # id -> data
_by_key: dict[str, str] = {}      # idempotency key -> id


def create(category: str, summary: str, description: str,
           requester: str, key: str) -> str:
    if key in _by_key:            # request already seen
        return _by_key[key]
    id_ = f"TCK-{1000 + len(_tickets) + 1}"
    _tickets[id_] = {"status": "open", "assignee": None,
                     "category": category, "summary": summary,
                     "description": description,
                     "requester": requester}
    _by_key[key] = id_
    return id_


def status(id: str):
    data = _tickets.get(id)
    if data is None:
        return None
    return {"status": data["status"],
            "assignee": data["assignee"]}
