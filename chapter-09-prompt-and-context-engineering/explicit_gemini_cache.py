"""Explicit prompt caching with Google's SDK (google-genai).

Listing from chapter 9, "Prompt caching" section: the stable prefix
(instructions and product documentation) is loaded into the cache once,
with an explicit time to live, and every later request pays full price
only for the new tokens. Requires the GOOGLE_API_KEY environment variable.
"""

import os
import sys

if not (os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")):
    print("Missing GOOGLE_API_KEY environment variable: create a key at")
    print("https://aistudio.google.com/apikey and then run:")
    print('  export GOOGLE_API_KEY="your-key"')
    sys.exit(1)

from google import genai
from google.genai import types

# Model names change over time: check the current list.
MODEL = "gemini-2.5-flash"

# Sample data: the stable context of the technical support assistant
# described in the text. In practice the documentation is a long excerpt:
# caching pays off on long, hot prefixes, and providers require a minimum
# content size to create one.
stable_instructions = (
    "You are the technical support assistant of a manufacturer of "
    "industrial components. Answer only based on the documentation "
    "provided; if a piece of information is not present, say so explicitly."
)
product_documentation = (
    "CP-40 centrifugal pump. Maximum flow rate: 40 m3/h. Maximum head: "
    "32 m. DN 50 flanged connection. Routine maintenance: check the "
    "mechanical seal every 2000 operating hours."
)
user_question = "How often should the CP-40 seal be checked?"

client = genai.Client()

# The stable prefix is loaded into the cache once,
# with an explicit time to live.
cache = client.caches.create(
    model=MODEL,
    config=types.CreateCachedContentConfig(
        system_instruction=stable_instructions,
        contents=[product_documentation],
        ttl="3600s",   # one hour of validity
    ),
)

# Every request pays full price only for the new tokens.
response = client.models.generate_content(
    model=MODEL,
    contents=user_question,
    config=types.GenerateContentConfig(cached_content=cache.name),
)

print(response.text)
