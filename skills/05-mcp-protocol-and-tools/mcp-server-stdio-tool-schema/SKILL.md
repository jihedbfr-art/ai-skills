---
name: mcp-server-stdio-tool-schema
description: Protocol specifications and implementation patterns for Model Context Protocol (MCP) servers using stdio transport and JSON-Schema tools.
version: 1.0.0
---

# MCP Server Architecture & Tool Schema

## Architectural Purpose
Model Context Protocol (MCP) standardizes how AI applications connect to external tools, databases, and context resources over a clean client-server interface (`stdio` or `SSE`).

---

## 1. Protocol Architecture

```text
+-------------------+                   +-------------------+
|    MCP Client     |   stdio / SSE     |    MCP Server     |
| (Claude Code/AGY) | <===============> | (DB / Tool Provider|
|                   |   JSON-RPC 2.0    |                   |
+-------------------+                   +-------------------+
```

---

## 2. Tool Definition Schema (JSON-RPC 2.0)

MCP tools are declared via standard `JSON-Schema`:

```json
{
  "name": "query_database",
  "description": "Executes a read-only SQL query against PostgreSQL database",
  "inputSchema": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "Valid SELECT SQL query string"
      },
      "maxRows": {
        "type": "integer",
        "default": 50,
        "description": "Maximum number of rows to return"
      }
    },
    "required": ["query"]
  }
}
```

---

## 3. Engineering Best Practices

1. **Tool Granularity**: Make tool descriptions explicit and unambiguous. Tell the model when to use the tool and what parameters mean.
2. **Error Handling**: Return structured error responses inside `content` array (`isError: true`) instead of crashing the stdio process.
3. **Security**: Validate all incoming parameters against injection vulnerabilities. Enforce strict read-only execution by default.
