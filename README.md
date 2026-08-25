<p align="center">
  <img src="assets/jihedailabs-logo.svg" width="180" alt="JihedAiLabs Logo" />
</p>

<h1 align="center">AI Engineering Skills Library</h1>

<p align="center">
  <b>32 skills for building LLM agents, RAG pipelines, and MCP integrations — written so a backend engineer or a coding agent can both run them as-is.</b>
</p>

<p align="center">
  <a href="README.fr.md">🇫🇷 Lire en Français</a> •
  <a href="#using-a-skill">Using a skill</a> •
  <a href="#-architecture--domains">Architecture</a> •
  <a href="#-conventions">Conventions</a> •
  <a href="#-license">License</a>
</p>

---

## Why this exists

Most AI engineering content online stops at "here's how RAG works" or "here's a LangChain demo." It rarely says what a chunking strategy costs in tokens, which reranking approach survives a real latency budget, or how to wire the same pattern into a Spring AI backend instead of a Python notebook.

Each skill here is written for someone who already knows what an LLM is and needs the production decision: which chunking size, which index, which guardrail, at what token and latency cost — with the target library version pinned so the advice doesn't rot silently.

## Using a skill

**As a human.** Open the `SKILL.md` for the domain you need, read the architectural context, and check the pinned library versions before applying it — an LLM API surface moves fast enough that untagged advice ages badly.

**As an agent skill.** Each skill directory follows the `SKILL.md` convention supported by several agentic coding assistants: YAML frontmatter (`name`, `description`, `audience`, `requires`) followed by the instructions in the body. Copy the ones you need into your assistant's skills directory:

```bash
cp -r skills/03-rag-architectures/hybrid-search-bm25-vector-pgvector ~/.config/agent-skills/
```

The frontmatter `description` is what the assistant matches against, so it's phrased as a trigger sentence, not a title.

---

## 🏗️ Architecture & Domains

```text
ai-skills/
├── 01-llm-foundations-and-models/     # Model selection, context window optimization, quantization & token math
├── 02-prompt-and-context-engineering/# Few-shot, Chain-of-Thought, ReAct, XML delimiters & context compression
├── 03-rag-architectures/              # Chunking strategies, hybrid search (BM25 + Vector), cross-encoder re-ranking & GraphRAG
├── 04-agentic-workflows/              # Single/multi-agent orchestration, supervisor loops, reflection loops & parallel tool-use
├── 05-mcp-protocol-and-tools/         # Model Context Protocol (MCP) servers, stdio/SSE transports & tool schemas
├── 06-spring-ai-integration/          # Spring AI ChatClient, Advisors, `@Bean` Tool Calling & PGVector integration
├── 07-vector-databases-and-embeddings/# Embedding models, HNSW indexing, PGVector tuning & similarity metrics
├── 08-ai-security-and-guardrails/     # Prompt injection defense, PII masking, secret leakage prevention & rate limits
├── 09-evaluations-and-observability/  # RAGAS metrics, pairwise LLM-as-a-judge, golden dataset regression gates & tracing
├── 10-coding-agents-and-workflow/     # Agentic coding workflows, Git-human compliance & refactoring templates
├── 11-custom-mcp-development/         # Custom MCP servers in Python/TS, resource providers, and custom tool building
├── 12-low-code-ai-workflows/          # n8n, Flowise, Dify workflows, visual agent orchestration, and automated pipelines
├── 13-ai-ux-and-frontend/             # Generative UI, Claude artifacts, v0.dev, and agent-oriented user experiences
├── 14-multimedia-and-generation/      # Video/Audio generation MCPs, PPTX automation, Sora/Runway multimodal agents
└── 15-frontier-models-and-trends/     # Frontier reasoning model comparisons, test-time compute budgeting & context windows
```

---

## 📋 Core Skill Roster

| Domain | Skills | Focus Area | Key Topics Covered |
| :--- | :---: | :--- | :--- |
| **01. LLM Foundations** | 2 | Model Selection & Economics | Tokenizer math, context window decay, quantization (GGUF/AWQ), pricing models |
| **02. Prompt & Context Eng.** | 2 | Prompt Optimization | System prompt architecture, XML boundaries, ReAct patterns, context truncation |
| **03. RAG Architectures** | 4 | Advanced Retrieval | Semantic chunking, BM25 + Vector hybrid search, cross-encoder rerank, GraphRAG |
| **04. Agentic Workflows** | 4 | Multi-Agent Orchestration | State graph persistence, supervisor pattern, reflection loops, parallel tool-use |
| **05. MCP & Tooling** | 2 | Protocol Standards | MCP server specification, stdio transport, JSON-Schema tool definitions |
| **06. Spring AI Integration** | 2 | Enterprise Java AI | `ChatClient` fluent API, `Advisor` chain, Spring Data PGVector, Tool Calling `@Bean` |
| **07. Vector DB & Embeddings**| 2 | Data Store Optimization | Embedding dimension trade-offs, HNSW index tuning, Cosine vs Inner Product |
| **08. AI Security** | 2 | Hardening & Guardrails | Indirect prompt injection, output sanitization, PII masking, token rate-limiting |
| **09. Evals & Observability** | 4 | Quality & Metrics | RAGAS metrics, pairwise LLM-as-judge, golden dataset CI gates, OpenTelemetry |
| **10. Coding Agents** | 2 | Developer Productivity | Autonomous agent workflows, Git commit hygiene, automated test generation |
| **11. Custom MCP** | 1 | Extending Context | Python/TS MCP server creation, custom tool APIs, SSE/stdio routing |
| **12. Low-Code AI** | 1 | Visual Workflows | n8n agent orchestration, Dify pipelines, branching logic |
| **13. AI UX & Frontend** | 1 | Generative Interfaces | Claude artifacts, v0.dev UI, streaming component rendering |
| **14. Multimedia AI** | 1 | Rich Content | Sora video workflows, automated PPTX generation, audio synthesis |
| **15. Frontier Models** | 2 | Model Evaluation & Cost | Reasoning model capability comparisons, test-time compute budgeting |

---

## 📐 Conventions & Design Principles

Every skill in this repository complies with 4 strict engineering constraints:

1. **Explicit Cost & Latency Estimation**: Every technique specifies its token consumption impact, latency penalty (TTFT / TBT), and maintenance complexity.
2. **API Surface Versioning**: All cited library APIs (Spring AI, LangChain, Anthropic SDK, OpenAI SDK) explicitly state the target version to prevent deprecation drift.
3. **No Artificial Bloat**: Each domain grows toward a **5 high-impact skills** ceiling — new entries are added only when they cover a genuinely distinct pattern, never to pad the count.
4. **Zero AI Traces**: All documentation and code samples use natural, authoritative engineering language grounded in real-world deployment experience.

---

## 📄 License

Distributed under the **MIT License**. Created & maintained by **Jihed Ben Arfa**.
