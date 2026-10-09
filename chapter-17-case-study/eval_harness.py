"""Chapter 17, listing "The eval harness": comparison against the baseline
and release verdict.

The helper functions mirror those from chapters 11 and 16:
valid_citations is the regular expression on the [n] markers, judge wraps
the rubric judge call (skipped when running with the stubs, as in the
listing comment), aggregate averages per metric.

Run:  python eval_harness.py
(runs with the stubs: no API key required)
"""

import re


def valid_citations(answer: str, n_sources: int) -> bool:
    markers = [int(m) for m in re.findall(r"\[(\d+)\]", answer)]
    return bool(markers) and all(1 <= m <= n_sources
                                 for m in markers)


def judge(case, answer) -> dict:
    # Groundedness and relevance with the rubric judge (ch. 16):
    # skipped when running with the stubs, as in the listing.
    return {}


def aggregate(results) -> dict:
    sums: dict = {}
    counts: dict = {}
    for r in results:
        for k, v in r.items():
            sums[k] = sums.get(k, 0) + (float(v) if not
                      isinstance(v, bool) else (1.0 if v else 0.0))
            counts[k] = counts.get(k, 0) + 1
    return {k: sums[k] / counts[k] for k in sums}


def evaluate_case(case, invoke):
    """invoke(request, user) -> final graph state.
    With the stubs in CI, with the real system in staging."""
    fin = invoke(case["request"], case["user"])
    if case["type"] == "document":
        return {
          "recall": case["expected_chunk"] in fin["sources"],
          "citations": valid_citations(fin["answer"],
                                       len(fin["sources"])),
          # groundedness and relevance: rubric judge
          # (ch. 16), skipped when running with the stubs
          **judge(case, fin["answer"]),
        }
    if case["type"] == "action":
        p = fin.get("ticket_proposal") or {}
        return {"proposal":
                p.get("category") == case["expected_category"]}
    # out of scope and adversarial: the expected answer
    # is a precise content, verifiable with a match
    return {"content":
            case["expected"] in fin.get("answer", "")}


def regression(golden, invoke, baseline, thresholds):
    agg = aggregate(evaluate_case(c, invoke) for c in golden)
    blockers = [m for m in thresholds
                if agg[m] - baseline[m] < thresholds[m]]
    for m in sorted(agg):
        print(f"{m:12s} {baseline.get(m, 0):.2f} "
              f"-> {agg[m]:.2f}")
    return blockers   # empty list = release allowed


if __name__ == "__main__":
    from langgraph.types import Command

    from assistant import graph

    def invoke(request, user):
        cfg = {"configurable":
               {"thread_id": f"eval-{abs(hash(request))}"}}
        fin = graph.invoke({"request": request,
                            "user": user, "steps": []}, cfg)
        # If the graph is suspended on the confirmation, in eval we
        # grant the approval and observe the full result.
        if fin.get("ticket_proposal") and not fin.get("action_result"):
            fin = graph.invoke(Command(resume="yes"), cfg)
        return fin

    # Demonstrative golden set: in the book the cases are sixty.
    GOLDEN = [
        {"type": "document", "user": "eval",
         "request": "What is the procedure for mileage "
                    "reimbursement?",
         "expected_chunk": "Travel policy - Art. 4"},
        {"type": "action", "user": "eval",
         "request": "Open a ticket: the monitor is broken",
         "expected_category": "IT"},
        {"type": "out", "user": "eval",
         "request": "What's the weather tomorrow?",
         "expected": "I can help"},
    ]
    BASELINE = {"recall": 1.00, "citations": 1.00,
                "proposal": 1.00, "content": 1.00}
    THRESHOLDS = {"recall": -0.02, "citations": -0.02,
                  "proposal": -0.001, "content": -0.001}

    blockers = regression(GOLDEN, invoke, BASELINE, THRESHOLDS)
    if blockers:
        print("Release BLOCKED on:", ", ".join(blockers))
        raise SystemExit(1)
    print("Release allowed: no metric below threshold.")
