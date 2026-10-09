"""Chapter 17, listings "The shared state", "The graph nodes" and
"Building the graph": the full orchestration of the company assistant.

The rag, operational, ticketing and model modules are deterministic stubs
here (see the respective files): the book describes them as the projects
from chapters 11 and 12 injected from outside. The graph runs end to end
with the stubs, without an API key, as described in the section on the
architecture: this is the orchestration test run by orchestration_test.py.
"""

# Model constants, as in chapters 11 and 15:
# they are the part of the code that ages first.
MODEL_LARGE = "gemini-2.5-pro"
MODEL_SMALL = "gemini-2.5-flash"

from typing import Annotated, Optional
from typing_extensions import TypedDict
from operator import add

class State(TypedDict):
    request: str        # the employee's question
    user: str           # identity: drives permissions and traces
    category: str       # the router's verdict
    answer: str         # final text, with citations
    sources: list[str]  # identifiers of the cited chunks
    ticket_proposal: Optional[dict]  # draft awaiting approval
    action_result: str  # result of the confirmed action
    steps: Annotated[list[str], add]  # accumulating trace


# --- The graph nodes: each node calls a piece built ---
# --- in the previous chapters.                       ---
from langgraph.types import interrupt

import rag          # chapter 11 RAG pipeline (here: stub)
import operational  # chapter 12 agent loop (here: stub)
import ticketing    # ticketing MCP server client (here: stub)
import model        # injected interface to the models (here: stub)

ROUTER_PROMPT = """Classify an employee's request.
SIMPLE: document question about a fact or a procedure.
COMPLEX: document question across several sources or ambiguous cases.
ACTION: asks to open a ticket or for the status of an order.
OUT: everything else. When unsure between SIMPLE and COMPLEX
choose COMPLEX. Reply with a single word."""

COURTESY = ("I can help with company documents, "
            "tickets, and order status.")

def router_node(state: State):
    verdict = model.generate(MODEL_SMALL, ROUTER_PROMPT,
                             state["request"][:2000]).strip()
    out = {"category": verdict, "steps": [f"router -> {verdict}"]}
    if verdict == "OUT":   # standard courtesy answer
        out["answer"] = COURTESY
    return out

def search_node(state: State):
    m = (MODEL_SMALL if state["category"] == "SIMPLE"
         else MODEL_LARGE)
    text, excerpts = rag.answer(
        state["request"], user=state["user"], model=m)
    return {"answer": text,
            "sources": [c["id"] for c in excerpts],
            "steps": ["search"]}

def operational_node(state: State):
    result = operational.run(state["request"],
                             user=state["user"])
    if result.ticket_proposal:   # draft: needs confirmation
        return {"ticket_proposal": result.ticket_proposal,
                "steps": ["operational: proposal"]}
    return {"answer": result.text,   # read-only
            "steps": ["operational: read"]}

def confirm_node(state: State):
    ok = interrupt({"to_confirm": state["ticket_proposal"]})
    if ok != "yes":
        return {"action_result": "cancelled by the user",
                "steps": ["confirm: no"]}
    # The write happens HERE, after the interrupt and outside
    # the model's control (chapters 12 and 14).
    r = ticketing.open_ticket(**state["ticket_proposal"])
    return {"action_result": f"opened ticket {r['id']}",
            "steps": ["confirm: yes"]}


# --- Building the graph. ---
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver

def route(state: State) -> str:
    if state["category"] in ("SIMPLE", "COMPLEX"):
        return "search"
    if state["category"] == "ACTION":
        return "operational"
    return END    # OUT: the router already wrote the answer

def needs_confirmation(state: State) -> str:
    return "confirm" if state.get("ticket_proposal") else END

builder = StateGraph(State)
builder.add_node("router", router_node)
builder.add_node("search", search_node)
builder.add_node("operational", operational_node)
builder.add_node("confirm", confirm_node)

builder.add_edge(START, "router")
builder.add_conditional_edges("router", route)
builder.add_conditional_edges("operational", needs_confirmation)
builder.add_edge("search", END)
builder.add_edge("confirm", END)

saver = InMemorySaver()   # minimal addition for execution
graph = builder.compile(checkpointer=saver)
# saver: InMemorySaver in tests, Postgres in production,
# as in chapter 14; the thread_id is the conversation.
