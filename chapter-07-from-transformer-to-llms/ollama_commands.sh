#!/bin/sh
# Commands shown in chapter 7, section "Hands-on: a model on your own
# computer". They require Ollama installed (https://ollama.com).

# pull the model (about 2 GB, int4 quantized)
ollama pull llama3.2

# start an interactive chat in the terminal
ollama run llama3.2
