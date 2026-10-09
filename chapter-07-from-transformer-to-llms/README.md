# Chapter 7 - From Transformer to LLMs

Code and materials for the listings of chapter 7, dedicated to the life cycle of an LLM (pretraining, instruction tuning, alignment, LoRA, quantization) and to the hands-on run of an open model locally with Ollama.

## Files

| File | Description |
|---|---|
| `chat_template_example.txt` | Example of a dialogue serialized in the chat template, with the `system`, `user`, and `assistant` roles and the special delimiter tokens. It is not executable code: it shows the format into which the server converts the messages before handing them to the model. Section "Chat formats". |
| `ollama_commands.sh` | The two terminal commands to pull (`ollama pull llama3.2`) and start an interactive chat (`ollama run llama3.2`) with a local quantized model. Section "Hands-on: a model on your own computer". |
| `local_ollama_chat.py` | Python script that chats with the local model through the Ollama HTTP server on port 11434, using the `system` and `user` roles seen in instruction tuning. Section "Hands-on: a model on your own computer". |

## How to run

Common prerequisite: [Ollama](https://ollama.com) installed on your machine (Linux, macOS, or Windows). No API keys or cloud connection are needed: everything runs locally.

1. Pull the model and try the chat from the terminal:

   ```bash
   sh ollama_commands.sh
   ```

   or run the two commands by hand. The download is about 2 GB (int4 quantized model in GGUF format).

2. Chat with the model from Python (the Ollama server must be running):

   ```bash
   pip install requests
   python3 local_ollama_chat.py
   ```

   If the server is not reachable, the script prints the instructions to start it and exits with code 1.

## Dependencies

- Python 3.12
- pip package: `requests`
- Ollama installed and running, with the `llama3.2` model pulled (about 2 GB on disk)
