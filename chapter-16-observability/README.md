# Chapter 16 - Observability and Evaluation

Code for the end-of-chapter project: the evaluation and regression pipeline for the ACME RAG from chapter 11, with a golden set, programmatic citation checking, an LLM judge with a rubric (and a deterministic stub for continuous integration), and a regression report with blocking thresholds; plus the tracing instrumentation with LangSmith and the materials for the rubric-based judge example.

## Files

| File | Description |
|---|---|
| `eval_pipeline.py` | The eval pipeline assembled into a single program: configuration and golden set, `valid_citations`, the judge rubric, `GeminiJudge` and `StubJudge`, `evaluate_system` and `regression_report` with the main block. Section "Code: an eval pipeline". |
| `tracing_langsmith.py` | The instrumentation with the `@traceable` decorator; the bodies of `rewrite` and `answer` are omitted as in the book because they are identical to chapter 11. Section "Tracing". |
| `comparison_rubric.txt` | The rubric prompt for comparing two answers: criteria in order of priority, reasoning before the verdict, JSON output. Section "Evaluation metrics". |
| `comparison_responses.txt` | Answers A and B from the example (B contains the 800 km maximum that does not exist in the excerpts: the case the verbosity bias rewards and the rubric exposes). Section "Evaluation metrics". |
| `eval/recordings.json` | The recorded answers the pipeline replays when it runs without an API key: two cases consistent with the golden set, with excerpts in the chapter 11 chunk format. Section "Code: an eval pipeline". |
| `eval/baseline_v1_4.json` | The archived baseline that `regression_report` compares against the candidate, aligned with the recordings so the demo pass ends without blocks (exit code 0). Section "Code: an eval pipeline". |

In the book the golden set has 50 cases; here the two shown in the listing (G01 and G02) are included. The listing with the `export LANGSMITH_*` commands is shown below; the one with the regression report output is output only and was not turned into a file.

## How to run

```bash
pip install google-genai
cd code/chapter-16-observability
python3 eval_pipeline.py
```

With no arguments the pipeline uses the stub judge and the recorded answers: no API key, as in CI. It prints the regression report (metric, base, cand, delta, result), writes `eval/candidate.json`, and exits with 0 if the release can proceed, with 1 if it is blocked. Run it from the chapter directory, because it reads `eval/...` with relative paths. The absolute metric values in this mode come from the stub heuristics (for example the expected refusal of G02 counts as not relevant): as the book says, the stub does not replace the judge, it replaces the API key, and the pass demonstrates the mechanics of comparing against the baseline.

```bash
export GEMINI_API_KEY=<your-key>   # free at https://aistudio.google.com/apikey
python3 eval_pipeline.py --with-api
```

With `--with-api` the judge is Gemini with the rubric and temperature at zero; to evaluate the real system you also need the `answer` function from chapter 11 (`code/chapter-11-rag/full_rag.py`), to import into the file: without it, the script explains and exits.

Tracing is activated through environment variables, without touching the code:

```bash
pip install langsmith
export LANGSMITH_TRACING=true
export LANGSMITH_API_KEY=<your-key>   # https://smith.langchain.com
export LANGSMITH_PROJECT=acme-assistant
python3 tracing_langsmith.py
```

`tracing_langsmith.py` shows the instrumentation: to produce complete traces the function bodies must be taken from the chapter 11 code.

## Requirements

- Python 3.12
- packages: `google-genai` (for `eval_pipeline.py`), `langsmith` (for `tracing_langsmith.py`)
- no credentials for the default pass of `eval_pipeline.py`; `GEMINI_API_KEY` (or `GOOGLE_API_KEY`) for `--with-api`; `LANGSMITH_API_KEY` for tracing. In both cases, if the variable is missing the script prints how to obtain it and exits with code 1
