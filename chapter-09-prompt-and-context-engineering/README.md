# Chapter 9 - Prompt and Context Engineering

Code and materials for the listings of chapter 9, devoted to the fundamental prompt engineering techniques (zero-shot, few-shot, chain-of-thought on the same order-email extraction task), to context engineering, prompt caching, and prompt injection.

## File

| File | Description |
|---|---|
| `order_email.txt` | The reference email from Meccanica Rossi S.r.l. that runs through the first half of the chapter. It is not code: it is the input data for the three extractor prompts. "Fundamental techniques" section. |
| `order_extractor.py` | The three order extractor prompts (zero-shot, few-shot, chain-of-thought), assembled as successive versions of the same program; it reads `order_email.txt` and prints the three complete prompts, ready to send to a model. "Zero-shot", "Few-shot", "Chain-of-thought" sections. |
| `explicit_gemini_cache.py` | Explicit cache management with Google's SDK: the stable prefix is loaded once with `client.caches.create` and reused by later requests through `cached_content`, using the technical support assistant data from the text. "Prompt caching" section. |
| `indirect_injection_email.txt` | The seemingly harmless email that hides, after the signature, a hostile instruction for the AI assistant. It is the attack data for indirect injection: it is not to be executed, it is to be studied. "Prompt injection" section. |
| `prompts/antipattern_politeness.txt` | First anti-pattern: politeness instead of precision ("as best you can", "fairly concise"). "Patterns and anti-patterns" section. |
| `prompts/measurable_constraints_rewrite.txt` | Rewrite of the first anti-pattern: measurable constraints (3-5 points, 20 words), an inclusion criterion, and the empty-case specification. "Patterns and anti-patterns" section. |
| `prompts/antipattern_negations.txt` | Second anti-pattern: accumulated negation, a list of prohibitions that never says what to do. "Patterns and anti-patterns" section. |
| `prompts/positive_rewrite.txt` | Rewrite of the second anti-pattern: the same constraints expressed as the desired behavior. "Patterns and anti-patterns" section. |

The two model-output listings (the JSON produced by the zero-shot prompt and the day count from the chain-of-thought) are transcripts of typical responses, not code, and are not reproduced as files.

## How to run

1. Print the three extractor prompts (no dependencies, no API key):

   ```bash
   python3 order_extractor.py
   ```

   The printed prompts can be pasted into any chat interface or sent via API to reproduce the chapter's experiments.

2. Try explicit prompt caching with Gemini:

   ```bash
   pip install google-genai
   export GOOGLE_API_KEY="your-key"
   python3 explicit_gemini_cache.py
   ```

   The key is created at https://aistudio.google.com/apikey; if it is missing, the script prints the instructions and exits with code 1. Note: explicitly creating a cache requires a minimum content size (thousands of tokens depending on the model), so with the miniature sample data the call may be rejected by the service; for a real test use a long documentation excerpt, as described in the worked example in the chapter.

The files in `prompts/` and the two emails are text materials to read or paste into your own experiments, in line with the "Prompts as code" section: prompts live in dedicated, versioned files, not drowned among the strings of application logic.

## Requirements

- Python 3.12
- Only for `explicit_gemini_cache.py`: pip package `google-genai` and the `GOOGLE_API_KEY` environment variable
