"""The orchestration test described in chapter 17: the graph runs end to
end with the stubs and the assert on the `steps` trace protects topology
and routing in continuous integration, without an API key.

Run:  python orchestration_test.py
"""

from langgraph.types import Command

from assistant import graph


def run(request: str, user: str, thread: str):
    cfg = {"configurable": {"thread_id": thread}}
    fin = graph.invoke({"request": request, "user": user,
                        "steps": []}, cfg)
    return fin, cfg


# 1) Document request: router -> search.
fin, _ = run("What is the procedure for mileage reimbursement?",
             "john.doe", "t1")
assert fin["steps"] == ["router -> SIMPLE", "search"], fin["steps"]
assert fin["sources"] == ["Travel policy - Art. 4"]
print("document ok:", fin["steps"])

# 2) Action with a write: router -> operational -> interrupt -> confirm.
fin, cfg = run("Open a ticket: the monitor is broken",
               "john.doe", "t2")
assert fin["steps"] == ["router -> ACTION", "operational: proposal"], \
    fin["steps"]
# The graph is suspended on the interrupt(): the proposal awaits approval.
fin = graph.invoke(Command(resume="yes"), cfg)
assert fin["action_result"].startswith("opened ticket TCK-"), \
    fin["action_result"]
print("action ok:", fin["steps"], "->", fin["action_result"])

# 3) Out of scope: the router replies with the courtesy formula.
fin, _ = run("What's the weather tomorrow?", "john.doe", "t3")
assert fin["steps"] == ["router -> OUT"], fin["steps"]
assert fin["answer"].startswith("I can help")
print("out of scope ok:", fin["steps"])

# 4) Idempotency: same key, same ticket (no duplicate).
import ticket
a = ticket.create("IT", "r", "d", "john.doe", "key-x")
b = ticket.create("IT", "r", "d", "john.doe", "key-x")
assert a == b
print("idempotency ok:", a, "==", b)

print("Orchestration test passed.")
