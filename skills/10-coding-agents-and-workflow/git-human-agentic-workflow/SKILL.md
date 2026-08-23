---
format: "v2"
name: "git-human-agentic-workflow"
title: "Git Human Agentic Workflow"
title_fr: "Git Human Agentic Workflow"
description: "Production conventions for AI coding assistants ensuring human commit style, clean Git history, zero AI traces, and safe repository autonomy."
description_fr: "Skill d'ingénierie et de sécurité pour git human agentic workflow."
domain: "10-coding-agents-and-workflow"
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
When AI coding agents (Claude Code, Antigravity, Aider) operate on software codebases, their commits must maintain senior engineering standards, authentic commit messages, and clean repository history without leaving machine-generated artifacts.

---

### 1. Commit Message Conventions (Conventional Commits)

Format: `<type>(<scope>): <concise human summary>`

- `feat(auth)`: Add OAuth2 JWT resource server validation
- `fix(security)`: Patch SQL injection vulnerability in search query
- `refactor(service)`: Extract transaction audit logging into REQUIRES_NEW service
- `docs(knowledge)`: Update Spring AI ChatClient advisor guide

### Forbidden Elements
- ❌ No `Co-Authored-By: Claude / Assistant` or AI signature tags.
- ❌ No verbose bulleted changelogs inside commit headers.
- ❌ No assistant config files (`CLAUDE.md`, `.agents/`) committed to public repositories (must remain in `.gitignore`).

---

### 2. Commit Granularity & Autonomy Rules

1. **Atomic Commits**: Commit single logical changes or feature units instead of monolithic multi-feature dumps.
2. **Local Isolation**: Always verify `.gitignore` excludes build artifacts (`target/`, `bin/`, `node_modules/`) and local secrets (`.env`) before staging.
3. **Identity Verification**: Explicitly check local Git identity prior to pushing:
   ```bash
   git config user.name "Your Name"
   git config user.email "your.email@example.com"
   ```

## Inputs
- Relevant source code, logs, network traces, or system specifications.

## Outputs
- Analysis findings, security audit report, or generated code artifacts.