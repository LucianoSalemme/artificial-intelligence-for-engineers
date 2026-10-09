"""Chat from Python with a local model served by Ollama.

Listing from chapter 7, section "Hands-on: a model on your own computer".
Requires Ollama running (the local server listens on port 11434) and the
model pulled with: ollama pull llama3.2
"""

import sys

import requests


def main():
    # the local Ollama server listens on port 11434
    try:
        response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": "llama3.2",
                "messages": [
                    {"role": "system",
                     "content": "You are a concise technical assistant."},
                    {"role": "user",
                     "content": "Explain in two sentences what quantization is."}
                ],
                "stream": False
            }
        )
    except requests.exceptions.ConnectionError:
        print("Could not reach Ollama at http://localhost:11434.")
        print("Install Ollama from https://ollama.com, then run:")
        print("  ollama pull llama3.2")
        print("and make sure the server is running (ollama serve).")
        sys.exit(1)

    print(response.json()["message"]["content"])


if __name__ == "__main__":
    main()
