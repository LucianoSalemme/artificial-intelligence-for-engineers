# Artificial Intelligence for Engineers: the code

All the source code for the book **"Artificial Intelligence for Engineers.
Transformers, LLMs, RAG, and AI Agents: from foundations to code"** by
Luciano Salemme, organized by chapter and ready to run.

Each directory corresponds to a chapter of the book and contains a README
with the map between the files and the listings, the instructions to run
them, and the specific requirements.

## Structure

| Directory                                   | Chapter                                      |
| ------------------------------------------- | -------------------------------------------- |
| `chapter-02-mathematical-foundations`       | 2. Mathematical Foundations                  |
| `chapter-03-neural-networks`                | 3. Neural Networks                           |
| `chapter-04-tokens-and-embeddings`          | 4. Tokens and Embeddings                     |
| `chapter-05-attention`                      | 5. The Attention Mechanism                   |
| `chapter-06-transformer`                    | 6. The Transformer Architecture (mini-GPT)   |
| `chapter-07-from-transformer-to-llms`       | 7. From Transformer to LLMs                  |
| `chapter-08-llms-via-api`                   | 8. Using LLMs via API                        |
| `chapter-09-prompt-and-context-engineering` | 9. Prompt and Context Engineering            |
| `chapter-10-semantic-search`                | 10. Semantic Search and Vector Databases     |
| `chapter-11-rag`                            | 11. Retrieval-Augmented Generation           |
| `chapter-12-agents`                         | 12. Agents                                   |
| `chapter-13-mcp`                            | 13. The Model Context Protocol               |
| `chapter-14-multi-agent`                    | 14. Multi-Agent Systems                      |
| `chapter-15-production`                     | 15. LLMs in Production                       |
| `chapter-16-observability`                  | 16. Observability and Evaluation             |
| `chapter-17-case-study`                     | 17. Case Study                               |

## Prerequisites

- **Python 3.12 or higher**
- about 3 GB of disk space for the dependencies (PyTorch is the
  heaviest) and about 500 MB for the embedding model downloaded on the
  first run of chapters 4 and 10

## Installation

```bash
git clone https://github.com/LucianoSalemme/artificial-intelligence-for-engineers.git
cd artificial-intelligence-for-engineers
python3 -m venv .venv
source .venv/bin/activate        # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Credentials (only for the chapters that call the APIs)

Chapters 8, 9 (caching), 11, 12 (Gemini adapter), and 14 (supervisor)
call the Gemini API. You need a key, free for the book's experiments,
from <https://aistudio.google.com>:

```bash
export GEMINI_API_KEY="your-key"
```

Every script checks the variable at startup: if it is missing, it
explains how to obtain it and exits without cryptic errors. Chapter 7
uses [Ollama](https://ollama.com) locally instead (no key); the tracing
in chapter 16 requires a free [LangSmith](https://smith.langchain.com)
account.

## Errors and improvements

If you find an error or have an idea for improving an example, open an
issue or a pull request: it will be a valuable contribution to those who
read after you.
