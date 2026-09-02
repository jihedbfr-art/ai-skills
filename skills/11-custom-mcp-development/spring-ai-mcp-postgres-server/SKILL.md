---
format: "v2"
name: "spring-ai-mcp-postgres-server"
title: "An MCP Server over PostgreSQL with Spring AI"
title_fr: "Un serveur MCP sur PostgreSQL avec Spring AI"
description: "Exposing PostgreSQL to an agent as MCP tools from a Spring Boot application, with the read-only boundary enforced in the tool rather than trusted to the prompt."
description_fr: "Exposer PostgreSQL à un agent sous forme d'outils MCP depuis une application Spring Boot, avec la frontière lecture seule appliquée dans l'outil plutôt que confiée au prompt."
domain: "11-custom-mcp-development"
tags: [mcp, spring-ai, postgres, java, engineering]
maturity: "stable"
audience: ["backend-engineer", "security-engineer", "coding-agent"]
requires: ["java", "maven", "postgresql"]
updated: "2026-09-02"
---

## Prerequisites
- Java 17, a Spring Boot 3.2.x application, and a reachable PostgreSQL instance.
- A database role scoped to exactly what the agent may see. The tool boundary is the last line of defence, not the first.

## Usage

### Architectural Context

The Model Context Protocol (MCP) standardizes how autonomous agents connect to external data and tools. Spring AI dramatically simplifies MCP server creation by eliminating boilerplate JSON schema generation. By using `@McpTool` and `@McpResource`, you expose Java methods directly to agents.

### 1. Execution Directives (Agent Instructions)

When an agent needs to query or mutate the underlying PostgreSQL database, it must adhere to the following:
1. **Discover Tools:** Use standard MCP handshakes to retrieve the tool list.
2. **Read-Only First:** Always prefer read-only queries before attempting mutations.
3. **Structured Outputs:** Ensure the agent parses the JSON-RPC response strictly according to the generated schema.

### 2. Spring Boot Implementation

The accompanying `examples/spring-mcp-postgres` Maven project demonstrates this architecture.

#### The MCP Tool Configuration

The `@McpTool` annotation instructs Spring AI to automatically generate the JSON schema for the LLM.

```java
import org.springframework.ai.mcp.annotation.McpTool;
import org.springframework.ai.mcp.annotation.McpToolParam;
import org.springframework.stereotype.Service;

@Service
public class CustomerMcpService {
    
    private final CustomerRepository repository;

    public CustomerMcpService(CustomerRepository repository) {
        this.repository = repository;
    }

    @McpTool(description = "Retrieves a customer's profile by their unique email address. Use this to lookup billing or contact info.")
    public CustomerProfile getCustomerByEmail(
        @McpToolParam(description = "The exact email address of the customer") String email) {
        return repository.findByEmail(email)
            .orElseThrow(() -> new RuntimeException("Customer not found"));
    }
}
```

### 3. Function Calling Schema

When Spring AI starts, it generates the following JSON schema exposed via the MCP protocol. Agents will ingest this automatically.

```json
{
  "name": "getCustomerByEmail",
  "description": "Retrieves a customer's profile by their unique email address. Use this to lookup billing or contact info.",
  "parameters": {
    "type": "object",
    "properties": {
      "email": {
        "type": "string",
        "description": "The exact email address of the customer"
      }
    },
    "required": ["email"]
  }
}
```

### 4. Deployment Hook

```bash
# build_mcp_server.sh
cd examples/spring-mcp-postgres
mvn clean package -DskipTests
java -jar target/spring-mcp-postgres-0.1.0.jar --spring.profiles.active=prod
```

---
*Architected for the autonomous enterprise. A JihedAiLabs project.*

## Inputs
- The repository methods to expose, and the schema the agent is allowed to reach.

## Outputs
- An MCP server speaking stdio, with each exposed method described as a typed tool.
