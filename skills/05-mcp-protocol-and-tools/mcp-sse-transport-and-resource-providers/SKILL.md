---
name: mcp-sse-transport-and-resource-providers
description: Architectural pattern for exposing Model Context Protocol (MCP) servers over HTTP using Server-Sent Events (SSE) and implementing dynamic Resource Providers.
version: 1.0.0
---

# MCP SSE Transport & Resource Providers

## Architectural Purpose
While the `stdio` transport is ideal for local, single-user desktop agents, enterprise applications require MCP servers to run remotely over HTTP. The Server-Sent Events (SSE) transport allows an MCP server to handle multiple concurrent clients. Additionally, the `Resource` pattern allows MCP servers to expose raw data streams (logs, files, DB tables) rather than just functional tools.

---

## 1. Core Pattern / Implementation

### Exposing a Resource
A Resource in MCP is identified by a URI template. It allows the LLM client to "read" data context directly without calling a parameterized tool.

```python
from mcp.server import Server
from mcp.types import Resource, TextContent

mcp_server = Server("telecom-logs-mcp")

@mcp_server.list_resources()
async def handle_list_resources() -> list[Resource]:
    return [
        Resource(
            uri="logs://billing/error.log",
            name="Billing Error Logs",
            mimeType="text/plain",
            description="Recent error logs for the telecom billing microservice"
        )
    ]

@mcp_server.read_resource()
async def handle_read_resource(uri: str) -> str:
    if uri == "logs://billing/error.log":
        # Simulate reading from AWS CloudWatch or local disk
        return "ERROR 2026-08-07: Insufficient balance for MSISDN +216..."
    raise ValueError(f"Resource {uri} not found")
```

---

## 2. Cost, Latency & Trade-offs
- **Token Math**: Resources can inject massive amounts of text into the LLM context window. Ensure the LLM client specifies truncation limits when reading resources.
- **Latency Penalty**: SSE requires establishing a persistent HTTP connection. Cloud load balancers (AWS ALB, NGINX) must be configured to support long-lived SSE connections without timing out prematurely (e.g., increase `proxy_read_timeout`).
- **Trade-off**: SSE is unidirectional (Server -> Client). The MCP standard uses a separate POST endpoint (`/messages`) for Client -> Server communication, requiring careful session mapping in the backend.

---

## 3. Verification Checklist
- [ ] SSE endpoints are secured behind an API Gateway enforcing Bearer token validation.
- [ ] Reverse proxies (NGINX/Traefik) have HTTP/2 enabled and timeouts extended for the `/sse` route.
- [ ] Resource URIs are strictly validated to prevent unauthorized access to internal host files.
