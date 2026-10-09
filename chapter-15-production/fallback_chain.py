"""Fallback chain across models and providers, Chapter 15,
section "Reliability".

The chain lives in the gateway: first the large model, then the
small one from the same provider, and finally an independent
provider. The model constants are those from the complexity
routing listing.
"""

from complexity_routing import LARGE_MODEL, SMALL_MODEL


class TransientError(Exception):
    """Temporary provider error (quota, capacity, network):
    it makes sense to move to the next step of the chain."""


FALLBACK_CHAIN = [
    ("vertex", LARGE_MODEL),        # primary path
    ("vertex", SMALL_MODEL),        # reduced capacity, same provider
    ("provider_b", "model-b"),      # independent provider
]

def generate_with_fallback(request, call, record):
    """call() runs the real call; record() feeds metrics and
    alarms. Both are injected, testable with stubs."""
    last_error = None
    for provider, model in FALLBACK_CHAIN:
        try:
            response = call(provider, model, request)
            record(provider, model, ok=True)
            return response
        except TransientError as error:
            record(provider, model, ok=False)
            last_error = error
    raise last_error


if __name__ == "__main__":
    # Demo stubs: the primary path is out of service,
    # the second step responds.
    def call_stub(provider, model, request):
        if model == LARGE_MODEL:
            raise TransientError("quota exhausted on the flagship model")
        return f"[response from {provider}/{model}]"

    def record_stub(provider, model, ok):
        outcome = "ok" if ok else "failed"
        print(f"record: {provider}/{model} -> {outcome}")

    response = generate_with_fallback("What is the status of order 812?",
                                      call_stub, record_stub)
    print("response:", response)
