# Section "Cosine similarity in practice": code check of the by-hand calculation.
import numpy as np

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

cat = np.array([0.8, 0.6, 0.1, 0.1])
dog = np.array([0.7, 0.7, 0.2, 0.1])
car = np.array([0.1, 0.2, 0.9, 0.7])

print(cosine_similarity(cat, dog))   # 0.9853...
print(cosine_similarity(cat, car))   # 0.3067...
print(cosine_similarity(dog, car))   # 0.3900...
