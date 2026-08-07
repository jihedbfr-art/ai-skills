---
name: opentelemetry-llm-tracing-and-ttft
description: Architectural pattern for monitoring AI agents using OpenTelemetry to track token usage, Time-To-First-Token (TTFT), and agent reasoning spans.
version: 1.0.0
---

# OpenTelemetry Tracing for LLMs

## Architectural Purpose
Standard APM (Application Performance Monitoring) tools fail to capture the nuances of Agentic workflows (tool call loops, token consumption per span, prompt compilation time). Utilizing OpenTelemetry (OTel) with LLM semantic conventions ensures full observability of AI pipelines in production.

---

## 1. Core Pattern / Implementation

### LLM Semantic Conventions
When recording a span for an LLM call, attach specific OTel attributes:

```java
import io.opentelemetry.api.trace.Span;
import io.opentelemetry.api.trace.Tracer;

public void callLlm(String prompt) {
    Span span = tracer.spanBuilder("llm.generate")
        .setAttribute("llm.system", "anthropic")
        .setAttribute("llm.model_name", "claude-3-5-sonnet-20240620")
        .startSpan();

    try (var scope = span.makeCurrent()) {
        long startTime = System.currentTimeMillis();
        
        // Blocking/Streaming API Call
        LlmResponse response = anthropicClient.generate(prompt);
        
        span.setAttribute("llm.usage.prompt_tokens", response.getInputTokens());
        span.setAttribute("llm.usage.completion_tokens", response.getOutputTokens());
        span.setAttribute("llm.latency.ttft_ms", response.getTtftMs());
        
    } catch (Exception e) {
        span.recordException(e);
    } finally {
        span.end();
    }
}
```

### Trace Structure for Agents
```text
[HTTP POST /chat] 
 └── [Agent Supervisor Node]
      ├── [RAG Retrieval Span] (query: PGVector)
      ├── [Tool Execution Span] (get_customer_data)
      └── [LLM Generation Span] (model: claude-3.5-sonnet, tokens: 450)
```

---

## 2. Cost, Latency & Trade-offs
- **Token Math**: N/A for OTel directly, but capturing exact token usage enables precise cost-per-user billing.
- **Latency Penalty**: Asynchronous OTel exporters add near-zero latency overhead to the hot path.
- **Trade-off**: Storing raw prompt and completion text inside OTel spans (`llm.prompts`) can lead to massive storage bloat in tracing backends (Jaeger/Datadog) and potential data privacy leaks.

---

## 3. Verification Checklist
- [ ] Raw prompt text and completions are excluded from trace attributes in production unless explicitly sanitized.
- [ ] Both TTFT (Time-To-First-Token) and TBT (Time-Between-Tokens) are captured for streaming responses.
- [ ] Tool execution spans are visually nested as children of the main Agent span in the tracing dashboard.
