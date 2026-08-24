---
format: "v2"
name: "reflection-and-self-critique-loops"
title: "Reflection And Self Critique Loops"
title_fr: "Boucles de Réflexion et Auto-Critique"
description: "Agent pattern where a generator LLM output is critiqued by a second pass (self or separate model) before being accepted, trading latency and tokens for correctness."
description_fr: "Pattern d'agent où la sortie d'un LLM générateur est critiquée par une seconde passe (soi-même ou un modèle séparé) avant acceptation, échangeant latence et tokens contre de la justesse."
domain: "04-agentic-workflows"
tags: [agents, orchestration, engineering, best-practices]
maturity: "stable"
audience: ["backend-engineer", "ai-engineer", "coding-agent"]
requires: ["bash", "git", "python"]
updated: "2026-08-25"
---



## Prerequisites
- A working single-pass agent loop (generator) already producing draft outputs.
- A cost budget that tolerates 1.5x-3x token spend per task (reflection is not free).

## Usage
### Architectural Purpose
A single forward pass optimizes for likely-next-token, not for correctness. Reflection inserts an explicit critique step that reads the draft output against the original task constraints and either approves it or returns a structured list of defects for a repair pass. This converts silent errors into visible, actionable failures before they reach the user.

---

### 1. Generate → Critique → Repair Loop

```text
+-------------+     +---------------+     +--------------+
|  Generator  | --> |    Critic     | --> |   Repairer   |
| (draft out) |     | (find defects)|     | (patch draft)|
+-------------+     +-------+-------+     +------+-------+
                            |                     |
                     defects=[] -> ACCEPT   loop back to Critic
                                              (max_reflections=2)
```

1. **Draft**: Generator produces an initial answer/code/plan against the task spec.
2. **Critique**: A separate prompt (or separate model) evaluates the draft strictly against a checklist derived from the task — not general quality, specific verifiable claims (e.g. "does this SQL reference a column that exists in the provided schema?").
3. **Repair**: If defects are non-empty, feed draft + defect list back to the generator for a targeted patch. Do not regenerate from scratch — targeted patches converge faster and cost fewer tokens.
4. **Cap iterations**: `max_reflections = 2` in production. Beyond 2 rounds, diminishing returns dominate and the loop usually indicates the task spec itself is ambiguous — escalate to a human instead of looping further.

---

### 2. Critique Prompt Contract

```python
CRITIQUE_SYSTEM = """You are a strict verifier, not a collaborator.
Check the DRAFT against the CHECKLIST only. Do not suggest style changes.
Return JSON: {"defects": [{"claim": str, "evidence": str}], "verdict": "ACCEPT"|"REJECT"}
A defect requires evidence quoted from the provided context — unverifiable
complaints are discarded."""

def critique(draft: str, checklist: list[str], context: str) -> dict:
    resp = client.messages.create(
        model="claude-haiku-4-5-20251001",  # cheaper model is fine for verification
        system=CRITIQUE_SYSTEM,
        messages=[{"role": "user", "content":
            f"CHECKLIST:\n{checklist}\n\nCONTEXT:\n{context}\n\nDRAFT:\n{draft}"}],
    )
    return json.loads(resp.content[0].text)
```

Using a smaller/cheaper model for the critic than the generator is a deliberate cost optimization: critique is a narrower, more constrained task than generation and does not need frontier reasoning capacity.

---

### 3. Failure Modes to Guard Against

- **Sycophantic critique**: a model critiquing its own output tends to under-report defects. Mitigate by using a different model family for the critic, or by forcing evidence-based JSON output rather than free-form approval.
- **Critique drift**: without a fixed checklist, the critic invents new requirements each round, causing the repair loop to oscillate instead of converge. Freeze the checklist at task start.
- **Unbounded cost**: always enforce `max_reflections` and log token spend per reflection round; alert if reflection cost exceeds the generation cost by more than 2x on average.

## Inputs
- Original task specification and acceptance checklist.
- Draft output from the generator pass.
- Reference context (schema, requirements, prior turns) the critic uses as ground truth.

## Outputs
- Accepted final output, or an escalation to a human with the last defect list attached.
- Structured defect log per reflection round (for offline eval and prompt tuning).
