"""Semantic search engine for Chapter 10.

Configuration and corpus (Listing 10.3), engine with indexing and exact
search using NumPy (Listing 10.4), evaluation set and recall measurement
(Listing 10.5).

Everything runs locally with sentence-transformers: on the first run the
model is downloaded from Hugging Face (an internet connection is required).
"""

from sentence_transformers import SentenceTransformer
import numpy as np

# Model names change over time: check the current catalog.
EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"

CORPUS = [
    {"id": "warranty-duration", "topic": "warranty", "text":
     "The warranty covers manufacturing defects for 24 months "
     "from the date of purchase."},
    {"id": "warranty-exclusions", "topic": "warranty", "text":
     "The warranty does not cover damage caused by improper use, "
     "impacts, contact with liquids, or unauthorized repairs."},
    {"id": "return", "topic": "warranty", "text":
     "You can exercise the right of withdrawal within 14 days of "
     "delivery, using the online form."},
    {"id": "power-on", "topic": "hardware", "text":
     "If the notebook shows no signs of life, disconnect the battery "
     "and the power adapter, wait a minute, and reconnect them."},
    {"id": "firmware-update", "topic": "software", "text":
     "To update the firmware, download the package from the "
     "manufacturer's website and follow the guided procedure."},
    {"id": "firmware-e4013", "topic": "software", "text":
     "Error E-4013 during the firmware update indicates a corrupted "
     "package: download the file again and retry."},
    {"id": "password", "topic": "account", "text":
     "To reset your password, use the 'recover credentials' link "
     "on the login page."},
    {"id": "support", "topic": "account", "text":
     "Phone support is available Monday to Friday, "
     "from 9 am to 6 pm."},
]


class SearchEngine:
    def __init__(self):
        self.model = SentenceTransformer(EMBEDDING_MODEL)
        self.chunks = []
        self.M = None          # matrix (n_chunks, 384)

    def index(self, documents):
        self.chunks = documents
        texts = [d["text"] for d in documents]
        # normalize_embeddings=True: dot product = cosine
        self.M = self.model.encode(
            texts, normalize_embeddings=True)

    def search(self, query, k=3):
        q = self.model.encode(
            query, normalize_embeddings=True)
        scores = self.M @ q              # one similarity per chunk
        best = np.argsort(-scores)[:k]
        return [(self.chunks[i]["id"], float(scores[i]))
                for i in best]


engine = SearchEngine()
engine.index(CORPUS)

TEST_CASES = [
    ("how long is the warranty?",            "warranty-duration"),
    ("the laptop won't turn on",             "power-on"),
    ("I forgot my credentials",              "password"),
    ("error E-4013",                         "firmware-e4013"),
    ("how do I return the product?",         "return"),
    ("does the warranty cover liquid damage?","warranty-exclusions"),
]


def recall_at_k(engine, test_cases, k):
    hits = 0
    for query, expected in test_cases:
        retrieved = [r[0] for r in engine.search(query, k=k)]
        if expected not in retrieved:
            print(f"MISSED @{k}: '{query}' -> {retrieved}")
        hits += int(expected in retrieved)
    return hits / len(test_cases)


if __name__ == "__main__":
    # A quick test, using the chapter's signature query.
    print(engine.search("the laptop won't turn on"))

    print("recall@1:", recall_at_k(engine, TEST_CASES, 1))
    print("recall@3:", recall_at_k(engine, TEST_CASES, 3))
