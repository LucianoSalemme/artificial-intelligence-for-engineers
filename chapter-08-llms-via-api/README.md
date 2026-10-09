# Chapter 8 - Using LLMs via API

Code for the listings of chapter 8: calls to an LLM through the `google-genai` Python SDK (Gemini API), from the minimal call up to structured output, function calling, streaming, a robust client and multimodal input.

## Files

| File | Description |
|---|---|
| `minimal_call.py` | The minimal complete call to an LLM. Section "Anatomy of a call". |
| `stateless_conversation.py` | The dialogue history kept by the client. Section "You keep the conversation". |
| `history_truncation.py` | Function `truncate_history` with `count_tokens` to stay within the context window. Section "The context window as a resource". |
| `generation_parameters.py` | Configuration with temperature, top_p, max_output_tokens, stop_sequences and thinking_budget. Section "Generation parameters". |
| `order_extraction.py` | Structured output: Pydantic schema and constrained call, then retry with feedback, assembled into a single program. Section "Structured output". |
| `warehouse_assistant.py` | Function calling: function and declaration, then the invocation loop; it creates `warehouse.db` by itself with the chapter's sample data. Section "Function calling". |
| `streaming.py` | Streaming generation. Section "Streaming and robustness". |
| `robust_client.py` | Timeout, error classification and exponential backoff with jitter. Subsection "Failures, retries and backoff". |
| `pdf_invoice_extraction.py` | PDF as input, validated JSON as output and an arithmetic check downstream. Section "Multimodality". |

## How to run

Requirements: Python 3.12 and the packages

```bash
pip install google-genai pydantic
```

All scripts call the Gemini API and read the key from the `GEMINI_API_KEY` environment variable (free key at https://aistudio.google.com/apikey):

```bash
export GEMINI_API_KEY=<your-key>
python3 minimal_call.py
```

If the variable is missing, every script reports it and exits with code 1.

Notes:

- `warehouse_assistant.py` creates on first run the database `warehouse.db` with the sample item VLV-2041 (42 units in aisle B3), as in the chapter text.
- `pdf_invoice_extraction.py` requires a file `invoice_1042.pdf` in the current directory; without it, it stops with a message.
- To use Vertex AI instead of the Gemini API, build the client as shown in the comments: `genai.Client(vertexai=True, project="...", location="...")`.

## Dependencies

- `google-genai` (official Google SDK for Gemini)
- `pydantic` (schemas and validation in `order_extraction.py` and `pdf_invoice_extraction.py`)
