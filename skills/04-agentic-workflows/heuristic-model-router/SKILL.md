---
format: "v2"
name: "heuristic-model-router"
title: "Routing Requests Across Models by Heuristic"
title_fr: "Router les requêtes entre modèles par heuristique"
description: "One model for everything is either too expensive or too shallow. A cheap heuristic router in front of a fast model, a reasoning model, and a local one, with the observability to prove it routed correctly."
description_fr: "Un modèle unique pour tout est soit trop cher, soit trop superficiel. Un routeur heuristique bon marché devant un modèle rapide, un modèle de raisonnement et un modèle local, avec l'observabilité qui prouve que le routage était correct."
domain: "04-agentic-workflows"
tags: [orchestration, routing, cost-optimization, engineering]
maturity: "stable"
audience: ["backend-engineer", "ai-engineer", "coding-agent"]
requires: ["python"]
updated: "2026-09-02"
---

## Prerequisites
- Python 3.10 or later, and credentials for every model the router can select.
- A traffic mix that genuinely varies in difficulty. Uniform traffic makes a router pure overhead.

## Usage

### Architectural Context

Industrial AI deployment requires abandoning the monolithic model approach. The "Vertex Reasoning Framework" uses a high-speed heuristic router to triage incoming requests. It assigns the cognitive workload to the most appropriate model dynamically, trading cost against analytical depth on a per-request basis.

### 1. Execution Directives (Agent Instructions)

The Routing Agent must classify incoming user intents into three tiers:
1. **Tier 1 (Speed & Extraction):** Route to `Gemini 1.5 Flash`. Use for simple RAG, summarization, and data extraction.
2. **Tier 2 (Architectural & Code):** Route to `Claude 3.7 Sonnet`. Use for large software engineering tasks. Dynamically inject the `thinking.budget_tokens` based on repository size.
3. **Tier 3 (Math & Deep Logic):** Route to `DeepSeek-R1`. Use for unresolved mathematical proofs or complex logical puzzles. You **MUST** strip the system prompt and set temperature to `0.6`.

### 2. Python Routing Hook

```python
# examples/heuristic_router.py

def heuristic_router(user_query: str):
    # In a real system, a fast classifier (like Gemini Flash or a fine-tuned BERT) 
    # evaluates the query to determine the intent tier.
    classification = fast_intent_classifier(user_query)
    
    if classification == "MATH_OR_LOGIC":
        print("Routing to DeepSeek-R1 (Tier 3)...")
        # Strip system prompt, enforce temp=0.6
        return execute_deepseek_r1(user_query, temperature=0.6)
        
    elif classification == "CODE_ARCHITECTURE":
        print("Routing to Claude 3.7 Sonnet (Tier 2)...")
        # Enforce budget governance
        return execute_claude_sonnet(user_query, thinking_budget=4000)
        
    else:
        print("Routing to Gemini 1.5 Flash (Tier 1)...")
        # Default low-latency execution
        return execute_gemini_flash(user_query)

def fast_intent_classifier(query: str) -> str:
    # Dummy implementation. Use keywords or a lightweight LLM.
    if "calculate" in query or "proof" in query: return "MATH_OR_LOGIC"
    if "refactor" in query or "architecture" in query: return "CODE_ARCHITECTURE"
    return "DEFAULT"
```

### 3. Observability

To prevent the router from becoming a black box, all routing decisions must be logged via OpenTelemetry. The resulting dashboard must display the exact model invoked and the latency delta, ensuring the enterprise has total transparency into the agent's cognitive choices.

---
*Architected for the autonomous enterprise. A JihedAiLabs project.*

## Inputs
- The request, and the routing rules mapping request shape to model.

## Outputs
- The chosen model's answer, plus the routing decision recorded for later audit.
