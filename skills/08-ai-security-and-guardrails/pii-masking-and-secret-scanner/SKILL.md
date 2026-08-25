---
format: "v2"
name: "pii-masking-and-secret-scanner"
title: "PII Masking and Secret Scanner"
title_fr: "PII Masking and Secret Scanner"
description: "Security pattern for intercepting and masking Personally Identifiable Information (PII) and credentials before sending prompts to external LLM APIs."
description_fr: "Pattern de sécurité pour intercepter et masquer les informations personnelles identifiables (PII) et les identifiants avant l'envoi des prompts aux API LLM externes."
domain: "08-ai-security-and-guardrails"
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
Sending unmasked customer data (SSN, credit cards, real names) or internal system credentials (API keys, connection strings) to public LLM APIs (OpenAI, Anthropic) violates GDPR, HIPAA, and enterprise security policies. A sanitization interceptor guarantees compliance.

---

### 1. Core Pattern / Implementation

### Interceptor Proxy Pattern
Deploy a lightweight sanitization layer (e.g., using Presidio by Microsoft or a regex-based interceptor) right before the HTTP call to the LLM.

```python
import re

CREDIT_CARD_REGEX = r"\b(?:\d[ -]*?){13,16}\b"
EMAIL_REGEX = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

def mask_pii(prompt: str) -> str:
    sanitized = re.sub(CREDIT_CARD_REGEX, "[REDACTED_CC]", prompt)
    sanitized = re.sub(EMAIL_REGEX, "[REDACTED_EMAIL]", sanitized)
    return sanitized

user_input = "My account is user@example.com and card is 4111 1111 1111 1111"
safe_prompt = mask_pii(user_input)
```

### De-Tokenization (Reversible Masking)
For complex workflows, the interceptor replaces PII with a UUID mapping (`<PERSON_1>`), sends it to the LLM, and replaces `<PERSON_1>` back with the real name when the LLM returns the output to the secure internal network.

---

### 2. Cost, Latency & Trade-offs
- **Token Math**: Redaction tags like `[REDACTED_EMAIL]` usually consume 3-4 tokens instead of the original text's tokens. Impact is negligible.
- **Latency Penalty**: Regex masking adds <5ms. Deep NLP models (like Presidio Analyzer) add 50-150ms of processing time before the LLM call.
- **Trade-off**: Over-redaction can destroy the LLM's context. If the LLM needs to write an email to a specific user, irreversible masking breaks the workflow.

---

### 3. Verification Checklist
- [ ] Ensure the interceptor runs on all outbound prompts AND all inbound RAG context chunks.
- [ ] Secrets (Bearer tokens, passwords) are filtered out using exact match against internal vault entries.
- [ ] Avoid relying solely on the LLM's system prompt (e.g., "Do not reveal PII") as it is vulnerable to prompt injection bypass.

## Inputs
- Relevant source code, logs, network traces, or system specifications.

## Outputs
- Analysis findings, security audit report, or generated code artifacts.