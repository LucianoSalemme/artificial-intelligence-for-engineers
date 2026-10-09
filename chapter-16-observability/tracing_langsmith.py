"""LangSmith instrumentation for the chapter 11 RAG.

Chapter 16, section "Tracing": the @traceable decorator applied to
the pipeline. As in the book, the bodies of rewrite and answer are
omitted because they are identical to chapter 11: the listing shows
the instrumentation, not the pipeline. Activation happens through
environment variables, without touching the code:

    export LANGSMITH_TRACING=true
    export LANGSMITH_API_KEY=...
    export LANGSMITH_PROJECT=acme-assistant
"""

# pip install langsmith
from langsmith import traceable

TOP_K = 5       # from the chapter 11 RAG
engine = None   # the in-memory search engine from chapter 11


@traceable(run_type="llm", name="rewrite")
def rewrite(question, history=""):
    ...   # body identical to chapter 11


@traceable(run_type="retriever", name="search")
def search(query, k=TOP_K):
    return engine.search(query, k)


@traceable(name="answer")   # chain-type run
def answer(question, history=""):
    ...   # body identical to chapter 11


if __name__ == "__main__":
    import os
    import sys
    if not os.environ.get("LANGSMITH_API_KEY"):
        print("Missing environment variable LANGSMITH_API_KEY: create a "
              "key at https://smith.langchain.com (Settings -> API Keys) "
              "and set LANGSMITH_TRACING=true, LANGSMITH_API_KEY and "
              "LANGSMITH_PROJECT as shown in the chapter.")
        sys.exit(1)
    print("Instrumentation ready: every call to answer produces a "
          "tree of traces in the configured project. For complete "
          "traces the bodies of rewrite and answer must be taken from "
          "the chapter 11 code (code/chapter-11-rag/full_rag.py).")
