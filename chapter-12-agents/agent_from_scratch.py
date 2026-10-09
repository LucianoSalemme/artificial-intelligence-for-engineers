"""A complete agent written from scratch, with no framework.

Tool registry, budget, session memory and loop,
plus a test with a fake model that replays a script:
it runs in a millisecond, with no API key.

Chapter 12, section "Code: an agent from scratch".
"""

from dataclasses import dataclass
from typing import Callable


@dataclass
class Tool:
    """Declaration plus runnable function."""
    name: str
    description: str
    parameters: dict           # JSON Schema of the arguments
    run: Callable[..., dict]
    write: bool = False        # True if it changes the world


class Registry:
    def __init__(self, tools):
        self._tools = {t.name: t for t in tools}

    def declarations(self):
        return [{"name": t.name, "description": t.description,
                 "parameters": t.parameters}
                for t in self._tools.values()]

    def requires_confirmation(self, name):
        t = self._tools.get(name)
        return t is not None and t.write

    def run(self, name, arguments):
        t = self._tools.get(name)
        # every error is a message FOR THE MODEL:
        # it must explain what to do next
        if t is None:
            return {"error": f"tool '{name}' does not exist; "
                    f"available: {sorted(self._tools)}"}
        try:
            return t.run(**arguments)
        except TypeError as e:
            return {"error": f"invalid arguments "
                             f"for {name}: {e}"}
        except Exception as e:
            return {"error": f"{name} failed: {e}"}


@dataclass
class Budget:
    """The guarantee that the agent terminates by construction."""
    max_turns: int = 12
    max_actions: int = 24
    turns: int = 0
    actions: int = 0

    def allows_turn(self):
        return self.turns < self.max_turns

    def allows_action(self):
        return self.actions < self.max_actions


class Memory:
    """Session history, provider-neutral."""
    def __init__(self, threshold=60):
        self._messages = []
        self._threshold = threshold

    def add(self, message):
        self._messages.append(message)

    def messages(self):
        if len(self._messages) <= self._threshold:
            return list(self._messages)
        # minimal compaction: task + recent tail.
        # A mature version would summarize the discarded
        # part here with a dedicated model call.
        return [self._messages[0],
                {"role": "user", "text":
                 "[history truncated: old turns omitted]"},
                *self._messages[-(self._threshold - 2):]]


@dataclass
class Response:
    text: str | None   # final answer, if the work is done
    calls: list        # [(name, arguments), ...] otherwise


def run_agent(task, model, registry, budget,
              confirm=lambda name, arguments: True):
    memory = Memory()
    memory.add({"role": "user", "text": task})

    while budget.allows_turn():
        budget.turns += 1
        # observe and reason: one model call
        r = model.generate(memory.messages(),
                           registry.declarations())
        memory.add({"role": "assistant",
                    "text": r.text,
                    "calls": r.calls})
        # no action requested: the work is done
        if not r.calls:
            return r.text or "(no response)"

        # act: every request goes through the guardrails
        for name, arguments in r.calls:
            if not budget.allows_action():
                result = {"error":
                          "action budget exhausted: wrap up "
                          "and report the status of the work"}
            elif (registry.requires_confirmation(name)
                  and not confirm(name, arguments)):
                result = {"error":
                          "action rejected by the operator"}
            else:
                budget.actions += 1
                result = registry.run(name, arguments)
            memory.add({"role": "tool",
                        "name": name, "result": result})

    return ("Stopped: turn budget exhausted. "
            "Memory holds the full trajectory.")


class FakeModel:
    """Replays a script: tests the loop without an API."""
    def __init__(self, script):
        self._script = list(script)

    def generate(self, messages, declarations):
        return self._script.pop(0)


# two fake tools over in-memory data
def search_orders(status, min_days=0):
    return {"orders": [{"id": "ORD-1207",
                        "supplier_id": "F-031",
                        "days_blocked": 12}]}


def prepare_reminder(order_id, recipient, body):
    return {"status": "draft created", "draft_id": "BZ-1"}


# abbreviated schemas for the test: the full ones are
# written as in the tool design section
SCHEMA = {"type": "object"}

registry = Registry([
    Tool("search_orders",
         "Search orders by status and age.",
         SCHEMA, search_orders),
    Tool("prepare_reminder",
         "Create the DRAFT of a reminder (does not send).",
         SCHEMA, prepare_reminder,
         write=True),
])


if __name__ == "__main__":
    script = [
        Response(None, [("search_orders",
                         {"status": "blocked", "min_days": 7})]),
        Response(None, [("prepare_reminder",
                         {"order_id": "ORD-1207",
                          "recipient": "orders@rossi.it",
                          "body": "Dear supplier, ..."})]),
        Response("Draft BZ-1 ready for ORD-1207.", []),
    ]

    budget = Budget(max_turns=5)
    result = run_agent("Prepare the reminders.",
                       FakeModel(script), registry, budget)
    print(result)                # Draft BZ-1 ready for ORD-1207.
    assert budget.turns == 3 and budget.actions == 2
