# Chapter 10 - Semantic Search and Vector Databases

Code for the chapter's final project: a complete, measurable semantic search engine, from exact scanning with NumPy to moving onto Qdrant.

## File

| File | Description |
|---|---|
| `semantic_search_engine.py` | Corpus of eight chunks, `SearchEngine` class with indexing and exact search via NumPy, evaluation set `TEST_CASES` and `recall_at_k` function; the main runs the query "the laptop won't turn on" and prints recall@1 and recall@3. Listings 10.3-10.5. |
| `qdrant_engine.py` | The same engine moved to Qdrant in `:memory:` mode, with upsert of the vectors and a query filtered on the `topic` metadata; imports the already indexed engine from the previous file. Listing 10.6. |

Listings 10.1 and 10.2 (fixed-size splitting and structural splitting) are illustrative chunking examples, not code, and do not appear here.

## How to run

```bash
pip install sentence-transformers numpy qdrant-client

python3 semantic_search_engine.py
python3 qdrant_engine.py
```

## Requirements

- Python 3.12.
- No credentials or API keys: everything runs locally.
- On the first run, `sentence-transformers` downloads the `paraphrase-multilingual-MiniLM-L12-v2` model from Hugging Face (an internet connection is needed once; after that it stays cached).
- Qdrant runs in memory inside the process: no server to install. For a real instance, replace `":memory:"` with the service URL.
