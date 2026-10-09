"""Scaled dot-product attention from scratch in PyTorch.

Reproduces, digit for digit, the numerical example from Chapter 5 on the
sentence "the cat sleeps": query/key/value projections, scores, softmax,
weighted average, and the causal variant.
"""

import math

import torch

# --- Listing 5.1: the sentence embeddings and the Q, K, V projections ---

# embeddings of the sentence "the cat sleeps", one token per row
X = torch.tensor([[1.,  0.],
                  [0.,  1.],
                  [1., -1.]])

# the three projection matrices from the worked-by-hand example
W_Q = torch.tensor([[1., 0.], [1., 1.]])
W_K = torch.tensor([[0., 1.], [1., 1.]])
W_V = torch.tensor([[1., 1.], [1., 0.]])

Q = X @ W_Q.T    # row i = W_Q x_i
K = X @ W_K.T
V = X @ W_V.T
print(Q, K, V, sep="\n")

# --- Listing 5.2: scaled dot-product attention in four lines ---

d_k = Q.shape[-1]                 # key dimension: 2
S = Q @ K.T / math.sqrt(d_k)      # rescaled scores, 3x3
A = torch.softmax(S, dim=-1)      # one distribution per row
Z = A @ V                         # weighted averages of the values
print(A)
print(Z)

# --- Listing 5.3: the complete function, with optional causal mask ---


def attention(Q, K, V, causal=False):
    """Scaled dot-product attention; if causal=True
    each token sees only itself and the ones before it."""
    d_k = Q.shape[-1]
    S = Q @ K.transpose(-2, -1) / math.sqrt(d_k)
    if causal:
        n = S.shape[-1]
        # True above the diagonal: the future positions
        future = torch.triu(torch.ones(n, n, dtype=torch.bool),
                            diagonal=1)
        S = S.masked_fill(future, float("-inf"))
    A = torch.softmax(S, dim=-1)
    return A @ V, A


# --- Listing 5.4: checking causal attention on the worked example ---

Z_c, A_c = attention(Q, K, V, causal=True)
print(A_c)
print(Z_c)
