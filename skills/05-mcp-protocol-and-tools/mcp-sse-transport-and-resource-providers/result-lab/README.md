# Offline lab: classify an MCP tool response

[Version française](README.fr.md)

Predict the outcome of each fixture before running it. Python 3.9 or later is enough; the lab uses the standard library and makes no network request. All six fixtures are synthetic.

From the repository root:

```bash
cd skills/05-mcp-protocol-and-tools/mcp-sse-transport-and-resource-providers/result-lab
python classify_result.py fixtures/success.json
python -m unittest -v
```

The first command prints only:

```json
{"classification": "candidate_success", "exit_code": 0}
```

## Exercises and expected results

Replace the fixture argument to inspect each case. Exit codes 1 and 2 are expected outcomes for the corresponding examples, not a broken Python installation.

| Fixture | Classification | Exit code | Lesson |
|---|---|---:|---|
| `success.json` | `candidate_success` | 0 | A text result can be considered for further validation |
| `tool-error.json` | `tool_error` | 1 | Read `result.isError`; an HTTP success alone would miss this failure |
| `protocol-error.json` | `protocol_error` | 2 | The envelope has an error instead of a tool result |
| `invalid-flag.json` | `invalid_response` | 2 | The string `"false"` is not the boolean `false` |
| `mixed-envelope.json` | `invalid_response` | 2 | An envelope cannot claim both result and error |
| `untrusted-content.json` | `candidate_success` | 0 | Accepted structure does not make embedded instructions trustworthy |

For the last case, explain why the content must stay data and cannot grant permission to change an access policy. Do not execute the instruction in the fixture. Then change an `isError` value locally and predict the classification before rerunning the command.

## Scope of the teaching script

This is a small classifier for JSON-RPC envelopes containing text-only tool results. It rejects several malformed shapes, declines structured or non-text results, and summarizes errors without echoing the payload or file path. Missing `isError` is treated as false in this exercise.

It is not a complete JSON-RPC or MCP validator, a client, an SSE decoder, or a prompt-injection detector. It does not correlate response IDs, check an output schema, validate authentication, or authorize an action. A non-text or structured result needs the appropriate SDK/schema handling rather than being declared invalid simply because this lab declines it. Use only the provided synthetic inputs for the exercises.

The six standard-library tests exercise fixture outcomes, malformed structures, unsupported content, the optional error flag, exit codes and output privacy. For a real connection, return to the [preflight guide](../connection-preflight.md). Protocol references: [MCP tool errors](https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling) and the [JSON-RPC response object](https://www.jsonrpc.org/specification#response_object).

---

<div align="center">
  <img src="../../../../assets/brand/jihedailabs-logo.svg" alt="JihedAiLabs" width="120">
  <br>
  <sub>A <a href="https://github.com/jihedbfr-art"><b>JihedAiLabs</b></a> project</sub>
</div>
