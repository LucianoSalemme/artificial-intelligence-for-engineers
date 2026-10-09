"""Full training loop of the 2-3-1 network on the XOR function.

The dense 2-3-1 network from chapter 3, built with PyTorch modules,
is trained on the four cases of the XOR function: the
non-linearly-separable problem that a single perceptron cannot solve.
"""

import torch
from torch import nn

# toy dataset: the four cases of the XOR function
X = torch.tensor([[0., 0.], [0., 1.], [1., 0.], [1., 1.]])
T = torch.tensor([[0.], [1.], [1.], [0.]])

torch.manual_seed(0)   # reproducible initialization

# the same 2-3-1 architecture as the by-hand example
model = nn.Sequential(
    nn.Linear(2, 3),   # hidden layer: W and b
    nn.Sigmoid(),
    nn.Linear(3, 1),   # output layer: v and c
    nn.Sigmoid()
)

loss_fn = nn.BCELoss()   # binary cross-entropy
optimizer = torch.optim.SGD(model.parameters(), lr=1.0)

for epoch in range(10001):
    y = model(X)                 # 1. forward pass over the 4 examples
    L = loss_fn(y, T)            # 2. compute the mean loss
    optimizer.zero_grad()        # 3. zero out the previous gradients
    L.backward()                 # 4. backpropagation
    optimizer.step()             # 5. update the parameters
    if epoch % 2000 == 0:
        print(f"epoch {epoch:5d}   loss {L.item():.4f}")

# responses of the trained network
print(model(X).detach().numpy().round(3))
