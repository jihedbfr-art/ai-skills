---
format: "v2"
name: "extended-thinking-budget-governance"
title: "Governing an Extended Thinking Budget"
title_fr: "Gouverner un budget de raisonnement étendu"
description: "Reasoning tokens are billed and unbounded by default. This is the middleware pattern that assigns a thinking budget per request class instead of paying for depth nobody asked for."
description_fr: "Les tokens de raisonnement sont facturés et non bornés par défaut. Voici le pattern de middleware qui attribue un budget de réflexion par classe de requête, au lieu de payer une profondeur que personne n'a demandée."
domain: "15-frontier-models-and-trends"
tags: [frontier-models, reasoning, cost-optimization, engineering]
maturity: "stable"
audience: ["backend-engineer", "ai-engineer", "coding-agent"]
requires: ["python"]
updated: "2026-09-02"
---

## Prerequisites
- Python 3.10 or later with the anthropic SDK 0.30 or later.
- A way to classify incoming requests by how much reasoning they deserve. Without it the budget is a constant, not a governor.

## Usage

### Architectural Context

Claude 3.7 Sonnet introduces "extended thinking", allowing the model to dedicate compute time to internal reasoning before responding. While this vastly improves performance on logic and coding tasks, **thinking tokens are billed at the same rate as output tokens**. Without strict governance, autonomous agents can easily exhaust financial limits.

### 1. Execution Directives (Agent Instructions)

When querying Claude 3.7 Sonnet via the Anthropic API, you must always classify the task and set the `thinking.budget_tokens` parameter.

- **Low Effort:** Disabled. For extraction and summaries.
- **Medium Effort:** `2000` to `5000` tokens. For code generation and structuring.
- **High Effort:** `8000` to `16000` tokens. For debugging architectures.
- **Max Effort:** `>50000` tokens. Strictly reserved for mathematically unsolvable or extremely intricate codebase analysis. (Requires human override).

### 2. Python Middleware Hook

The following middleware demonstrates how to dynamically inject and enforce budget limits before the request reaches the Anthropic API.

```python
# examples/budget_governor.py
import os
from anthropic import Anthropic

class ClaudeBudgetGovernor:
    def __init__(self, api_key: str):
        self.client = Anthropic(api_key=api_key)
        self.EFFORT_TIERS = {
            "low": 0,
            "medium": 4000,
            "high": 12000
        }

    def generate_response(self, prompt: str, effort_tier: str = "medium"):
        budget = self.EFFORT_TIERS.get(effort_tier, 0)
        
        # Thinking budget must be at least 1024 if enabled
        if budget > 0 and budget < 1024:
            budget = 1024

        max_tokens = budget + 4000 # Add buffer for final answer

        params = {
            "model": "claude-3-7-sonnet-20250219",
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": prompt}]
        }

        if budget > 0:
            params["thinking"] = {
                "type": "enabled",
                "budget_tokens": budget
            }

        response = self.client.messages.create(**params)
        return response.content[0].text

# Usage:
# governor = ClaudeBudgetGovernor("sk-ant-...")
# print(governor.generate_response("Architect a scalable microservice...", "high"))
```

### 3. Financial Cost Formula

To estimate cost programmatically:

`Total Cost = (Input_Tokens × $3.00/1M) + ((Thinking_Tokens + Output_Tokens) × $15.00/1M)`

Ensure your autonomous loops implement a circuit breaker using this formula.

---
*Architected for the autonomous enterprise. A JihedAiLabs project.*

## Inputs
- The request, and its complexity class.

## Outputs
- A response produced under an explicit thinking budget, and the token cost that budget implied.
