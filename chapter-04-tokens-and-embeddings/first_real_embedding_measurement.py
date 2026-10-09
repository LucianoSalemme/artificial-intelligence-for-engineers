# Listing 4.2 (lst:cap03_prima_misura): first measurement on real embeddings.
# pip install sentence-transformers
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer(
    "paraphrase-multilingual-MiniLM-L12-v2")

vectors = model.encode(["cat", "dog", "car"])
print(vectors.shape)   # (3, 384): three vectors with 384 components

print(util.cos_sim(vectors, vectors))
