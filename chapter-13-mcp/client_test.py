# client_test.py: exercises the server over the protocol,
# with no external processes and no model at all.
import asyncio
from mcp import Client

from server import mcp   # our MCPServer

async def main():
    async with Client(mcp) as client:
        # 1. Does the server expose what it should?
        listing = await client.list_tools()
        names = [t.name for t in listing.tools]
        assert "order_status" in names
        assert "open_complaint" in names

        # 2. Does the happy path return the right data?
        r = await client.call_tool("order_status",
                                   {"number": "ORD-1042"})
        assert r.structured_content["found"] is True
        assert r.structured_content["status"] == "shipped"

        # 3. Is the error case informative?
        r = await client.call_tool("order_status",
                                   {"number": "ORD-9999"})
        assert r.structured_content["found"] is False
        assert "customer_orders" in \
            r.structured_content["error"]

        print("All checks passed.")

asyncio.run(main())
