---
format: "v2"
name: "gemini-context-caching"
title: "Gemini Context Caching on Vertex AI"
title_fr: "Context caching de Gemini sur Vertex AI"
description: "When the same large context is sent on every request, caching it server-side changes the bill from linear to near-flat. The API, the TTL trade-off, and the break-even formula."
description_fr: "Quand le même contexte volumineux est renvoyé à chaque requête, le mettre en cache côté serveur fait passer la facture de linéaire à quasi plate. L'API, l'arbitrage sur le TTL, et la formule du point d'équilibre."
domain: "01-llm-foundations-and-models"
tags: [gemini, context-caching, cost-optimization, engineering]
maturity: "stable"
audience: ["backend-engineer", "ai-engineer", "coding-agent"]
requires: ["python"]
updated: "2026-09-02"
---

## Prerequisites
- Python 3.10 or later with the google-genai SDK.
- A context large enough and stable enough to be worth caching. Below the provider's minimum token count, caching is refused outright.

## Usage

### Architectural Context

Standard agent architectures suffer from context bloat: reloading the same massive codebase, legal documents, or video transcriptions for every query exponentially increases latency and cost. 

Gemini 1.5 Pro features a massive 2-million token context window. The "Vertex AI Context Caching" module allows background processes to preload and freeze these colossal cognitive environments in Vertex AI memory. End-user queries are then routed to this persistent cache, cutting inference latency to fractions of a second and drastically reducing operational costs.

### 1. Execution Directives (Agent Instructions)

When orchestrating large data loads into Gemini:
1. **TTL Management:** Caches cost money to maintain per hour. Set a strict Time-To-Live (TTL) (e.g., 60 minutes) for volatile codebases.
2. **Background Refresh:** Implement a chron-job or webhook to asynchronously refresh the cache when the underlying repository receives a git push. Do not update the cache synchronously during a user request.

### 2. Python Caching Hook

```python
# examples/gemini_caching.py
import datetime
from google import genai
from google.genai import types

client = genai.Client(api_key="GEMINI_API_KEY")

def freeze_cognitive_environment(document_path: str):
    # Upload the massive document (e.g., a PDF, Video, or concatenated codebase)
    document = client.files.upload(file=document_path)
    
    # Freeze the context in memory with a 60-minute TTL
    cache = client.caches.create(
        model="gemini-1.5-pro-002",
        config=types.CreateCachedContentConfig(
            contents=[document],
            system_instruction="You are an expert software architect analyzing this frozen codebase.",
            ttl=datetime.timedelta(minutes=60),
        )
    )
    
    print(f"Context Cached Successfully. Cache Name: {cache.name}")
    return cache.name

def query_frozen_environment(cache_name: str, user_query: str):
    # Route the query to the frozen cache for ultra-fast, low-cost inference
    response = client.models.generate_content(
        model="gemini-1.5-pro-002",
        contents=user_query,
        config=types.GenerateContentConfig(
            cached_content=cache_name,
        )
    )
    return response.text
```

### 3. Financial Cost Formula

`Total Cost = (Cache_Storage_Cost_Per_Hour) + (Input_Tokens × Discounted_Cache_Rate) + (Output_Tokens × Standard_Rate)`

Using caching reduces the input token cost by up to 50-75% depending on the exact Google Cloud tier.

---
*Architected for the autonomous enterprise. A JihedAiLabs project.*

## Inputs
- The shared context, the expected number of requests against it, and the cache lifetime.

## Outputs
- A cache handle reused across requests, and the cost comparison against sending the context every time.
