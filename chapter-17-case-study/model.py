"""Deterministic stub of the interface to the models: the FakeModel from
chapter 14. No network call, scripted verdicts, so the graph runs in
continuous integration without an API key.

In production its place is taken by the adapter to Vertex AI behind the
chapter 15 gateway, injected with the same generate() interface.
"""


def generate(model_name: str, prompt: str, text: str) -> str:
    """Convenience router: classifies with a few keywords."""
    t = text.lower()
    if "ticket" in t or "order" in t or "orders" in t:
        return "ACTION"
    if any(p in t for p in ("reimbursement", "procedure", "manual",
                            "circular", "leave", "error")):
        return "SIMPLE"
    if any(p in t for p in ("compare", "difference", "which rule")):
        return "COMPLEX"
    return "OUT"
