# Chapter 15 - LLMs in Production

Code for Chapter 15 of the book "Artificial Intelligence for Engineers": the three techniques shown in the chapter listings, with the logic separated from the calls and the dependencies injected, as in the text.

## Files

| File | Description |
|---|---|
| `semantic_cache.py` | The `SemanticCache` class, which indexes responses by semantic similarity of the question. Section "Latency". |
| `complexity_routing.py` | The model constants, the `ROUTER_PROMPT`, and the `route` function that dispatches requests between the small and large models. Section "Costs". |
| `fallback_chain.py` | The `FALLBACK_CHAIN` and the `generate_with_fallback` function that walks the steps up to the independent provider. Section "Reliability". |

`fallback_chain.py` imports the constants `LARGE_MODEL` and `SMALL_MODEL` from `complexity_routing.py`, as in the chapter, where the fallback listing reuses the names defined in the routing listing.

## How to run

Each file is self-contained and includes a demo block with stubs in place of the real calls (in the book the `embed`, `classify`, `generate`, `call`, and `record` functions are injected and in production talk to the LLM gateway):

```
python3 semantic_cache.py
python3 complexity_routing.py
python3 fallback_chain.py
```

## Dependencies

Python 3.12, no external libraries, no credentials: the examples use only the standard library and demo stubs.
