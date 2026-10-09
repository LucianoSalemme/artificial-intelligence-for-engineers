"""Chapter 17, listing "The ticketing MCP server, in brief":
the MCP adapter on top of the pure logic in ticket.py.

The two lessons of the listing: the idempotency key (derived from the
conversation thread_id) and the speaking errors, which explain the
alternatives to the model instead of raising an anonymous exception.

Note on the SDK: the import follows the book (from mcp.server import
MCPServer); with SDK versions that still expose FastMCP, adapt the
import as documented in the chapter 13 README.
"""

# ticket_server.py: MCP adapter on top of ticket.py.
from mcp.server import MCPServer
import ticket    # pure logic: create(), status(); unit tests

mcp = MCPServer("company-ticketing")

CATEGORIES = ("IT", "MAINTENANCE", "FACILITY")

@mcp.tool()
def open_ticket(category: str, summary: str,
                description: str, requester: str,
                key: str) -> dict[str, object]:
    """Opens an internal support ticket. Allowed
    categories: IT, MAINTENANCE, FACILITY. Operation with
    permanent effects: call it only after the user's
    explicit confirmation. 'key' is the idempotency
    identifier of the request."""
    if category not in CATEGORIES:
        return {"opened": False,
                "error": f"Category '{category}' is not "
                         "valid: use IT, MAINTENANCE "
                         "or FACILITY."}
    id_ = ticket.create(category, summary, description,
                        requester, key)
    return {"opened": True, "id": id_}

@mcp.tool()
def ticket_status(id: str) -> dict[str, object]:
    """Status and assignee of an existing ticket,
    given its identifier in the TCK-XXXX format."""
    data = ticket.status(id)
    if data is None:
        return {"found": False,
                "error": f"No ticket {id}: check "
                         "the TCK-XXXX format."}
    return {"found": True, **data}


if __name__ == "__main__":
    mcp.run()   # stdio transport, as in chapter 13
