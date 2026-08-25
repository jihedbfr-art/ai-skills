---
format: "v2"
name: "supervisor-multi-agent-orchestration"
title: "Supervisor Multi-Agent Orchestration"
title_fr: "Supervisor Multi-Agent Orchestration"
description: "Multi-agent design pattern using a centralized Supervisor agent to route tasks, evaluate worker outputs, and manage global state."
description_fr: "Pattern de conception multi-agents utilisant un agent superviseur centralisé pour router les tâches, évaluer les sorties des agents travailleurs et gérer l'état global."
domain: "04-agentic-workflows"
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
Monolithic single-agent loops degrade in quality as task complexity increases. The Supervisor pattern divides responsibility into specialized worker agents directed by an orchestrator agent that manages state transitions.

---

### 1. Supervisor Architecture Topology

```text
               +-----------------------+
               |   Supervisor Agent    |
               | (Router & Evaluator)  |
               +-----------+-----------+
                           |
       +-------------------+-------------------+
       |                   |                   |
+------v-------+   +-------v------+   +--------v------+
| Research     |   | Code Writer  |   | Quality/Audit |
| Worker Agent |   | Worker Agent |   | Worker Agent  |
+--------------+   +--------------+   +---------------+
```

---

### 2. Supervisor Loop Lifecycle

1. **Task Decomposition**: Supervisor receives initial goal, evaluates current state graph, and selects the next worker node.
2. **Worker Execution**: Worker agent runs isolated loop with restricted tools (e.g. read-only search vs code edit).
3. **Output Critique**: Worker returns output to Supervisor. Supervisor inspects completion criteria.
4. **State Transition**: Supervisor transitions to next worker or signals `FINISH`.

---

### 3. Production Constraints & Safety

- **Max Turn Circuit Breaker**: Cap total multi-agent loops (e.g. `max_iterations = 15`) to prevent infinite recursion loops.
- **Shared State Isolation**: Pass immutable state snapshots between agents; workers append to state instead of mutating global variables.
- **Human-in-the-Loop Intercept**: Trigger approval requests on destructive actions (database drop, external API mutation, git push).

## Inputs
- Relevant source code, logs, network traces, or system specifications.

## Outputs
- Analysis findings, security audit report, or generated code artifacts.