---
format: "v2"
name: "prompt-injection-defense-guardrails"
title: "Prompt Injection Defense Guardrails"
title_fr: "Prompt Injection Defense Guardrails"
description: "Security patterns for mitigating direct and indirect prompt injection attacks, enforcing input sanitization, and output schema guardrails."
description_fr: "Skill d'ingénierie et de sécurité pour prompt injection defense guardrails."
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
Prompt injection occurs when untrusted user or document input manipulates the LLM's system instructions, leading to unauthorized data exfiltration, system command execution, or safety bypasses.

---

### 1. Defense-in-Depth Layer Topology

```text
[1. INPUT SANITIZER]  -> Strip control characters & escape XML tags.
[2. PROMPT BOUNDARY]  -> Isolate untrusted input inside strict <user_input> tags.
[3. LLM GUARDRAIL]    -> Parallel secondary classifier evaluating intent.
[4. OUTPUT VALIDATOR] -> Schema validation & PII/Secret regex scanning.
```

---

### 2. Mitigation Rules & Code Pattern

### Rule 1: Strict Input Escaping
Before placing user input into a prompt template, escape XML delimiters (`<`, `>`):

```java
public String sanitizeUserInput(String rawInput) {
    if (rawInput == null) return "";
    return rawInput
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace("\"", "&quot;");
}
```

### Rule 2: Output Secret Scanner
Scan model completion for API keys, bearer tokens, or internal IP addresses prior to returning response to the caller.

---

### 3. OWASP Top 10 for LLM Summary

1. **LLM01: Prompt Injection** (Direct & Indirect via RAG documents).
2. **LLM02: Sensitive Information Disclosure** (System prompt exfiltration, PII leak).
3. **LLM06: Excessive Agency** (Granting agents destructive tool permissions without human approval).

## Inputs
- Relevant source code, logs, network traces, or system specifications.

## Outputs
- Analysis findings, security audit report, or generated code artifacts.