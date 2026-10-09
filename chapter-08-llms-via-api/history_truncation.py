"""History truncation: the context window as a resource to manage.

Chapter 8, section "The context window as a resource".
"""

import os
import sys

from google import genai
from google.genai import types

if not (os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")):
    print("Missing environment variable GEMINI_API_KEY: create a free key "
          "at https://aistudio.google.com/apikey and then run "
          "export GEMINI_API_KEY=<your-key>")
    sys.exit(1)

MODEL = "gemini-2.5-flash"
client = genai.Client()

TOKEN_THRESHOLD = 50_000   # a budget we set for ourselves, not the model's limit

def truncate_history(history: list) -> list:
    """Drop the oldest turns until the history fits the budget.

    Removes messages in pairs (question + response) so the
    conversation is not left with an unpaired turn.
    """
    while len(history) > 2:
        count = client.models.count_tokens(
            model=MODEL, contents=history)
        if count.total_tokens <= TOKEN_THRESHOLD:
            break
        del history[0:2]   # remove the oldest exchange
    return history


if __name__ == "__main__":
    # small sample history to see the function at work
    exchanges = [
        ("What is a centrifugal pump?",
         "It is a machine that transfers energy to a liquid "
         "through a rotating impeller."),
        ("And how do you calculate its head?",
         "From the difference in total head between discharge and suction."),
    ]
    history = []
    for question, response in exchanges:
        history.append(types.Content(
            role="user", parts=[types.Part.from_text(text=question)]))
        history.append(types.Content(
            role="model", parts=[types.Part.from_text(text=response)]))

    history = truncate_history(history)
    count = client.models.count_tokens(model=MODEL, contents=history)
    print(f"messages in history: {len(history)}, "
          f"total tokens: {count.total_tokens} "
          f"(budget: {TOKEN_THRESHOLD})")
