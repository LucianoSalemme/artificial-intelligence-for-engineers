"""PyTorch examples from Chapter 2 (Mathematical Foundations).

Reproduces in code the worked examples: the gradient computed with
autograd, softmax with temperature and cross-entropy. The two listings
from the section "PyTorch: tensors with the gradient built in" form a
single session and are assembled here in the book's order.
"""

import torch
import torch.nn.functional as F

# ------------------------------------------------------------------
# Listing 4: autograd, the gradient computed automatically
# ------------------------------------------------------------------

p = torch.tensor([4.0, 2.0], requires_grad=True)
f = p[0]**2 + 4 * p[1]**2   # f(4, 2) = 32
f.backward()                # gradient computed automatically
print(p.grad)               # tensor([ 8., 16.])

# ------------------------------------------------------------------
# Listing 5: softmax, temperature and cross-entropy
# ------------------------------------------------------------------

z = torch.tensor([2.0, 1.0, 0.5, -1.0])   # the four logits

p = torch.softmax(z, dim=0)
print(p)  # tensor([0.6095, 0.2242, 0.1360, 0.0303])

# Effect of temperature on the logits
print(torch.softmax(z / 0.5, dim=0))  # T=0.5: concentrated distribution
print(torch.softmax(z / 2.0, dim=0))  # T=2:   flattened distribution

# Cross-entropy: the correct token has index 1
target = torch.tensor([1])
print(F.cross_entropy(z.unsqueeze(0), target))  # tensor(1.4952)
