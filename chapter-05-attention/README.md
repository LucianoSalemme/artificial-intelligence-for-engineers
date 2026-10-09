# Chapter 5 - The Attention Mechanism

Code for Chapter 5 of *Artificial Intelligence for Engineers*: scaled dot-product attention implemented from scratch in PyTorch, reproducing digit for digit the numerical example worked by hand in the chapter on the sentence "the cat sleeps".

## File

| File | Description |
|------|-------------|
| `attention_from_scratch.py` | Embeddings and Q, K, V projections, scaled dot-product attention, and the `attention` function with an optional causal mask, verified against the worked-by-hand example. Listings 5.1-5.4, section "Implementation from scratch in PyTorch". |

The chapter's four listings are parts of the same program and are assembled into a single file, in the order in which they appear in the book. The console-output-only listings are not reproduced: they are what the script prints.

## How to run

```bash
pip install torch
python3 attention_from_scratch.py
```

The script prints, in order: the Q, K, and V matrices; the attention weight matrix and the outputs Z of bidirectional attention; the weight matrix and outputs of the causal variant. The values match those computed by hand in the chapter (for example the weights of "sleeps": 0.2840, 0.5760, 0.1400).

## Dependencies

- Python 3.12
- `torch` (PyTorch)

No API key or external service: everything runs locally on CPU.
