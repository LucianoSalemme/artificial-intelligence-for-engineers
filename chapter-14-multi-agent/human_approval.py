# Chapter 14, "Human-in-the-loop" section: suspending the graph with
# interrupt() and resuming with Command(resume=...) on the same thread_id.
# The "approval" node and the two invocations are the book listing;
# the State and the graph built around the node are the minimum
# needed to make it runnable. Runs without an API key.
# pip install langgraph
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt, Command

class State(TypedDict):
    summary: str
    outcome: str

def approval(state):
    """Approval node: suspends the graph before
    the irreversible action."""
    verdict = interrupt({
        "question": "Confirm the international shipment?",
        "summary": state["summary"],
    })
    if verdict != "yes":
        return {"outcome": "cancelled by the operator"}
    return {"outcome": "approved"}

builder = StateGraph(State)
builder.add_node("approval", approval)
builder.add_edge(START, "approval")
builder.add_edge("approval", END)
graph = builder.compile(checkpointer=InMemorySaver())

# First invocation: the graph reaches the approval node,
# suspends, and returns the payload.
config = {"configurable": {"thread_id": "order-7"}}
suspended = graph.invoke({"summary": "..."}, config)
print("Graph suspended. Interrupt payload:",
      suspended["__interrupt__"][0].value)

# Hours later, possibly from another process: the operator's
# reply resumes execution from the checkpoint.
final = graph.invoke(Command(resume="yes"), config)
print("Outcome:", final["outcome"])
