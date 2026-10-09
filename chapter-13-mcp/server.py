# server.py: the MCP layer on top of the logic in orders.py.
from mcp.server import MCPServer

import orders

mcp = MCPServer("acme-orders")

@mcp.tool()
def order_status(number: str) -> dict[str, object]:
    """Return the status, customer, total, and last update date
    of an order given its number, in the ORD-XXXX format. Use it
    when the user asks about a specific order."""
    conn = orders.open_connection()
    try:
        data = orders.order_status(conn, number)
    finally:
        conn.close()
    if data is None:
        # Informative runtime error: the model reads it,
        # understands it, and can correct itself (chapter 12).
        return {"found": False,
                "error": f"No order with number {number}. "
                         "Check the ORD-XXXX format or search "
                         "by customer with customer_orders."}
    return {"found": True, **data}

@mcp.tool()
def customer_orders(customer: str, limit: int = 10) -> list[dict]:
    """List a customer's most recent orders, searched by name
    (partial match allowed). Return at most 'limit' orders with
    number, status, and total."""
    conn = orders.open_connection()
    try:
        return orders.orders_for(conn, customer, limit)
    finally:
        conn.close()

@mcp.tool()
def open_complaint(order_number: str,
                   reason: str) -> dict[str, object]:
    """Open a formal complaint on an order. This operation has
    permanent effects: use it only after the user has explicitly
    confirmed they want to proceed."""
    conn = orders.open_connection()
    try:
        if orders.order_status(conn, order_number) is None:
            return {"opened": False,
                    "error": f"Order {order_number} does not "
                             "exist: no complaint opened."}
        complaint_id = orders.open_complaint(conn, order_number,
                                             reason)
    finally:
        conn.close()
    return {"opened": True, "complaint_id": complaint_id}

@mcp.resource("orders://schema")
def database_schema() -> str:
    """Schema of the orders database: tables, fields, and the
    possible statuses of an order."""
    return orders.SCHEMA

@mcp.prompt(title="Complaint handling")
def complaint_handling(order_number: str) -> str:
    """Instruct the assistant on the ACME complaint policy."""
    return (f"Handle a complaint for order {order_number} "
            "following the ACME policy: 1) check the status "
            "with the order_status tool; 2) if it was delivered "
            "more than 30 days ago, explain that the complaint "
            "must be forwarded to after-sales support; "
            "3) otherwise summarize the problem for the user, "
            "ask for explicit confirmation, and only then use "
            "open_complaint.")

if __name__ == "__main__":
    mcp.run()   # communication over stdio; the server is now listening
