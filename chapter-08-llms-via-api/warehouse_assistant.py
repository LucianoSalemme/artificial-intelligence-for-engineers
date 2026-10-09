"""Function calling: warehouse assistant over a SQLite database.

Chapter 8, section "Function calling": the section's two listings
(function + declaration, then the invocation loop) assembled
into a single program.
"""

import os
import sqlite3
import sys

from google import genai
from google.genai import types

if not (os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")):
    print("Missing environment variable GEMINI_API_KEY: create a free key "
          "at https://aistudio.google.com/apikey and then run "
          "export GEMINI_API_KEY=<your-key>")
    sys.exit(1)

MODEL = "gemini-2.5-flash"
client = genai.Client()


def item_stock(code: str) -> dict:
    """Reads the stock of an item from the warehouse database."""
    con = sqlite3.connect("warehouse.db")
    row = con.execute(
        "SELECT description, quantity, location "
        "FROM stock WHERE code = ?", (code,)).fetchone()
    con.close()
    if row is None:
        # READABLE error: the model will see it and can react
        return {"error": f"no item with code {code}"}
    return {"description": row[0],
            "quantity": row[1],
            "location": row[2]}

declaration = types.FunctionDeclaration(
    name="item_stock",
    description=("Returns description, available quantity and "
                 "location of a warehouse item given its code."),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "code": types.Schema(
                type=types.Type.STRING,
                description="item code, for example VLV-2041"),
        },
        required=["code"],
    ),
)
tools = [types.Tool(function_declarations=[declaration])]

FUNCTIONS = {"item_stock": item_stock}

def warehouse_assistant(question: str) -> str:
    contents = [types.Content(
        role="user", parts=[types.Part.from_text(text=question)])]
    config = types.GenerateContentConfig(
        system_instruction=(
            "You are the warehouse assistant. For any stock data "
            "ALWAYS use the tool: never answer from memory."),
        tools=tools,
        temperature=0.0,
    )

    while True:
        response = client.models.generate_content(
            model=MODEL, contents=contents, config=config)
        # the response (text OR invocation requests) goes into the history
        contents.append(response.candidates[0].content)

        if not response.function_calls:
            return response.text   # no call: this is the final answer

        parts = []
        for call in response.function_calls:
            function = FUNCTIONS[call.name]
            try:
                result = function(**call.args)
            except Exception as error:
                result = {"error": str(error)}
            parts.append(types.Part.from_function_response(
                name=call.name, response=result))
        contents.append(types.Content(role="user", parts=parts))


def prepare_database() -> None:
    """Creates warehouse.db with the sample data cited in the chapter."""
    con = sqlite3.connect("warehouse.db")
    con.execute(
        "CREATE TABLE IF NOT EXISTS stock ("
        "code TEXT PRIMARY KEY, description TEXT, "
        "quantity INTEGER, location TEXT)")
    con.execute(
        "INSERT OR IGNORE INTO stock VALUES (?, ?, ?, ?)",
        ("VLV-2041", "2-inch ball valve", 42, "aisle B3"))
    con.commit()
    con.close()


if __name__ == "__main__":
    prepare_database()
    print(warehouse_assistant(
        "How many VLV-2041 do we have, and where are they?"))
