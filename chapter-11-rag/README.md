# Chapter 11 - Retrieval-Augmented Generation

Code for the end-of-chapter project: a document assistant for the fictional ACME Inc. that answers employees' questions about internal policies, cites its sources, and evaluates itself with the three metrics of the chapter (recall, groundedness, relevance).

## Files

| File | Description |
|---|---|
| `full_rag.py` | The complete RAG assembled into a single program: configuration and client, ingestion with structural chunking, in-memory search engine (from chapter 10), query pipeline (rewriting, retrieval, generation), and evaluation with an LLM judge. Section "Code: a complete RAG". |
| `generation_prompt.txt` | The full generation prompt (the five rules with the example excerpts), included for reference: in the program it appears in abbreviated form in the `INSTRUCTIONS` constant. Section "The generation prompt". |
| `data/travel_policy.txt` | Sample document base: Articles 3-7 referenced in the live test and in the example prompt. |
| `data/leave_policy.txt` | Sample document base: Article 4 on notice is the expected chunk of the second question in the eval set. |
| `data/security_policy.txt` | Sample document base: third indexed document. |

The documents in `data/` do not appear in full in the book: they are rebuilt in minimal form from the passages cited in the text (mileage reimbursement of 0.42 euros/km, meal cap of 50 euros in Italy and 80 abroad, 30 days of notice for two weeks of leave), using the article format `Article N: Title` required by structural chunking.

## How to run

```bash
pip install google-genai numpy
export GEMINI_API_KEY=<your-key>   # free at https://aistudio.google.com/apikey
cd code/chapter-11-rag
python3 full_rag.py
```

The script must be launched from the chapter directory, because it reads the documents with relative paths (`data/...`). On startup it indexes the three documents, runs the live test of the personal-car question (with the citation map), and runs `evaluate` on the sample eval set, printing recall@5, groundedness, and relevance. In the book the eval set has 30 questions; here only the two shown in the listing are included.

## Dependencies

- Python 3.12
- packages: `google-genai`, `numpy`
- environment variable `GEMINI_API_KEY` (or `GOOGLE_API_KEY`): without a key the script prints how to get one and exits
