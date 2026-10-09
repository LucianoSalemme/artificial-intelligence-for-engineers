"""The client keeps the conversation: the API is stateless.

Chapter 8, section "You keep the conversation".
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

history = []   # the dialogue memory: a simple list

def ask(question: str) -> str:
    # 1. append the user's question to the history
    history.append(types.Content(
        role="user",
        parts=[types.Part.from_text(text=question)]))

    # 2. send the WHOLE history, not just the last message
    response = client.models.generate_content(
        model=MODEL,
        contents=history,
        config=types.GenerateContentConfig(
            system_instruction="You are a concise technical assistant."),
    )

    # 3. append the model's response (role "model")
    history.append(response.candidates[0].content)
    return response.text

print(ask("What is a centrifugal pump?"))
print(ask("And how do you calculate its head?"))
