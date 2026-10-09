"""The two tool declarations side by side: a tool
is an API whose user reads it but does not try it.

Chapter 12, section "Tool design".
"""

import json

# BAD: the model has to guess everything
BAD_DECLARATION = {
    "name": "query",
    "description": "runs a query over the orders",
    "parameters": {
        "type": "object",
        "properties": {
            "q": {"type": "string"}},
        "required": ["q"]}}

# GOOD: intent, constraints and examples in the declaration
GOOD_DECLARATION = {
    "name": "search_orders",
    "description": (
        "Search purchase orders by status and age. "
        "Use it for questions about open, blocked or "
        "overdue orders. It does not return archived orders: "
        "for those use search_archive."),
    "parameters": {
        "type": "object",
        "properties": {
            "status": {
                "type": "string",
                "enum": ["open", "blocked", "fulfilled"],
                "description": "order status"},
            "min_days": {
                "type": "integer",
                "description": ("minimum age in days of the "
                                "current status, e.g. 7")}},
        "required": ["status"]}}


if __name__ == "__main__":
    print("# BAD: the model has to guess everything")
    print(json.dumps(BAD_DECLARATION, indent=2, ensure_ascii=False))
    print()
    print("# GOOD: intent, constraints and examples in the declaration")
    print(json.dumps(GOOD_DECLARATION, indent=2, ensure_ascii=False))
