"""The adapter for the real model: the only piece that touches
google-genai. The loop, the memory, the budget and the registry
come from agent_from_scratch.py and stay intact.

Chapter 12, section "Code: an agent from scratch".
"""

import os
import sys

from google import genai
from google.genai import types

from agent_from_scratch import Budget, Response, run_agent, registry

if not (os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")):
    print("The GEMINI_API_KEY environment variable is missing: create a free "
          "key at https://aistudio.google.com/apikey and then run "
          "export GEMINI_API_KEY=<your-key>")
    sys.exit(1)

MODEL = "gemini-2.5-flash"   # model names evolve

SYSTEM = ("You are the purchasing office assistant. Use the "
          "tools to establish the facts: never answer from "
          "memory. Prepare drafts only: sending is up to "
          "an operator.")


class GeminiModel:
    """Adapter between the neutral format and google-genai."""
    def __init__(self, client, model=MODEL):
        self._client, self._model = client, model

    def generate(self, messages, declarations):
        config = types.GenerateContentConfig(
            system_instruction=SYSTEM,
            tools=[types.Tool(function_declarations=[
                types.FunctionDeclaration(**d)
                for d in declarations])],
            temperature=0.0)
        r = self._client.models.generate_content(
            model=self._model,
            contents=self._convert(messages),
            config=config)
        calls = [(c.name, dict(c.args))
                 for c in (r.function_calls or [])]
        return Response(None if calls else r.text,
                        calls)

    def _convert(self, messages):
        contents = []
        for m in messages:
            if m["role"] == "user":
                contents.append(types.Content(role="user",
                    parts=[types.Part.from_text(
                        text=m["text"])]))
            elif m["role"] == "assistant":
                parts = ([types.Part.from_text(
                             text=m["text"])]
                         if m.get("text") else [])
                parts += [types.Part.from_function_call(
                              name=n, args=a)
                          for n, a in m.get("calls", [])]
                contents.append(types.Content(role="model",
                                              parts=parts))
            else:   # tool result
                contents.append(types.Content(role="user",
                    parts=[types.Part.from_function_response(
                        name=m["name"],
                        response=m["result"])]))
        return contents


if __name__ == "__main__":
    client = genai.Client()   # or Vertex AI, as in Chapter 8
    print(run_agent(
        "Find the orders blocked for more than 7 days "
        "and prepare the supplier reminders.",
        GeminiModel(client), registry, Budget(),
        confirm=lambda name, arguments:
            input(f"run {name}({arguments})? [y/n] ") == "y"))
