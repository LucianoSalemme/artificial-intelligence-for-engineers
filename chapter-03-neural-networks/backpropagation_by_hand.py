"""PyTorch check of the calculations worked out by hand on the 2-3-1 network.

It builds the network with exactly the weights of the by-hand example from
chapter 3, runs the forward pass and asks PyTorch for the gradients,
which match digit for digit those from the backpropagation on paper.
"""

import torch

# weights and biases identical to the by-hand example
W = torch.tensor([[ 0.3, -0.2],
                  [ 0.5,  0.4],
                  [-0.4,  0.6]], requires_grad=True)
b = torch.tensor([ 0.1, -0.3,  0.2], requires_grad=True)
v = torch.tensor([ 0.6, -0.1,  0.8], requires_grad=True)
c = torch.tensor([-0.3], requires_grad=True)

x = torch.tensor([1.0, 0.5])   # input
t = torch.tensor([1.0])        # correct answer (target)

h = torch.sigmoid(W @ x + b)   # hidden layer
y = torch.sigmoid(v @ h + c)   # output layer
L = 0.5 * (y - t)**2           # squared-error loss

L.backward()                   # automatic backpropagation

print(f"y = {y.item():.4f}   L = {L.item():.4f}")
print(f"dL/dv1  = {v.grad[0].item():.4f}")
print(f"dL/dw11 = {W.grad[0, 0].item():.4f}")
