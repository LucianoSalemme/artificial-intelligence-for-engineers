"""Evaluation and regression pipeline for the ACME RAG.

Chapter 16, section "Code: an eval pipeline": golden set with
expected outcomes, programmatic citation checking, LLM judge with a
rubric, regression report with blocking thresholds. The answer
function is a parameter: pass the answer function from chapter 11 to
evaluate the real system (--with-api), or a stub that replays
recorded answers when the pipeline itself is under test.

Usage, from the chapter directory:
    python3 eval_pipeline.py             # CI: stub judge, no API key
    python3 eval_pipeline.py --with-api  # Gemini judge (GEMINI_API_KEY)

Exit code: 0 if the release can proceed, 1 if it is blocked.
"""

import re, json

from google import genai
from google.genai import types

# Configuration. The judge is a measuring instrument:
# its model and version are frozen during comparisons
# and recorded alongside the results.
JUDGE_MODEL   = "gemini-2.5-flash"  # names evolve
JUDGE_VERSION = "judge-v2"

THRESHOLDS = {  # maximum tolerated regression per metric
    "recall": 0.02, "citations": 0.02,
    "grounded": 0.02, "relevant": 0.04,
}

REFUSAL = ("I could not find this information "
           "in the available documents.")

GOLDEN_SET = [
    {"id": "G01",
     "question": ("What is the reimbursement for using "
                  "a personal car?"),
     "expected_chunk": "Travel policy - Art. 5",
     "type": "normal"},
    {"id": "G02",
     "question": ("Can I work remotely from "
                  "abroad?"),
     "expected_chunk": None,   # not in the documents:
     "type": "no_answer"},  # a refusal is expected
    # ... 50 cases, sampled from traffic and annotated
    # as described in the section on eval sets
]


def valid_citations(answer, n_excerpts):
    """Every cited [n] must correspond to an excerpt
    that was actually provided. Exact check, no model."""
    if answer.strip() == REFUSAL:
        return True   # a refusal cites nothing, and that is correct
    numbers = {int(n) for n in re.findall(r"\[(\d+)\]",
                                          answer)}
    return (len(numbers) > 0 and
            all(1 <= n <= n_excerpts for n in numbers))


RUBRIC = """Evaluate the answer of a document
assistant.
Question: {question}
Excerpts provided to the assistant:
{excerpts}
Answer to evaluate: {answer}

Criteria, in order of priority:
1. GROUNDED: every statement is supported by the
   excerpts. An explicit refusal counts as grounded.
   A single unsupported statement makes the answer
   ungrounded. Length is not a merit.
2. RELEVANT: the answer addresses what the question
   asks.
First list any unsupported statements, then reply
ONLY in JSON:
{{"unsupported": [...], "grounded": true|false,
  "relevant": true|false}}"""


class GeminiJudge:
    """The real judge: an LLM with a rubric, JSON output."""

    def __init__(self, client, model=JUDGE_MODEL):
        self.client, self.model = client, model

    def evaluate(self, question, excerpts, answer):
        prompt = RUBRIC.format(
            question=question,
            excerpts="\n".join(c["text"] for c in excerpts),
            answer=answer)
        r = self.client.models.generate_content(
            model=self.model, contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.0,
                response_mime_type="application/json"))
        v = json.loads(r.text)
        return {"grounded": bool(v["grounded"]),
                "relevant": bool(v["relevant"])}

class StubJudge:
    """Deterministic judge for CI and development: grounded
    if every number in the answer appears in the excerpts,
    relevant if the answer is not a refusal."""

    def evaluate(self, question, excerpts, answer):
        if answer.strip() == REFUSAL:
            return {"grounded": True, "relevant": False}
        text = " ".join(c["text"] for c in excerpts)
        numbers = re.findall(r"\d+(?:,\d+)?", answer)
        return {"grounded": all(n in text for n in numbers),
                "relevant": True}


def evaluate_system(answer_fn, golden_set, judge):
    """Runs the system on every case and computes the
    metrics, per case and aggregate."""
    cases = []
    for case in golden_set:
        answer, excerpts = answer_fn(case["question"])
        judgment = judge.evaluate(case["question"],
                                  excerpts, answer)
        cases.append({
            "id": case["id"],
            "recall": (case["expected_chunk"] is None or
                       any(c["id"] == case["expected_chunk"]
                           for c in excerpts)),
            "citations": valid_citations(answer,
                                         len(excerpts)),
            "grounded": judgment["grounded"],
            "relevant": judgment["relevant"],
        })
    n = len(cases)
    metrics = {m: sum(c[m] for c in cases) / n
               for m in THRESHOLDS}
    return {"judge": JUDGE_VERSION,
            "cases": cases, "metrics": metrics}


def regression_report(baseline, candidate, thresholds):
    """Compares two runs on the same golden set.
    Returns True if the release can proceed."""
    assert baseline["judge"] == candidate["judge"], \
        "different judges: comparison not valid"
    blocked = False
    print(f"{'metric':<12}{'base':>6}{'cand':>6}"
          f"{'delta':>8}   result")
    for m, base in baseline["metrics"].items():
        cand = candidate["metrics"][m]
        delta = cand - base
        failed = delta < -thresholds[m]
        blocked = blocked or failed
        print(f"{m:<12}{base:>6.2f}{cand:>6.2f}"
              f"{delta:>+8.2f}   "
              f"{'BLOCK' if failed else 'ok'}")
    # per-case diff: which case changed outcome, and where
    for b, c in zip(baseline["cases"], candidate["cases"]):
        for m in thresholds:
            if b[m] and not c[m]:
                print(f"  regressed {c['id']} on {m}")
    return not blocked

if __name__ == "__main__":
    import os
    import sys
    if "--with-api" in sys.argv:
        if not (os.environ.get("GEMINI_API_KEY")
                or os.environ.get("GOOGLE_API_KEY")):
            print("Missing environment variable GEMINI_API_KEY: create a "
                  "free key at https://aistudio.google.com/apikey "
                  "and set export GEMINI_API_KEY=<your-key>")
            sys.exit(1)
        client = genai.Client()
        judge = GeminiJudge(client)
        try:
            run_fn = answer            # from chapter 11
        except NameError:
            print("With --with-api you need the answer function from the "
                  "chapter 11 RAG (code/chapter-11-rag/full_rag.py): "
                  "import it into this file to evaluate the real system.")
            sys.exit(1)
    else:                          # CI: no API key
        judge = StubJudge()
        reg = json.load(open("eval/recordings.json"))
        run_fn = lambda d: (reg[d]["answer"],
                            reg[d]["excerpts"])
    candidate = evaluate_system(run_fn, GOLDEN_SET, judge)
    baseline = json.load(open("eval/baseline_v1_4.json"))
    ok = regression_report(baseline, candidate, THRESHOLDS)
    json.dump(candidate, open("eval/candidate.json", "w"))
    sys.exit(0 if ok else 1)
