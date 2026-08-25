---
format: "v2"
name: "llm-selection-and-token-math"
title: "LLM Selection and Token Math"
title_fr: "LLM Selection and Token Math"
description: "Architectural guidelines for LLM provider selection, context window decay management, tokenizer calculations, and pricing trade-offs."
description_fr: "Directives architecturales pour le choix du fournisseur LLM, la gestion de la dégradation de la fenêtre de contexte, le calcul des tokens et les arbitrages de coût."
domain: "01-llm-foundations-and-models"
tags: [cybersecurity, engineering, best-practices]
maturity: "stable"
audience: ["backend-engineer", "security-engineer", "coding-agent"]
requires: ["bash", "git"]
updated: "2026-08-08"
---



## Prerequisites
- Target system, dependencies and environment configured.

## Usage
### Architectural Context
Selecting the right Large Language Model (LLM) for enterprise workloads requires balancing reasoning capability, context window retention, Time-To-First-Token (TTFT), and operational costs. 

---

### 1. Token Ratio & Estimation Rules

### Standard Character-to-Token Ratios
- **English Prose**: ~1 token = 4 characters (0.75 words per token).
- **Source Code (Java/Python)**: ~1 token = 2.5 to 3 characters (due to indentation, syntax symbols, camelCase split).
- **Structured JSON/XML**: ~1 token = 2 characters (high density of quotes, braces, colons).

### Math Formula for Context Window Cost
$$\text{Cost} = \left(\frac{\text{Input Tokens}}{1,000,000} \times \text{Input Price}\right) + \left(\frac{\text{Output Tokens}}{1,000,000} \times \text{Output Price}\right)$$

---

### 2. Context Window Decay Mitigation

As context length grows beyond 32k tokens, LLM recall efficiency exhibits a U-shaped accuracy curve ("Lost in the Middle").

### Production Mitigation Rules
1. **Critical Instructions Placement**: Place core system instructions and constraints at the **very beginning** or **very end** of the context prompt.
2. **Context Compression**: Truncate middle conversation history when exceeding 70% of maximum model context.
3. **Structured Delimiters**: Wrap long background documents inside XML tags (`<document id="doc1">...</document>`).

---

### 3. Cost & Latency Benchmark Matrix

| Model Tier | Typical TTFT | Latency (TBT) | Relative Cost | Primary Use Case |
| :--- | :--- | :--- | :--- | :--- |
| **Frontier (Claude 3.5 Sonnet / GPT-4o)** | 400 - 800 ms | ~80 tok/s | High | Complex reasoning, agentic coding, architecture design |
| **Fast / Balanced (Claude 3.5 Haiku / GPT-4o-mini)** | 150 - 300 ms | ~150 tok/s | Low (10x cheaper) | High-volume classification, simple RAG, intent routing |
| **Local Open Source (Llama 3.3 70B / Qwen 2.5)** | Depends on HW | ~40-90 tok/s | Infra cost | Data privacy compliance, offline / air-gapped deployment |

---

### 4. Verification Checklist

- [ ] System prompt places critical constraints in top 10% of total token budget.
- [ ] Output token limits (`max_tokens`) are explicitly set to prevent infinite generation loops.
- [ ] Context size monitored to trigger auto-truncation before hitting provider HTTP 400 bounds.

## Inputs
- Relevant source code, logs, network traces, or system specifications.

## Outputs
- Analysis findings, security audit report, or generated code artifacts.