# Chapter 6 - The Transformer Architecture (mini-GPT)

Code for Chapter 6 of the book *Artificial Intelligence for Engineers*: a miniature GPT-2, complete and working, written in PyTorch component by component.

## File

| File | Description |
|------|-------------|
| `mini_gpt.py` | The complete mini-GPT: configuration (`GPTConfig`), causal multi-head attention (`CausalSelfAttention`), feed-forward and Transformer block (`MLP`, `Block`), model with weight tying (`MiniGPT`), forward pass with cross-entropy, autoregressive generation (`generate`), and the final smoke test. Mini-GPT parts 1-6, section "Writing a complete mini-GPT". |

The six listings in the book are parts of the same program and are assembled here into a single file, in the chapter's order. The smoke test (part 6) is wrapped in an `if __name__ == "__main__":` block. The listing with the execution output is not a code file and is not reproduced.

## How to run

```bash
pip install torch
python3 mini_gpt.py
```

Runs on any CPU, in a few seconds. The expected output (with the listing's seed 42):

```
parameters: 834304
initial loss: 5.5538   expected: 5.5452
[0, 95, 196, 49, 75, 157, 86, 79, 160]
[0, 216, 216, 216, 216, 216, 216, 216, 216]
```

The chapter's three checks: the parameter count, the initial loss close to ln(256) ≈ 5.5452 (the sanity check on the output head), and the two generations from the untrained model: random bytes with sampling, repetition of token 216 with greedy decoding (T = 0).

The exact generated token values can vary between PyTorch versions and platforms, for the reasons discussed in the chapter about floating-point nondeterminism.

## Requirements

- Python 3.12
- `torch` (PyTorch), the only external dependency
- No API credentials, no external service: everything runs locally
