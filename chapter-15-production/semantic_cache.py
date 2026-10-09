"""Semantic response cache, Chapter 15, section "Latency".

The linear scan is chosen for clarity: in production the index of
questions lives in one of the vector databases from Chapter 10.
"""

import math


class SemanticCache:
    """Response cache indexed by semantic similarity
    of the question."""
    def __init__(self, embed, threshold=0.92):
        self.embed = embed    # text -> normalized vector function
        self.threshold = threshold
        self.entries = []     # pairs (vector, response)

    def search(self, question):
        v = self.embed(question)
        best, score = None, 0.0
        for vector, response in self.entries:
            # cosine = dot product: vectors are normalized
            s = sum(a * b for a, b in zip(v, vector))
            if s > score:
                best, score = response, s
        return best if score >= self.threshold else None

    def save(self, question, response):
        self.entries.append((self.embed(question), response))


def demo_embed(text):
    """Toy bag-of-words embedding, normalized.
    It only makes the example runnable: in production embed
    is a real embedding model (Chapter 10)."""
    dimensions = 64
    v = [0.0] * dimensions
    for word in text.lower().split():
        v[hash(word) % dimensions] += 1.0
    norm = math.sqrt(sum(x * x for x in v)) or 1.0
    return [x / norm for x in v]


if __name__ == "__main__":
    cache = SemanticCache(demo_embed)
    cache.save("what are the store opening hours",
               "The store is open Monday to Saturday, 9am to 7pm.")

    # Same question with a different word order: hit.
    similar_question = "the store opening hours what are"
    print("similar question   ->", cache.search(similar_question))

    # Different question: below threshold, no response from the cache.
    different_question = "can I pay on delivery?"
    print("different question ->", cache.search(different_question))
