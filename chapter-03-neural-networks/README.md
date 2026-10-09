# Chapter 3 - Neural Networks

Code for chapter 3 of *Artificial Intelligence for Engineers*: the dense 2-3-1 network (two inputs, three sigmoid hidden neurons, one sigmoid output) on which the chapter works out the forward pass and backpropagation by hand, and its full training on the XOR function.

## Files

| File | Description |
|------|-------------|
| `backpropagation_by_hand.py` | Builds the 2-3-1 network with the weights of the by-hand example, runs the forward pass and prints the output, the loss and the gradients `dL/dv1` and `dL/dw11`, identical to those computed on paper. Section "The training loop in PyTorch". |
| `train_xor.py` | Trains the 2-3-1 network with `nn.Sequential`, `BCELoss` and `SGD` on the four cases of XOR for 10,000 epochs, printing the loss and the final responses. Section "The training loop in PyTorch". |

The two console-output-only listings reported in the chapter are not files: they show the expected result of running these scripts.

## How to run

```bash
pip install torch
python3 backpropagation_by_hand.py
python3 train_xor.py
```

Expected output of the first script:

```
y = 0.5998   L = 0.0801
dL/dv1  = -0.0552
dL/dw11 = -0.0141
```

The second script brings the loss from about 0.69 down to about 0.001 and responds `0.001` / `0.999` on the four cases of XOR (the exact values depend on the initialization; the fixed seed makes them reproducible).

## Dependencies

- Python 3.12
- PyTorch (`pip install torch`)

No credentials or external services: both scripts run entirely locally on CPU.
