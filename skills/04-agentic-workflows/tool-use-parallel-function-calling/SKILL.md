---
format: "v2"
name: "tool-use-parallel-function-calling"
title: "Tool Use Parallel Function Calling"
title_fr: "Appels d'Outils en Parallèle"
description: "Dispatching multiple independent tool calls from a single LLM turn concurrently instead of sequentially, to cut end-to-end agent latency."
description_fr: "Distribuer plusieurs appels d'outils indépendants issus d'un même tour LLM de manière concurrente plutôt que séquentielle, pour réduire la latence globale de l'agent."
domain: "04-agentic-workflows"
tags: [agents, tool-use, engineering, performance]
maturity: "stable"
audience: ["backend-engineer", "ai-engineer", "coding-agent"]
requires: ["bash", "python"]
updated: "2026-08-25"
---



## Prerequisites
- Tool definitions with independent side effects (no ordering dependency between calls in the same batch).
- An async-capable execution layer (asyncio, virtual threads, or a task queue).

## Usage
### Architectural Purpose
Modern tool-calling models can emit several tool calls in one turn instead of one at a time. Executing them sequentially wastes wall-clock time when the calls do not depend on each other's results (e.g. "get weather in Paris" and "get weather in Tokyo"). Parallel dispatch collapses N sequential round-trips into a single fan-out/fan-in step.

---

### 1. Sequential vs Parallel Timeline

```text
Sequential (3 independent tool calls, ~400ms each):
[LLM turn] -> [call A 400ms] -> [call B 400ms] -> [call C 400ms] -> [LLM turn]
Total tool time: ~1200ms

Parallel:
[LLM turn] -> [call A | call B | call C]  (concurrent, bounded by slowest = 400ms)
             -> [LLM turn]
Total tool time: ~400ms
```

---

### 2. Dispatch and Result Reassembly

```python
import asyncio

async def dispatch_tool_calls(tool_calls: list[dict], registry: dict) -> list[dict]:
    async def run_one(call):
        fn = registry[call["name"]]
        try:
            result = await fn(**call["input"])
            return {"tool_use_id": call["id"], "content": result, "is_error": False}
        except Exception as exc:
            # A failed tool call must still return a tool_result block —
            # omitting it breaks the conversation's message structure.
            return {"tool_use_id": call["id"], "content": str(exc), "is_error": True}

    return await asyncio.gather(*(run_one(c) for c in tool_calls))
```

Results must be returned to the model in the same order the calls were requested, each tagged with its `tool_use_id` — the API matches results to calls by ID, not by position, so an out-of-order return list is still correct, but a missing ID breaks the turn.

---

### 3. When NOT to Parallelize

- **Dependent calls**: if call B's arguments depend on call A's result, they cannot be in the same batch — the model will (correctly) request them across two turns.
- **Shared mutable state**: two tool calls writing to the same row/file concurrently need explicit locking or must be forced sequential regardless of model batching.
- **Rate-limited external APIs**: fan-out amplifies burst request rate; cap concurrency with a semaphore (`asyncio.Semaphore(n)`) sized to the upstream API's rate limit rather than the batch size.

## Inputs
- A model turn containing one or more `tool_use` blocks.
- A tool registry mapping tool name to an async-callable implementation.

## Outputs
- A `tool_result` block per `tool_use_id`, submitted together in the next user turn.
- Reduced p95 agent latency for turns with 2+ independent tool calls (typically 40-70% reduction vs sequential dispatch).
