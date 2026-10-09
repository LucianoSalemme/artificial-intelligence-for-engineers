# Chapter 4 - Tokens and Embeddings

Code for chapter 4 of the book "Artificial Intelligence for Engineers": BPE tokenization in practice, cosine similarity on toy vectors and on real embeddings, and the exploration of a semantic space with `sentence-transformers`.

## File

| File | Description |
|------|-------------|
| `count_tokens_tiktoken.py` | Counts and inspects the tokens of an English sentence and an Italian one with `tiktoken`. Listing 4.1, section "Tokens and costs". |
| `cosine_similarity_by_hand.py` | NumPy check of the by-hand cosine similarity calculation on three four-component vectors. Section "Cosine similarity in practice". |
| `first_real_embedding_measurement.py` | First similarity measurement on real embeddings with `sentence-transformers`. Listing 4.2. |
| `explore_embedding_space.py` | Exploration of an embedding space: nearest words, sentences, semantic search, and PCA projection. Listings 4.3-4.7, section "Code: exploring an embedding space". |

## How to run

Requires Python 3.12. Install the dependencies:

```bash
pip install numpy tiktoken sentence-transformers scikit-learn
```

Then run the individual scripts:

```bash
python3 count_tokens_tiktoken.py
python3 cosine_similarity_by_hand.py
python3 first_real_embedding_measurement.py
python3 explore_embedding_space.py
```

## Requirements

- No credentials or API keys.
- `cosine_similarity_by_hand.py` runs fully offline.
- `count_tokens_tiktoken.py` downloads the `cl100k_base` tokenizer data on first run (it needs an internet connection once, then it stays cached).
- `first_real_embedding_measurement.py` and `explore_embedding_space.py` download the `paraphrase-multilingual-MiniLM-L12-v2` model from Hugging Face on first run (about 470 MB, then cached locally); the model runs comfortably on CPU.

The printed numeric values may differ slightly from those reported in the book depending on the model version: the ranking of the similarities, as explained in the text, stays the same.
