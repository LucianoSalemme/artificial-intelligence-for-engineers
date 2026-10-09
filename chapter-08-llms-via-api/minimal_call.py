"""Minimal complete call to an LLM via API.

Chapter 8, section "Anatomy of a call".
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

# Model names change from month to month: keep them in ONE
# configuration constant, not scattered through the code.
MODEL = "gemini-2.5-flash"

# The client reads the key from the GEMINI_API_KEY environment variable.
# On Vertex AI: genai.Client(vertexai=True, project="...", location="...")
client = genai.Client()

response = client.models.generate_content(
    model=MODEL,
    contents="Explain in two sentences the difference between a process and a thread.",
    config=types.GenerateContentConfig(
        system_instruction=(
            "You are a technical assistant for software engineers. "
            "Answer in English, concisely."
        ),
        temperature=0.3,
    ),
)

print(response.text)              # the response text
print(response.usage_metadata)    # input and output tokens
