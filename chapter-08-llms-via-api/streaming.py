"""Streaming: tokens arrive as the model generates them.

Chapter 8, section "Streaming and robustness".
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

stream = client.models.generate_content_stream(
    model=MODEL,
    contents="Explain water hammer in a hydraulic system.",
    config=types.GenerateContentConfig(temperature=0.4),
)

full_text = []
for chunk in stream:
    if chunk.text:                      # some chunks are empty
        print(chunk.text, end="", flush=True)
        full_text.append(chunk.text)

full_response = "".join(full_text)   # to save in the history
