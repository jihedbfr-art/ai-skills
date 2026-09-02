---
format: "v2"
name: "gemini-agents-and-search-grounding"
title: "Gemini Agents API and Search Grounding"
title_fr: "API Agents de Gemini et grounding sur la recherche"
description: "Building agents on the Gemini Agents API with Google Search grounding, and the per-query cost that grounding adds on top of tokens."
description_fr: "Construire des agents sur l'API Agents de Gemini avec grounding Google Search, et le coût par requête que le grounding ajoute au-dessus des tokens."
domain: "04-agentic-workflows"
tags: [gemini, agents, grounding, orchestration, engineering]
maturity: "stable"
audience: ["backend-engineer", "ai-engineer", "coding-agent"]
requires: ["python"]
updated: "2026-09-02"
---

## Prerequisites
- Python 3.10 or later with the google-genai SDK installed.
- A Google AI or Vertex AI project with billing enabled: grounding is billed per query, not per token.

## Usage

### Architectural Context

Building autonomous agents traditionally required heavy third-party orchestration frameworks (like LangChain or AutoGen) to manage memory, tool execution, and loops. The Google Gemini API now offers a native, server-side Agents API that handles state, memory, and tool execution natively within Google Cloud.

A massive enterprise advantage of the Gemini API is **Google Search Grounding**. Instead of building complex, fragile RAG (Retrieval-Augmented Generation) pipelines with vector databases to keep the model up-to-date, Grounding connects the LLM directly to the live Google Search index in real-time.

### 1. Execution Directives (Agent Instructions)

When architecting a Gemini agent:
1. **Prefer Native Grounding:** Before implementing a Vector DB, evaluate if Google Search Grounding satisfies the knowledge requirement. It is infinitely more resilient than maintaining chunking pipelines.
2. **System Instructions:** Use `system_instruction` to define the persona.

### 2. Python Hook: Grounded Agent

This script demonstrates how to instantiate a Gemini model that forces fact-checking via Google Search before generating an answer.

```python
# examples/gemini_grounded_agent.py
import os
from google import genai
from google.genai import types

# Initialize the new standard SDK
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def research_market_trends(query: str):
    """
    Executes a query using Gemini 1.5 Pro, firmly grounded in real-time Google Search results.
    """
    print(f"Agent is researching: {query}")
    
    response = client.models.generate_content(
        model='gemini-1.5-pro-002',
        contents=query,
        config=types.GenerateContentConfig(
            # Enable Google Search Grounding
            tools=[{"google_search": {}}],
            system_instruction="You are a market research analyst. Provide precise, data-driven answers."
        )
    )
    
    print("\n--- Final Report ---")
    print(response.text)
    
    # Extract the grounding metadata to verify the sources the agent used
    if response.candidates and response.candidates[0].grounding_metadata:
        metadata = response.candidates[0].grounding_metadata
        print("\n--- Sources Used ---")
        if metadata.grounding_chunks:
            for chunk in metadata.grounding_chunks:
                if chunk.web:
                    print(f"- {chunk.web.title}: {chunk.web.uri}")

if __name__ == "__main__":
    # research_market_trends("What were the financial impacts of the latest US Federal Reserve rate cuts?")
    pass
```

### 3. Financial Cost Formula for Grounding

While standard Gemini inference is billed per token, using the Google Search tool incurs a flat dynamic retrieval fee.

- **Dynamic Retrieval (Google Search):** $35.00 per 1,000 requests.

**Enterprise Heuristic:** Do not enable Grounding on every single conversational turn. Use an architectural router (see `vertex-reasoning-router`) to determine if the user's query requires real-time facts before enabling the tool, thus saving $0.035 per unnecessary invocation.

---
*Architected for the autonomous enterprise. A JihedAiLabs project.*

## Inputs
- The question to answer, and whether it needs facts newer than the model's training data.

## Outputs
- A grounded answer with its source citations, and the grounding cost for the call.
