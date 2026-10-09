"""NumPy examples from Chapter 2 (Mathematical Foundations).

Reproduces in code the calculations worked out by hand in the chapter:
cosine similarity, matrix-vector product, broadcasting and gradient
descent. The three listings from the section "The tools: NumPy and
PyTorch" form a single session and are assembled here in the book's
order.
"""

import numpy as np

# ------------------------------------------------------------------
# Listing 1: tensors, arrays and vectorized operations
# ------------------------------------------------------------------

# The three documents from the worked example:
# word counts (antenna, transistor, recipe)
d1 = np.array([3.0, 2.0, 0.0])
d2 = np.array([2.0, 3.0, 0.0])
d3 = np.array([0.0, 0.0, 4.0])

print(np.dot(d1, d2))        # 12.0
print(np.linalg.norm(d1))    # 3.605551... = square root of 13

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

print(cosine_similarity(d1, d2))      # 0.9230769...
print(cosine_similarity(d1, d3))      # 0.0
print(cosine_similarity(2 * d1, d2))  # 0.9230769...: scale is irrelevant

# ------------------------------------------------------------------
# Listing 2: broadcasting
# ------------------------------------------------------------------

# Matrix-vector product from the worked example
W = np.array([[ 1.0, 0.0, 2.0],
              [-1.0, 3.0, 1.0]])
x = np.array([2.0, 1.0, 0.5])
print(W @ x)          # [3.  1.5]: one dot product per row

# Broadcasting: centering the columns of a matrix
X = np.array([[1.0, 2.0],
              [3.0, 4.0],
              [5.0, 6.0]])
m = X.mean(axis=0)    # mean of each column: [3. 4.]
print(X - m)          # the row m is subtracted from every row of X

# ------------------------------------------------------------------
# Listing 3: gradient descent in code
# ------------------------------------------------------------------

def gradient(p):
    x, y = p
    return np.array([2 * x, 8 * y])  # gradient of x^2 + 4y^2

p = np.array([4.0, 2.0])             # starting point
eta = 0.1                            # learning rate
for k in range(3):
    p = p - eta * gradient(p)        # update rule
    f = p[0]**2 + 4 * p[1]**2
    print(k + 1, p, round(f, 6))

# 1 [3.2 0.4] 10.88
# 2 [2.56 0.08] 6.5792
# 3 [2.048 0.016] 4.195328
