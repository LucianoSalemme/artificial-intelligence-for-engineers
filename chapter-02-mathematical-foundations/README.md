# Chapter 2 - Mathematical Foundations

Code for the section "The tools: NumPy and PyTorch" of Chapter 2: the examples worked out by hand in the chapter (cosine similarity, matrix product, gradient descent, softmax and cross-entropy) translated into NumPy and PyTorch, so that every result can be checked line by line.

## File

| File | Description |
|------|-------------|
| `numpy_examples.py` | Dot product, norm and cosine similarity, matrix-vector product, broadcasting and three steps of gradient descent in NumPy. Subsections "Tensors, arrays and vectorized operations", "Broadcasting" and "Gradient descent in code". |
| `pytorch_examples.py` | Automatic gradient with autograd, softmax with temperature and cross-entropy in PyTorch. Subsection "PyTorch: tensors with the gradient built in". |

## How to run

```bash
pip install numpy torch

python3 numpy_examples.py
python3 pytorch_examples.py
```

## Dependencies

- Python 3.12
- `numpy` for `numpy_examples.py`
- `torch` for `pytorch_examples.py`

No credentials or external services: every script runs locally and prints the same numbers computed by hand in the chapter.
