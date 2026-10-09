# Chapter 12 - Agents

Code for Chapter 12 of "Artificial Intelligence for Engineers": an agent built from scratch, with no framework, with a tool registry, budget, memory, loop and an adapter for the real model.

## Files

| File | Description |
|---|---|
| `tool_design_declarations.py` | The two tool declarations side by side: the bad one (`query`) and the good one (`search_orders`). Section "Tool design". |
| `skills/supplier-reminders/SKILL.md` | The reminders skill as a real file, with YAML frontmatter and a procedure. Section "Skills: procedural knowledge on demand". |
| `skills/supplier-reminders/reminder_template.md` | The template referenced at step 3 of the skill. Section "Skills: procedural knowledge on demand". |
| `agent_from_scratch.py` | The core of the agent assembled in order: `Tool` and `Registry`, `Budget`, `Memory`, `Response`, the `run_agent` loop and the test with `FakeModel` that replays a script. Section "Code: an agent from scratch". |
| `gemini_agent.py` | The `GeminiModel` adapter between the neutral format and google-genai, with console human confirmation for write tools. Section "Code: an agent from scratch". |

The two listings of the reminder trajectory (turns 1-4, section "The agentic loop") are transcripts of the exchange between model and tools, not code: they are not reproduced as files.

## How to run

Without credentials, the loop test with the fake model:

```bash
python3 agent_from_scratch.py
```

It prints `Draft BZ-1 ready for ORD-1207.` and checks with an assert that the budget counts 3 turns and 2 actions.

The declarations from the tool design section:

```bash
python3 tool_design_declarations.py
```

The agent with the real model (requires the API key and the `google-genai` package):

```bash
pip install google-genai
export GEMINI_API_KEY=<your-key>   # https://aistudio.google.com/apikey
python3 gemini_agent.py
```

Before every `prepare_reminder` the console asks for confirmation, because the tool is marked `write=True`. As an alternative to the key, the client can be created on Vertex AI as in Chapter 8: `genai.Client(vertexai=True, project="...", location="...")`.

## Dependencies

- Python 3.12
- `agent_from_scratch.py` and `tool_design_declarations.py`: standard library only, no credentials.
- `gemini_agent.py`: the `google-genai` package and the `GEMINI_API_KEY` (or `GOOGLE_API_KEY`) environment variable.
