# Chapter 14, "LangGraph" section: a minimal graph with deterministic
# stub nodes, a conditional edge, a reducer, and a checkpointer.
# Runs without an API key.
# pip install langgraph
from typing import Annotated
from typing_extensions import TypedDict
from operator import add

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver

class State(TypedDict):
    request: str
    urgent: bool
    steps: Annotated[list[str], add]  # reducer: accumulate

def classify(state: State):
    """Deterministic stub node: in a real system there would
    be a model call here."""
    urgent = "urgent" in state["request"].lower()
    return {"urgent": urgent, "steps": ["classify"]}

def fast_handling(state: State):
    return {"steps": ["fast_handling"]}

def standard_handling(state: State):
    return {"steps": ["standard_handling"]}

def route(state: State) -> str:
    """Conditional edge routing: returns the name of
    the next node."""
    if state["urgent"]:
        return "fast_handling"
    return "standard_handling"

builder = StateGraph(State)
builder.add_node("classify", classify)
builder.add_node("fast_handling", fast_handling)
builder.add_node("standard_handling", standard_handling)

builder.add_edge(START, "classify")
builder.add_conditional_edges("classify", route)
builder.add_edge("fast_handling", END)
builder.add_edge("standard_handling", END)

graph = builder.compile(checkpointer=InMemorySaver())

config = {"configurable": {"thread_id": "case-42"}}
final = graph.invoke(
    {"request": "URGENT: the site is down", "steps": []},
    config)
print(final["steps"])  # ['classify', 'fast_handling']
