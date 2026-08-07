<p align="center">
  <img src="assets/jihedailabs-logo.svg" width="180" alt="JihedAiLabs Logo" />
</p>

<h1 align="center">AI Engineering Skills Library</h1>

<p align="center">
  <b>A pragmatic, production-ready engineering knowledge base for building AI systems, LLM agents, RAG pipelines, and Model Context Protocol (MCP) integrations.</b>
</p>

<p align="center">
  <a href="README.fr.md">🇫🇷 Lire en Français</a> •
  <a href="#-architecture--domains">Architecture</a> •
  <a href="#-conventions">Conventions</a> •
  <a href="#-license">License</a>
</p>

---

## 📌 Overview

This repository provides **50 actionable AI Engineering skills** organized into **10 core domains**. Each skill is written in a hybrid format: human-readable architectural guidance paired with machine-executable patterns for AI coding assistants and developers.

It bridges the gap between theoretical AI concepts and enterprise production realities (token economics, latency tradeoffs, state management, security guardrails, and Spring AI integration).

---

## 🏗️ Architecture & Domains

```text
ai-skills/
├── 01-llm-foundations-and-models/     # Model selection, context window optimization, quantization & token math
├── 02-prompt-and-context-engineering/# Few-shot, Chain-of-Thought, ReAct, XML delimiters & context compression
├── 03-rag-architectures/              # Chunking strategies, hybrid search (BM25 + Vector), re-ranking & metadata filtering
├── 04-agentic-workflows/              # Single/multi-agent orchestration, supervisor loops, human-in-the-loop & memory
├── 05-mcp-protocol-and-tools/         # Model Context Protocol (MCP) servers, stdio/SSE transports & tool schemas
├── 06-spring-ai-integration/          # Spring AI ChatClient, Advisors, `@Bean` Tool Calling & PGVector integration
├── 07-vector-databases-and-embeddings/# Embedding models, HNSW indexing, PGVector tuning & similarity metrics
├── 08-ai-security-and-guardrails/     # Prompt injection defense, PII masking, secret leakage prevention & rate limits
├── 09-evaluations-and-observability/  # RAGAS metrics, LLM-as-a-judge, OpenTelemetry tracing & latency monitoring
└── 10-coding-agents-and-workflow/     # Agentic coding workflows, Git-human compliance & refactoring templates
```

---

## 📋 Core Skill Roster (5 Skills per Domain)

| Domain | Focus Area | Key Topics Covered |
| :--- | :--- | :--- |
| **01. LLM Foundations** | Model Selection & Economics | Tokenizer math, context window decay, quantization (GGUF/AWQ), pricing models |
| **02. Prompt & Context Eng.** | Prompt Optimization | System prompt architecture, XML boundaries, ReAct patterns, context truncation |
| **03. RAG Architectures** | Advanced Retrieval | Semantic chunking, BM25 + Vector hybrid search, Cohere re-ranking, PGVector |
| **04. Agentic Workflows** | Multi-Agent Orchestration | State graph persistence, supervisor pattern, reflection loop, tool execution |
| **05. MCP & Tooling** | Protocol Standards | MCP server specification, stdio transport, JSON-Schema tool definitions |
| **06. Spring AI Integration** | Enterprise Java AI | `ChatClient` fluent API, `Advisor` chain, Spring Data PGVector, Tool Calling `@Bean` |
| **07. Vector DB & Embeddings**| Data Store Optimization | Embedding dimension trade-offs, HNSW index tuning, Cosine vs Inner Product |
| **08. AI Security** | Hardening & Guardrails | Indirect prompt injection, output sanitization, PII masking, token rate-limiting |
| **09. Evals & Observability** | Quality & Metrics | Faithfulness & Answer Relevancy (RAGAS), OpenTelemetry spans, TTFT latency |
| **10. Coding Agents** | Developer Productivity | Autonomous agent workflows, Git commit hygiene, automated test generation |

---

## 📐 Conventions & Design Principles

Every skill in this repository complies with 4 strict engineering constraints:

1. **Explicit Cost & Latency Estimation**: Every technique specifies its token consumption impact, latency penalty (TTFT / TBT), and maintenance complexity.
2. **API Surface Versioning**: All cited library APIs (Spring AI, LangChain, Anthropic SDK, OpenAI SDK) explicitly state the target version to prevent deprecation drift.
3. **No Artificial Bloat**: Roster is strictly capped at **5 high-impact skills per domain** to maintain maximum signal-to-noise ratio.
4. **Zero AI Traces**: All documentation and code samples use natural, authoritative engineering language grounded in real-world deployment experience.

---

## 📄 License

Distributed under the **MIT License**. Created & maintained by **Jihed Ben Arfa**.
