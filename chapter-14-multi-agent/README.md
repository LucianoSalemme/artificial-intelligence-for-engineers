# Chapter 14 - Multi-Agent Systems

Code for chapter 14 of "Artificial Intelligence for Engineers": orchestrating multiple agents with LangGraph, human-in-the-loop with checkpoints, and the final supervisor + specialists project.

## Files

| File | Description |
|---|---|
| `minimal_graph.py` | Minimal graph with deterministic stub nodes: typed state with a reducer, a conditional edge, an in-memory checkpointer. Section "LangGraph". |
| `human_approval.py` | Approval node that suspends the graph with `interrupt()` and resumes with `Command(resume=...)`; the prints show the interrupt payload and the outcome. Section "Human-in-the-loop". |
| `supervisor_specialists.py` | The chapter project: a supervisor that delegates to an analyst and a writer on a LangGraph graph with checkpoints, with model calls behind a single interface and the real implementation `VertexModel` (Gemini via `google-genai`). Section "Code: supervisor and specialists". |
| `agent-card.json` | The example A2A agent card, which the protocol publishes at `/.well-known/agent-card.json`. Section "Communication between agents". |

The listing with the expected execution output (end of chapter) is console output and was not turned into a file.

## How to run

```bash
pip install langgraph google-genai

python3 minimal_graph.py           # without an API key
python3 human_approval.py          # without an API key
export GEMINI_API_KEY=<key>        # from https://aistudio.google.com/apikey
python3 supervisor_specialists.py
```

`minimal_graph.py` and `human_approval.py` run locally without an API key
(they use deterministic stub nodes). `supervisor_specialists.py` calls Gemini
through `VertexModel`: if the key is missing, the script reports it and exits
with code 1. Alternatively, on Vertex AI, use
`genai.Client(vertexai=True, project="...", location="...")` as shown in the
comment in the code.

## Dependencies

- Python 3.12
- `langgraph` (all scripts)
- `typing_extensions` (installed automatically with `langgraph`)
- `google-genai` and `GEMINI_API_KEY` (only for `supervisor_specialists.py`)
