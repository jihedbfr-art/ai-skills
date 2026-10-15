# Check an MCP connection before giving an agent tools

[Version française](connection-preflight.fr.md)

Record the server commit, SDK version, protocol version and transport first. A working HTTP health endpoint says nothing about tool authorization. A successful connection also says nothing about the quality of a tool result.

## Establish the transport

For protocol 2025-11-25, distinguish stdio from Streamable HTTP. SSE can carry a Streamable HTTP response; it does not by itself identify the older two-endpoint transport. In the tested MCP Guard snapshot, the legacy connection uses `/sse` and `/mcp/message`; posting to `/mcp` is not its call path.

Use the endpoint documented by the server and an MCP client that negotiates its supported version. For stdio, inspect the launch command, working directory and environment; protocol messages belong on stdout and diagnostics on stderr.

## Record each boundary separately

| Check | Evidence to retain |
|---|---|
| Initialize and discover tools | Negotiated version and tool names; redact credentials |
| Validate arguments | A valid input and an invalid input with an explicit result |
| Read a result | JSON-RPC errors and `result.isError` are checked before using content |
| Exercise permissions | A denied call fails at the server even if the agent requests it |
| Separate callers | A reader stays denied after an admin call and during concurrent clients |
| Bound retries | Timeouts and denial are surfaced; no automatic replay of a side effect |

Test side-effecting tools with an inert fixture or a disposable resource. Record the action that occurred as well as the response. A timeout leaves the outcome uncertain; determine whether the operation ran before retrying.

## Replay the verified reference

Java 17, Maven and Docker are required. Use a new checkout:

```bash
git clone https://github.com/jihedbfr-art/mcp-keycloak-guard.git
cd mcp-keycloak-guard
git checkout 177fdef
mvn verify
```

The five integration tests at this snapshot were replayed locally on 14 October 2026. They cover unauthenticated and invalid-token requests, a caller without MCP roles, reader/admin tool results and concurrent caller isolation. The reader's admin-tool refusal is an MCP tool error, not an assumption about an HTTP 403 response. These tests do not establish audience rejection, downstream token isolation or Streamable HTTP support.

## Sources and cost

Practice result interpretation in the [offline response lab](result-lab/README.md): six synthetic fixtures and a standard-library Python classifier. Its `candidate_success` result is not permission to execute the received content. The lab deliberately separates a correctly shaped response from a trusted result.

Use [MCP transports](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports) for protocol scope and [tool error handling](https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) for result interpretation. The reference [PR](https://github.com/jihedbfr-art/mcp-keycloak-guard/pull/1) is not a published release. A local Docker test is slower than a schema check, but it exercises authentication and asynchronous invocation together. Repeat it when those boundaries change; keep a small inert check for routine connection validation.

---

<div align="center">
  <img src="../../../assets/brand/jihedailabs-logo.svg" alt="JihedAiLabs" width="120">
  <br>
  <sub>A <a href="https://github.com/jihedbfr-art"><b>JihedAiLabs</b></a> project</sub>
</div>
