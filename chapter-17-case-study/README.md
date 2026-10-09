# Chapter 17 - Case Study

The final chapter of the book assembles the pieces built in the previous
chapters into a company assistant: router, search agent (RAG), operational
agent with human confirmation, MCP server, evaluation.

The chapter code is the architectural "glue": the listings show the shared
state, the nodes, the LangGraph graph, the ticketing MCP server and the
eval harness. As the book says, the graph runs end to end with the stubs
(the FakeModel from chapter 14 and the in-memory client from chapter 13):
this is how it is meant to run here, without an API key.

## Files

| File | Description |
|------|-------------|
| `assistant.py` | The shared state, the nodes and the construction of the LangGraph graph, assembled in the order of the book. Listings "The shared state", "The graph nodes", "Building the graph". |
| `model.py`, `rag.py`, `operational.py`, `ticketing.py` | Deterministic stubs: in the book they are the chapter 11 and 12 projects injected from outside. |
| `ticket.py` | Pure ticketing logic, with the idempotency key described in the text. |
| `ticket_server.py` | MCP adapter on top of `ticket.py`. Listing "The ticketing MCP server, in brief". |
| `orchestration_test.py` | The orchestration test described in the text, with asserts on the `steps` trace. |
| `eval_harness.py` | The eval harness with a demonstrative golden set of 3 cases (60 in the book). Listing "The eval harness". |

## How to run

```bash
python orchestration_test.py   # the graph with the stubs, without an API key
python eval_harness.py         # the regression on the demo golden set
```

Both run offline. `ticket_server.py` requires the `mcp[cli]` package;
the import `from mcp.server import MCPServer` follows the book, and with
SDKs that still expose `FastMCP` it must be adapted (see the chapter 13
README).

## Requirements

- `langgraph` (and `typing_extensions`, installed with it)
- `mcp[cli]` only for `ticket_server.py`
