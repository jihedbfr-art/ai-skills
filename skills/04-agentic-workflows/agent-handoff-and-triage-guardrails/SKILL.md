---
format: "v2"
name: "agent-handoff-and-triage-guardrails"
title: "Agent Handoff and Triage Guardrails"
title_fr: "Passage de relais entre agents et garde-fous de triage"
description: "Routing a request from a triage agent to a specialist, and why the guardrail belongs in the tool the specialist calls rather than in the instruction telling it to behave."
description_fr: "Router une requête d'un agent de triage vers un spécialiste, et pourquoi le garde-fou appartient à l'outil que le spécialiste appelle, et non à la consigne qui lui demande de bien se tenir."
domain: "04-agentic-workflows"
tags: [agents, orchestration, handoff, engineering]
maturity: "stable"
audience: ["backend-engineer", "security-engineer", "coding-agent"]
requires: ["python"]
updated: "2026-09-02"
---

## Prerequisites
- Python 3.10 or later with the openai SDK 1.40 or later.
- At least two agents with genuinely different permissions. Handoff between equals buys nothing.

## Usage

### Architectural Context

Modern agentic architecture has moved away from linear chains of prompts toward networks of specialized agents. Using the OpenAI ecosystem (Swarm methodology), a "Triage Agent" can dynamically transfer a conversation (along with its entire state and context) to an "Expert Agent" when a specific domain is detected.

### 1. Execution Directives (Agent Instructions)

When architecting an OpenAI multi-agent system:
1. **Define Agents as Functions:** Represent a handoff as a Tool Call. When Agent A returns Agent B, the execution loop shifts context to Agent B.
2. **Structured Outputs for Guardrails:** Always use `response_format={"type": "json_schema", ...}` to guarantee that the LLM generates data strictly conforming to enterprise data structures, neutralizing prompt injections.

### 2. Python Handoff Hook

The following code hands a request from a triage agent to a database specialist, carrying the conversation context across the boundary.

```python
# examples/agent_handoff.py
from pydantic import BaseModel
from openai import OpenAI

client = OpenAI()

class TransferToDatabaseExpert(BaseModel):
    query_context: str
    urgency: str

def triage_agent(user_message: str):
    response = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": "You are a triage agent. If the user asks about databases, transfer them to the DB Expert."},
            {"role": "user", "content": user_message}
        ],
        tools=[
            openai.pydantic_function_tool(TransferToDatabaseExpert)
        ]
    )
    
    tool_calls = response.choices[0].message.tool_calls
    if tool_calls and tool_calls[0].function.name == "TransferToDatabaseExpert":
        print("Executing Handoff to Database Expert...")
        # In a real system, you pass the context to the next agent loop
        return "HANDOFF_TRIGGERED"
    
    return response.choices[0].message.content

# Usage
# result = triage_agent("Can you run a SQL query to drop the users table?")
```

### 3. Security Guardrails

Never allow an agent to construct raw SQL strings via plain text generation. Use the **Structured Outputs** feature to force the LLM to output an AST (Abstract Syntax Tree) or a safe JSON representation of the query, which your backend safely translates via an ORM.

---
*Architected for the autonomous enterprise. A JihedAiLabs project.*

## Inputs
- The incoming request, and the specialist definitions with their allowed tools.

## Outputs
- The specialist's answer, or a refusal produced by the tool boundary rather than by the prompt.
