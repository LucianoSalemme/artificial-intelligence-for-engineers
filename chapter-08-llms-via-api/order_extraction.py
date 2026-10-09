"""Structured output with a Pydantic schema and retry with feedback.

Chapter 8, section "Structured output": the two listings of the section
(schema + constrained call, then the full pattern with retry)
assembled into a single program.
"""

import os
import sys

from google import genai
from google.genai import types
from pydantic import BaseModel, Field, ValidationError

if not (os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")):
    print("Missing environment variable GEMINI_API_KEY: create a free key "
          "at https://aistudio.google.com/apikey and then run "
          "export GEMINI_API_KEY=<your-key>")
    sys.exit(1)

MODEL = "gemini-2.5-flash"
client = genai.Client()


class OrderLine(BaseModel):
    code: str = Field(description="item code, e.g. VLV-2041")
    quantity: int = Field(ge=1)
    unit_price_eur: float = Field(ge=0)

class Order(BaseModel):
    """Schema of the order extracted from a customer email."""
    customer: str
    lines: list[OrderLine]
    urgent: bool
    notes: str | None = None


# small sample catalog for the validator's business rules
CATALOG = {"VLV-2041"}

MAX_ATTEMPTS = 3

def extract_order(email_text: str) -> Order:
    """Extract a validated order, with retry on error."""
    contents = [f"Extract the order from this email:\n\n{email_text}"]

    for attempt in range(MAX_ATTEMPTS):
        response = client.models.generate_content(
            model=MODEL,
            contents=contents,
            config=types.GenerateContentConfig(
                temperature=0.0,
                response_mime_type="application/json",
                response_schema=Order,
            ),
        )
        try:
            order = Order.model_validate_json(response.text)
            # business rules beyond the schema
            if not all(line.code in CATALOG for line in order.lines):
                raise ValueError("item code not in catalog")
            return order
        except (ValidationError, ValueError) as error:
            # send back the bad output and the error:
            # on the next attempt the model sees its own mistake
            contents.append(response.text)
            contents.append(
                f"The previous output is not valid: {error}. "
                "Fix it and return only the JSON.")

    raise RuntimeError(f"extraction failed after {MAX_ATTEMPTS} attempts")


if __name__ == "__main__":
    # sample email consistent with the chapter's case
    email_text = (
        "Hello,\n"
        "please ship us urgently 12 valves, item code VLV-2041, "
        "at the agreed price of 45.50 euro each.\n"
        "Best regards,\n"
        "Rossi Workshops Ltd."
    )
    order = extract_order(email_text)
    print(order.lines[0].code, order.lines[0].quantity)
    print(order)
