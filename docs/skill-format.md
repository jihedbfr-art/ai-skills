# 📐 AI Skill Format Specification

> Standardized format for all skills in the `ai-skills` repository.

## 1. Frontmatter Requirements

Every `SKILL.md` must start with YAML frontmatter containing:

```yaml
---
name: domain-skill-name
description: A clear, single-sentence summary of the architectural pattern or technique.
version: 1.0.0
---
```

## 2. Document Structure

Each skill must follow this 4-section layout:

1. **# Title**: Standard title naming the pattern.
2. **## Architectural Context / Purpose**: High-level problem statement and engineering objective.
3. **## Core Pattern / Implementation**: Code snippets, SQL queries, or architectural diagrams.
4. **## Cost, Latency & Trade-offs**: Token usage impact, TTFT latency penalty, and maintenance trade-offs.
5. **## Verification Checklist**: Actionable verification steps.

## 3. Engineering Constraints

- **Token & Latency Math**: Explicitly state estimated costs or latency penalties.
- **API Versioning**: Name target library versions (Spring AI 1.0.0-M5, OpenAI SDK v1.x).
- **No AI Traces**: Clean, authoritative engineering prose. No marketing filler or AI badges.
