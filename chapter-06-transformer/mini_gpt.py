"""Mini-GPT: a complete decoder-only Transformer implementation.

Code for Chapter 6 (The Transformer Architecture), assembled from the six
listings in the book: configuration, attention, block, model,
generation, smoke test.
"""

import math
import torch
from torch import nn
from torch.nn import functional as F
from dataclasses import dataclass


# --- Part 1: configuration -----------------------------------------

@dataclass
class GPTConfig:
    vocab_size: int = 50257   # vocabulary size
    block_size: int = 1024    # maximum context length
    n_layer:    int = 12      # number of stacked blocks
    n_head:     int = 12      # attention heads per block
    n_embd:     int = 768     # hidden state size
    dropout:    float = 0.1   # dropout fraction


# --- Part 2: causal multi-head attention ----------------------------

class CausalSelfAttention(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        assert cfg.n_embd % cfg.n_head == 0
        # a single projection produces Q, K, and V concatenated
        self.qkv  = nn.Linear(cfg.n_embd, 3 * cfg.n_embd)
        self.proj = nn.Linear(cfg.n_embd, cfg.n_embd)
        self.n_head = cfg.n_head
        self.drop = nn.Dropout(cfg.dropout)
        # triangular causal mask, created once
        m = torch.tril(torch.ones(cfg.block_size, cfg.block_size))
        self.register_buffer(
            "mask", m.view(1, 1, cfg.block_size, cfg.block_size))

    def forward(self, x):
        B, T, C = x.shape          # batch, tokens, channels
        q, k, v = self.qkv(x).split(C, dim=2)
        # from (B, T, C) to (B, heads, T, C // heads)
        q = q.view(B, T, self.n_head, C // self.n_head).transpose(1, 2)
        k = k.view(B, T, self.n_head, C // self.n_head).transpose(1, 2)
        v = v.view(B, T, self.n_head, C // self.n_head).transpose(1, 2)
        # scaled dot-product attention with causal mask
        att = (q @ k.transpose(-2, -1)) / math.sqrt(k.size(-1))
        att = att.masked_fill(
            self.mask[:, :, :T, :T] == 0, float("-inf"))
        att = F.softmax(att, dim=-1)
        y = self.drop(att) @ v
        y = y.transpose(1, 2).contiguous().view(B, T, C)
        return self.proj(y)


# --- Part 3: feed-forward and Transformer block ---------------------

class MLP(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        # expand to 4x, nonlinearity, compress back
        self.fc   = nn.Linear(cfg.n_embd, 4 * cfg.n_embd)
        self.proj = nn.Linear(4 * cfg.n_embd, cfg.n_embd)
        self.drop = nn.Dropout(cfg.dropout)

    def forward(self, x):
        return self.drop(self.proj(F.gelu(self.fc(x))))


class Block(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        self.ln1 = nn.LayerNorm(cfg.n_embd)
        self.att = CausalSelfAttention(cfg)
        self.ln2 = nn.LayerNorm(cfg.n_embd)
        self.mlp = MLP(cfg)

    def forward(self, x):
        x = x + self.att(self.ln1(x))   # communication between tokens
        x = x + self.mlp(self.ln2(x))   # per-token processing
        return x


# --- Part 4: the full model ------------------------------------------

class MiniGPT(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        self.cfg = cfg
        self.wte = nn.Embedding(cfg.vocab_size, cfg.n_embd)
        self.wpe = nn.Embedding(cfg.block_size, cfg.n_embd)
        self.drop = nn.Dropout(cfg.dropout)
        self.blocks = nn.ModuleList(
            Block(cfg) for _ in range(cfg.n_layer))
        self.ln_f = nn.LayerNorm(cfg.n_embd)
        self.head = nn.Linear(cfg.n_embd, cfg.vocab_size, bias=False)
        self.head.weight = self.wte.weight   # weight tying
        self.apply(self._init_weights)

    def _init_weights(self, module):
        # GPT-2 style initialization: small Gaussian weights
        if isinstance(module, (nn.Linear, nn.Embedding)):
            nn.init.normal_(module.weight, mean=0.0, std=0.02)
            if isinstance(module, nn.Linear) and module.bias is not None:
                nn.init.zeros_(module.bias)

    # --- Part 5: forward pass and generation -------------------------

    def forward(self, idx, target=None):
        B, T = idx.shape
        pos = torch.arange(T, device=idx.device)
        # token embeddings + position embeddings
        x = self.drop(self.wte(idx) + self.wpe(pos))
        for block in self.blocks:
            x = block(x)
        x = self.ln_f(x)
        logits = self.head(x)     # (B, T, vocab_size)
        loss = None
        if target is not None:
            # cross-entropy over all positions at once
            loss = F.cross_entropy(
                logits.view(-1, logits.size(-1)), target.view(-1))
        return logits, loss

    @torch.no_grad()
    def generate(self, idx, max_new_tokens, temperature=1.0, top_k=None):
        for _ in range(max_new_tokens):
            # truncate the context to the maximum window
            ctx = idx[:, -self.cfg.block_size:]
            logits, _ = self(ctx)
            logits = logits[:, -1, :]   # only the last position
            if temperature == 0.0:      # greedy
                next_token = logits.argmax(dim=-1, keepdim=True)
            else:
                logits = logits / temperature
                if top_k is not None:   # zero out the tail
                    threshold = torch.topk(logits, top_k).values[:, [-1]]
                    logits[logits < threshold] = float("-inf")
                p = F.softmax(logits, dim=-1)
                next_token = torch.multinomial(p, num_samples=1)
            idx = torch.cat([idx, next_token], dim=1)
        return idx


# --- Part 6: smoke test of the freshly built model -------------------

if __name__ == "__main__":
    torch.manual_seed(42)
    cfg = GPTConfig(vocab_size=256, block_size=64,
                    n_layer=4, n_head=4, n_embd=128, dropout=0.0)
    model = MiniGPT(cfg)

    n_params = sum(p.numel() for p in model.parameters())
    print(f"parameters: {n_params}")

    # forward on random data: the loss should be about ln(256)
    x = torch.randint(0, 256, (2, 10))
    t = torch.randint(0, 256, (2, 10))
    logits, loss = model(x, t)
    print(f"initial loss: {loss.item():.4f}"
          f"   expected: {math.log(256):.4f}")

    # generation with the untrained model
    model.eval()
    start = torch.zeros(1, 1, dtype=torch.long)
    print(model.generate(start, 8, temperature=1.0, top_k=40)[0].tolist())
    print(model.generate(start, 8, temperature=0.0)[0].tolist())
