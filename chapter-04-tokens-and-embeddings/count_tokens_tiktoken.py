# Listing 4.1 (lst:cap03_tiktoken): count and inspect the tokens of a sentence.
# pip install tiktoken
import tiktoken

# the tokenizer used by the GPT-4 models (~100k entries)
enc = tiktoken.get_encoding("cl100k_base")

sentences = [
    "The engineer measures the output voltage.",
    "L'ingegnere misura la tensione di uscita.",
]
for sentence in sentences:
    token_ids = enc.encode(sentence)
    pieces = [enc.decode([i]) for i in token_ids]
    print(f"{len(token_ids):3d} tokens  {pieces}")
