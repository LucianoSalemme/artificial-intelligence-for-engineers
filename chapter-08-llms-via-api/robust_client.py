"""Robust client: timeout, error classification, retry with exponential
backoff and jitter, truncation check, usage logging.

Chapter 8, section "Failures, retries and backoff".
"""

import logging
import os
import random
import sys
import time
from google import genai
from google.genai import errors, types

if not (os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")):
    print("Missing environment variable GEMINI_API_KEY: create a free key "
          "at https://aistudio.google.com/apikey and then run "
          "export GEMINI_API_KEY=<your-key>")
    sys.exit(1)

MODEL = "gemini-2.5-flash"         # model names keep changing
TRANSIENT_CODES = {429, 500, 502, 503, 504}
log = logging.getLogger("llm_client")

# explicit timeout: never wait forever (value in ms)
client = genai.Client(
    http_options=types.HttpOptions(timeout=60_000))

def generate(contents, config,
             max_attempts: int = 5,
             max_wait: float = 30.0) -> types.GenerateContentResponse:
    """Call with retry, exponential backoff and outcome checks."""
    for attempt in range(max_attempts):
        try:
            response = client.models.generate_content(
                model=MODEL, contents=contents, config=config)

            # response arrived but truncated: for us that is an error
            reason = response.candidates[0].finish_reason
            if reason != types.FinishReason.STOP:
                raise RuntimeError(f"generation interrupted: {reason}")

            usage = response.usage_metadata
            log.info("tokens input=%s output=%s",
                     usage.prompt_token_count,
                     usage.candidates_token_count)
            return response

        except errors.APIError as error:
            if error.code not in TRANSIENT_CODES:
                raise                     # permanent: no point retrying
            if attempt == max_attempts - 1:
                raise                     # attempts exhausted
            wait = min(2 ** attempt, max_wait)
            wait += random.uniform(0, wait)     # jitter
            log.warning("error %s, retrying in %.1f s",
                        error.code, wait)
            time.sleep(wait)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    response = generate(
        contents="Explain water hammer in a hydraulic system.",
        config=types.GenerateContentConfig(temperature=0.4),
    )
    print(response.text)
