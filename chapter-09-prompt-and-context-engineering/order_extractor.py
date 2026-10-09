"""Builds the three prompts of the chapter 9 order extractor.

Listings from the "Fundamental techniques" section: the same task,
extracting structured data from an order email, tackled with a zero-shot
prompt, a few-shot one and a chain-of-thought one. The book presents the
three prompts as successive versions of the same program ("same
instructions as the zero-shot prompt, plus: ...", "instructions and
example as in the few-shot prompt, plus: ..."), so here they are assembled
in a single file in the order of the chapter. The script reads the
reference email from order_email.txt and prints the three prompts ready to
send to a model.
"""

from pathlib import Path

# Zero-shot prompt instructions (section "Zero-shot: the instruction alone").
INSTRUCTIONS = """\
Extract the order data from the following email and
return it as a JSON object with these fields:
"customer", "quote_reference", "line_items" (a list
of objects with "description", "code", "quantity"),
"delivery" (an object with "timeframe" and "address").
Reply only with the JSON, nothing else."""

# Few-shot addition (section "Few-shot: conventions are shown"):
# the conventions and an example built specifically around edge cases.
CONVENTIONS_AND_EXAMPLE = """\
Conventions: "code" is the supplier's article code,
null if absent; "quantity" is always a number; the
unit goes in the "unit" field ("pcs" for pieces).

Example.
Email:
<<<
Hello, we are ordering 2 coils of rope (50 m each)
and 10 carabiners code MK-77. Delivery this week
to Via Roma 1, Pavia.
>>>
Reply:
{"customer": null, "quote_reference": null,
 "line_items": [
   {"description": "rope, 50 m coils",
    "code": null, "quantity": 2, "unit": "coils"},
   {"description": "carabiners", "code": "MK-77",
    "quantity": 10, "unit": "pcs"}],
 "delivery": {"timeframe": "this week",
   "address": "Via Roma 1, Pavia"}}"""

# Chain-of-thought addition (section "Chain-of-thought: the reasoning
# before the result"): computing the deadline date in business days.
DEADLINE_INSTRUCTIONS = """\
Add the "deadline" field (format YYYY-MM-DD) to the
JSON: the received date is Monday, March 2, 2026 and
the timeframe must be computed in business days
(Saturdays and Sundays excluded, counting starts from
the day after the received date).

Before the JSON, show the day count one by one. Then
write === and the JSON on a new line."""


def zero_shot_prompt(email):
    """The instruction alone, followed by the email between delimiters."""
    return f"{INSTRUCTIONS}\n\nEmail:\n<<<\n{email}\n>>>"


def few_shot_prompt(email):
    """Same instructions as the zero-shot prompt, plus conventions and example."""
    return (
        f"{INSTRUCTIONS}\n\n{CONVENTIONS_AND_EXAMPLE}\n\n"
        f"Now extract the data from this email:\n<<<\n{email}\n>>>"
    )


def chain_of_thought_prompt(email):
    """Instructions and example as in the few-shot, plus the date calculation."""
    return (
        f"{INSTRUCTIONS}\n\n{CONVENTIONS_AND_EXAMPLE}\n\n"
        f"{DEADLINE_INSTRUCTIONS}\n\n"
        f"Now extract the data from this email:\n<<<\n{email}\n>>>"
    )


def main():
    path = Path(__file__).parent / "order_email.txt"
    email = path.read_text(encoding="utf-8").strip()

    prompts = [
        ("ZERO-SHOT PROMPT", zero_shot_prompt(email)),
        ("FEW-SHOT PROMPT", few_shot_prompt(email)),
        ("CHAIN-OF-THOUGHT PROMPT", chain_of_thought_prompt(email)),
    ]
    for title, text in prompts:
        print("=" * 60)
        print(title)
        print("=" * 60)
        print(text)
        print()


if __name__ == "__main__":
    main()
