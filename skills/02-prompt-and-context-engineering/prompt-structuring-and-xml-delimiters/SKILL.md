---
name: prompt-structuring-and-xml-delimiters
description: Production patterns for prompt engineering using XML tag boundaries, system instructions separation, and structured outputs.
version: 1.0.0
---

# Prompt Structuring & XML Delimiters Pattern

## Architectural Purpose
Unstructured text prompts lead to instruction confusion, prompt injection vulnerabilities, and unpredictable LLM outputs. Using explicit XML element boundaries isolates user input from system rules and forces deterministic parsing.

---

## 1. System Prompt Architecture

A production-grade system prompt follows a 4-layer structure:

```text
[1. ROLE & IDENTITY] -> Define exact persona, authority level, and bounds.
[2. CORE INSTRUCTIONS] -> Bulleted list of imperative rules.
[3. CONTEXT & REFERENCE] -> XML-wrapped data payload (<context>...</context>).
[4. OUTPUT FORMAT SCHEMA] -> Strict JSON schema or XML output template.
```

---

## 2. XML Tag Boundary Pattern

### Example Prompt Template

```xml
<system_instructions>
You are a Senior Java Microservices Architect. Analyze the code snippet inside <source_code>.
Rules:
- Identify thread-safety risks, memory leaks, and performance bottlenecks.
- Respond ONLY using the XML schema defined in <output_format>.
</system_instructions>

<output_format>
<analysis>
  <severity>HIGH | MEDIUM | LOW</severity>
  <issue>Description</issue>
  <recommendation>Fix proposal</recommendation>
</analysis>
</output_format>

<source_code>
${USER_INPUT_CODE}
</source_code>
```

---

## 3. Engineering Benefits & Tradeoffs

| Metric | Impact | Rationale |
| :--- | :--- | :--- |
| **Parsing Reliability** | +95% | Eliminates ambiguity between prompt instructions and user data. |
| **Injection Resilience** | High | Prevents user input from hijacking instructions outside `<source_code>`. |
| **Token Overhead** | ~10-20 tokens | Minimal syntax cost for substantial stability gain. |

---

## 4. Verification Checklist

- [ ] All dynamic user inputs are strictly wrapped inside dedicated XML tags (`<user_data>`, `<query>`).
- [ ] Output format requires root XML tags or JSON Schema enforcement.
- [ ] No unescaped closing XML tags exist within user input fields.
