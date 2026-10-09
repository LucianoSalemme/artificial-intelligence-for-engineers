# Capstone project for chapter 4: explore an embedding space.
# It assembles listings 4.3-4.6 (lst:cap03_parole, lst:cap03_vicini,
# lst:cap03_frasi, lst:cap03_ricerca, lst:cap03_pca) in the order of the book.

# --- Listing 4.3: twelve words, three semantic fields ---
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer(
    "paraphrase-multilingual-MiniLM-L12-v2")

words = ["cat", "dog", "horse", "parrot",
         "car", "truck", "bicycle", "train",
         "bread", "cheese", "pasta", "wine"]

# normalize_embeddings=True: vectors rescaled to unit norm
V = model.encode(words, normalize_embeddings=True)
print(V.shape)   # (12, 384)

# --- Listing 4.4: the nearest neighbors of each word ---
S = V @ V.T   # 12 x 12 matrix of cosine similarities

for i, word in enumerate(words):
    order = np.argsort(-S[i])         # indices by decreasing similarity
    neighbors = [f"{words[j]} {S[i, j]:.2f}"
                 for j in order[1:4]]  # the first one is the word itself
    print(f"{word:12s} -> {neighbors}")

# --- Listing 4.5: sentence similarity, paraphrase vs intruder ---
sentences = [
    "The technician restarted the server after the update.",
    "After the update, the sysadmin brought the machine back up.",
    "Carbonara is made with guanciale, eggs, and pecorino.",
]
F = model.encode(sentences, normalize_embeddings=True)
print((F @ F.T).round(2))

# --- Listing 4.6: a miniature semantic search ---
documents = [
    "To reset your password, open the user panel.",
    "The contract renews automatically every twelve months.",
    "If it overheats, the device shuts down.",
    "The warranty covers manufacturing defects for two years.",
    "The app syncs with the cloud every fifteen minutes.",
]
D = model.encode(documents, normalize_embeddings=True)

query = "I forgot my login credentials"
q = model.encode(query, normalize_embeddings=True)

scores = D @ q                        # one similarity per document
for i in np.argsort(-scores):
    print(f"{scores[i]:.2f}  {documents[i]}")

# --- Listing 4.7: 2D projection of the space with PCA ---
from sklearn.decomposition import PCA

XY = PCA(n_components=2).fit_transform(V)
for (x, y), word in zip(XY, words):
    print(f"{word:12s} {x:6.2f} {y:6.2f}")
