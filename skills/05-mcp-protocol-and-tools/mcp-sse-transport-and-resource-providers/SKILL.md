---
format: "v2"
name: "mcp-sse-transport-and-resource-providers"
title: "MCP SSE Transport and Resource Providers"
title_fr: "Transport SSE MCP et fournisseurs de ressources"
description: "Use when diagnosing an MCP connection: identify its transport and verify caller isolation and tool errors before connecting an agent."
description_fr: "À utiliser pour diagnostiquer une connexion MCP : identifier son transport et vérifier l'isolation des appelants et les erreurs d'outils avant de connecter un agent."
domain: "05-mcp-protocol-and-tools"
tags: [cybersecurity, engineering, best-practices]
maturity: "stable"
audience: ["backend-engineer", "security-engineer", "coding-agent"]
requires: ["bash", "git"]
updated: "2026-10-15"
---



## Prerequisites
- Target system, dependencies and environment configured.

## Usage
### Architectural Purpose
Use the [offline response lab](result-lab/README.md), also available in [French](result-lab/README.fr.md), to practice result classification before testing a live connection. Its output is a teaching classification, never an authorization decision.

Version scope: the implementation below is a legacy SSE sketch, not a current SDK compatibility claim. MCP 2025-11-25 defines stdio and Streamable HTTP; the old two-endpoint HTTP+SSE transport belongs to the 2024-11-05 protocol. Do not infer a transport from the presence of SSE alone. Use the [connection preflight](connection-preflight.md) and its [French version](connection-preflight.fr.md) before connecting an agent. The [transport specification](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports) defines the distinction.

Local stdio servers run as subprocesses. For a remote deployment, select the HTTP transport supported by the server and client. Resource providers expose named data alongside tools. The legacy example below illustrates that resource pattern; check its SDK API before reusing it.

---

### 1. Core Pattern / Implementation

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

### 2. Cost, Latency & Trade-offs
- **Token Math**: Resources can inject massive amounts of text into the LLM context window. Ensure the LLM client specifies truncation limits when reading resources.
- **Latency Penalty**: SSE requires establishing a persistent HTTP connection. Cloud load balancers (AWS ALB, NGINX) must be configured to support long-lived SSE connections without timing out prematurely (e.g., increase `proxy_read_timeout`).
- **Trade-off**: SSE is unidirectional (Server -> Client). The MCP standard uses a separate POST endpoint (`/messages`) for Client -> Server communication, requiring careful session mapping in the backend.

---

### 3. Verification Checklist
- [ ] SSE endpoints are secured behind an API Gateway enforcing Bearer token validation.
- [ ] Reverse proxies (NGINX/Traefik) have HTTP/2 enabled and timeouts extended for the `/sse` route.
- [ ] Resource URIs are strictly validated to prevent unauthorized access to internal host files.

## Inputs
- Relevant source code, logs, network traces, or system specifications.

## Outputs
- Analysis findings, security audit report, or generated code artifacts.
