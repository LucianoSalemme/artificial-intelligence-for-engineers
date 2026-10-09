# Chapter 13 - The Model Context Protocol

Code for the chapter 13 guided project: an MCP server for the orders database of ACME Inc., built with the official Python SDK and tested without any model.

## Files

| File | Description |
|------|-------------|
| `orders.py` | Pure data-access module, with no dependency on MCP. Section "Building an MCP server". |
| `server.py` | The two `server.py` listings assembled into a single file: the `order_status` and `customer_orders` tools, then `open_complaint`, the `orders://schema` resource, and the `complaint_handling` prompt. Section "The MCP layer". |
| `client_test.py` | In-memory MCP client that checks the tools, the happy path, and the error case. Section "Testing, without a model". |
| `seed_data.py` | Fills `orders.db` with the sample data from the text (three sample orders, including ORD-1042 from Rossi Ltd in the shipped status). Section "Testing, without a model". |
| `claude_desktop_config.json` | Example configuration of a host (Claude Desktop) to launch the server over stdio; adapt it with the real absolute path to `server.py`. Section "Testing, without a model". |

The chapter listings that are transcripts of JSON-RPC messages (the `initialize` handshake, `tools/list`, `tools/call`, `resources/read`, `prompts/get`) and the tool poisoning example from the security section are illustrative material, not runnable files, and are not reproduced here.

## Requirements

- Python 3.12
- MCP Python SDK: `pip install "mcp[cli]"` (the `cli` extra adds the `mcp` command, used by the Inspector)
- No API key: all testing runs without models

Naming note (from the chapter): the SDK's high-level API was born under the name `FastMCP`; in version 2 of the SDK the class is named `MCPServer`, but the programming model is the same. If your SDK version still uses `FastMCP`, adapt the import in `server.py`.

## How to run

1. Populate the test database (creates `orders.db` in the current directory):

       python3 seed_data.py

2. Test over the protocol, with the in-memory client:

       python3 client_test.py

   Expected: `All checks passed.`

3. Exploration with the MCP Inspector (requires Node.js):

       mcp dev server.py

4. Start the server over stdio (normally the host launches it):

       python3 server.py

   To expose it over the network: `mcp.run(transport="streamable-http", port=3001)` instead of `mcp.run()`.

5. Hooking it up to Claude Desktop: copy the block from `claude_desktop_config.json` into the host configuration, with the absolute path to `server.py`.
