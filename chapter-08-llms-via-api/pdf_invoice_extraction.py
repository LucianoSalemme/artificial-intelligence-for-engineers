"""Multimodality: extracting structured data from a PDF invoice.

Chapter 8, section "Multimodality": multimodal input plus structured
output, with an arithmetic consistency check downstream.
"""

import os
import sys

from google import genai
from google.genai import types
from pydantic import BaseModel

if not (os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")):
    print("Missing environment variable GEMINI_API_KEY: create a free key "
          "at https://aistudio.google.com/apikey and then run "
          "export GEMINI_API_KEY=<your-key>")
    sys.exit(1)

MODEL = "gemini-2.5-flash"
client = genai.Client()


class InvoiceData(BaseModel):
    """Invoice header. Uncertain fields stay None."""
    number: str | None
    date: str | None            # ISO format, e.g. "2026-03-31"
    supplier: str | None
    net_eur: float | None
    vat_eur: float | None
    total_eur: float | None


def queue_for_review(data: InvoiceData) -> None:
    """Placeholder: in a real system it queues the document for human review."""
    print("DOCUMENT QUEUED FOR REVIEW (incomplete or inconsistent data):")
    print(data)


if __name__ == "__main__":
    if not os.path.exists("invoice_1042.pdf"):
        print("File invoice_1042.pdf not found: copy a PDF invoice with "
              "this name into the directory to try the example.")
        sys.exit(1)

    with open("invoice_1042.pdf", "rb") as f:
        document = types.Part.from_bytes(
            data=f.read(), mime_type="application/pdf")

    response = client.models.generate_content(
        model=MODEL,
        contents=[
            document,
            "Extract the header data from this invoice. If a field "
            "is missing or cannot be read with certainty, leave it "
            "null: NEVER infer or invent it.",
        ],
        config=types.GenerateContentConfig(
            temperature=0.0,
            response_mime_type="application/json",
            response_schema=InvoiceData,
        ),
    )

    data = InvoiceData.model_validate_json(response.text)
    print(data)

    # arithmetic consistency check: an LLM is not an ALU
    if (None in (data.net_eur, data.vat_eur, data.total_eur)
            or abs(data.net_eur + data.vat_eur
                   - data.total_eur) > 0.01):
        queue_for_review(data)      # human review, not a discard
