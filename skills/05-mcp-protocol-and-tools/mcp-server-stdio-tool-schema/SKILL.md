---
format: "v2"
name: "mcp-server-stdio-tool-schema"
title: "Mcp Server Stdio Tool Schema"
title_fr: "MCP Server: stdio and Tool Schema"
description: "Protocol specifications and implementation patterns for Model Context Protocol (MCP) servers using stdio transport and JSON-Schema tools."
description_fr: "Spécifications du protocole et patterns d'implémentation pour les serveurs MCP (Model Context Protocol) utilisant le transport stdio et des outils décrits en JSON-Schema."
domain: "05-mcp-protocol-and-tools"
tags: [cybersecurity, engineering, best-practices]
maturity: "stable"
audience: ["backend-engineer", "security-engineer", "coding-agent"]
requires: ["bash", "git"]
updated: "2026-08-08"
---



## Prerequisites
- Target system, dependencies and environment configured.

## Usage
### Architectural Purpose
Model Context Protocol (MCP) standardizes how AI applications connect to external tools, databases, and context resources over a clean client-server interface (`stdio` or `SSE`).

---

### 1. Protocol Architecture

```text
+-------------------+                   +-------------------+
|    MCP Client     |   stdio / SSE     |    MCP Server     |
| (Claude Code/AGY) | <===============> | (DB / Tool Provider|
|                   |   JSON-RPC 2.0    |                   |
+-------------------+                   +-------------------+
```

---

### 2. Tool Definition Schema (JSON-RPC 2.0)

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

### 3. Engineering Best Practices

1. **Tool Granularity**: Make tool descriptions explicit and unambiguous. Tell the model when to use the tool and what parameters mean.
2. **Error Handling**: Return structured error responses inside `content` array (`isError: true`) instead of crashing the stdio process.
3. **Security**: Validate all incoming parameters against injection vulnerabilities. Enforce strict read-only execution by default.

## Inputs
- Relevant source code, logs, network traces, or system specifications.

## Outputs
- Analysis findings, security audit report, or generated code artifacts.