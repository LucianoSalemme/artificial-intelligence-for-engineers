# Chapter 14, "Code: supervisor and specialists" section: a supervisor
# that coordinates two specialists (analyst and writer) on a LangGraph
# graph with a typed shared state and checkpointing. Model calls go
# through a single interface, with the real implementation on Vertex AI
# (VertexModel). Requires GEMINI_API_KEY or GOOGLE_API_KEY.
# pip install langgraph google-genai
import os
import sys
from typing import Annotated
from typing_extensions import TypedDict
from operator import add

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver

MODEL = "gemini-2.5-flash"

class VertexModel:
    """Real implementation: Gemini via google-genai,
    as in chapter 8."""
    def __init__(self):
        if not (os.environ.get("GEMINI_API_KEY")
                or os.environ.get("GOOGLE_API_KEY")):
            print("The GEMINI_API_KEY variable is missing: create an "
                  "API key at https://aistudio.google.com/apikey and "
                  "set it with: export GEMINI_API_KEY=<key>")
            sys.exit(1)
        from google import genai
        # on Vertex AI: genai.Client(vertexai=True,
        #   project="...", location="...")
        self.client = genai.Client()

    def generate(self, prompt: str) -> str:
        r = self.client.models.generate_content(
            model=MODEL, contents=prompt)
        return r.text

model = VertexModel()

class State(TypedDict):
    request: str      # the user's task
    analysis: str     # the analyst's output
    draft: str        # the writer's output
    next_agent: str   # the supervisor's decision
    delegation: str   # the instruction for the specialist
    steps: Annotated[list[str], add]  # trace

def supervisor_node(state: State):
    # The supervisor gets a snapshot of the state,
    # not the full contents.
    analysis = "ready" if state["analysis"] else "missing"
    draft = "ready" if state["draft"] else "missing"
    prompt = (
        "You are the supervisor of a team of agents.\n"
        "Available specialists:\n"
        "- analyst: gathers and summarizes the facts\n"
        "- writer: writes the final text\n"
        f"Task: {state['request']}\n"
        "Work status:\n"
        f"- analysis: {analysis}\n"
        f"- draft: {draft}\n"
        "Reply with the name of the specialist to activate "
        "and, on a new line, the instruction for it; or DONE.")
    lines = model.generate(prompt).strip().splitlines()
    next_agent = lines[0].strip().lower()
    delegation = "\n".join(lines[1:]).strip()
    return {"next_agent": next_agent, "delegation": delegation,
            "steps": [f"supervisor -> {next_agent}"]}

def analyst_node(state: State):
    prompt = ("You are the analyst. Supervisor's instruction: "
              f"{state['delegation']}\n"
              f"Overall task: {state['request']}")
    return {"analysis": model.generate(prompt),
            "steps": ["analyst"]}

def writer_node(state: State):
    prompt = ("You are the writer. Supervisor's instruction: "
              f"{state['delegation']}\n"
              f"Available analysis:\n{state['analysis']}")
    return {"draft": model.generate(prompt),
            "steps": ["writer"]}

def route(state: State) -> str:
    """Conditional edge: from the supervisor to the chosen
    specialist, or to the end."""
    if state["next_agent"] == "done":
        return END
    return state["next_agent"]

builder = StateGraph(State)
builder.add_node("supervisor", supervisor_node)
builder.add_node("analyst", analyst_node)
builder.add_node("writer", writer_node)

builder.add_edge(START, "supervisor")
builder.add_conditional_edges("supervisor", route)
builder.add_edge("analyst", "supervisor")
builder.add_edge("writer", "supervisor")

graph = builder.compile(checkpointer=InMemorySaver())

config = {"configurable": {"thread_id": "note-2026-081"}}
final = graph.invoke(
    {"request": ("a summary note on multi-agent "
                 "systems for the technical committee"),
     "analysis": "", "draft": "",
     "next_agent": "", "delegation": "", "steps": []},
    config)

print("Trace:", " | ".join(final["steps"]))
print("Final draft:", final["draft"])
