"""Complexity routing, Chapter 15, section "Costs".

A cheap classifier on the small model dispatches requests: the
simple ones to the small model, the complex ones to the large model.
The logic is separated from the calls: classify and generate are
injected.
"""

# Model names evolve: constants to update.
LARGE_MODEL = "gemini-2.5-pro"
SMALL_MODEL = "gemini-2.5-flash"

ROUTER_PROMPT = """Classify a user request.
SIMPLE: a question about facts, statuses, known procedures.
COMPLEX: reasoning over multiple sources, drafting detailed
text, ambiguous or unusual cases.
When in doubt answer COMPLEX.
Answer with a single word: SIMPLE or COMPLEX."""

def route(request, classify, generate):
    """Dispatch the request to the right model.
    classify and generate are injected: in tests they are stubs,
    in production they call the gateway."""
    verdict = classify(SMALL_MODEL, ROUTER_PROMPT,
                       request[:2000])   # the start is enough
    model = (SMALL_MODEL if verdict.strip() == "SIMPLE"
             else LARGE_MODEL)
    return generate(model, request), model


if __name__ == "__main__":
    # Demo stubs: in production the two functions
    # call the LLM gateway.
    def classify_stub(model, prompt, request):
        complex_cues = ("compare", "analyze", "draft")
        text = request.lower()
        if any(cue in text for cue in complex_cues):
            return "COMPLEX"
        return "SIMPLE"

    def generate_stub(model, request):
        return f"[response from {model}]"

    requests = [
        "What time does the Verona warehouse open?",
        "What is the status of shipment 4517?",
        "Compare the two shipping quotes and draft a recommendation.",
    ]
    for request in requests:
        response, model = route(request, classify_stub, generate_stub)
        print(f"{model:18} <- {request}")
