"""Stub of the chapter 11 RAG pipeline: fixed answer with a citation.

In the real system this module is the chapter 11 project
(code/chapter-11-rag/full_rag.py) applied to the company hybrid
index, with the filter on the user's permissions.
"""


def answer(question: str, user: str, model: str):
    text = ("The reimbursement for using your personal car is "
            "0.42 euros per kilometer [1]. "
            "(stub answer, not from a model)")
    excerpts = [{"id": "Travel policy - Art. 4"}]
    return text, excerpts
