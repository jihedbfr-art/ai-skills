---
name: mcp-python-server-fastapi
description: Architectural pattern for building custom Model Context Protocol (MCP) servers using Python, SSE transport, and FastAPI for enterprise integrations.
version: 1.0.0
---

# Custom MCP Server with Python & FastAPI

## Architectural Purpose
Building custom MCP servers enables AI agents (like Claude or Antigravity) to access proprietary enterprise data and internal APIs securely. While `stdio` is great for local CLI tools, Server-Sent Events (SSE) via FastAPI allows hosting remote, scalable MCP providers for cloud-based agents.

---

## 1. Core Pattern / Implementation

Using the official `mcp` Python SDK:

```python
from fastapi import FastAPI
from mcp.server.sse import SseServerTransport
from mcp.server import Server
from contextlib import asynccontextmanager

app = FastAPI()
mcp_server = Server("enterprise-crm-mcp")

@mcp_server.tool()
async def get_customer_data(customer_id: str) -> str:
    """Retrieve secure customer billing data from internal CRM."""
    # Internal API call simulated
    return f"Customer {customer_id} has active enterprise tier."

@app.get("/sse")
async def handle_sse():
    transport = SseServerTransport("/messages")
    await mcp_server.connect(transport)
    return transport.response
```

---

## 2. Cost, Latency & Trade-offs
- **Token Math**: Tool schemas (JSON schema) consume ~100-300 input tokens per tool. Keep descriptions concise.
- **Latency Penalty**: SSE connection setup adds ~150ms TTFT overhead on the first interaction, but subsequent tool calls are persistent.
- **Trade-off**: SSE requires open ports and authentication (Bearer tokens), unlike `stdio` which runs in the local process sandbox.

---

## 3. Verification Checklist
- [ ] Tool definitions include rich docstrings (used for `description` in schema).
- [ ] SSE transport is secured via standard OAuth2/Bearer token middleware in FastAPI.
- [ ] Inputs are validated against prompt injection before executing destructive SQL/API calls.
