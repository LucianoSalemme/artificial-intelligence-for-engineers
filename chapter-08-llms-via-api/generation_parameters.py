"""The generation parameters travel in the call configuration.

Chapter 8, section "Generation parameters".
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

config = types.GenerateContentConfig(
    temperature=0.2,          # task with a "right" answer
    top_p=0.95,
    max_output_tokens=1024,   # safety cap on cost and latency
    stop_sequences=["END"],   # optional early stop
    # for reasoning models: how much "thinking" to allow
    thinking_config=types.ThinkingConfig(thinking_budget=0),
)

if __name__ == "__main__":
    response = client.models.generate_content(
        model=MODEL,
        contents="Explain in two sentences the difference between a process and a thread.",
        config=config,
    )
    print(response.text)
